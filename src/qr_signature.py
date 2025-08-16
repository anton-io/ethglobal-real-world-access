#!/usr/bin/env bash
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image


def qr_generate(data, fnf_qr='qr_keypass.png'):
    # Create QR code instance.
    qr = qrcode.QRCode(
        version=1,  # Size of the QR code (1 to 40).
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level.
        box_size=10,  # Size of each box in pixels.
        border=4,     # Border thickness.
    )

    # Add data to the QR code.
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code.
    img = qr.make_image(fill_color="black", back_color="white")
    # Save the QR code image:
    img.save("qr_keypass.png")
    return True


def qr_read(fnf_qr='qr_keypass.png'):
    # Load the QR code image.
    image = Image.open(fnf_qr)

    # Decode the QR code
    decoded_objects = decode(image)

    # Print the decoded data
    for obj in decoded_objects:
        print("Decoded Data:", obj.data.decode("utf-8"))
        print("Type:", obj.type)
    return obj.data.decode("utf-8")

def example():
    data_write = {
        "user": "0x25a0fEC55dD7cc314A8Bb00e666489524b7d9cB9",
        "tstart": 1755555555,
        "tend": 1755559155,
        "ens": "room123.hotel.eth",
        "sig1": "0x50b985ba21094dce584b288d2726ddaf185675c80f955df07d956784b0f97d8d18dae37032c182b3196e4bd4a41796ebb8719ec97f1fd525d12a76da60419ab51b",
        "sig2": "0x8169b59a86b3b752a858d14b05c2751679b50d925d23b835ad63cee7352b65ae310dac6268266e5aabb1e7b52164ce95bbccebc10a1490d36563a9ba8f61081b1b"
    }
    qr_generate(data_write)

    # Read generated QR code:
    data_read = qr_read()

    # Check for exact equality.
    if data_write != data_read:
        print("error: written and read data is different!")


if __name__ == "__main__":
    example()