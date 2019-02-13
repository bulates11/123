#��� ��������� ����, ��������� ��������� ��� ���������� ��������� ��� ������ � 
# ���� � ������ ����.������� ���� ������ ������ �� ������� �� ����� ���������� �����
# ��������� ����, �� ������, ��� ��� ������������. ����� �� ����� ����� � ����������
# ������� getResult �� ������ ���������� ��������� ��� ��� ����������

from PyQt5.QtWidgets import (QWidget, QLabel, QApplication, QComboBox, QPushButton)
from PyQt5.QtGui import QPixmap, QFont
import sys
import requests
import xml.etree.cElementTree as ET
from pygame import mixer # Load the required library




class CBR_API(QWidget):
    def music_start(self):
        play=True
        if play:
            mixer.init()
            mixer.music.load(r'Photo\Gimn.mp3')
            mixer.music.play()    
    def music_end(self):
        mixer.music.pause()     
    def secret(self):
        play=True
        if play:
            mixer.init()
            mixer.music.load(r'Photo\secret.mp3')
            mixer.music.play()        
    
    
    
    
    def __init__(self):
        super().__init__()
        self.initUI()
        
        
        
    def initUI(self):
        logo = QLabel(self)
        logo.setPixmap(QPixmap("Photo/�������� ����� �������.jpg"))
        logo.move(0, 0)
        self.daysline()
        self.monthline()
        self.yearline()
        secret_button = QPushButton('', self)
        secret_button.resize(5, 5)
        secret_button.move(170, 80)
        secret_button.clicked.connect(self.secret)
        start_button = QPushButton('Start', self)
        start_button.resize(50, 20)
        start_button.move(300, 240)    
        start_button.clicked.connect(self.music_start)
        end_button = QPushButton('End', self)
        end_button.resize(50, 20)
        end_button.move(300, 260)     
        end_button.clicked.connect(self.music_end)
        ok_button = QPushButton('��', self)
        ok_button.resize(50, 20)
        ok_button.move(300, 220)
        ok_button.clicked.connect(self.Request)
        self.resultat()
        self.setFixedSize(400, 400)
        self.setWindowTitle('����� ������� � ����')
        self.show()
  
  
  
  
                
                
                
    def daysline(self):
        self.days_combo = QComboBox(self)
        day_label = QLabel("����", self)
        day_label.move(20, 240)
        for day in range(1, 31):
            self.days_combo.addItem('%d' % day)
        self.days_combo.move(20, 220)
    def monthline(self):
        self.month_combo = QComboBox(self)
        month_label = QLabel("�����", self)
        month_label.move(80, 240)
        for month_num in range(1, 13):
            self.month_combo.addItem('%d' % month_num)
        self.month_combo.move(80, 220)
    def yearline(self):
        self.year_combo = QComboBox(self)
        month_label = QLabel("���", self)
        month_label.move(140, 240)
        for year_num in range(1997, 2020):
            self.year_combo.addItem('%d' % year_num)
        self.year_combo.move(140, 220)
        
        
        
        
        
        
        
    
    
    def resultat(self):
        font = QFont()
        font.setFamily("segoe script")
        font.setPointSize(18)
        euro_label = QLabel(self)
        euro_label.setPixmap(QPixmap("Photo/���� �����.png"))
        euro_label.move(30, 320)
        self.euro_value = QLabel("0 ���.", self)
        self.euro_value.setFont(font)
        self.euro_value.move(100, 320)
        dollar_label = QLabel(self)
        dollar_label.setPixmap(QPixmap("Photo/������ �����.png"))
        dollar_label.move(30, 260)
        self.dollar_value = QLabel("0 ���.", self)
        self.dollar_value.setFont(font)
        self.dollar_value.move(100, 263)        

    
  
  
  

    def Request(self):
        day_val = self.days_combo.currentText()
        month_val = self.month_combo.currentText()
        year_val = self.year_combo.currentText()
        result = self.getResult(day_val, month_val, year_val)
        self.dollar_value.setText('%s ���.' % result['dollar'])
        self.dollar_value.adjustSize()
        self.euro_value.setText('%s ���.' % result['euro'])
        self.euro_value.adjustSize()
        
        
        
        
        
        
    def getResult(self, day, month, year):
        """
        ��������� ������ � API ����� ������.

        :param day: ��������� ����.
        :param month: ��������� ����� ������.
        :param year: ��������� ���
        :return: dict
        """

        result = {
            'usd': 0,
            'eur': 0,
        }

        if int(day) < 10:
            day = '0%s' % day

        if int(month) < 10:
            month = '0%s' % month

        try:
            # ��������� ������ � API.
            get_xml = requests.get(
                'http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s/%s/%s' % (day, month, year)
            )

            # ������� XML ��������� ElementTree
            structure = ET.fromstring(get_xml.content)
        except:
            return result

        try:
            # ����� ����� ������� (USD ID: R01235)
            dollar = structure.find("./*[@ID='R01235']/Value")
            result['dollar'] = dollar.text.replace(',', '.')
        except:
            result['dollar'] = 'x'

        try:
            # ����� ����� ���� (EUR ID: R01239)
            euro = structure.find("./*[@ID='R01239']/Value")
            result['euro'] = euro.text.replace(',', '.')
        except:
            result['euro'] = 'x'

        return result



















if __name__ == '__main__':
    app = QApplication(sys.argv)
    money = CBR_API()
    sys.exit(app.exec_())
    