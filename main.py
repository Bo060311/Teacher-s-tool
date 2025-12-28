import sys
from PyQt6.QtWidgets import (QMainWindow, QApplication, QStackedWidget, QMessageBox, QTableWidgetItem)
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QTimer, Qt
from PyQt6 import uic
import random
import json
import math as mt
import pygame
from datetime import datetime as dt

class sign_up(QMainWindow):
#------------------------------------------------------------------    
    def center(self):#Hàm giúp cửa sổ luôn ở giữa màn hình
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        size.moveCenter(screen.center())
        self.move(size.topLeft())
#------------------------------------------------------------------
    def __init__(self):#load dữ liệu từ file
        super().__init__()
        uic.loadUi("current ui/signup.ui",self)
        self.signup.clicked.connect(self.address_signup) 
        self.had.clicked.connect(self.goto_signin)
        self.credit_btn.clicked.connect(self.credit)
        self.center()
#------------------------------------------------------------------
    def mesg(self,text,sign):#hàm tạo thông báo
        message = QMessageBox()
        message.setWindowTitle(sign)
        message.setText(text)
        message.show()
        message.exec()
#------------------------------------------------------------------    
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
                    self.mesg("Không tìm thấy file","Lỗi")
                    break
                if password == passcofirm:
                    if not len(password) > 8:
                        self.mesg("Cần nhập hơn 8 chữ cái","Lỗi đăng nhập")
                        break
                    else:
                        data2 = {
                        "username":username,
                        "password":password,
                        "class":[],
                        "hs_cc":1
                        }#Gom username và password để tiện
                        data["user"].append(data2)
                        with open("dulieu.json","w", encoding="utf-8") as f:#lưu vào file dữ liệu
                            json.dump(data,f,indent=4,ensure_ascii=False)
                        self.mesg("Success","Thông báo")
                        self.name1.setText("")
                        self.pass1.setText("")
                        self.pass_confirm.setText("")
                        break

                else:
                    self.mesg("Password is not same","Lỗi đăng nhập")
                    break
#------------------------------------------------------------------    
    def goto_signin(self):#đi đến màn hình đăng nhập
        self.sign_in.show()
        self.close()
#------------------------------------------------------------------
    def credit(self):
        self.goto_credit.show()
        self.goto_credit.play_sound()
        self.close()
#------------------------------------------------------------------
class sign_in(QMainWindow):#lớp xử lí đăng nhập
    def center(self):#vẫn là hàm căn giữa
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        size.moveCenter(screen.center())
        self.move(size.topLeft())
    #------------------------------------------------------------------
    def __init__(self):#lấy dữ liệu từ file UI
        super().__init__()
        uic.loadUi("current ui/signin.ui",self)
        self.signin.clicked.connect(self.address_signin)
        self.didnt_have.clicked.connect(self.goto_signup)
        self.credit_btn.clicked.connect(self.credit)
        self.center()
    #------------------------------------------------------------------
    def message(self,text,sign):#vẫn là hộp thoại thông báo
        message_box = QMessageBox()
        message_box.setWindowTitle(sign)
        message_box.setText(text)
        message_box.show()
        message_box.exec()
    #------------------------------------------------------------------
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
                    if i["username"] == "Lò Văn Tùng":
                        self.message("Chào mừng thầy Tùng đã quay trở lại","Thông báo")
                        self.name2.setText("")
                        self.pass2.setText("")
                        self.tungtool.current_user = username
                        self.tungtool.load_danh_sach()
                        self.tungtool.play_song()
                        self.tungtool.music(self.tungtool.volume.value())
                        self.tungtool.show()
                        self.go_to_tung()
                    else:
                        self.message("Login successfully","Thông báo")
                        self.name2.setText("")
                        self.pass2.setText("")
                        self.mainmenu.current_user = username
                        self.mainmenu.play_song()
                        self.mainmenu.music(self.mainmenu.volume.value())
                        self.mainmenu.load_danh_sach()
                        self.mainmenu.show()
                        found = True
                        self.main()
                else:
                    self.message("Password is incorrect","Lỗi đăng nhập")
                return
        if not found:
            self.message("Cannot find any accounts with that username","Lỗi")
    #------------------------------------------------------------------
    def goto_signup(self):#đi đến màn hình đăng kí
        self.signup.show()
        self.close()
    #------------------------------------------------------------------
    def go_to_tung(self):
        self.tungtool.show()
        self.close()
    #------------------------------------------------------------------
    def main(self):#đi đến màn hình chính
        self.mainmenu.show()
        self.close()
    #------------------------------------------------------------------
    def credit(self):
        self.goto_credit.show()
        self.goto_credit.play_sound()
        self.close()
