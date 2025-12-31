import datetime

from PyQt5.QtWidgets import *

from ui_py.ReturnPage import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal

from db.arac import Arac
from db import hatalar
from db.kullanici import Kullanici

class ReturnPage(QMainWindow):
    iadeEdildi = pyqtSignal(str)

    def __init__(self, plaka):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_iade.clicked.connect(self.arac_iade)

        self.ui.lineEdit_adIade.textChanged.connect(
            lambda text: self.to_upper(text, self.ui.lineEdit_adIade))

        arac = Arac.bul(plaka)
        self.ui.lineEdit_plakaIade.setText(plaka)
        self.ui.lineEdit_markaIade.setText(arac.marka)
        self.ui.lineEdit_modelIade.setText(arac.model)

        baslangicTarihi = datetime.datetime.strptime(arac.baslangic_tarihi, "%Y-%m-%d")
        baslangicTarihiDuzeltilmis = baslangicTarihi.strftime("%d.%m.%Y")

        bitisTarihi = datetime.datetime.strptime(arac.bitis_tarihi, "%Y-%m-%d")
        bitisTarihiDuzeltilmis = bitisTarihi.strftime("%d.%m.%Y")

        self.ui.lineEdit_baslangicIade.setText(baslangicTarihiDuzeltilmis)
        self.ui.lineEdit_bitisIade.setText(bitisTarihiDuzeltilmis)
        self.ui.lineEdit_tarihIade.setText(datetime.date.today().strftime("%d.%m.%Y"))

        normal_tutar = arac.ucret_hesapla(arac.baslangic_tarihi, arac.bitis_tarihi)
        iade_tutari = arac.iade_ucreti_hesapla()
        odenecek = normal_tutar - iade_tutari
        self.ui.lineEdit_normalTutarIade.setText(str(normal_tutar))
        self.ui.lineEdit_iadeTutariIade.setText(str(iade_tutari))
        self.ui.lineEdit_odenecekIade.setText(str(odenecek))

    def arac_iade(self):
        arac = Arac.bul(self.ui.lineEdit_plakaIade.text())
        if arac is not None:
            try:
                kullanici = Kullanici(self.ui.lineEdit_adIade.text())
                arac.iade(kullanici)
                #arac.iadeTarihi = datetime.date.today().strftime("%Y-%m-%d")
                self.iadeEdildi.emit(self.ui.lineEdit_plakaIade.text())
                self.close()
            except hatalar.BosStringHatasi:
                QMessageBox.warning(self, "Hata", "Bilgileri doldurunuz.")
            except hatalar.YanlisKullanici:
                QMessageBox.warning(self, "Hata", "Aracı kiralayan kişi siz değilsiniz.")
        else:
            QMessageBox.warning(self, "Hata", "Araç sistemde bulunmuyor.")

    def to_upper(self, text, line_edit):
        cursor_pos = line_edit.cursorPosition()
        line_edit.setText(text.upper())
        line_edit.setCursorPosition(cursor_pos)