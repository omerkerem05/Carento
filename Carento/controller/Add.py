from PyQt5.QtWidgets import *
from ui_py.AddPage import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal

from db.arac import Arac
from db import hatalar

class AddPage(QMainWindow):
    eklendi = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_ekle.clicked.connect(self.arac_ekle)

        self.ui.lineEdit_plakaEkle.textChanged.connect(
            lambda text: self.to_upper(text, self.ui.lineEdit_plakaEkle))
        self.ui.lineEdit_markaEkle.textChanged.connect(
            lambda text: self.to_upper(text, self.ui.lineEdit_markaEkle))
        self.ui.lineEdit_modelEkle.textChanged.connect(
            lambda text: self.to_upper(text, self.ui.lineEdit_modelEkle))

    def arac_ekle(self):
        arac = Arac.bul(self.ui.lineEdit_plakaEkle.text())
        if arac is None:
            try:
                arac = Arac(self.ui.lineEdit_plakaEkle.text(), self.ui.lineEdit_markaEkle.text(),
                            self.ui.lineEdit_modelEkle.text(), float(self.ui.spinBox_gunlukUcretEkle.text()))
                self.eklendi.emit(self.ui.lineEdit_plakaEkle.text())
                self.close()
            except hatalar.BosStringHatasi:
                QMessageBox.warning(self, "Hata", "Bilgileri doldurunuz.")
            except hatalar.GecersizUcretHatasi:
                QMessageBox.warning(self, "Hata", "Ücret giriniz.")
        else:
            QMessageBox.warning(self, "Hata", "Sistemde bulunmayan bir araba giriniz.")

    def to_upper(self, text, line_edit):
        cursor_pos = line_edit.cursorPosition()
        line_edit.setText(text.upper())
        line_edit.setCursorPosition(cursor_pos)