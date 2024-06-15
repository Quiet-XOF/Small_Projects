import argparse
import datetime
import io
from PySide6 import QtCore, QtGui, QtWidgets
import qrcode
import sys
        

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Set up main window
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setWindowTitle("QR Code Generator")

        # Input text/url for code
        self.textURL = QtWidgets.QLineEdit()
        self.textURL.setMaxLength(150)
        self.textURL.setPlaceholderText("Enter QR Text Here")
        self.textURL.setClearButtonEnabled(True)
        self.layout.addWidget(self.textURL)
        self.textURL.textChanged.connect(self.getUrl)

        # Button to confirm text
        #self.confirm_button = QtWidgets.QPushButton("Confirm", self)
        #self.layout.addWidget(self.confirm_button)
        #self.confirm_button.clicked.connect(self.getUrl)

        # Choose colors
        # TODO can probably get rid of label
        colors = ["black", "blue", "brown", "cyan", "darkblue", "darkcyan", "darkgreen", "darkgrey", "darkmagenta", "darkred", "green", "lightgrey", "magenta", "red", "white", "yellow"]        
        self.fill = QtWidgets.QLabel()
        self.fill.setText("black")
        self.fill_combo = QtWidgets.QComboBox()
        self.fill_combo.addItems(colors)
        self.fill_combo.currentIndexChanged.connect(self.getFillColor)
        self.back = QtWidgets.QLabel()
        self.back.setText("white")
        self.back_combo = QtWidgets.QComboBox()
        self.back_combo.addItems(colors)
        self.back_combo.currentIndexChanged.connect(self.getBackColor)
        #self.layout.addWidget(self.fill)
        self.layout.addWidget(self.fill_combo)
        #self.layout.addWidget(self.back)
        self.layout.addWidget(self.back_combo)     

        # Print QRCode
        self.qrimage = QtWidgets.QLabel(self)   
        self.qrimage.setAlignment(QtCore.Qt.AlignCenter)     
        self.layout.addWidget(self.qrimage)

        # URL/text
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)

        # Download Image
        self.download_button = QtWidgets.QPushButton("Download", self)
        self.layout.addWidget(self.download_button)
        self.download_button.clicked.connect(self.downloadImage)

    def getUrl(self):
        # TODO Sanitize input
        QRtext = self.textURL.text()
        self.label.setText(QRtext)
        self.getImage()

    def getFillColor(self):
        new_color = self.fill_combo.currentText()
        self.fill.setText(new_color)
        self.getImage()

    def getBackColor(self):
        new_color = self.back_combo.currentText()
        self.back.setText(new_color)
        self.getImage()

    def getImage(self):
        qr = qrcode.QRCode()
        qr.add_data(self.textURL.text())
        image = qr.make_image(fill_color=self.fill.text(), back_color=self.back.text())
        
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        buffer_image = QtGui.QImage.fromData(buffer.read())
        pixmap = QtGui.QPixmap.fromImage(buffer_image)
        self.qrimage.setPixmap(pixmap)

        self.qr_image_buffer = buffer

    def downloadImage(self):
        if hasattr(self, "qr_image_buffer"):
            options = QtWidgets.QFileDialog.Options()
            file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save QR Code Image", "", "PNG Files (*.png);;All Files (*)", options=options)
            if file_name:
                with open(file_name, "wb") as f:
                    f.write(self.qr_image_buffer.getvalue())

def generateGUI():
    app = QtWidgets.QApplication([])
    widget = Widget()
    widget.resize(600, 400)
    widget.show()
    sys.exit(app.exec())

def parse_args():
    parser = argparse.ArgumentParser(
        description="Create QR Codes.",
        epilog="Enter text in quotes."   
    )
    parser.add_argument("text")
    parser.add_argument("--fill", "-f", help="Choose fill color.", action="store")
    parser.add_argument("--back", "-b", help="Choose back color.", action="store")
    return parser.parse_args()

def useArgsParse():
    try: 
        args = parse_args()
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
    image.save(f"QRCode_{stamp}.png")

if __name__ == "__main__":
    if len(sys.argv) == 1: generateGUI()
    else: useArgsParse()