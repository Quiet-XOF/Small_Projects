import argparse
import datetime
import qrcode
import sys
        
# A program that generates QR Codes
def parse_args():
    parser = argparse.ArgumentParser(
        description="Create QR Codes.",
        epilog="Enter text in quotes."   
    )
    parser.add_argument("text")
    parser.add_argument("--fill", "-f", help="Choose fill color.", action="store")
    parser.add_argument("--back", "-b", help="Choose back color.", action="store")
    return parser.parse_args()

def main():
    try: args = parse_args()
    except:
        print(f"Usage: python program.py \"Enter text here.\"")
        return

    if args.fill: fill = args.fill
    else: fill = "black"

    if args.back: back = args.back
    else: back = "white"

    qr = qrcode.QRCode()
    qr.add_data(args.text)

    try: image = qr.make_image(fill_color=fill, back_color=back)
    except:
        print("Error with color name.")
        return

    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image.save(f"QRCode{stamp}.png")

if __name__ == "__main__":
    main()