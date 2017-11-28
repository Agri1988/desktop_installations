import sqlite3
from PyQt4 import QtGui, QtCore
import main1_4 as main_window

conn = sqlite3.connect('my.db')


class WorkmanWindow(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.mainWindow = parent
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowTitle('Pracowniki')
        self.resize(350, 350)
        self.mainLayout = QtGui.QGridLayout()
        self.mainLayout.verticalSpacing()
        self.mainLayout.setVerticalSpacing(10)
        self.mainLayout.setRowStretch(20,100)
        self.setLayout(self.mainLayout)

        self.show()
        #self.insertLineInDb()
        self.header()

        self.icon_plus = QtGui.QIcon('plus.ico')
        self.addbtn = QtGui.QPushButton()
        self.addbtn.setIcon(self.icon_plus)
        self.mainLayout.addWidget(self.addbtn, 15, 0,3,0)
        self.connect(self.addbtn, QtCore.SIGNAL('clicked ()'),self.insertLineInDb)



    def insertLineInDb(self):
        print('egfds')
        c = conn.cursor()
        c.execute('INSERT INTO workman DEFAULT VALUES')
        conn.commit()
        self.clearWindow()
        self.header()

    def header (self):
        c = conn.cursor()
        c.execute('PRAGMA  TABLE_INFO (workman)')
        tbl_workman_lst = c.fetchall()
        c.close()
        print (tbl_workman_lst)
        self.workman_header = []
        print (self.workman_header)
        for i in range(len(tbl_workman_lst)):
            if i == 0:
                self.workman_header.append(QtGui.QLabel(self))
                self.workman_header[i].setText('№')
                self.workman_header[i].setAlignment(QtCore.Qt.AlignHCenter)
                self.workman_header[i].setMaximumSize(30,30)
                self.mainLayout.addWidget(self.workman_header[i], 0, i)
            if i == 1:
                self.workman_header.append(QtGui.QLabel(self))
                self.workman_header[i].setText('Imię')
                self.workman_header[i].setAlignment(QtCore.Qt.AlignHCenter)
                self.workman_header[i].setMaximumSize(100, 30)
                self.mainLayout.addWidget(self.workman_header[i], 0, i)
            if i ==2:
                self.workman_header.append(QtGui.QLabel(self))
                self.workman_header[i].setText('Nazwisko')
                self.workman_header[i].setAlignment(QtCore.Qt.AlignHCenter)
                self.workman_header[i].setMaximumSize(100, 30)
                self.mainLayout.addWidget(self.workman_header[i], 0, i)
            if i == 3:
                self.workman_header.append(QtGui.QLabel(self))
                self.workman_header[i].setText('id')
                self.workman_header[i].setAlignment(QtCore.Qt.AlignHCenter)
                self.workman_header[i].setMaximumSize(100, 30)
                self.mainLayout.addWidget(self.workman_header[i], 0, i)
        c = conn.cursor()
        c.execute('SELECT * FROM workman')
        tbl_workman_lst_information = c.fetchall()
        c.close()
        #print (tbl_workman_lst_information)
        self.workman_object = []
        self.icon_delete = QtGui.QIcon('delete.ico')
        for i in range(len(tbl_workman_lst_information)):
            self.workman_object.append([])
            #print (self.workman_object)
            #print (tbl_workman_lst_information[i])
            for j in range(len(tbl_workman_lst_information[i])):
                print (tbl_workman_lst_information[i][j])
                if j == 0:
                    self.workman_object[i].append(QtGui.QLabel(self))
                    self.workman_object[i][j].setText(str(tbl_workman_lst_information[i][j]))
                    self.workman_object[i][j].setMaximumSize(30, 30)
                    self.mainLayout.addWidget(self.workman_object[i][j], i+1, j)
                if j == 1:
                    self.workman_object[i].append(QtGui.QLineEdit(self))
                    self.workman_object[i][j].setText(tbl_workman_lst_information[i][j])
                    self.workman_object[i][j].setMaximumSize(80, 30)
                    self.mainLayout.addWidget(self.workman_object[i][j], i+1, j)
                    self.connect(self.workman_object[i][j], QtCore.SIGNAL('textChanged(QString)'),
                                 lambda txt=i, id=tbl_workman_lst_information[i][0], i=i,j=j: self.changeCellData(id=id, i=i,j=j))
                if j == 2:
                    self.workman_object[i].append(QtGui.QLineEdit(self))
                    self.workman_object[i][j].setText(tbl_workman_lst_information[i][j])
                    self.workman_object[i][j].setMaximumSize(80, 30)
                    self.mainLayout.addWidget(self.workman_object[i][j], i+1, j)
                    self.connect(self.workman_object[i][j], QtCore.SIGNAL('textChanged(QString)'),
                                 lambda txt=i, id=tbl_workman_lst_information[i][0], i=i, j=j:
                                 self.changeCellData(id=id, i=i, j=j))
                if j == 3:
                    self.workman_object[i].append(QtGui.QLineEdit(self))
                    if (tbl_workman_lst_information[i][j] == None) or (tbl_workman_lst_information[i][j] == 'None'):
                        self.workman_object[i][j].setText('')
                        print ('lalala')
                    else:
                        self.workman_object[i][j].setText(str(tbl_workman_lst_information[i][j]))
                    self.workman_object[i][j].setMaximumSize(60, 30)
                    self.workman_object[i][j].setInputMask("999999;_")
                    self.mainLayout.addWidget(self.workman_object[i][j], i+1, j)
                    self.connect(self.workman_object[i][j], QtCore.SIGNAL('textChanged(QString)'),
                                 lambda txt=i, id=tbl_workman_lst_information[i][0], i=i, j=j:
                                 self.changeCellData(id=id, i=i, j=j))

                    self.workman_object[i].append(QtGui.QPushButton(self))
                    self.workman_object[i][j+1].setText('')
                    self.workman_object[i][j+1].setIcon(self.icon_delete)
                    self.workman_object[i][j+1].setMaximumSize(40, 30)
                    self.mainLayout.addWidget(self.workman_object[i][j+1], i + 1, j+1)
                    self.connect(self.workman_object[i][j+1], QtCore.SIGNAL('clicked ()'),
                                 lambda i = i: self.delWorkmanLine(id=tbl_workman_lst_information[i][0], index=i))


    def clearWindow (self):
        for i in range(len(self.workman_object)):
            for j in self.workman_object[i]:
                j.deleteLater()
        for i in self.workman_header:
            i.deleteLater()
    def delWorkmanLine (self, id,index):
        print(id, type(id))
        c = conn.cursor()
        c.execute('DELETE FROM workman WHERE id="%s"' % id)
        conn.commit()
        self.clearWindow()
        self.header()

    def changeCellData (self,id,i, j):
        c = conn.cursor()
        c.execute('PRAGMA table_info (workman) ')
        det = c.fetchall()
        print (det)
        print (det[j])
        c = conn.cursor()
        c.execute('UPDATE workman SET "%s" = "%s" WHERE id="%s"'
                  % (str(det[j][1]), str(self.workman_object[i][j].text()), id))

        conn.commit()








if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    main = WorkmanWindow()

    sys.exit(app.exec_())

