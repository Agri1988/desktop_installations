import sqlite3
from PyQt4 import QtGui, QtCore
conn = sqlite3.connect('my.db')
import Instalation


class EquipmentWindow(QtGui.QDialog):
    def __init__(self, parent=None, id=1):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle('Zużyty sprzęt')
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.resize(400, 100)
        self.id = id
        self.mainLayout = QtGui.QGridLayout()
        self.setLayout(self.mainLayout)

        self.show()
        self.insertLineInDb()
        self.header()

    #метод для вставки новой строк в базу данных с полученным id
    #если строка с данным id существует, продолжается выполнение кода
    def insertLineInDb(self):
        try:
            c = conn.cursor()
            c.execute('INSERT INTO equipment ("id") VALUES ("%i")' % self.id)
            conn.commit()
        except sqlite3.IntegrityError:
            pass
    #создание шапки документа
    def header(self):
        c = conn.cursor()
        c.execute('SELECT * FROM equipment WHERE id = "%s"' % self.id)
        self.equipment = c.fetchall()
        print (self.equipment)
        equipment_name = ['Modem', 'Decoder', 'ONT', 'Dysk<br>Twardy', 'Karta', 'PoE', 'MoCa', 'LifePlug']
        modem_type = ['', 'Funbox2.0', 'Funbox3.0']
        decoder_type = ['', 'Samsung ICU100', 'Sagem UHD-88']
        hdd_type = ['', '320Gb', '500Gb']
        karta_type = ['', 'VIA', 'SIM']
        self.equipment_object = []


        # создание заголовков шапки документа
        self.equipment_object.append([])
        for i in range(len(equipment_name)):
            self.equipment_object[0].append(QtGui.QLabel(self))
            self.equipment_object[0][i].setText('%s' % equipment_name[i])
            self.mainLayout.addWidget(self.equipment_object[0][i], 0, i, QtCore.Qt.AlignHCenter)


        self.equipment_object.append([])

        #поле для выбора типа модема
        self.equipment_object[1].append(QtGui.QComboBox(self))
        for i in range(len(modem_type)):
            j = len(self.equipment_object[1]) - 1

            self.equipment_object[1][j].addItem(modem_type[i])
            if (self.equipment[0][j+1] == None):
                pass
            else:
                if self.equipment[0][j+1] in modem_type[1:] :
                    index = modem_type.index(self.equipment[0][j+1])
                    self.equipment_object[1][j].setCurrentIndex(index)
            self.connect(self.equipment_object[1][j], QtCore.SIGNAL('activated(const QString&)'),
                         lambda tmp = i, index = j+1: self.changeCellData(index))

            self.mainLayout.addWidget(self.equipment_object[1][j], 1, j)

        # поле для выбора типа декодера
        self.equipment_object[1].append(QtGui.QComboBox(self))
        for i in range(len(decoder_type)):
            j = len(self.equipment_object[1]) - 1

            self.equipment_object[1][j].addItem(decoder_type[i])
            if self.equipment[0][j+1] == None:
                pass
            else:
                if self.equipment[0][j+1] in decoder_type[1:] :
                    index = decoder_type.index(self.equipment[0][j+1])
                    self.equipment_object[1][j].setCurrentIndex(index)
            self.connect(self.equipment_object[1][j], QtCore.SIGNAL('activated(const QString&)'),
                         lambda tmp=i, index=j + 1: self.changeCellData(index))
            self.mainLayout.addWidget(self.equipment_object[1][j], 1, j)

        # поле для отметки чекбокса о наличии ОНТ
        j = len(self.equipment_object[1])
        self.equipment_object[1].append(QtGui.QCheckBox(self))
        self.equipment_object[1][j].setText('')
        if self.equipment[0][j+1] == 2:
            self.equipment_object[1][j].setCheckState(2)
        else:
            pass
        self.connect(self.equipment_object[1][j], QtCore.SIGNAL('stateChanged(int)'),
                     lambda tmp=i, index=j + 1: self.changeCellData(index))
        self.equipment_object[1][j].checkState()
        self.mainLayout.addWidget(self.equipment_object[1][j], 1, j)

        # поле для выбора типа жесткого диска
        self.equipment_object[1].append(QtGui.QComboBox(self))
        for i in range(len(hdd_type)):
            j = len(self.equipment_object[1]) - 1
            self.equipment_object[1][j].addItem(hdd_type[i])
            if self.equipment[0][j+1] == None:
                pass
            else:
                if self.equipment[0][j+1] in hdd_type[1:] :
                    index = hdd_type.index(self.equipment[0][j+1])
                    self.equipment_object[1][j].setCurrentIndex(index)
            self.connect(self.equipment_object[1][j], QtCore.SIGNAL('activated(const QString&)'),
                         lambda tmp=i, index=j + 1: self.changeCellData(index))
            self.mainLayout.addWidget(self.equipment_object[1][j], 1, j)

        # поле для выбора типа карты
        self.equipment_object[1].append(QtGui.QComboBox(self))
        for i in range(len(karta_type)):
            j = len(self.equipment_object[1]) - 1
            self.equipment_object[1][j].addItem(karta_type[i])
            if self.equipment[0][j+1] == None:
                pass
            else:
                if self.equipment[0][j+1] in karta_type[1:] :
                    index = karta_type.index(self.equipment[0][j+1])
                    self.equipment_object[1][j].setCurrentIndex(index)
            self.connect(self.equipment_object[1][j], QtCore.SIGNAL('activated(const QString&)'),
                         lambda tmp=i, index=j + 1: self.changeCellData(index))
            self.mainLayout.addWidget(self.equipment_object[1][j], 1, j)

        # поле для отметки использования POE, MoCa И LifePlug
        for i in range(0, 3):
            j = len(self.equipment_object[1])
            self.equipment_object[1].append(QtGui.QCheckBox(self))
            if self.equipment[0][j + 1] == 2:
                self.equipment_object[1][j].setCheckState(2)
            else:
                pass
            self.connect(self.equipment_object[1][j], QtCore.SIGNAL('stateChanged(int)'),
                         lambda tmp=i, index=j + 1: self.changeCellData(index))
            self.equipment_object[1][j].checkState()
            self.mainLayout.addWidget(self.equipment_object[1][j], 1, j, QtCore.Qt.AlignHCenter)

        # поле для выбора количества установленных декодеров
        j = len(self.equipment_object[1])
        self.equipment_object[1].append(QtGui.QSpinBox(self))
        if self.equipment[0][j + 1] == None:
            pass
        else:
            if self.equipment[0][j + 1] > 0:
                self.equipment_object[1][j].setValue(int(self.equipment[0][j + 1]))
        self.connect(self.equipment_object[1][j], QtCore.SIGNAL('valueChanged(int)'),
                     lambda tmp=i, index=j + 1: self.changeCellData(index))
        # self.equipment_object[1][j].setText('')
        self.mainLayout.addWidget(self.equipment_object[1][j], 2, 1)

        # поле для дополнительных отметок
        j = len(self.equipment_object[1])
        self.equipment_object[1].append(QtGui.QLineEdit(self))
        if self.equipment[0][j + 1] == None:
            self.equipment_object[1][j].setText('Dodatkowę uwagi')
        else:
            self.equipment_object[1][j].setText(self.equipment[0][j + 1])


        self.connect(self.equipment_object[1][j], QtCore.SIGNAL('textChanged(QString)'),
                     lambda tmp=i, index=j + 1: self.changeCellData(index))
        self.mainLayout.addWidget(self.equipment_object[1][j], 2, 2, 1, 6)

        #self.changeCellData()

    def changeCellData (self,index=0):
        c = conn.cursor()
        c.execute('PRAGMA table_info (equipment) ')
        det = c.fetchall()
        print (det)
        print (det[index][1])
        c = conn.cursor()
        if index in [3,6,7,8]:
            c.execute('UPDATE equipment SET "%s" = "%s" WHERE id="%s"'
                      % (str(det[index][1]), str(self.equipment_object[1][index-1].checkState()), self.id))

            conn.commit()
        elif index in [1,2,4,5]:
            c.execute('UPDATE equipment SET "%s" = "%s" WHERE id="%s"'
                      % (str(det[index][1]), str(self.equipment_object[1][index-1].currentText()), self.id))
            conn.commit()
        elif index == 9:
            c.execute('UPDATE equipment SET "%s" = "%s" WHERE id="%s"'
                      % (str(det[index][1]), str(self.equipment_object[1][index - 1].value()), self.id))
            conn.commit()
        elif index == 10:
            c.execute('UPDATE equipment SET "%s" = "%s" WHERE id="%s"'
                      % (str(det[index][1]), str(self.equipment_object[1][index-1].text()), self.id))
            conn.commit()

if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    main = EquipmentWindow()

    sys.exit(app.exec_())