from PyQt5.QtWidgets import *
from ui_py.LoginPage import Ui_MainWindow

from controller.Admin import AdminPage
from controller.User import UserPage


class LoginPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton_kullanici.clicked.connect(self.kullanici_giris)
        self.ui.pushButton_admin.clicked.connect(self.admin_giris)

    def kullanici_giris(self):
        self.user_pencere = UserPage()
        self.user_pencere.setWindowTitle("Kullanıcı Paneli")
        self.user_pencere.show()

    def admin_giris(self):
        self.admin_pencere = AdminPage()
        self.admin_pencere.setWindowTitle("Admin Paneli")
        self.admin_pencere.show()

app = QApplication([])
pencere = LoginPanel()
pencere.show()
app.exec_()