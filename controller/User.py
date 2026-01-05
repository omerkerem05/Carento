from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer

from ui_py.UserPage import Ui_MainWindow
from controller.Rent import RentPage
from controller.Return import ReturnPage
from db.arac import Arac


class UserPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_filtrele.clicked.connect(self.filtrele_panel)
        self.ui.pushButton_filtreUygula.clicked.connect(self.listele)
        self.ui.pushButton_kirala.clicked.connect(self.open_rent_page)
        self.ui.pushButton_iadeEt.clicked.connect(self.open_return_page)

        self.ui.lineEdit_markaFiltrele.textChanged.connect(lambda text: self.to_upper(text, self.ui.lineEdit_markaFiltrele))
        self.ui.lineEdit_modelFiltrele.textChanged.connect(lambda text: self.to_upper(text, self.ui.lineEdit_modelFiltrele))

        self.ui.tableWidget_aracListesi.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.ui.dockWidget.hide()
        self.listele()
        QTimer.singleShot(0, self.sutun_ayarlari)

    def listele(self):
        marka_filtre = self.ui.lineEdit_markaFiltrele.text() or None
        model_filtre = self.ui.lineEdit_modelFiltrele.text() or None
        min_filtre = self.ui.lineEdit_minFiyat.text() or None
        max_filtre = self.ui.lineEdit_maxFiyat.text() or None
        secim = self.ui.comboBox_kiraDurumuFiltrele.currentText()
        match secim:
            case "Kirada olanları göster":
                durum_filtre = False
            case "Müsait olanları göster":
                durum_filtre = True
            case _:
                durum_filtre = None

        arabalar = Arac.listele(marka_filtre, model_filtre, min_filtre, max_filtre, durum_filtre)

        self.ui.tableWidget_aracListesi.setRowCount(0)

        for arac in arabalar:
            row = self.ui.tableWidget_aracListesi.rowCount()
            self.ui.tableWidget_aracListesi.insertRow(row)

            plaka_item = QTableWidgetItem(arac.plaka)
            plaka_item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_aracListesi.setItem(row, 0, plaka_item)
            marka_item = QTableWidgetItem(arac.marka)
            marka_item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_aracListesi.setItem(row, 1, marka_item)
            model_item = QTableWidgetItem(arac.model)
            model_item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_aracListesi.setItem(row, 2, model_item)
            ucret_item = QTableWidgetItem(str(int(arac.ucret)) + " TL")
            ucret_item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_aracListesi.setItem(row, 3, ucret_item)
            durum_item = QTableWidgetItem(("Müsait" if arac.musait_mi else "Kirada"))
            durum_item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_aracListesi.setItem(row, 4, durum_item)

    def open_rent_page(self):
        row = self.ui.tableWidget_aracListesi.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Hata", "Araç seçmediniz!")
            return
        plaka = self.ui.tableWidget_aracListesi.item(row, 0).text()
        if not Arac.bul(plaka).musait_mi:
            QMessageBox.warning(self, "Hata", "Seçtiğiniz araç zaten kirada.")
            return
        self.rent_page = RentPage(plaka)
        self.rent_page.kiralandi.connect(self.refresh_after_rent)
        self.rent_page.show()

    def refresh_after_rent(self, plaka):
        self.listele()
        QMessageBox.information(self, "Bilgilendirme", f"{plaka} plakalı araç başarıyla kiralandı!")

    def open_return_page(self):
        row = self.ui.tableWidget_aracListesi.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Hata", "Araç seçmediniz!")
            return
        plaka = self.ui.tableWidget_aracListesi.item(row, 0).text()
        if Arac.bul(plaka).musait_mi:
            QMessageBox.warning(self, "Hata", "Seçtiğiniz araç kirada değil.")
            return
        self.return_page = ReturnPage(plaka)
        self.return_page.iadeEdildi.connect(self.refresh_after_return)
        self.return_page.show()

    def refresh_after_return(self, plaka):
        self.listele()
        QMessageBox.information(self, "Bilgilendirme", f"{plaka} plakalı araç başarıyla iade edildi!")

    def filtrele_panel(self):
        if self.ui.dockWidget.isVisible():
            self.ui.dockWidget.hide()
        else:
            self.ui.dockWidget.show()
        QTimer.singleShot(0, self.sutun_ayarlari)

    def sutun_ayarlari(self):
        self.ui.tableWidget_aracListesi.setColumnWidth(0, int((self.ui.tableWidget_aracListesi.width()-25) * 0.21))
        self.ui.tableWidget_aracListesi.setColumnWidth(1, int((self.ui.tableWidget_aracListesi.width()-25) * 0.2))
        self.ui.tableWidget_aracListesi.setColumnWidth(2, int((self.ui.tableWidget_aracListesi.width()-25) * 0.2))
        self.ui.tableWidget_aracListesi.setColumnWidth(3, int((self.ui.tableWidget_aracListesi.width()-25) * 0.2))
        self.ui.tableWidget_aracListesi.setColumnWidth(4, int((self.ui.tableWidget_aracListesi.width()-25) * 0.2))

    def resizeEvent(self, event):
        self.sutun_ayarlari()
        return super().resizeEvent(event)

    def mousePressEvent(self, event):
        self.ui.tableWidget_aracListesi.clearSelection()
        self.ui.tableWidget_aracListesi.setCurrentItem(None)
        self.clearFocus()
        super().mousePressEvent(event)

    def to_upper(self, text, line_edit):
        cursor_pos = line_edit.cursorPosition()
        line_edit.setText(text.upper())
        line_edit.setCursorPosition(cursor_pos)