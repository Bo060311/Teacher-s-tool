import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QMessageBox, QTableWidgetItem)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QTimer
from PyQt6 import uic
import random
import json
from datetime import datetime as dt

class sign_up(QMainWindow):
    def center(self):#Hàm giúp cửa sổ luôn ở giữa màn hình
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        size.moveCenter(screen.center())
        self.move(size.topLeft())
    def __init__(self):#load dữ liệu từ file
        super().__init__()
        uic.loadUi("signup.ui",self)
        self.signup.clicked.connect(self.address_signup) 
        self.had.clicked.connect(self.goto_signin)
        self.center()
    def mesg(self,text):#hàm tạo thông báo
        message = QMessageBox()
        message.setText(text)
        message.show()
        message.exec()
    def address_signup(self):#hàm xử lí đăng kí
        username = self.name1.text()
        password = self.pass1.text()
        passcofirm = self.pass_confirm.text()
        with open("dulieu.json","r",encoding= "utf-8") as f:#lấy dữ liệu từ file dât
            data = json.load(f)
        for u in data["user"]:
            if u["username"] == username and u["password"] == password:#nếu tài khoản đã có thì nhắc nhở
                self.mesg("Tài khoản đã tồn tại")
                break
            else:
                try:
                    with open("dulieu.json","r", encoding="utf-8") as f:
                        data = json.load(f)# lấy dữ liệu
                except (FileNotFoundError, json.JSONDecodeError):#nếu ko tìm thấy thì thôi
                    data = {"user":[]}
                    self.mesg("Không tìm thấy file")
                    break
                if password == passcofirm:
                    if not len(password) > 8:
                        self.mesg("Cần nhập hơn 8 chữ cái")
                        break
                    else:
                        data2 = {
                        "username":username,
                        "password":password,
                        "class":[]
                        }#Gom username và password để tiện
                        data["user"].append(data2)
                        with open("dulieu.json","w", encoding="utf-8") as f:#lưu vào file dữ liệu
                            json.dump(data,f,indent=4,ensure_ascii=False)
                        self.mesg("Success")
                        break

                else:
                    self.mesg("Password is not same")
                    break
    def goto_signin(self):#đi đến màn hình đăng nhập
        self.sign_in.show()
        self.close()
class sign_in(QMainWindow):#lớp xử lí đăng nhập
    def center(self):#vẫn là hàm căn giữa
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        size.moveCenter(screen.center())
        self.move(size.topLeft())
    def __init__(self):#lấy dữ liệu từ file UI
        super().__init__()
        uic.loadUi("signin.ui",self)
        self.signin.clicked.connect(self.address_signin)
        self.didnt_have.clicked.connect(self.goto_signup)
        self.center()
    def message(self,text):#vẫn là hộp thoại thông báo
        message_box = QMessageBox()
        message_box.setText(text)
        message_box.show()
        message_box.exec()
    def address_signin(self):# xử lí đăng nhập
        found = False
        username = self.name2.text()
        password = self.pass2.text()
        current_name = None
        current_pass = None
        with open("dulieu.json","r", encoding="utf-8") as f:#lôi dữ liệu từ file dữ liệu
            data = json.load(f)
        for i in data["user"]:#check su sánh tài khoảng đang đăng nhập và tài khoản đã lưu
            if i["username"] == username:
                if i["password"] == password:
                    self.message("Login successfully")
                    self.mainmenu.current_user = username
                    found = True
                    self.main()
                else:
                    self.message("Password is incorrect")
                return
        if not found:
            self.message("Cannot find any accounts with that username")

    def goto_signup(self):#đi đến màn hình đăng kí
        self.signup.show()
        self.close()
    def main(self):#đi đến màn hình chính
        self.mainmenu.show()
        self.close()
