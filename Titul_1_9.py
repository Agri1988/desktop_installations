from PyQt4 import QtGui, QtCore

#подключение базы данных
import sqlite3
conn = sqlite3.connect('my.db')
c = conn.cursor()

       

      


        
class Titul (QtGui.QMainWindow):

    def __init__(self, parent=None):
        super (Titul, self).__init__(parent)
        self.showDialog()
        self.mainWindow()
        #print (dialog.login_index)
        #print (mainWindow)
        
        
    def showDialog(self):       #окно приветствия и входа
        c = conn.cursor()
        c.execute('SELECT * FROM users') #выборка из базы данных 
        self.row_users = c.fetchall()
        #print (self.row_users)
        self.users=[]
        self.iter = 0
        for i in self.row_users:
            for j in i:
                if j == self.row_users[self.iter][1]:
                    self.users.append(j)
                else:
                    continue
            self.iter +=1
        #print (self.users)
        try:
            text, ok  = QtGui.QInputDialog.getText(self, 'Łogowanie', 'Wprowadź swój Login')
            if text in self.users:
                self.login_index = self.users.index(text)
                print (self.login_index)
            else:
                QtGui.QMessageBox.critical(self, 'Alarm!!!', 'Enter your name:')
                text, ok  = QtGui.QInputDialog.getText(self, 'Łogowanie', 'Wprowadź swój Login')
                self.login_index = self.users.index(text)
        except AttributeError:
            print ('LOL')
            sys.exit() 
        except ValueError:
            print ('LOL')
            sys.exit() 
        
        try:
            text, ok  = QtGui.QInputDialog.getText(self, 'Łogowanie', 'Wprowadź swóje Hasło')
            if (str(text)) == (str(self.row_users[self.login_index][2])):
                self.password = (text)
                print ('welcom!', self.users[self.login_index], self.password)
            else:
                QtGui.QMessageBox.critical(self, 'Alarm!!!', 'Enter correct Password:')
                text, ok  = QtGui.QInputDialog.getText(self, 'Łogowanie', 'Wprowadź swóje Hasło')
        except AttributeError:
            print ('LOL')
            sys.exit() 
        except ValueError:
            print ('LOL')
            sys.exit()
        c.close()
        
    def mainWindow (self):
        # определяем содержимое области(виджета) прокрутки
        
        self.scrollLayout = QtGui.QGridLayout()
        # добавляем  ране созданный слой прокрутки
        # на виджет прокрутки
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)
        # определяем область механизм прокрутки (QScrollArea)
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True) #разрешаем проктурку
        self.scrollArea.setWidget(self.scrollWidget)
        # создаём главный вертикальный слой
        self.mainLayout = QtGui.QGridLayout()
        self.mainLayout.addWidget(self.scrollArea,
                                  1,1,12,11) # добавляем область прокрутки
                                            #addWidget(<Koмnoнeнт>, <Строка>, <Столбец>,
                                            #<Количество строк>,
                                            #<Количество столбцов>[, QtCore.Qt.Align________])
        # определяем "центральный виджет"
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)
 
        # устанавливаем "центральный виджет"
        self.setCentralWidget(self.centralWidget)

        self.setWindowTitle('Ewidencja czasu pracy ELORAN')
        self.resize (800, 450)
        self.show()

        self.years_list()   
        self.btn_accept()
        self.months()
        self.headerLabel()
        self.clickMonth()
        self.saveRaport_btn()
        self.creatTmp()
        self.update()
        
      
    
    def btn_accept (self): #добавление новой строки в таблицу
        self.dayForInsert = QtGui.QComboBox()
        self.dayForInsert.setMaximumSize(100, 20)
        self.mainLayout.addWidget(self.dayForInsert, 0,1)
        for i in range(1,32):
            if i < 10:
                self.dayForInsert.addItem('0'+str(i))
            else:
                self.dayForInsert.addItem(str(i))
        self.dayForInsert.setEnabled(False)
        self.dayForInsert.setMaxVisibleItems(5)
        
        self.btn = QtGui.QPushButton('Wybierz dzień i naciśnij aby dodać linię')
        self.btn.setEnabled (False)
        self.mainLayout.addWidget(self.btn, 0,2,1,10)
        self.connect(self.btn, QtCore.SIGNAL('clicked()'), lambda : self.addBlankLine())
        

    def get_list_text (self):#получение информации о выбранном году
        self.year = self.comboBox.currentText()#принимает значение вписаное комбобокс
        print (self.year)


    def years_list (self):
        c = conn.cursor()
        c.execute('SELECT year FROM year')
        self.row = c.fetchall()
        self.comboBox = QtGui.QComboBox()
        self.comboBox.setMaximumSize(100, 20)
        self.mainLayout.addWidget(self.comboBox, 0, 0 )
        
        for i in range(len(self.row)):
            self.comboBox.addItem(str(self.row[i][0]))
        #self.comboBox.activated["const QString&"].connect(self.get_list_text)
        self.connect(self.comboBox, QtCore.SIGNAL ('activated(const QString&)'), self.get_list_text)
        self.connect(self.comboBox, QtCore.SIGNAL ('activated(const QString&)'), self.clickMonth)
        #self.btn_2[self.getIndexMonthBtn()].emit(QtCore.SIGNAL('clicked(bool)'), True)
       
    def months (self):
        
        c = conn.cursor()
        c.execute('SELECT * FROM month')
        self.row_2 = c.fetchall()
        #print (self.row_2)
        self.btn_2 =[]
        for i in range(len(self.row_2)):
            self.btn_2.append(QtGui.QRadioButton(str(self.row_2[i][1])))
            self.mainLayout.addWidget(self.btn_2[i], i+1, 0 )
            self.connect(self.btn_2[i], QtCore.SIGNAL("clicked()"),lambda : self.get_list_text())
            self.connect(self.btn_2[i], QtCore.SIGNAL("clicked()"),lambda mon=i: self.get_month_information(mon))
            self.connect(self.btn_2[i], QtCore.SIGNAL('clicked()'), lambda :self.clearMonth())#удаление элементов 
            self.connect(self.btn_2[i], QtCore.SIGNAL('clicked()'), lambda : self.information())#построение строк из базы данных
            self.connect(self.btn_2[i], QtCore.SIGNAL('clicked()'), lambda:(self.btn.setEnabled (True), self.dayForInsert.setEnabled(True)))
            
            
                
                
        c.close()
    #удаление элементов 
    def clearMonth(self):
        
        try:
            for i in range(len(self.object)):
                for j in range(len(self.object[i])):
                    self.object[i][j].deleteLater()

        except AttributeError:
            pass
    
    def get_month_information (self, mon): #получение номера месяца
        self.month = self.row_2[mon][0]
        return self.month
        #print (self.month)

    

    def headerLabel(self): #создание заголовка полей
        self.headerLabelDate = QtGui.QLabel('Data')
        self.scrollLayout.addWidget(self.headerLabelDate, 1,1,QtCore.Qt.AlignTop)
        self.headerLabelCount = QtGui.QLabel('Iłość Zleceń')
        self.headerLabelCount.setMaximumSize(60, 20)
        self.scrollLayout.addWidget(self.headerLabelCount, 1,2,QtCore.Qt.AlignTop)
        self.headerLabelTime_1 = QtGui.QLabel('Czas rozpoczęcia i zakończenia prac instalacyjnych')
        self.scrollLayout.addWidget(self.headerLabelTime_1, 1,3,1,8,QtCore.Qt.AlignTop)
        self.headerLabelTime_1.setMaximumSize(350, 20)
        self.headerLabelTime_2 = QtGui.QLabel('Łącznie')
        self.scrollLayout.addWidget(self.headerLabelTime_2, 1,11,QtCore.Qt.AlignTop)


    
    def information (self): #создание текстовых полей и внесение в них данных из базы данных
        c = conn.cursor()
        c.execute('SELECT * FROM working_time WHERE users_id=%s ORDER BY date' %(str(self.login_index+1)))
        self.row_3 = c.fetchall()
        self.object = []
        #print (self.row_3)
        for i in range(len(self.row_3)):
            self.object.append([])
             #создание поля с датой   
            if (str(self.row_3[i][1][3:5:]) == str(self.month))and(str(self.row_3[i][1][6::]) == (str(self.year))):
                
                self.object[i].append(QtGui.QDateEdit(self))
                self.object[i][0].setDate(QtCore.QDate(int(self.row_3[i][1][6::]),
                                           int(self.row_3[i][1][3:5:]),
                                           int(self.row_3[i][1][0:2:])))
                self.scrollLayout.addWidget(self.object[i][0], i+2, 1,QtCore.Qt.AlignTop)
                self.object[i][0].setMaximumSize(80, 20)
                
                date = str(self.object[i][0].date())
                self.connect(self.object[i][0], QtCore.SIGNAL('dateChanged(const QDate&)'),
                             lambda date=date,strIndex = self.row_3[i][0]: self.insertDate(date, strIndex))
                
                #создание полей с временем
                for j in range(2,(len(self.row_3[i])-1)):
                    

                    if j == 2:
                        
                        self.object[i].append(QtGui.QLineEdit(self))
                        self.object[i][j-1].setMaximumSize(25, 20)
                        self.object[i][j-1].setInputMask("9;_")
                        if ((str(self.row_3[i][j])) != 'None') and ((str(self.row_3[i][j])) != ''):
                            self.object[i][j-1].setText(str(self.row_3[i][j]))
                        else:
                            self.object[i][j-1].setText('00:00')
                        self.scrollLayout.addWidget(self.object[i][j-1],i+2,j,QtCore.Qt.AlignTop)
                        timeIndex = self.object[i].index(self.object[i][j-1])
                        #print (self.timeIndex)
                        self.connect(self.object[i][j-1], QtCore.SIGNAL('editingFinished ()'), lambda progStrIndex = i,culumnIndex = j-1 ,
                                     strIndex = self.row_3[i][0], timeIndex = timeIndex: self.insertTime(progStrIndex,timeIndex,strIndex, culumnIndex))
                        self.connect(self.object[i][j-1], QtCore.SIGNAL('editingFinished ()'), lambda rowIndex = i : self.allTime(rowIndex))

                        
                    elif j == 11:
                        #создание пол я для подсчета итогового времени
                        self.object[i].append(QtGui.QLineEdit(self))
                        self.object[i][j-1].setText(str(self.row_3[i][11]))
                        self.object[i][j-1].setMaximumSize(45, 20)
                        self.scrollLayout.addWidget(self.object[i][j-1], i+2, 11,QtCore.Qt.AlignTop)
                        index_summ = self.object[i].index(self.object[i][j-1])
                        #print (index_summ)
                        self.connect(self.object[i][j-1], QtCore.SIGNAL('editingFinished ()'), lambda progStrIndex = i,summ_index = index_summ, strIndex = self.row_3[i][0],
                                     rowIndex = i : self.insertAllTime(progStrIndex,summ_index, strIndex, rowIndex))
                        
                    else:
                        self.object[i].append(QtGui.QLineEdit(self))
                        culumnIndex = len(self.object[i])-1
                        self.object[i][j-1].setMaximumSize(40, 20)
                        self.object[i][j-1].setInputMask("99:99;_")
                        if ((str(self.row_3[i][j])) != 'None') and ((str(self.row_3[i][j])) != ''):
                            self.object[i][j-1].setText(str(self.row_3[i][j]))
                        else:
                            self.object[i][j-1].setText('00:00')
                        self.scrollLayout.addWidget(self.object[i][j-1],i+2,j,QtCore.Qt.AlignTop)
                        timeIndex = self.object[i].index(self.object[i][j-1])
                        #print (self.timeIndex)
                        self.connect(self.object[i][j-1], QtCore.SIGNAL('editingFinished ()'), lambda progStrIndex = i,culumnIndex = j-1 ,
                                     strIndex = self.row_3[i][0], timeIndex = timeIndex: self.insertTime(progStrIndex,timeIndex,strIndex, culumnIndex))
                        self.connect(self.object[i][j-1], QtCore.SIGNAL('editingFinished ()'), lambda rowIndex = i : self.allTime(rowIndex))
                        #print (index_summ)
                        self.connect(self.object[i][j-1], QtCore.SIGNAL('editingFinished ()'), lambda progStrIndex = i,summ_index = 10, strIndex = self.row_3[i][0],
                                     rowIndex = i : self.insertAllTime(progStrIndex,summ_index, strIndex, rowIndex))
                
                

               
                
                
        c.close()
        #print (len(self.object))
    #получение индекса активной кнопки RadioButton
    def getIndexMonthBtn(self):
        for i in range(len(self.btn_2)):
            if (self.btn_2[i].isChecked()) == True:
                index_btn = self.btn_2.index(self.btn_2[i])
        return index_btn
    #добавление новой строки    
    def addBlankLine (self):
        gridRow = len(self.object)
        day = str(self.dayForInsert.currentText())
        date = str(day +'.'+ str(self.month)+'.'+str(self.year))
        index = str(self.login_index+1)
        print (self.getIndexMonthBtn())
           
        #print (index_btn)
        c = conn.cursor()
        c.execute('INSERT INTO working_time ("date", "users_id") VALUES ("%s", "%s" )' %(date, index ))
        conn.commit()
        self.btn_2[self.getIndexMonthBtn()].emit(QtCore.SIGNAL('clicked(bool)'), True)

    

        
      #Вычисление общего времени 
    def allTime (self, rowIndex):
        c = conn.cursor()
        #выборка из базы данных строки совподающие с id выбранного пользователя
        c.execute('SELECT * FROM working_time WHERE users_id=%s ORDER BY date' %(str(titul.login_index+1)))
        alltime = c.fetchall()
        alltime = alltime[rowIndex][3:11]
        alltime_f = []
        for i in range(len(alltime)):
            if (alltime[i] == '') or (alltime[i] == 'None') or (alltime[i] == '00:00') or (alltime[i] == None):
                alltime_f.append(0)
            else:
                alltime_f.append((int(alltime[i][0:2])*60)+(int(alltime[i][3:])))
        for i in range (1,len(alltime_f),2):
            x = ((alltime_f[i])-(alltime_f[i-1]))
            alltime_f.append(x)
        x = 0
        #print (alltime_f)
        for i in alltime_f[8:]:
            x = x + i
        #print (x)
        #print (x // 60)
        #print (x%60)
        self.alltime_f = str(x // 60) + ':' + str(x % 60)
        return self.alltime_f
        #alltime_f = []

        #print (self.alltime_f)
    
    # вставка даты в базу данных
    def insertDate(self, date, strIndex):
        c.execute('PRAGMA table_info (working_time) ')
        row_date = c.fetchall()
        row_date = row_date[1][1]
        date = str(date)
        date = date[19:-1]
        date = date.replace(' ', '')
        date = date.split(',')
        #print (date[2])
        if len(date[2]) == 1:
            date.insert(2, ('0'+ str(date[2])))
            date.pop(3)
        if len(date[1]) == 1:
            date.insert(1, ('0'+ str(date[1])))
            date.pop(2)
        date = (str(date[2]) +'.' + str(date[1]) + '.' + str(date[0]))
        #print ((date))
        c.execute('UPDATE working_time SET "%s"="%s" WHERE id=%s' %(str(row_date),str(date), strIndex ))
        conn.commit()
        #print (row_date)

    #вставка итогового времени по дню в базу данных    
    def insertAllTime(self, progStrIndex,summ_index, strIndex, rowIndex):
        c.execute('PRAGMA table_info (working_time) ')
        row_alltime = c.fetchall()
        row_alltime = row_alltime[11][1]
        # (self.allTime(rowIndex))
        #print ((str(row_alltime),(str(self.allTime(rowIndex))), strIndex ))
        c.execute('UPDATE working_time SET "%s"="%s" WHERE id=%s' %(str(row_alltime),(str(self.allTime(rowIndex))), strIndex ))
        conn.commit()
        #print (self.object[summ_index].text())
        self.object[progStrIndex][summ_index].setText(str(self.alltime_f))
            
    #вставка времени инсталяции
    def insertTime(self,progStrIndex, timeIndex,strIndex, culumnIndex):
        c = conn.cursor()
        #self.timeText = self.object[timeIndex].text()
        c.execute('PRAGMA table_info (working_time) ')
        row = c.fetchall()
        c.execute('UPDATE working_time SET "%s"="%s" WHERE id=%s' %((str(row[culumnIndex+1][1])),(str(self.object[progStrIndex][timeIndex].text())), strIndex ))
        conn.commit()
        c.close()

    def clickMonth(self):
        self.btn_2[0].emit(QtCore.SIGNAL('clicked(bool)'), True)   
        self.btn_2[0].toggle()

    def saveRaport_btn (self):
        self.raport_btn = QtGui.QPushButton('Utworz raport')
        self.mainLayout.addWidget(self.raport_btn, 13, 11)

    def creatTmp (self):
        f = open('my.db', 'br')
        tmp = open('tmp', 'bw')
        for i in f:
            tmp.write(i)
        tmp.close()

    def newData (self):
        conn_tmp = sqlite3.connect('tmp')
        c_tmp = conn_tmp.cursor()
        c_tmp.execute('SELECT * FROM working_time')
        table = c_tmp.fetchall()

        c.execute('SELECT * FROM working_time')
        table_2 = c.fetchall()
        result = []
        for i in table_2:
            if i not in table:
              result.append(i)
        conn_tmp.close()
        return (result)
        import os
        os.remove('tmp')


    def closeEvent(self, event):
        from datetime import datetime
        # получить текущее время
        now = datetime.strftime(datetime.now(), "%M_%H_%d_%m_%y")
        file = open(('%s.txt' % now), 'w')
        for i in self.newData():

            file.write(str(i)+'\n')
        file.close()
        import ftpconnect
        ftpconnect.fileToFtp('%s.txt' %now)
        self.newData()

        

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    titul = Titul()
    
    sys.exit(app.exec_())
