import  sys
import  cv2
from PyQt5 import  QtCore, QtWidgets
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow,QFileDialog
import pytesseract



class ShowImage(QMainWindow):
    def __init__(self):
        super(ShowImage, self).__init__()
        loadUi('GUI.ui',self)
        self.Image = None
        self.pushButton.clicked.connect(self.fungsi)

        self.pushButton_5.clicked.connect(self.ocr)
        self.pushButton_2.clicked.connect(self.load)

        self.actionsave.triggered.connect(self.save)



    def ocr(self):

        pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        img = self.Image

        #grayscale
        img1 = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        cv2.imshow("grayscale",img1)
        #print(img1)

        #Tresshold
        ret, img2 = cv2.threshold(img1, 120, 255, cv2.THRESH_TRUNC)
        cv2.imshow("Thres",img2)
        #print(img2)

        #morfologi erosi
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (1, 2))
        erosi = cv2.erode(img2, kernel, iterations=1)
        #print(erosi)
        text = pytesseract.image_to_string(erosi, lang='ind')
        #print(text)
        self.label_4.setText(text)

        #normalisasi
        for word in text.splitlines():
            if "PROVINSI" in word:
                word = word.replace("","")
                self.label_6.setText(word)

            if "KABUPATEN" in word:
                word = word.replace("","")
                self.label_7.setText(word)

            if "NIK " in word:
                word = word.replace("NIK 1", "NIK :")
                self.label_8.setText(word)

            if "Nama " in word:
                word = word.replace("", "")
                word = word.replace("Nama ", "Nama : ")
                word = word.replace("Nama : :", "Nama : ")
                self.label_9.setText(word)


            if "Tempat" in word :
                word = word.replace("Tg!", "Tgl")
                word = word.replace("Tgi", "Tgl")
                self.label_10.setText(word)


            if "Jenis " in word:
                word = word.replace("kelamin", "kelamin :")
                word = word.replace("Kelamin ", "Kelamin : ")
                word = word.replace("Darah", "Darah : ")
                word = word.replace("Darah : :", "Darah : ")
                self.label_11.setText(word)

            if "Alamat" in word:
                word = word.replace("Alamat ", "Alamat : ")
                self.label_12.setText(word)

            if "RTRW" in word:
                word = word.replace("RTRW", "RT/RW :")
                self.label_13.setText(word)

            if "Kel" in word:
                word = word.replace("Kell", "Kel/")
                word = word.replace("Kel/", "Kel/")
                word = word.replace("KelDesa","Kel/Desa :")
                word = word.replace("T/O","TO")
                self.label_14.setText(word)

            if "Kecamatan" in word:
                word = word.replace("", "")
                self.label_15.setText(word)

            if "Agama" in word:
                word = word.replace("Agama ", "Agama : ")
                word = word.replace("Agama : :", "Agama : ")
                self.label_16.setText(word)

            if "Status" in word:
                word = word.replace("", "")
                self.label_17.setText(word)

            if "Pekerjaan" in word:
                word = word.replace("Pekerjaan ", "Pekerjaan : ")
                word = word.replace("Pekerjaan : :", "Pekerjaan : ")
                self.label_18.setText(word)

            if "Kewarga" in word:
                word = word.replace("","")
                self.label_19.setText(word)

            if "Berlaku" in word:
                word = word.replace("Hingga ", "Hingga : ")
                self.label_20.setText(word)

            #print(word)





        self.Image = erosi
        self.displayImage(2)




    def fungsi(self):

        self.Image, img = QFileDialog.getOpenFileName(self, 'Open File ', 'r' + 'C:\\',
                                                                                        "Image Files(*.jpg *.jpeg)")

        imagePath = self.Image[0]
        print(imagePath)
        pixmap = QPixmap(imagePath)


        self.label.setPixmap(QPixmap(pixmap))
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.label.setScaledContents(True)

    def load(self):
        img = cv2.imread(self.Image)
        self.Image = img
        self.displayImage(1)




    def save(self):
        cv2.imwrite('output.jpg', self.Image)


    def displayImage(self, window):
        qformat = QImage.Format_Indexed8

        if len(self.Image.shape)==3:
            if(self.Image.shape[2])==4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        img = QImage(self.Image, self.Image.shape[1], self.Image.shape[0],
                     self.Image.strides[0], qformat)

        img = img.rgbSwapped()


        if window == 1:
            self.label.setPixmap(QPixmap.fromImage(img))
            self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label.setScaledContents(True)
        if window == 2:
            self.label_2.setPixmap(QPixmap.fromImage(img))
            self.label_2.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.label_2.setScaledContents(True)
            return self.label




app = QtWidgets.QApplication(sys.argv)
window = ShowImage()
window.setWindowTitle('Aplikasi Pendeteksi Teks KTP')
window.show()
sys.exit(app.exec_())