class mainmenu(QMainWindow):#lớp khởi tạo màn hình chính
    def load_danh_sach(self):
        with open("dulieu.json","r", encoding="utf-8") as f:    
            data = json.load(f)
        for u in data["user"]:
            if u["username"] == self.current_user:
                lop = u["class"]
                break
        self.tableHocSinh.setRowCount(len(lop))
        for i, row in enumerate(lop):#--> index,value
            for j, val in enumerate(row):#--> index,value
                self.tableHocSinh.setItem(i, j, QTableWidgetItem(val)) # --> row,column,value
    def center(self):#Yeah, vẫn là căn giữa mành hình
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        size.moveCenter(screen.center())
        self.move(size.topLeft())
    def __init__(self):#lấy dữ liệu UI từ file UI
        super().__init__()
        uic.loadUi("menu.ui",self)
        self.tableHocSinh.setRowCount(0)
        self.current_user = None 
        self.logout.clicked.connect(self.goto_signin)
        self.update.clicked.connect(self.tao_danh_sach)
        self.save.clicked.connect(self.luu_danh_sach)
        self.load_ds.clicked.connect(self.load_danh_sach)
        self.rdnum.clicked.connect(self.random)
        self.center()
        self.setup_time()
    def tao_danh_sach(self):# hàm tạo danh sách lớp
        # Lấy số từ ô nhập sĩ số
        so_luong = self.spinBoxSiSo.value()
        lop = self.lop.text()
        
        # Thiết lập số hàng cho bảng
        self.tableHocSinh.setRowCount(so_luong)

        # Chạy vòng lặp để điền từng hàng
        for i in range(so_luong):
            # Điền cột 0: Số thứ tự
            self.tableHocSinh.setItem(i, 0, QTableWidgetItem(str(i + 1)))

            # Điền cột 1 và 2: Để trống; cột 3 điền lớp 
            self.tableHocSinh.setItem(i, 1, QTableWidgetItem(""))
            self.tableHocSinh.setItem(i, 2, QTableWidgetItem(""))
            self.tableHocSinh.setItem(i,3,QTableWidgetItem(str(lop)))
    def luu_danh_sach(self):
        table_data = []
        for row in range(self.tableHocSinh.rowCount()):             
            row_list = []                                           
            for col in range(self.tableHocSinh.columnCount()):
                item = self.tableHocSinh.item(row, col)
                row_list.append(item.text() if item else "")
            table_data.append(row_list)
        print(table_data)
        with open("dulieu.json","r", encoding="utf-8") as f:    
            data = json.load(f)
        for u in data["user"]:
            if u["username"] == self.current_user:
                u["class"] = (table_data)
                break
        print(data)
        with open("dulieu.json","w", encoding="utf-8") as f:
            json.dump(data,f,indent=4,ensure_ascii=False)
    def goto_signin(self):#đi đến mành hình đăng nhập
        self.sign_in.show()
        self.close()
    def random(self):
        with open("dulieu.json","r",encoding="utf-8") as f:
            data = json.load(f)
        for u in data["user"]:
            if u["username"] == self.current_user:
                lop = u["class"]
        num = random.randint(0,len(lop))
        self.rd_out.setText(str(num))
    def today(self):
        now = dt.now()
        day = now.day
        month = now.month
        year = now.year
        h = now.hour
        m = now.minute
        s = now.second
        self.time.setText(f"{now.day:02d}/{now.month:02d}/{now.year}")
        self.date.setText(f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}")
    def setup_time(self):
    # Tạo timer để update mỗi giây
        self.timer = QTimer()
        self.timer.timeout.connect(self.today)
        self.timer.start(1000)  # 1000 ms = 1 giây
#code khởi tạo và chậy app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    signin_window = sign_in()
    signup_window = sign_up()
    mainmenu_window = mainmenu()
    signin_window.signup = signup_window
    signup_window.sign_in = signin_window
    signin_window.mainmenu = mainmenu_window
    mainmenu_window.sign_in = signin_window
    signin_window.show()
    app.exec()
    #buồn ngủ quá, mệt vãi