#------------------------------------------------------------------
class mainmenu(QMainWindow):#lớp khởi tạo màn hình chính

    def message(self,text):
        message_box = QMessageBox()
        message_box.setWindowTitle("Thông báo")
        message_box.setText(text)
        message_box.show()
        message_box.exec()
    #------------------------------------------------------------------
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
    #------------------------------------------------------------------
    def center(self):#Yeah, vẫn là căn giữa mành hình
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        size.moveCenter(screen.center())
        self.move(size.topLeft())
    #------------------------------------------------------------------
    def __init__(self):#lấy dữ liệu UI từ file UI
        super().__init__()
        uic.loadUi("current ui/menu.ui",self)
        self.index = 0
        self.song = ["music/mood.mp3","music/Tet.mp3","music/Eiffel 65 - Blue (Da Ba Dee) (1080p_30fps_AV1-128kbit_AAC) (online-audio-converter.com).mp3","music/Forget.mp3","music/Last Christmas.mp3"]
        self.tableHocSinh.setRowCount(0)
        self.logout.clicked.connect(self.goto_signin)
        self.update.clicked.connect(self.tao_danh_sach)
        self.save.clicked.connect(self.luu_danh_sach)
        self.volume.valueChanged.connect(self.music)
        self.previous.clicked.connect(self.lui)
        self.next.clicked.connect(self.tien)
        # self.music()
        # self.load_ds.clicked.connect(self.load_danh_sach)
        # self.load_danh_sach()
        self.rdnum.clicked.connect(self.random)
        self.center()
        self.setup_time()
        self.may_tinh.clicked.connect(self.goto_cal)

        self.current_user = None 
    #------------------------------------------------------------------
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
    #------------------------------------------------------------------
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
        # print(data)
        with open("dulieu.json","w", encoding="utf-8") as f:
            json.dump(data,f,indent=4,ensure_ascii=False)
            self.message("Success")
    #------------------------------------------------------------------
    def goto_signin(self):#đi đến mành hình đăng nhập
        pygame.mixer.music.stop()
        self.sign_in.show()
        self.close()
    #------------------------------------------------------------------
    def random(self):
        with open("dulieu.json","r",encoding="utf-8") as f:
            data = json.load(f)
        for u in data["user"]:
            if u["username"] == self.current_user:
                lop = u["class"]
        num = random.randint(1,len(lop))
        self.rd_out.setText(str(num))
    #------------------------------------------------------------------
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
    #------------------------------------------------------------------
    def setup_time(self):
    # Tạo timer để update mỗi giây
        self.timer = QTimer()
        self.timer.timeout.connect(self.today)
        self.timer.start(1000)  # 1000 ms = 1 giây
    #------------------------------------------------------------------
    def goto_cal(self):
        self.calculator.show()
    #------------------------------------------------------------------
    def lui(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.song)-1
        self.play_song()
    def tien(self):
        self.index += 1
        if self.index >= len(self.song):
            self.index = 0
        self.play_song()
    def music(self,value):        
        pygame.mixer.music.set_volume(value/100)
    def play_song(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.song[self.index])
        pygame.mixer.music.play(-1)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
