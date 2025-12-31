from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer

from ui_py.AdminPage import Ui_MainWindow
from controller.Add import AddPage
from controller.Edit import EditPage
from db.arac import Arac

class AdminPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_filtrele.clicked.connect(self.filtrele_panel)
        self.ui.pushButton_filtreUygula.clicked.connect(self.listele)
        self.ui.pushButton_ekle.clicked.connect(self.open_add_page)

        self.ui.lineEdit_markaFiltrele.textChanged.connect(lambda text: self.to_upper(text, self.ui.lineEdit_markaFiltrele))
        self.ui.lineEdit_modelFiltrele.textChanged.connect(lambda text: self.to_upper(text, self.ui.lineEdit_modelFiltrele))

        self.ui.tableWidget_aracListesi.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.ui.tableWidget_aracListesi.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.tableWidget_aracListesi.customContextMenuRequested.connect(self.table_context_menu)

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
            ucret_item = QTableWidgetItem(str(int(arac.ucret))+ " TL")
            ucret_item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_aracListesi.setItem(row, 3, ucret_item)
            durum_item = QTableWidgetItem(("Müsait" if arac.musait_mi else "Kirada"))
            durum_item.setTextAlignment(Qt.AlignCenter)
            self.ui.tableWidget_aracListesi.setItem(row, 4, durum_item)

    def table_context_menu(self, pos):
        selected = self.ui.tableWidget_aracListesi.itemAt(pos)
        if selected is None:
            return  # Boş alana sağ tıkladıysa menü çıkmasın

        menu = QMenu()

        delete_action = QAction("Sil", self)
        delete_action.triggered.connect(self.clicked_delete)
        edit_action = QAction("Düzenle", self)
        edit_action.triggered.connect(self.clicked_edit)

        menu.addAction(delete_action)
        menu.addAction(edit_action)

        menu.setStyleSheet("""
                QMenu {
                    background-color: #343434;
                    color: #e4e3e0;
                    border: 1px solid #2e2e2e;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 6px 20px;
                    background-color: transparent;
                    color: #e4e3e0;
                }
                QMenu::item:selected {
                    background-color: #2a2a2a;
                }
            """)

        menu.exec_(self.ui.tableWidget_aracListesi.mapToGlobal(pos))


    def open_add_page(self):
        self.add_page = AddPage()
        self.add_page.eklendi.connect(self.refresh_after_add)
        self.add_page.show()

    def refresh_after_add(self, plaka):
        self.listele()
        QMessageBox.information(self, "Bilgilendirme", f"{plaka} plakalı araç başarıyla eklendi!")


    # DELETE
    def clicked_delete(self):
        row = self.ui.tableWidget_aracListesi.currentRow()
        if row < 0:
            return
        plaka = self.ui.tableWidget_aracListesi.item(row, 0).text()
        arac = Arac.bul(plaka)
        onay = QMessageBox.question(self, "Silme İşlemi",
                                    f"{plaka} plakalı aracı silmek istediğinize emin misiniz?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if onay == QMessageBox.Yes:
            Arac.sil(arac)
            self.listele()
            QMessageBox.information(self, "Bilgilendirme", "Araç başarıyla silindi.")


    #EDIT
    def clicked_edit(self):
        row = self.ui.tableWidget_aracListesi.currentRow()
        if row < 0:
            return
        self.open_edit_page()

    def open_edit_page(self):
        row = self.ui.tableWidget_aracListesi.currentRow()
        plaka = self.ui.tableWidget_aracListesi.item(row, 0).text()
        self.edit_page = EditPage(plaka)
        self.edit_page.duzenlendi.connect(self.refresh_after_edit)
        self.edit_page.show()

    def refresh_after_edit(self, plaka):
        self.listele()
        QMessageBox.information(self, "Bilgilendirme", f"{plaka} plakalı araç başarıyla düzenlendi!")



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