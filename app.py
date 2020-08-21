# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 23:36:01 2020

@author: frdiersln
"""

from PyQt5 import QtWidgets
import sys
from MainWindow import Ui_Form

from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import Qt
import webbrowser

class App(QtWidgets.QMainWindow):
    
    def __init__(self):
        
        super(App, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Twitch GiveAway!")
        self.ui.textEdit.setText("")
        self.ui.textEdit_2.setText("")
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.ui.oPos = self.pos()
        self.setFixedSize(769, 908) 
        self.ui.frame.setVisible(0)
        self.vis = 0
        self.dil = "Türkçe"
        self.ui.frame.setGeometry(290, 60, 361 , 131)
        self.ui.textEdit.setLineWrapMode(False)
        self.ui.textEdit_2.setLineWrapMode(False)
        self.katilimcilar = []
        self.k_mesajlari = []
        self.kazananlar = []
        with open("kanal.txt", "r") as kanal_file:
            self.ui.textEdit.setText(kanal_file.read())
            self.kanal = str(self.ui.textEdit.toPlainText())
        self.ui.spinBox.setValue(1)
        self.kontrol = 0
        self.ui.groupBox_2.setTitle("Destek")
        self.setAttribute(Qt.WA_TranslucentBackground)
        
    def mousePressEvent(self, event):
        self.oPos = event.globalPos()

    def mouseMoveEvent(self, QMouseEvent):
        delta = QPoint(QMouseEvent.globalPos() - self.oPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oPos = QMouseEvent.globalPos()
        
    def ayarlar(self):
        
        if self.vis == 0:
            
            self.vis = 1
            self.ui.frame.setVisible(1)
            
        elif self.vis == 1:
            
            self.vis = 0
            self.ui.frame.setVisible(0)
            
    def kere_cek(self,sayi):
        
        if str(sayi) == "":
            
            self.ui.spinBox.setValue(1)
            
        elif sayi > 20:
            
            self.ui.spinBox.setValue(20)
            
        elif sayi < 1:
            
            self.ui.spinBox.setValue(1)
            
    def language(self):
        
        self.dil = "eng"
        self.ui.horizontalSlider.setSliderPosition(1)
        self.ui.label_2.setText("Everyone")
        self.ui.label_3.setText("Channel:")
        self.ui.label.setText("Keyword:")
        self.ui.pushButton_2.setText("Draw")
        self.ui.label_6.setText("Winners")
        self.ui.label_5.setText("Attendants")
        self.ui.groupBox.setTitle("Language")
        self.ui.groupBox_2.setTitle("Donate")
        if self.ui.pushButton.text() == "Başlat":
            self.ui.pushButton.setText("Start")
        elif self.ui.pushButton.text() == "Durdur":
            self.ui.pushButton.setText("Stop")
    
    def dil(self): 
        
        self.dil = "Türkçe"
        self.ui.horizontalSlider.setSliderPosition(1)
        self.ui.label_2.setText("Herkese açık")
        self.ui.label_3.setText("Kanal İsmi:")
        self.ui.label.setText("Anahtar Kelime:")
        self.ui.pushButton_2.setText("Çek")
        self.ui.label_6.setText("Kazananlar")
        self.ui.label_5.setText("Katılanlar")
        self.ui.groupBox.setTitle("Dil")
        self.ui.groupBox_2.setTitle("Destek")

        if self.ui.pushButton.text() == "Start":
            self.ui.pushButton.setText("Başlat")
        elif self.ui.pushButton.text() == "Stop":
            self.ui.pushButton.setText("Durdur")

    def kanal(self):
        
        self.kanal = str(self.ui.textEdit.toPlainText())
        if str(self.kanal) == "":
            pass
        elif "\n" in str(self.kanal):
            pass
        else:
            with open("kanal.txt", "w") as kanal_file:
                kanal_file.write(str(self.kanal))
                
        if "\n" in str(self.ui.textEdit.toPlainText()):
            x = (str(self.ui.textEdit.toPlainText())).split('\n')
            self.ui.textEdit.setText(x[0])
            if self.ui.textEdit.toPlainText() == "":
                pass
            else:
                self.ui.textEdit_2.setFocus()
            self.baslat()
        
    def keyword(self):
        
        self.keyword = str(self.ui.textEdit_2.toPlainText())
        if "\n" in str(self.ui.textEdit_2.toPlainText()):
            x = (str(self.ui.textEdit_2.toPlainText())).split('\n')
            self.ui.textEdit_2.setText(x[0])
            if self.kanal == "":
                
                self.ui.textEdit.setFocus()
            
            else:
                
                self.ui.pushButton.setFocus()
                
            self.baslat()
        
    def baslat(self): #pushButton
        
        if self.ui.pushButton.text() == "Başlat":
            
            if not (self.kanal or self.keyword):
                
                self.thr1 = Thread(target=self.shake, args = (self.ui.textEdit, self ))
                self.thr1.start()
                self.thr2 = Thread(target=self.shake, args = (self.ui.textEdit_2, self))
                self.thr2.start()
                                        
            elif not self.kanal:
                
                self.thr1 = Thread(target=self.shake, args = (self.ui.textEdit, self ))
                self.thr1.start()
                
            elif not self.keyword:
         
                self.thr2 = Thread(target=self.shake, args = (self.ui.textEdit_2, self))
                self.thr2.start()
                
            else: #döngüyü başlat butona Durdur yaz
                
                if self.dil == "Türkçe":
                    self.ui.pushButton.setText("Durdur")
                elif self.dil == "eng":
                    self.ui.pushButton.setText("Stop")
                self.thr = Thread(target=self.dongu)
                self.thr.start()
                
        elif self.ui.pushButton.text() == "Start":
            
            if not (self.kanal or self.keyword):
                
                self.thr1 = Thread(target=self.shake, args = (self.ui.textEdit, self ))
                self.thr1.start()
                self.thr2 = Thread(target=self.shake, args = (self.ui.textEdit_2, self))
                self.thr2.start()
                                        
            elif not self.kanal:
                
                self.thr1 = Thread(target=self.shake, args = (self.ui.textEdit, self ))
                self.thr1.start()
                
            elif not self.keyword:
         
                self.thr2 = Thread(target=self.shake, args = (self.ui.textEdit_2, self))
                self.thr2.start()
                
            else: #döngüyü başlat butona stop yaz
                
                if self.dil == "Türkçe":
                    self.ui.pushButton.setText("Durdur")
                elif self.dil == "eng":
                    self.ui.pushButton.setText("Stop")
                self.thr = Thread(target=self.dongu)
                self.thr.start()
        
        elif self.ui.pushButton.text() == "Durdur": #butona başlat yaz driverı kapat
                
            if self.dil == "Türkçe":
                self.ui.pushButton.setText("Başlat")
            elif self.dil == "eng":
                self.ui.pushButton.setText("Start")
            self.bool = False
            self.driver.close()
            
        elif self.ui.pushButton.text() == "Stop": #butona start yaz driverı kapat
                
            if self.dil == "Türkçe":
                self.ui.pushButton.setText("Başlat")
            elif self.dil == "eng":
                self.ui.pushButton.setText("Start")
            self.bool = False
            self.driver.close()
            
    def cek(self): #pushButton_2
        
        if self.katilimcilar == []:
 
            self.thr3 = Thread(target=self.shake, args = (self.ui.listWidget, self ))
            self.thr3.start()
            
        elif len(self.katilimcilar) == len(self.kazananlar):

            pass
            
        else:
            
            sayi = self.ui.spinBox.value()
            self.kontrol += sayi

            while len(self.kazananlar) < self.kontrol:
                
                if len(self.katilimcilar) == len(self.kazananlar):
                    break
                        
                kazanan = random.choice(self.katilimcilar)
                    
                if kazanan in self.kazananlar:
                    pass
                else:
                        
                    self.kazananlar.append(kazanan)
                    self.ui.listWidget_2.addItem(kazanan)
                    if self.dil == "Türkçe":
                        self.ui.label_6.setText("Kazananlar ({})".format(len(self.kazananlar)))
                    elif self.dil == "eng":
                        self.ui.label_6.setText("Winners ({})".format(len(self.kazananlar)))
    
    def dongu(self):
                    
        url = ("https://www.twitch.tv/popout/{}/chat?popout=".format(self.kanal))
    
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(chrome_options = options) 
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(0, 0)
        self.driver.get(url)
        
        self.mod = self.ui.horizontalSlider.sliderPosition()
        
        self.bool = True
        while self.bool:
                
            time.sleep(1)
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
        
            mesajlar = soup.find_all("div", {"class": "chat-line__message"})
        
            for mesaj in mesajlar:
                
                kullanici = mesaj.find("span", {"class": "chat-author__display-name"})
                
                icerik = mesaj.find("span", {"class": "text-fragment"})
                
                badges = mesaj.find_all("img", {"class": "chat-badge"})
              
                if icerik is not None:
                
                    if self.keyword in (icerik.text):
                                                    
                        if self.mod == 1: #herkese açık
                            
                            if mesaj.text in self.k_mesajlari:
                                
                                pass
                            
                            else:
                                
                                self.k_mesajlari.append(mesaj.text)
                            
                            
                            if kullanici.text in self.katilimcilar:
                                
                                pass
                            
                            else:
                                
                                self.katilimcilar.append(kullanici.text)
                                self.ui.listWidget.addItem(kullanici.text)
                                
                        elif self.mod == 2: #sadece sub
                            
                            sub = False
                            
                            for badge in badges:
                            
                                if "Subscriber" in str(badge):
                                    sub = True
                            
                            if sub:
                            
                                if mesaj.text in self.k_mesajlari:
                                        
                                    pass
                                    
                                else:
                                        
                                    self.k_mesajlari.append(mesaj.text)
                                    
                                    
                                    if kullanici.text in self.katilimcilar:
                                            
                                        pass
                                        
                                    else:
                                            
                                        self.katilimcilar.append(kullanici.text)
                                        self.ui.listWidget.addItem(kullanici.text)
                            
                        elif self.mod == 3: #3 ay üstü
                            
                            sub = False
                            
                            for badge in badges:
                            
                                if "Subscriber" in str(badge):

                                    yeterli = True
                                                                            
                                    alt = str(badge.get('alt'))
                                    
                                    m = alt.split(" (")
                                    
                                    for i in range (1, 3):
                                        
                                        if m[0] == ("{}-Month Subscriber".format(i)):

                                            yeterli = False
                                    
                                    if yeterli:
                                        
                                        if mesaj.text in self.k_mesajlari:
                                                
                                            pass
                                            
                                        else:
                                                
                                            self.k_mesajlari.append(mesaj.text)
                                            
                                            
                                            if kullanici.text in self.katilimcilar:
                                                    
                                                pass
                                                
                                            else:
                                                    
                                                self.katilimcilar.append(kullanici.text)
                                                self.ui.listWidget.addItem(kullanici.text)
                            
                        elif self.mod == 4: #6 ay üstü
                            
                            sub = False
                            
                            for badge in badges:
                            
                                if "Subscriber" in str(badge):

                                    yeterli = True
                                                                            
                                    alt = str(badge.get('alt'))
                                    
                                    m = alt.split(" (")
                                    
                                    for i in range (1, 6):
                                        
                                        if m[0] == ("{}-Month Subscriber".format(i)):

                                            yeterli = False
                                    
                                    if yeterli:
                                        
                                        if mesaj.text in self.k_mesajlari:
                                                
                                            pass
                                            
                                        else:
                                                
                                            self.k_mesajlari.append(mesaj.text)
                                            
                                            
                                            if kullanici.text in self.katilimcilar:
                                                    
                                                pass
                                                
                                            else:
                                                    
                                                self.katilimcilar.append(kullanici.text)
                                                self.ui.listWidget.addItem(kullanici.text)

                        elif self.mod == 5: #9 ay üstü
                           
                            sub = False
                            
                            for badge in badges:
                            
                                if "Subscriber" in str(badge):

                                    yeterli = True
                                                                            
                                    alt = str(badge.get('alt'))
                                    
                                    m = alt.split(" (")
                                    
                                    for i in range (1, 9):
                                        
                                        if m[0] == ("{}-Month Subscriber".format(i)):

                                            yeterli = False
                                    
                                    if yeterli:
                                        
                                        if mesaj.text in self.k_mesajlari:
                                                
                                            pass
                                            
                                        else:
                                                
                                            self.k_mesajlari.append(mesaj.text)
                                            
                                            
                                            if kullanici.text in self.katilimcilar:
                                                    
                                                pass
                                                
                                            else:
                                                    
                                                self.katilimcilar.append(kullanici.text)
                                                self.ui.listWidget.addItem(kullanici.text)
                            
                        elif self.mod == 6: #12 ay üstü
                           
                            sub = False
                            
                            for badge in badges:
                            
                                if "Subscriber" in str(badge):

                                    yeterli = True
                                                                            
                                    alt = str(badge.get('alt'))
                                    
                                    m = alt.split(" (")
                                    
                                    for i in range (1, 12):
                                        
                                        if m[0] == ("{}-Month Subscriber".format(i)):

                                            yeterli = False
                                    
                                    if yeterli:
                                        
                                        if mesaj.text in self.k_mesajlari:
                                                
                                            pass
                                            
                                        else:
                                                
                                            self.k_mesajlari.append(mesaj.text)
                                            
                                            
                                            if kullanici.text in self.katilimcilar:
                                                    
                                                pass
                                                
                                            else:
                                                    
                                                self.katilimcilar.append(kullanici.text)
                                                self.ui.listWidget.addItem(kullanici.text)
                            
                        elif self.mod == 7: #24 ay üstü
                            
                            sub = False
                            
                            for badge in badges:
                            
                                if "Subscriber" in str(badge):

                                    yeterli = True
                                                                            
                                    alt = str(badge.get('alt'))
                                    
                                    m = alt.split(" (")
                                    
                                    for i in range (1, 24):
                                        
                                        if m[0] == ("{}-Month Subscriber".format(i)):

                                            yeterli = False
                                    
                                    if yeterli:
                                        
                                        if mesaj.text in self.k_mesajlari:
                                                
                                            pass
                                            
                                        else:
                                                
                                            self.k_mesajlari.append(mesaj.text)
                                            
                                            
                                            if kullanici.text in self.katilimcilar:
                                                    
                                                pass
                                                
                                            else:
                                                    
                                                self.katilimcilar.append(kullanici.text)
                                                self.ui.listWidget.addItem(kullanici.text)
                            
                        elif self.mod == 8: #48 ay üstü
                            
                            sub = False
                            
                            for badge in badges:
                            
                                if "Subscriber" in str(badge):

                                    yeterli = True
                                                                            
                                    alt = str(badge.get('alt'))
                                    
                                    m = alt.split(" (")
                                    
                                    for i in range (1, 48):
                                        
                                        if m[0] == ("{}-Month Subscriber".format(i)):

                                            yeterli = False
                                    
                                    if yeterli:
                                        
                                        if mesaj.text in self.k_mesajlari:
                                                
                                            pass
                                            
                                        else:
                                                
                                            self.k_mesajlari.append(mesaj.text)
                                            
                                            
                                            if kullanici.text in self.katilimcilar:
                                                    
                                                pass
                                                
                                            else:
                                                    
                                                self.katilimcilar.append(kullanici.text)
                                                self.ui.listWidget.addItem(kullanici.text)
                                                
            if self.dil == "Türkçe":
                self.ui.label_5.setText("Katılanlar ({})".format(len(self.katilimcilar)))      
            elif self.dil == "eng":      
                self.ui.label_5.setText("Attenders ({})".format(len(self.katilimcilar)))             
    
    def shake(self, item, x):
        
        x = item.x()
        y = item.y()
        
        stil = str(item.styleSheet)
        item.setStyleSheet("QTextEdit { background-color: rgba(133, 17, 156, 26); }")
        
        for i in range (7):
        
            time.sleep(0.07)
            item.setGeometry(QtCore.QRect(x - 3, y, item.width(), item.height()))
            time.sleep(0.07)
            item.setGeometry(QtCore.QRect(x + 3, y, item.width(), item.height()))
                 
        item.setStyleSheet(stil)
        item.setGeometry(QtCore.QRect(x, y, item.width(), item.height()))
        
    
    def slider(self):
        
        if self.dil == "Türkçe":
        
            if self.ui.horizontalSlider.sliderPosition() == 1:
            
                self.ui.label_2.setText("herkese açık")
                
            elif self.ui.horizontalSlider.sliderPosition() == 2:
                
                self.ui.label_2.setText("sadece aboneler")
                
            elif self.ui.horizontalSlider.sliderPosition() == 3:
                
                self.ui.label_2.setText("3 ay üstü")
                
            elif self.ui.horizontalSlider.sliderPosition() == 4:
                
                self.ui.label_2.setText("6 ay üstü")
                
            elif self.ui.horizontalSlider.sliderPosition() == 5:
                
                self.ui.label_2.setText("9 ay üstü")
                
            elif self.ui.horizontalSlider.sliderPosition() == 6:
                
                self.ui.label_2.setText("12 ay üstü")
                
            elif self.ui.horizontalSlider.sliderPosition() == 7:
                
                self.ui.label_2.setText("24 ay üstü")
                
            elif self.ui.horizontalSlider.sliderPosition() == 8:
            
                self.ui.label_2.setText("48 ay üstü")
                
        elif self.dil == "eng":
            
            if self.ui.horizontalSlider.sliderPosition() == 1:
            
                self.ui.label_2.setText("Everyone")
                
            elif self.ui.horizontalSlider.sliderPosition() == 2:
                
                self.ui.label_2.setText("Just Subs")
                
            elif self.ui.horizontalSlider.sliderPosition() == 3:
                
                self.ui.label_2.setText("Over 3 Months")
                
            elif self.ui.horizontalSlider.sliderPosition() == 4:
                
                self.ui.label_2.setText("Over 6 Months")
                
            elif self.ui.horizontalSlider.sliderPosition() == 5:
                
                self.ui.label_2.setText("Over 9 Months")
                
            elif self.ui.horizontalSlider.sliderPosition() == 6:
                
                self.ui.label_2.setText("Over 12 Months")
                
            elif self.ui.horizontalSlider.sliderPosition() == 7:
                
                self.ui.label_2.setText("Over 24 Months")
                
            elif self.ui.horizontalSlider.sliderPosition() == 8:
            
                self.ui.label_2.setText("Over 48 Months")

            
    def res_katilan(self):
        
        self.ui.listWidget.clear()
        self.katilimcilar = []
        if self.dil == "Türkçe":
            self.ui.label_5.setText("Katılanlar ({})".format(len(self.katilimcilar)))
        elif self.dil == "eng":
            self.ui.label_5.setText("Attenders ({})".format(len(self.katilimcilar)))
        
    def res_kazanan(self):
        
        self.ui.listWidget_2.clear()
        self.kazananlar = []
        self.kontrol = 0
        if self.dil == "Türkçe":
            self.ui.label_6.setText("Kazananlar ({})".format(len(self.kazananlar)))
        elif self.dil == "eng":
            self.ui.label_6.setText("Winners ({})".format(len(self.kazananlar)))
        
    def bagis(self):
        
        webbrowser.open('https://www.bynogame.com/destekle/FerdiEraslan')
        
def application():
    
    application = QtWidgets.QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(application.exec_())
    
application()
