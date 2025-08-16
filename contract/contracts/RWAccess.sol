// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @notice Minimal ERC20 interface for PYUSD.
interface IERC20 {
    function transferFrom(address from, address to, uint256 value) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function balanceOf(address a) external view returns (uint256);
    function decimals() external view returns (uint8);
}

/// @title Real-World Access with PYUSD payments & external signature fulfillment.
/// @author
/// @notice Single-asset controller with ENS label, second-based pricing, and collision-safe accesses.
contract RWAcess {
    // -------------------- Types --------------------
    struct Access {
        address user;
        uint64 tstart;
        uint64 tend;
        bool signed;         // whether external signature has been populated.
        bytes signature;     // off-chain signature payload (opaque blob).
    }

    // -------------------- Events --------------------
    event PricePerSecondUpdated(uint256 oldPrice, uint256 newPrice);
    event ENSUpdated(string oldENS, string newENS);

    // Access lifecycle
    event AccessCreated(
        bytes32 indexed accessId,
        address indexed user,
        uint64 tstart,
        uint64 tend,
        string ens,
        bytes signature // Empty on creation.
    );

    event AccessSigned(
        bytes32 indexed accessId,
        address indexed user,
        uint64 tstart,
        uint64 tend,
        string ens,
        bytes signature
    );

    // -------------------- Storage --------------------
    address public immutable pyusd;     // PYUSD token address
    address public owner;               // contract admin / payment sink
    string  public ens;                 // ENS label for this asset
    uint256 public pricePerSecond;      // PYUSD (6dp typical) per second

    // Accesses.
    mapping(bytes32 => Access) public accesses;  // accessId => Access.

    // Day buckets -> list of accessIds that intersect this day.
    // Day index = unixDay = timestamp / 86400.
    mapping(uint32 => bytes32[]) internal accessesByDay;

    // Caps to avoid pathological gas usage
    uint32 public constant SECONDS_PER_DAY = 86400;
    uint8  public constant MAX_ACCESS_DAYS = 7;        // tend must be within 7 days of tstart (MVP-safe)
    uint16 public constant MAX_DAY_BUCKET_SCAN = 200;  // sanity cap per day scan

    // -------------------- Modifiers --------------------
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    // -------------------- Constructor --------------------
    constructor(address _pyusd, uint256 _pricePerSecond, string memory _ens) {
        require(_pyusd != address(0), "PYUSD=0");
        owner = msg.sender;
        pyusd = _pyusd;
        pricePerSecond = _pricePerSecond;
        ens = _ens;
    }

    // -------------------- Admin / Config --------------------
    function setPricePerSecond(uint256 newPrice) external onlyOwner {
        uint256 old = pricePerSecond;
        pricePerSecond = newPrice;
        emit PricePerSecondUpdated(old, newPrice);
    }

    /// @notice Sets the ENS name for the asset. Only the "user"/controller can set this.
    function setENS(string calldata newENS) external onlyOwner {
        string memory old = ens;
        ens = newENS;
        emit ENSUpdated(old, newENS);
    }

    // -------------------- Public: Pay & Book --------------------
    /// @notice Pays in PYUSD for [tstart, tend) and creates a access if interval does not overlap an existing one.
    ///         Caller must have approved this contract for the required PYUSD amount.
    function pay(uint64 tstart, uint64 tend) external returns (bytes32 accessId) {
        require(tend > tstart, "tend<=tstart");

        // Duration & caps
        uint64 duration = tend - tstart;
        // Enforce max span to bound per-day loop gas
        require(_daysBetween(tstart, tend) <= MAX_ACCESS_DAYS, "Access too long");

        // Reject overlaps
        _revertIfOverlaps(tstart, tend);

        // Calculate payment
        // PYUSD typically 6 decimals; pricePerSecond should be set accordingly.
        uint256 cost = uint256(duration) * pricePerSecond;

        // Pull funds
        require(IERC20(pyusd).transferFrom(msg.sender, owner, cost), "PYUSD transfer failed");

        // Persist access
        accessId = keccak256(
            abi.encodePacked(msg.sender, tstart, tend, block.timestamp, block.prevrandao, address(this))
        );

        Access storage b = accesses[accessId];
        b.user = msg.sender;
        b.tstart = tstart;
        b.tend = tend;
        // b.signed = false by default
        // b.signature = empty by default

        // Index by days covered
        (uint32 dStart, uint32 dEnd) = _daySpan(tstart, tend);
        for (uint32 d = dStart; d <= dEnd; d++) {
            // light sanity cap
            require(accessesByDay[d].length < MAX_DAY_BUCKET_SCAN, "Day bucket full");
            accessesByDay[d].push(accessId);
        }

        emit AccessCreated(accessId, msg.sender, tstart, tend, ens, bytes(""));
    }

    // -------------------- Off-chain fulfillment --------------------
    /// @notice External process attaches an access signature after any off-chain checks.
    ///         Only `signer` may call; emits AccessSigned.
    function fulfillSignature(bytes32 accessId, bytes calldata signature) external onlyOwner {
        Access storage b = accesses[accessId];
        require(b.user != address(0), "Unknown access");
        require(!b.signed, "Already signed");
        b.signed = true;
        b.signature = signature;
        emit AccessSigned(accessId, b.user, b.tstart, b.tend, ens, signature);
    }

    // -------------------- Views / Helpers --------------------
    function getAccess(bytes32 accessId) external view returns (Access memory) {
        return accesses[accessId];
    }

    function quote(uint64 tstart, uint64 tend) external view returns (uint256 pyusdAmount) {
        require(tend > tstart, "tend<=tstart");
        return uint256(tend - tstart) * pricePerSecond;
    }

    // -------------------- Internal: Overlap logic --------------------
    function _revertIfOverlaps(uint64 tstart, uint64 tend) internal view {
        (uint32 dStart, uint32 dEnd) = _daySpan(tstart, tend);

        // Scan accesses bucketed by each involved day (bounded by MAX_ACCESS_DAYS and MAX_DAY_BUCKET_SCAN).
        for (uint32 d = dStart; d <= dEnd; d++) {
            bytes32[] storage ids = accessesByDay[d];
            uint256 len = ids.length;
            for (uint256 i = 0; i < len; i++) {
                Access storage b = accesses[ids[i]];
                // An id may appear multiple times across days; this is fine—check is cheap.
                if (_overlaps(tstart, tend, b.tstart, b.tend)) {
                    revert("Interval overlaps existing access");
                }
            }
        }
    }

    function _overlaps(
        uint64 aStart,
        uint64 aEnd,
        uint64 bStart,
        uint64 bEnd
    ) internal pure returns (bool) {
        // Overlap if max(start) < min(end)
        return (aStart < bEnd) && (bStart < aEnd);
    }

    function _daySpan(uint64 tstart, uint64 tend) internal pure returns (uint32 dStart, uint32 dEnd) {
        dStart = uint32(tstart / SECONDS_PER_DAY);
        // If tend falls exactly on day boundary, it belongs to previous day bucket for [start, end)
        uint64 adjustedEnd = tend > 0 ? (tend - 1) : 0;
        dEnd = uint32(adjustedEnd / SECONDS_PER_DAY);
    }

    function _daysBetween(uint64 tstart, uint64 tend) internal pure returns (uint8) {
        (uint32 dStart, uint32 dEnd) = _daySpan(tstart, tend);
        return uint8(dEnd - dStart + 1);
    }

    // -------------------- Ownership --------------------
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "newOwner=0");
        owner = newOwner;
    }
}