#------------------------------------------------------------------
class tungui(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("current ui/tungtest.ui",self)
        self.index = 0
        self.song = ["music/mood.mp3","music/Tet.mp3","music/Eiffel 65 - Blue (Da Ba Dee) (1080p_30fps_AV1-128kbit_AAC) (online-audio-converter.com).mp3","music/Forget.mp3","music/Last Christmas.mp3"]
        self.center()
        self.setup_time()
        self.bt.clicked.connect(self.bai_tap)
        self.save.clicked.connect(self.luu_danh_sach)
        self.update.clicked.connect(self.tao_danh_sach)
        self.logout.clicked.connect(self.goto_signin)
        self.calculator.clicked.connect(self.casio)
        self.volume.valueChanged.connect(self.music)
        self.previous.clicked.connect(self.lui)
        self.next.clicked.connect(self.tien)
    #------------------------------------------------------------------
    def bai_tap(self):
        with open("dulieu.json","r", encoding="utf-8") as f:
            data = json.load(f)
        for i in data["user"]:
            if i["username"] == "Lò Văn Tùng":
                hs = i["class"]
                start = i["hs_cc"]
                break
        sott1 = [int(j[0]) for j in hs]
        b = self.so_ban.value()
        if b > len(hs):
            self.message("What the hell nah")
        else:
            result = []
            for v,u in enumerate(data["user"]):
                if u["username"] == "Lò Văn Tùng":
                    tung = v
                    break
                    break
            for y in range(b):
                index = (start+y)%len(sott1)
                result.append(sott1[index])
            if len(result) > 0:
                start = result[len(result)-1]
                data["user"][v]["hs_cc"] = start
                with open("dulieu.json","w", encoding="utf-8") as f:
                    json.dump(data,f,indent=4,ensure_ascii=False)
                result1 = [str(x) for x in result]
                self.name.setText(f"Mời bạn có số thứ tự {",".join(result1)}")
    #------------------------------------------------------------------
    def message(self,text):
        message_box = QMessageBox()
        message_box.setWindowTitle("Thông báo")
        message_box.setText(text)
        message_box.show()
        message_box.exec()
    #------------------------------------------------------------------
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
    #------------------------------------------------------------------
    def center(self):#Yeah, vẫn là căn giữa mành hình
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        size.moveCenter(screen.center())
        self.move(size.topLeft())
    #------------------------------------------------------------------
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
    #------------------------------------------------------------------
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
        # print(data)
        with open("dulieu.json","w", encoding="utf-8") as f:
            json.dump(data,f,indent=4,ensure_ascii=False)
            self.message("Success")
    #------------------------------------------------------------------
    def goto_signin(self):#đi đến mành hình đăng nhập
        pygame.mixer.music.stop()
        self.sign_in.show()
        self.close()
    #------------------------------------------------------------------
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
    #------------------------------------------------------------------
    def setup_time(self):
    # Tạo timer để update mỗi giây
        self.timer = QTimer()
        self.timer.timeout.connect(self.today)
        self.timer.start(1000)  # 1000 ms = 1 giây
    #------------------------------------------------------------------
    def center(self):#Yeah, vẫn là căn giữa mành hình
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        size.moveCenter(screen.center())
        self.move(size.topLeft())
    #------------------------------------------------------------------
    def casio(self):
        self.calculator.show()
    def lui(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.song)-1
        self.play_song()
    def tien(self):
        self.index += 1
        if self.index >= len(self.song):
            self.index = 0
        self.play_song()
    def music(self,value):        
        pygame.mixer.music.set_volume(value/100)
    def play_song(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.song[self.index])
        pygame.mixer.music.play(-1)
#------------------------------------------------------------------
class credit(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("current ui/credit.ui",self)
        self.back.clicked.connect(self.goto_signin)
        
    def play_sound(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load("music/sans.mp3")
        pygame.mixer.music.play()
    def goto_signin(self):
        pygame.mixer.music.stop()
        self.signin.show()
        self.close()
#------------------------------------------------------------------
class calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("current ui/calculator.ui",self)
        self.center()
        self.a = ""
        self.music()
        self.sfx = ["music/bruh.mp3","music/fahhhhhhhhhhhhhh.mp3","music/trojan.mp3"]
        self.one.clicked.connect(self.mot)#bug nặng vl
        self.two.clicked.connect(self.hai)
        self.three.clicked.connect(self.ba)
        self.four.clicked.connect(self.bon)
        self.five.clicked.connect(self.nam)
        self.six.clicked.connect(self.sau)
        self.seven.clicked.connect(self.bay)
        self.eight.clicked.connect(self.tam)
        self.nine.clicked.connect(self.chin)
        self.zero.clicked.connect(self.khong)
        self.plus.clicked.connect(self.cong)
        self.minus.clicked.connect(self.tru)
        self.mutiply.clicked.connect(self.nhan)
        self.divide.clicked.connect(self.chia)
        self.equal.clicked.connect(self.bang)
        self.delete_all.clicked.connect(self.xoa)
    #------------------------------------------------------------------
    def center(self):#Yeah, vẫn là căn giữa mành hình
        screen = QGuiApplication.primaryScreen().availableGeometry()
        size = self.frameGeometry()
        size.moveCenter(screen.center())
        self.move(size.topLeft())
    #------------------------------------------------------------------
    def mot(self):
        self.pheptinh("1")
    #------------------------------------------------------------------
    def hai(self):
        self.pheptinh("2")
    #------------------------------------------------------------------
    def ba(self):
        self.pheptinh("3")
    #------------------------------------------------------------------
    def bon(self):
        self.pheptinh("4")
    #------------------------------------------------------------------
    def nam(self):
        self.pheptinh("5")
    #------------------------------------------------------------------
    def sau(self):
        self.pheptinh("6")
    #------------------------------------------------------------------
    def bay(self):
        self.pheptinh("7")
    #------------------------------------------------------------------
    def tam(self):
        self.pheptinh("8")
    #------------------------------------------------------------------
    def chin(self):
        self.pheptinh("9")
    #------------------------------------------------------------------
    def khong(self):
        self.pheptinh("0")
    #------------------------------------------------------------------
    def cong(self):
        self.pheptinh("+")
    #------------------------------------------------------------------
    def tru(self):
        self.pheptinh("-")
    #------------------------------------------------------------------
    def nhan(self):
        self.pheptinh("*")
    #------------------------------------------------------------------
    def chia(self):
        self.pheptinh("/")
    #------------------------------------------------------------------
    def bang(self):
        self.pheptinh("=")
    #------------------------------------------------------------------
    def xoa(self):
        self.pheptinh("X")
    #------------------------------------------------------------------
    def music(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1)
    def play_music(self,song):
        
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()
    def pheptinh(self,operation):
        if operation == "=":
            try:
                b = eval(self.a)
                self.result.setText(str(b))
            except (ZeroDivisionError, SyntaxError):
                self.play_music(random.choice(self.sfx))
                self.message("Lỗi phép tính","Oh hell nah")
                self.a = ""
                self.result.setText(self.a)
            
        elif operation == "X":
            self.a = ""
            self.result.setText(self.a) 
        else:
            self.a += operation
            self.result.setText(self.a)
    #------------------------------------------------------------------
    def message(self,text,sign):
        message_box = QMessageBox()
        message_box.setWindowTitle(sign)
        message_box.setText(text)
        message_box.show()
        message_box.exec()
#------------------------------------------------------------------
if __name__ == "__main__":
    #code khởi tạo và chậy app
    app = QApplication(sys.argv)
    signin_window = sign_in()
    signup_window = sign_up()
    mainmenu_window = mainmenu()
    tungtool_window = tungui()
    credit_window = credit()
    casio_window = calculator()
    mainmenu_window.calculator = casio_window
    tungtool_window.calculator = casio_window
    signin_window.goto_credit = credit_window
    signup_window.goto_credit = credit_window
    credit_window.signin = signin_window
    tungtool_window.sign_in = signin_window
    signin_window.signup = signup_window
    signin_window.tungtool = tungtool_window
    signup_window.sign_in = signin_window
    signin_window.mainmenu = mainmenu_window
    mainmenu_window.sign_in = signin_window
    signin_window.show()
    app.exec()
    #buồn ngủ quá, mệt vãi