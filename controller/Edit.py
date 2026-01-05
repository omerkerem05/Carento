from PyQt5.QtWidgets import *
from ui_py.EditPage import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal

from db.arac import Arac
from db import hatalar

class EditPage(QMainWindow):
    duzenlendi = pyqtSignal(str)

    def __init__(self, plaka):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_duzenle.clicked.connect(self.arac_duzenle)

        self.ui.lineEdit_markaDuzenle.textChanged.connect(
            lambda text: self.to_upper(text, self.ui.lineEdit_markaDuzenle))
        self.ui.lineEdit_modelDuzenle.textChanged.connect(
            lambda text: self.to_upper(text, self.ui.lineEdit_modelDuzenle))

        self.ui.lineEdit_plakaDuzenle.setText(plaka)

    def arac_duzenle(self):
        arac = Arac.bul(self.ui.lineEdit_plakaDuzenle.text())
        if arac is not None:
            try:
                arac = Arac(self.ui.lineEdit_plakaDuzenle.text(), self.ui.lineEdit_markaDuzenle.text(),
                            self.ui.lineEdit_modelDuzenle.text(), float(self.ui.spinBox_gunlukUcretDuzenle.text()))
                self.duzenlendi.emit(self.ui.lineEdit_plakaDuzenle.text())
                self.close()
            except hatalar.BosStringHatasi:
                QMessageBox.warning(self, "Hata", "Bilgileri doldurunuz.")
            except hatalar.GecersizUcretHatasi:
                QMessageBox.warning(self, "Hata", "Ücret giriniz.")
        else:
            QMessageBox.warning(self, "Hata", "Araç sistemde bulunmuyor.")

    def to_upper(self, text, line_edit):
        cursor_pos = line_edit.cursorPosition()
        line_edit.setText(text.upper())
        line_edit.setCursorPosition(cursor_pos)