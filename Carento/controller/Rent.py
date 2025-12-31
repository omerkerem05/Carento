from PyQt5.QtWidgets import *

from ui_py.RentPage import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal, QDate

from db.arac import Arac
from db import hatalar
from db.kullanici import Kullanici

class RentPage(QMainWindow):
    kiralandi = pyqtSignal(str)

    def __init__(self, plaka):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_kirala.clicked.connect(self.arac_kirala)

        self.ui.lineEdit_adKirala.textChanged.connect(
            lambda text: self.to_upper(text, self.ui.lineEdit_adKirala))
        self.ui.dateEdit_baslangicKirala.dateChanged.connect(self.ucret_degistir)
        self.ui.dateEdit_bitisKirala.dateChanged.connect(self.ucret_degistir)

        arac = Arac.bul(plaka)
        self.ui.lineEdit_plakaKirala.setText(plaka)
        self.ui.lineEdit_markaKirala.setText(arac.marka)
        self.ui.lineEdit_modelKirala.setText(arac.model)

        self.ui.dateEdit_baslangicKirala.setDate(QDate.currentDate())
        self.ui.dateEdit_bitisKirala.setDate(QDate.currentDate().addDays(1))

    def arac_kirala(self):
        arac = Arac.bul(self.ui.lineEdit_plakaKirala.text())
        if arac is not None:
            try:
                kullanici = Kullanici(self.ui.lineEdit_adKirala.text())
                arac.kirala(kullanici, self.ui.dateEdit_baslangicKirala.date().toString("yyyy-MM-dd"),
                            self.ui.dateEdit_bitisKirala.date().toString("yyyy-MM-dd"))
                arac.kira_ucreti_hesapla(self.ui.dateEdit_baslangicKirala.date().toString("yyyy-MM-dd"),
                                         self.ui.dateEdit_bitisKirala.date().toString("yyyy-MM-dd"))
                self.kiralandi.emit(self.ui.lineEdit_plakaKirala.text())
                self.close()
            except hatalar.BosStringHatasi:
                QMessageBox.warning(self, "Hata", "Bilgileri doldurunuz.")
            except hatalar.GecersizTarihHatasi:
                QMessageBox.warning(self, "Hata", "Geçersiz tarih girdiniz.")
        else:
            QMessageBox.warning(self, "Hata", "Araç sistemde bulunmuyor.")

    def ucret_degistir(self):
        arac = Arac.bul(self.ui.lineEdit_plakaKirala.text())
        try:
            ucret = arac.kira_ucreti_hesapla(self.ui.dateEdit_baslangicKirala.date().toString("yyyy-MM-dd"),
                                             self.ui.dateEdit_bitisKirala.date().toString("yyyy-MM-dd"))
            self.ui.lineEdit_toplamUcretKirala.setText(str(ucret))
        except hatalar.GecersizTarihHatasi:
            self.ui.lineEdit_toplamUcretKirala.setText("---")

    def to_upper(self, text, line_edit):
        cursor_pos = line_edit.cursorPosition()
        line_edit.setText(text.upper())
        line_edit.setCursorPosition(cursor_pos)