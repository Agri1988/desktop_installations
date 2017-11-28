import sqlite3
from PyQt4 import QtGui, QtCore
conn = sqlite3.connect('my.db')
import Equipment


class InstalationWindow(QtGui.QDialog):
    def __init__(self, parent=None, id=1):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle('Szchegóły instalacji')
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.resize(200, 200)
        self.id = id
        self.mainLayout = QtGui.QGridLayout()
        self.setLayout(self.mainLayout)

        self.show()
        self.insertLineInDb()
        self.header()
        self.informationFromDb()

    # метод для вставки новой строк в базу данных с полученным id
    # если строка с данным id существует, продолжается выполнение кода
    def insertLineInDb(self):
        try:
            c = conn.cursor()
            c.execute('INSERT INTO details_of_installation ("id") VALUES ("%s")' %self.id)
            conn.commit()
        except sqlite3.IntegrityError:
            pass

    # создание шапки документа
    def header(self):
        c = conn.cursor()
        c.execute('SELECT * FROM details_of_installation WHERE id = "%s"' % self.id)
        self.inst_line = c.fetchall()
        #print(self.inst_line[0])

        self.lbl_success = QtGui.QLabel('<b>Wyniki instalacji</b>')
        self.lbl_success.setMaximumSize(100, 30)
        self.lbl_success.setMinimumSize(100, 30)
        self.mainLayout.addWidget(self.lbl_success, 1, 1, 1, 2)

        self.bt_succ = QtGui.QRadioButton('Skuteczna')
        if (self.inst_line[0][1] == 'True'):
            self.bt_succ.setChecked(True)
        self.bt_succ.setMaximumSize(70, 30)
        self.mainLayout.addWidget(self.bt_succ, 1, 0)
        self.connect(self.bt_succ, QtCore.SIGNAL('clicked ()'), self.bt_succ_click)

        self.bt_unsucc = QtGui.QRadioButton('Nie skuteczna')
        if (self.inst_line[0][1] == 'False'):
            self.bt_unsucc.setChecked(True)
        self.bt_unsucc.setMaximumSize(70, 30)
        self.mainLayout.addWidget(self.bt_unsucc, 1, 3., QtCore.Qt.AlignLeft)
        self.connect(self.bt_unsucc, QtCore.SIGNAL('clicked ()'), self.bt_unsucc_click)

        self.order_number = QtGui.QLineEdit()
        if (self.inst_line[0][2] == None) or (self.inst_line[0][2] == ''):
            self.order_number.setText('Wprowadź numer zlecenia')
        else:
            self.order_number.setText(str(self.inst_line[0][2] ))
        self.order_number.setMaximumSize(170, 30)
        self.order_number.setMinimumSize(170, 30)
        self.mainLayout.addWidget(self.order_number, 0, 0, 1, 3, QtCore.Qt.AlignLeft)
        self.connect(self.order_number, QtCore.SIGNAL('textChanged(QString)'), lambda text=self.order_number.text():
                                                                            self.changeOrderNumber(text))

        self.call_cor = QtGui.QLabel('Tęcza <br> dyspozytora')
        self.call_cor.setAlignment(QtCore.Qt.AlignHCenter)
        self.call_cor.setMaximumSize(60, 60)
        self.call_cor.setMinimumSize(60, 60)
        self.mainLayout.addWidget(self.call_cor, 3, 0)

        self.call_tech = QtGui.QLabel('Tęcza <br> technika')
        self.call_tech.setAlignment(QtCore.Qt.AlignHCenter)
        self.call_tech.setMaximumSize(60, 60)
        self.call_tech.setMinimumSize(60, 60)
        self.mainLayout.addWidget(self.call_tech, 3, 1)

        self.signal = QtGui.QLabel('Pomiary<br>OPP<br>GO')
        self.signal.setAlignment(QtCore.Qt.AlignHCenter)
        self.signal.setMaximumSize(60, 60)
        self.signal.setMinimumSize(60, 60)
        self.mainLayout.addWidget(self.signal, 3, 2)

        self.install_type = QtGui.QLabel('Typ instalacji')
        self.install_type.setAlignment(QtCore.Qt.AlignHCenter)
        self.install_type.setAlignment(QtCore.Qt.AlignTop)
        self.install_type.setMaximumSize(60, 30)
        self.install_type.setMinimumSize(60, 30)
        self.mainLayout.addWidget(self.install_type, 3, 3)

    def bt_succ_click (self):
        if self.bt_succ.isChecked () == True:
            c = conn.cursor()
            c.execute('UPDATE details_of_installation SET success = "True" WHERE id="%s"' %self.id)
            conn.commit()
            self.informationFromDb()

    def bt_unsucc_click(self):
        if self.bt_unsucc.isChecked () == True:
            c = conn.cursor()
            c.execute('UPDATE details_of_installation SET success = "False" WHERE id="%s"' %self.id)
            conn.commit()
            self.informationFromDb()
        for i in range(4, len(self.inst_object)):
            self.inst_object[i].setEnabled(False)

    def changeOrderNumber (self,text):
        c = conn.cursor()
        c.execute('UPDATE details_of_installation SET order_number = "%s" WHERE id="%s"' % (str(text), self.id))
        conn.commit()
        self.informationFromDb()

    def changeCellData (self,index):
        c = conn.cursor()
        c.execute('PRAGMA table_info (details_of_installation) ')
        det = c.fetchall()
        print (det)
        print (det[index][1])
        c = conn.cursor()
        if (index == 6) or (index==4):
            c.execute('UPDATE details_of_installation SET "%s" = "%s" WHERE id="%s"'
                      % (str(det[index][1]), str(self.inst_object[index - 3].toPlainText()), self.id))

            conn.commit()
        elif index == 9:
            c.execute('UPDATE details_of_installation SET "%s" = "%s" WHERE id="%s"'
                      % (str(det[index][1]), str(self.inst_object[index - 3].currentText()), self.id))
            conn.commit()
        else:
            c.execute('UPDATE details_of_installation SET "%s" = "%s" WHERE id="%s"'
                      % (str(det[index][1]), str(self.inst_object[index - 3].text()), self.id))
            conn.commit()
        #self.informationFromDb()

    def informationFromDb(self):
        c = conn.cursor()
        c.execute('SELECT * FROM details_of_installation WHERE id = "%s"' %self.id )
        self.inst_line = c.fetchall()
        #print(self.inst_line)
        self.inst_object = []
        for i in range(3,len(self.inst_line[0])+1):
            if i == 3:
                i=0
                self.inst_object.append(QtGui.QLineEdit(self))
                self.inst_object[i].setMaximumSize(40, 25)
                self.inst_object[i].setAlignment(QtCore.Qt.AlignTop)
                self.connect(self.inst_object[i], QtCore.SIGNAL('editingFinished ()'),
                             lambda i=i + 3: self.changeCellData(i))
                if self.inst_line[0][3] == None:
                    self.inst_object[i].setText('')
                    self.inst_object[i].setInputMask("99:99;_")
                else:
                    self.inst_object[i].setText(self.inst_line[0][3])
                self.mainLayout.addWidget(self.inst_object[i], 4,0)
                continue
            if i == 4:
                i = 1
                self.inst_object.append(QtGui.QPlainTextEdit(self))
                self.inst_object[i].setMaximumSize(60, 50)
                #self.inst_object[i].setAlignment(QtCore.Qt.AlignTop)
                self.connect(self.inst_object[i], QtCore.SIGNAL('textChanged()'),
                             lambda i=i + 3: self.changeCellData(i))
                if self.inst_line[0][4] == None:
                    self.inst_object[i].setPlainText('')

                else:
                    self.inst_object[i].setPlainText(self.inst_line[0][4])
                self.mainLayout.addWidget(self.inst_object[i], 5, 0)
                continue
            if i == 5:
                i=2
                self.inst_object.append(QtGui.QLineEdit(self))
                self.inst_object[i].setMaximumSize(40, 25)
                self.inst_object[i].setAlignment(QtCore.Qt.AlignTop)
                self.connect(self.inst_object[i], QtCore.SIGNAL('editingFinished ()'),
                             lambda i=i + 3: self.changeCellData(i))
                if self.inst_line[0][5] == None:
                    self.inst_object[i].setText('')
                    self.inst_object[i].setInputMask("99:99;_")
                else:
                    self.inst_object[i].setText(self.inst_line[0][5])
                self.mainLayout.addWidget(self.inst_object[i], 4,1)
                continue
            if i == 6:
                i = 3
                self.inst_object.append(QtGui.QPlainTextEdit(self))
                self.inst_object[i].setMaximumSize(60, 50)
                #self.inst_object[i].setAlignment(QtCore.Qt.AlignTop)
                self.connect(self.inst_object[i], QtCore.SIGNAL('textChanged()'),
                             lambda i=i + 3: self.changeCellData(i))
                if self.inst_line[0][6] == None:
                    self.inst_object[i].setPlainText('')

                else:
                    self.inst_object[i].setPlainText(self.inst_line[0][6])
                self.mainLayout.addWidget(self.inst_object[i], 5, 1)
                continue
            if i == 7:
                i=4
                self.inst_object.append(QtGui.QLineEdit(self))
                self.inst_object[i].setMaximumSize(40, 25)
                self.inst_object[i].setAlignment(QtCore.Qt.AlignTop)
                self.connect(self.inst_object[i], QtCore.SIGNAL('editingFinished ()'),
                                                                lambda i=i + 3: self.changeCellData(i))
                if self.inst_line[0][7] == None:
                    self.inst_object[i].setText('')
                    self.inst_object[i].setInputMask("99:99;_")
                else:
                    self.inst_object[i].setText(self.inst_line[0][7])
                self.mainLayout.addWidget(self.inst_object[i], 4,2)
                continue
            if i == 8:
                i = 5
                self.inst_object.append(QtGui.QLineEdit(self))
                self.inst_object[i].setMaximumSize(40, 25)
                self.inst_object[i].setAlignment(QtCore.Qt.AlignTop)
                self.connect(self.inst_object[i],QtCore.SIGNAL('editingFinished ()'), lambda i=i+3:self.changeCellData(i))
                if self.inst_line[0][8] == None:
                    self.inst_object[i].setText('')
                    self.inst_object[i].setInputMask("99:99;_")
                else:
                    self.inst_object[i].setText(self.inst_line[0][8])
                self.mainLayout.addWidget(self.inst_object[i], 5, 2)
                continue
            if i == 9:
                i = 6
                self.inst_object.append(QtGui.QComboBox(self))
                lst_type = ['1P', '2P', '3P', '3P MR', '3P MR3e','']
                for t in lst_type:
                    self.inst_object[i].addItem(str(t))
                self.mainLayout.addWidget(self.inst_object[i], 4, 3)
                self.connect(self.inst_object[i], QtCore.SIGNAL('activated(int)'), lambda tmp=i, i=i+3: self.changeCellData(i))
                #self.connect(self.inst_object[i], QtCore.SIGNAL('activated(int)'), lambda:self.on_click())
                if self.inst_line[0][9] == None:
                    self.inst_object[i].setMaximumSize(65, 30)
                    self.inst_object[i].setMinimumSize(65, 30)
                    self.inst_object[i].setCurrentIndex(5)
                else:
                    for type in lst_type:
                        if type == self.inst_line[0][i+3]:
                            self.inst_object[i].setCurrentIndex(lst_type.index(type))
                continue
            if i ==10:
                i = 7
                self.inst_object.append(QtGui.QPushButton(self))
                self.inst_object[i].setText('Dodaj sprzęt')
                self.mainLayout.addWidget(self.inst_object[i],5,3)
                self.connect(self.inst_object[i], QtCore.SIGNAL('clicked ()'),
                             lambda id=str(self.id):self.wakeUpWindow(id))
                break

        if (self.inst_line[0][1] == 'False'):
            for i in range(4,len(self.inst_object)):
                self.inst_object[i].setEnabled(False)

    def wakeUpWindow(self, id):
        self.equipmentWindow = Equipment.EquipmentWindow(parent=self,id=int(id))
    def on_click(self):
        btn = QtGui.QPushButton(self)
        self.connect(btn, QtCore.SIGNAL('clicked ()'), lambda :self.changeCellData(int(9)))
        btn.emit(QtCore.SIGNAL('clicked (bool)'), True)

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    main = InstalationWindow()

    sys.exit(app.exec_())