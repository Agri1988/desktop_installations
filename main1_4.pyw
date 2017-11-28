from PyQt4 import QtGui, QtCore
from datetime import datetime, timedelta
import Instalation
import SortByDate
import Workman
from parsing_xps import inf_whith_documents
import forSortingMenu as ymd

# подключение базы данных
import sqlite3

conn = sqlite3.connect('my.db')
c = conn.cursor()

def import_installation ():
    dict = inf_whith_documents()
    #print(dict)
    for keys, value in dict.items():
        #print((dict[keys][3][:10]).replace('-', '.'), dict[keys][3][11:16], dict[keys][3][-5:], dict[keys][1], dict[keys][0][8:15])
        c = conn.cursor()
        c.execute('INSERT INTO installing ("date", "time_1", "time_2", "address", "workman1", "workman2") '
                  'VALUES ("%s", "%s", "%s", "%s", "%s", "%s")'
                  %((dict[keys][3][:10]).replace('-', '.'), dict[keys][3][11:16],
                    dict[keys][3][-5:], dict[keys][1], dict[keys][4],dict[keys][5] ) )
        conn.commit()
        c.execute('SELECT MAX ("id") FROM installing')
        id = c.fetchall()[0][0]
        success = ''
        if dict[keys][6] == '+':
            success = 'True'
        elif dict[keys][6] == '-':
            success = 'False'
        try:
            c = conn.cursor()
            c.execute('INSERT INTO details_of_installation ("id", "success", "order_number") VALUES ("%s", "%s", "%s")'
                      %(id, success, dict[keys][0][8:15]))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
import_installation()
class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)
        self.mainWindow()
        self.move(0,0)
        self.showMaximized()


    def mainWindow(self):
        # определяем содержимое области(виджета) прокрутки

        self.scrollLayout = QtGui.QGridLayout()
        # добавляем  ране созданный слой прокрутки
        # на виджет прокрутки
        self.scrollWidget = QtGui.QWidget()
        self.scrollWidget.setLayout(self.scrollLayout)
        # определяем область механизм прокрутки (QScrollArea)
        self.scrollArea = QtGui.QScrollArea()
        self.scrollArea.setWidgetResizable(True)  # разрешаем проктурку
        self.scrollArea.setWidget(self.scrollWidget)
        # создаём главный вертикальный слой
        self.mainLayout = QtGui.QGridLayout()
        self.scrollLayout.verticalSpacing()
        self.scrollLayout.setVerticalSpacing(10)
        self.scrollLayout.setRowStretch(20, 100)
        self.mainLayout.addWidget(self.scrollArea,1, 2,31,10)
                                            # добавляем область прокрутки
                                            # addWidget(<Koмnoнeнт>, <Строка>, <Столбец>,
                                            # <Количество строк>,
                                            # <Количество столбцов>[, QtCore.Qt.Align________])

                                            # определяем "центральный виджет"

        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(self.mainLayout)

        # устанавливаем "центральный виджет"
        self.setCentralWidget(self.centralWidget)

        self.setWindowTitle('Instalacje Eloran')
        self.resize(1350, 450)
        self.show()
        #self.addInstalationInDb()
        self.information(datetime.strftime(datetime.now(), "%Y.%m.%d"))

        self.icon_delete = QtGui.QIcon('delete.ico')
        self.iconForRefresz = QtGui.QIcon()
        self.iconForRefresz.addFile('refresh.ico', QtCore.QSize(32, 32),
                                    mode=QtGui.QIcon.Normal)
        self.iconAddInstallation = QtGui.QIcon()
        self.iconAddInstallation.addFile('plus.ico', QtCore.QSize(32, 32),
                                         mode=QtGui.QIcon.Normal)
        self.icon_month_btn_forward = QtGui.QIcon()
        self.icon_month_btn_forward.addFile('rigth_arrow.ico', QtCore.QSize(32, 32),
                                            mode=QtGui.QIcon.Normal)
        self.icon_month_btn_back = QtGui.QIcon()
        self.icon_month_btn_back.addFile('left_arrow.ico', QtCore.QSize(32, 32),
                                         mode=QtGui.QIcon.Normal)
        self.iconWorkman = QtGui.QIcon('drill.png')

        #создание кнопки для добавления инсталяции
        self.btn_addInstalation = QtGui.QPushButton(self)
        #self.btn_addInstalation.setText('Dodaj instalację')
        self.btn_addInstalation.setMaximumSize(30,30)
        self.btn_addInstalation.setIcon(self.iconAddInstallation)
        self.mainLayout.addWidget(self.btn_addInstalation, 0,3)
        self.connect(self.btn_addInstalation, QtCore.SIGNAL('clicked ()'), self.addInstalationInDb)

        #создание поля для ввода даты при добавлении новой инсталяции
        self.instalationDate = QtGui.QDateEdit(self)
        self.instalationDate.setDate(QtCore.QDate(datetime.today()))
        self.mainLayout.addWidget(self.instalationDate, 0,2)
        

        #создание кнопки открывающей модальное диалоговое окно
        #со списком сотрудников
        self.buttonWorkman = QtGui.QPushButton(self)
        self.buttonWorkman.setText('Lista pracowników')
        self.buttonWorkman.setMaximumSize(120, 30)
        self.buttonWorkman.setMinimumSize(120, 30)
        self.buttonWorkman.setIcon(self.iconWorkman)
        self.mainLayout.addWidget(self.buttonWorkman, 0, 11)
        # вызов метода открывающего окно
        self.connect(self.buttonWorkman, QtCore.SIGNAL('clicked ()'), self.wakeUpWorkmanWindow)

        self.options_menu = QtGui.QMenu(self)
        self.options_menu.addAction('Wyświetl wszystkie', lambda: self.success_all(status=2))
        self.options_menu.addAction('Wyświetl skuteczne', lambda: self.success_all(status=1))
        self.options_menu.addAction('Wyświetl nie skuteczne', lambda: self.success_all(status=0))

        self.btn_all_success = QtGui.QPushButton(self)
        self.btn_all_success.setText('Opcje wyświetlenia')
        self.btn_all_success.setMenu(self.options_menu)
        self.mainLayout.addWidget(self.btn_all_success, 0, 7)
        # self.connect(self.btn_all_success, QtCore.SIGNAL('clicked ()'),
        #              lambda: (self.btn_all_success.setDown(True), self.success_all(status=2)))
        #
        # self.btn_true_success = QtGui.QPushButton(self)
        # self.btn_true_success.setText('Wyświetl skuteczne')
        # self.mainLayout.addWidget(self.btn_true_success, 0, 8)
        # self.connect(self.btn_true_success, QtCore.SIGNAL('clicked ()'),
        #              lambda: (self.btn_true_success.setDown(True), self.success_all(status=1)))
        #
        # self.btn_false_success = QtGui.QPushButton(self)
        # self.btn_false_success.setText('Wyświetl nie skuteczne')
        # self.mainLayout.addWidget(self.btn_false_success, 0, 9)
        # self.connect(self.btn_false_success, QtCore.SIGNAL('clicked ()'),
        #              lambda: (self.btn_false_success.setDown(True), self.success_all(status=0)))

        self.btn_import_installation = QtGui.QPushButton(self)
        #self.btn_import_installation.setText('Odśwież')
        self.btn_import_installation.setMaximumSize(30,30)
        self.btn_import_installation.setMinimumSize(30,30)

        self.btn_import_installation.setIcon(self.iconForRefresz)
        self.mainLayout.addWidget(self.btn_import_installation, 0, 10)
        self.connect(self.btn_import_installation, QtCore.SIGNAL('clicked ()'), lambda: (import_installation(),self.success_all(status=2)))

        self.daysBtn()
        #self.sortByDate()
        self.monthAndYear()
        self.sortMenu()
        self.number_installation_finder()



    # создание группы радиокнопок с датами +-4 дня от текущей даты
    def daysBtn(self, month_year=(datetime.strftime(datetime.now(), "%Y.%m"))):
        self.month_year=month_year
        self.days_btn = []
        month_dict = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
        for key, value in month_dict.items():
            if key == int(month_year[5::]):
                
                for i in range(1,value+1):
                    if len(str(i)) == 1:
                        day = '0'+str(i)
                    else:
                        day = str(i)
                    date = str(month_year + '.' + day)
                    #weekday = datetime.weekday(datetime.now() - timedelta(delta)) #получение номера дня недели
                    #weekday_dict = {6:'Niedziela', 0:'Poniedziałek', 1:'Wtorek', 2:'środa', 3:'Czwartek', 4:'Piątek', 5:'Sobota'}
                    #for d in range (7):
                        #if d == weekday:
                            #weekday = weekday_dict[d]
                    self.days_btn.append(QtGui.QRadioButton(self))
                    self.days_btn[i-1].setMaximumSize(120,15)
                    self.days_btn[i-1].setText(date)

                    if self.days_btn[i-1].text() == datetime.strftime(datetime.now(), "%Y.%m.%d"):
                        self.days_btn[i-1].toggle()
                    self.mainLayout.addWidget(self.days_btn[i-1], i, 0,1,2, QtCore.Qt.AlignTop)
                    #self.days_btn[i].setToolTip('%s' %str(weekday))
                    self.connect(self.days_btn[i-1], QtCore.SIGNAL('clicked ()'), lambda: self.clearInformation()) #очистка информационного поля
                    #вызов информационного поля согласно текущей дате
                    self.connect(self.days_btn[i-1], QtCore.SIGNAL('clicked ()'), lambda date = date: self.information(date))
                    #print (type(date), date)

    def monthAndYear (self):
        self.month_btn_back = QtGui.QPushButton()
        self.month_btn_back.setIcon(self.icon_month_btn_back)
        self.mainLayout.addWidget(self.month_btn_back, 0, 0)
        self.month_btn_back.setMaximumSize(40,25)

        self.month_btn_forward = QtGui.QPushButton()
        self.month_btn_forward.setIcon(self.icon_month_btn_forward)
        self.mainLayout.addWidget(self.month_btn_forward, 0, 1)
        self.month_btn_forward.setMaximumSize(40, 25)
        self.connect(self.month_btn_forward, QtCore.SIGNAL('clicked ()'), self.clearDaysBtn)
        self.connect(self.month_btn_forward, QtCore.SIGNAL('clicked ()'), self.changeMonthPlus)
        self.connect(self.month_btn_forward, QtCore.SIGNAL('clicked ()'), self.monthAndYear)
        self.connect(self.month_btn_back, QtCore.SIGNAL('clicked ()'), self.clearDaysBtn)
        self.connect(self.month_btn_back, QtCore.SIGNAL('clicked ()'), self.changeMonthMinus)
        self.connect(self.month_btn_back, QtCore.SIGNAL('clicked ()'), self.monthAndYear)

    def changeMonthPlus(self):
        date = self.month_year
        #print (date)
        #print(date[5:])
        if (int(date[5:]) !=12) and ((int(date[5:]) <9)) :
            print(int(date[5:])+1)
            date= (date[0:4]+'.0'+str(int(date[5:])+1))
        elif (int(date[5:]) ==9):
            print(2)
            date = (date[0:4] +'.'+ str(int(date[5:]) + 1))
        elif (int(date[5:]) < 12) and (int(date[5:]) >= 10):
            print(2)
            date = (date[0:4] +'.'+ str(int(date[5:]) + 1))
        elif int(date[5:]) == 12:
            print(3)
            date=(str(int(date[0:4])+1) + '.01')
        self.daysBtn(month_year=date)
    def changeMonthMinus(self):
        date = self.month_year
        #print (date)
        #print(date[5:])
        if (int(date[5:]) !=1) and ((int(date[5:]) <11)) :
            #print(int(date[5:])-1)
            date= (date[0:4]+'.0'+str(int(date[5:])-1))
        elif (int(date[5:]) ==9):
            #print(2)
            date = (date[0:4] +'.'+ str(int(date[5:]) -1))
        elif (int(date[5:]) <=12) and (int(date[5:]) >= 10):
            #print(2)
            date = (date[0:4] +'.'+ str(int(date[5:]) -1))
        elif int(date[5:]) == 1:
            #print(3)
            date=(str(int(date[0:4])-1) + '.12')
        self.daysBtn(month_year=date)

    def clearDaysBtn(self):
        for i in range(len(self.days_btn)):
            self.days_btn[i].deleteLater()     #удаление каждого объекта PyQt4
        self.days_btn.clear()
    def sortMenu (self):
            self.menuBtn = QtGui.QPushButton('Raporty')
            self.mainLayout.addWidget(self.menuBtn, 0, 4)
            self.year_menu = QtGui.QMenu()
            self.menuBtn.setMenu(self.year_menu)
            year_menu_lst = {}
            month_menu_lst = {}
            day_menu_lst = {}
            employes_menu = QtGui.QMenu('Pracowniki')
            workman_dict = self.workman_lst
            workman_dict.pop('')
            ymd_dict = ymd.year_month_day()
            for year_number, year in enumerate(ymd.sort_year(ymd_dict)):
                print( year)
                year_menu_lst[year] = (self.year_menu.addMenu(year))
                #month_menu_lst['years'] = year_menu_lst[year].addAction('Roczny')
                for month_number, month in enumerate(ymd.sort_months(year)):
                    print (month, month_number)
                    month_menu_lst[year+month] = (year_menu_lst[year].addMenu(ymd.month_name(month)))

                    day_menu_lst['months'] = (month_menu_lst[year + month].addAction('Ogólny za miesiąc',
                                                     lambda month=month, year=year: self.monthes_raport(month, year)))


                    day_menu_lst['employes']=(month_menu_lst[year + month].addMenu('Pracowniki'))
                    for key, value in workman_dict.items():
                        day_menu_lst['employes'].addAction(value,
                                        lambda date=(month+year), workman_key=key: self.workman_raport(date, workman_key))

                    for day in ymd_dict[year][month]:
                        day_menu_lst[year+month+day]=(month_menu_lst[year+month].addAction(day,
                                            lambda date=(year + '.' + month + '.' + day): self.day_raport(date)))
            print(year_menu_lst, '\n', month_menu_lst, '\n', day_menu_lst)

    def monthes_raport (self, month, year):
        SortByDate.allDB(month=month, year=year,workmans=self.workman_lst)

    def workman_raport (self, date, workman_key):
        self.clearInformation()
        self.information(date=date,workman=workman_key)

    def day_raport (self, date):
        self.clearInformation()
        self.information(date=date)
    def number_installation_finder (self):
        c = conn.cursor()
        c.execute('SELECT order_number FROM details_of_installation ')
        tmp = c.fetchall()
        # создание и заполнение списка номеров инсталяций
        order_number_lst = []
        for i in range(len(tmp)):
            for j in tmp[i]:
                # print (j)
                if j == None:
                    continue
                else:
                    order_number_lst.append(str(j))
        # print (order_number_lst)
        # несмотря на то что поле называется date_field в него вписывается номер инсталяции
        self.date_field = QtGui.QLineEdit(self)
        self.date_field.setToolTip('Wprowadź numer zlecenia')
        self.date_field.setText('')
        self.date_field.setInputMask("9999999;_")
        self.date_field.setMaximumSize(75, 25)
        self.date_field.setCompleter(
            QtGui.QCompleter(order_number_lst))  # предлагает значение после начала ввода номера
        self.mainLayout.addWidget(self.date_field, 0, 5)
        # несмотря на то что поле называется date_field в него вписывается номер инсталяции
        self.connect(self.date_field, QtCore.SIGNAL('returnPressed()'),
                     lambda: (self.clearInformation(), self.information(instalation_number=(self.date_field.text()))))



        #преобразование даты
    def dateConvert(self, date):
        #print(date,' ; ', type(date))
        date = date
        #формата 11.03.2017   <class 'str'>
        #в строку <2017.03.11 <class 'str'> >
        if type(date) == str:
            #print(type(date), date)
            date = str(date)
            #print(date)
            date = (date[-4:] + '.' + date[3:5] + '.' + date[0:2])
            #print(type(date), date)
            return date
        #формата <PyQt4.QtCore.QDate(2017, 3, 12) <class 'PyQt4.QtCore.QDate'>>
        # в строку <2017.03.12    <class 'str'>>
        if type(date) == QtCore.QDate:
            date = str(date)
            date = date[19:-1].replace(' ', '')
            date = date.split(',')
            # print (date[2])
            if len(date[2]) == 1:
                date.insert(2, ('0' + str(date[2])))
                date.pop(3)
            if len(date[1]) == 1:
                date.insert(1, ('0' + str(date[1])))
                date.pop(2)
            date = (str(date[0]) + '.' + str(date[1]) + '.' + str(date[2]))
            #print (date,' ; ', type(date))
            return date

    #очищает информационное поле удаляя все объекты созданные методом <self.information>
    def clearInformation(self):
        #try:
        for i in range(len(self.object)):
            for j in range(len(self.object[i])):
                self.object[i][j].deleteLater()     #удаление каждого объекта PyQt4
        self.object.clear()                         # очистка списка Python содержащего ссылки на ообъекты PyQt4
        #except AttributeError:
         #   pass

    # Добавление инсталяции в базу данных, строка содержит только дату которая выбрана
    # в поле для ввода даты инсталяции <self.instalationDate> преобразованной методом <self.dateConvert>
    def addInstalationInDb(self):
        c = conn.cursor()
        c.execute('INSERT INTO installing ("date") VALUES ("%s")' %self.dateConvert(date=self.instalationDate.date()))
        conn.commit()
        c.execute('SELECT MAX ("id") FROM installing')
        id = c.fetchall()[0][0]

        try:
            c = conn.cursor()
            c.execute('INSERT INTO details_of_installation ("id", "success") VALUES ("%s", "True")' %id)
            conn.commit()
        except sqlite3.IntegrityError:
            pass


        if (datetime.strftime(datetime.now(), "%Y.%m.%d")) == (self.dateConvert(date=self.instalationDate.date())):
            for indx in range(len(self.days_btn)):
                if self.days_btn[indx].text() == (datetime.strftime(datetime.now(), "%Y.%m.%d")):
                    self.days_btn[indx].toggle()
                #print (self.days_btn[indx].text())
            self.clearInformation()
            self.information(datetime.strftime(datetime.now(), "%Y.%m.%d"))
           # print('1')

        else:
            for indx in range(len(self.days_btn)):
                if self.days_btn[indx].text() == (self.dateConvert(date=self.instalationDate.date())):
                    self.days_btn[indx].toggle()
            self.clearInformation()
            self.information(self.dateConvert(date=self.instalationDate.date()))
            #print('2')

    def information(self, date=(datetime.strftime(datetime.now(), "%Y.%m.%d")), instalation_number='', workman='', address = '',
                    success = ['True', 'False']):  # создание текстовых полей и внесение в них данных из базы данных
        self.args = [date, instalation_number, workman, address, success]
        print(self.args)
        if success == ['True', 'False']:
            tmp = 'IS NOT NULL'
        elif success == 'True':
            tmp = '= "True"'
        elif success == 'False':
            tmp = '= "False"'
        c = conn.cursor()
        #если в метод передана только дата
        if (instalation_number == '') and (workman=='') and (address == ''):
            c.execute('SELECT * FROM installing WHERE date = "%s"'
                      'AND (id IN (SELECT id FROM details_of_installation WHERE success %s ))'
                      % (str(date), tmp))
            self.row_3 = c.fetchall()
            #print (1)
        #если в метод передана дата и имя сотрудника
        elif (instalation_number == '') and (workman != ''):
            #print (instalation_number, '\n', workman,'\n', date)
            c.execute('SELECT * FROM installing WHERE (workman1 = "%s"OR workman2 = "%s") AND date LIKE "%s.%s.__"'
                      'AND (id IN (SELECT id FROM details_of_installation WHERE success %s ))'
                % (workman, workman, date[-4:], date[0:2], tmp))
            self.row_3 = c.fetchall()
            #print (2)
        #передан адрес
        elif address != '':
            self.row_3 = SortByDate.by_address(address)
            #print(address)
        #если в метод передан только номер инсталяции
        else:
            c.execute('SELECT * FROM installing WHERE id = (SELECT id FROM details_of_installation WHERE order_number = "%s" )'
                      % str(instalation_number))
            self.row_3 = c.fetchall()
            #print (3)
        #создание списка сотрудников
        c.execute('SELECT * FROM workman')
        self.workman = c.fetchall()
        self.workman_lst = {}
        self.workman_lst['']=''
        for w in range(len(self.workman)):
            self.workman_lst[self.workman[w][0]]= str(self.workman[w][1])+' '+ str(self.workman[w][2])
        #print (self.workman_lst)
        #создание полей согласно выборке из базы данных
        self.object = []
        #print (self.row_3)
        for i in range (len(self.row_3)):
            #создание нового списка внутри главного списка <self.object[]> для каждой новой строки
            self.object.append([])
            for j in range(len(self.row_3[i])):
                #номер по порядку
                if j == 0:
                    self.object[i].append(QtGui.QLabel())
                    self.object[i][j].setText(str(i+1))
                    self.object[i][j].setMaximumSize(25, 25)
                    self.object[i][j].setMinimumSize(25, 25)
                    self.object[i][j].setAlignment(QtCore.Qt.AlignCenter)
                    self.scrollLayout.addWidget(self.object[i][j], i, j,QtCore.Qt.AlignTop)
                    #поле даты (поле недоступно для редактирования)
                elif j == 1:
                    self.object[i].append(QtGui.QDateEdit())
                    self.object[i][j].setDate(QtCore.QDate(int(self.row_3[i][j][0:4]),
                                           int(self.row_3[i][j][5:7]),
                                           int(self.row_3[i][j][8:])))
                    self.object[i][j].setMaximumSize(130, 25)
                    self.object[i][j].setMinimumSize(130, 25)
                    self.scrollLayout.addWidget(self.object[i][j], i, j,QtCore.Qt.AlignTop)
                    self.object[i][j].setEnabled(False)

                    #поле для выбора времени начала инсталяции
                elif j == 2:
                    time = ['08:00', '11:00', '14:00', '17:00', '20:00']
                    self.object[i].append(QtGui.QComboBox())
                    for t in range(0, len(time)-1):
                        self.object[i][j].addItem(str(time[t]))
                    for w in time:
                        if w == str(self.row_3[i][j]):
                            self.object[i][j].setCurrentIndex(time.index(w))
                    self.insertInCell((self.object[i][j].currentText()),i, j)
                    self.scrollLayout.addWidget(self.object[i][j], i, j,QtCore.Qt.AlignTop)
                    self.object[i][j].setMaximumSize(60, 25)
                    self.object[i][j].setMinimumSize(60, 25)
                    self.connect(self.object[i][j], QtCore.SIGNAL('activated(const QString&)'),
                                 lambda tmp=i, i=i, j=j: self.insertInCell(tmp, i, j))

                # поле для выбора времени конца инсталяции
                elif j == 3:
                    self.object[i].append(QtGui.QComboBox())
                    for t in range(1, len(time)):
                        self.object[i][j].addItem(str(time[t]))
                    for w in time:
                        if w == str(self.row_3[i][j]):
                            self.object[i][j].setCurrentIndex(time.index(w)-1)
                    self.insertInCell((self.object[i][j].currentText()), i, j)
                    self.scrollLayout.addWidget(self.object[i][j], i, j,QtCore.Qt.AlignTop)
                    self.object[i][j].setMaximumSize(60, 25)
                    self.object[i][j].setMinimumSize(60, 25)
                    self.connect(self.object[i][j], QtCore.SIGNAL('activated(const QString&)'),
                                 lambda tmp=i, i=i, j=j: self.insertInCell(tmp, i, j))

                # поле для адреса инсталяции
                elif j == 4:
                    self.object[i].append(QtGui.QLineEdit())
                    if (self.row_3[i][j] == None) or (self.row_3[i][j] == 'None'):
                        self.object[i][j].setText('')
                    else:
                        self.object[i][j].setText(str(self.row_3[i][j]))
                    self.scrollLayout.addWidget(self.object[i][j], i, j,QtCore.Qt.AlignTop)
                    self.object[i][j].setMaximumSize(300, 25)
                    self.object[i][j].setMinimumSize(300, 25)
                    self.connect(self.object[i][j], QtCore.SIGNAL('textChanged(QString)'),
                                 lambda tmp=i, i=i, j=j: self.insertInCell(tmp, i, j))

                # поле 1 и 2 для выбора сотрудника
                elif (j == 5) or (j ==6):
                    self.object[i].append(QtGui.QComboBox(self))
                    tmp = []
                    for value in self.workman_lst.values():
                        self.object[i][j].addItem(str(value))
                        tmp.append(str(value))
                    for key, value in self.workman_lst.items():
                        #print (key)
                        #print (value)
                        #print (self.row_3[i][j])

                        if str(key) == str(self.row_3[i][j]):

                            self.object[i][j].setCurrentIndex(tmp.index(value))

                    self.scrollLayout.addWidget(self.object[i][j], i, j,QtCore.Qt.AlignTop)
                    self.object[i][j].setMaximumSize(150, 25)
                    self.object[i][j].setMinimumSize(150, 25)
                    self.connect(self.object[i][j], QtCore.SIGNAL('activated(const QString&)'),
                                 lambda tmp=i, i=i, j=j: self.insertInCell(tmp, i, j))

                # кнопки :<Szczegóły instalacji> - дополнительно,  <Usuń> - удалить строку
                else:
                    self.object[i].append(QtGui.QPushButton('Szczegóły instalacji'))
                    self.object[i][j].setMaximumSize(125, 25)
                    self.object[i][j].setMinimumSize(125, 25)
                    self.scrollLayout.addWidget(self.object[i][j], i, j, QtCore.Qt.AlignTop)
                    #по нажатию кнопки вызывается модальное диалоговое окна с дополнительной информацией для инсталяции
                    self.connect(self.object[i][j], QtCore.SIGNAL('clicked ()'), lambda id=str(self.row_3[i][0]):
                                                                self.wakeUpInstalationWindow(id))

                    self.object[i].append(QtGui.QPushButton())
                    self.object[i][j + 1].setIcon(self.icon_delete)
                    self.object[i][j+1].setMaximumSize(60, 25)
                    self.object[i][j+1].setMinimumSize(60, 25)
                    self.scrollLayout.addWidget(self.object[i][j+1], i, j+1, QtCore.Qt.AlignTop)
                    #полное удаление информации о инсталяции из базы данных и объектов Python и PyQt4 из программы
                    #при вызове метода <self.delLine>по нажатию кнопки <Usuń>
                    self.connect(self.object[i][j+1], QtCore.SIGNAL('clicked ()'),
                                 lambda id=str(self.row_3[i][0]), index=i:self.delLine(id=id,index=index))

                    self.object[i].append(QtGui.QCheckBox(''))
                    #self.object[i][j + 2].setIcon(self.icon_delete)
                    self.object[i][j + 2].setMaximumSize(25, 25)
                    self.object[i][j + 2].setMinimumSize(25, 25)
                    if (self.object[i][5].currentIndex() > 0) and (self.object[i][6].currentIndex() > 0):
                        self.object[i][j+2].setCheckState(2)
                        self.object[i][2].setEnabled(False)
                        self.object[i][3].setEnabled(False)
                        self.object[i][5].setEnabled(False)
                        self.object[i][6].setEnabled(False)
                    self.scrollLayout.addWidget(self.object[i][j + 2], i, j + 2, QtCore.Qt.AlignTop)
                    # чекбокс для блокирования изменения данных
                    self.connect(self.object[i][j + 2], QtCore.SIGNAL('stateChanged(int)'),
                                 lambda tmp=i, i=i: self.changeActivity(index=tmp, i=i ))
                    self.connect(self.object[i][5], QtCore.SIGNAL('activated(const QString&)'),
                                 lambda tmp=i, i=i: self.on_ChangedCombobox(tmp, i))
                    self.connect(self.object[i][6], QtCore.SIGNAL('activated(const QString&)'),
                                 lambda tmp=i, i=i: self.on_ChangedCombobox(tmp, i))
        try:
            self.changeFontColor(lst_object=self.object, lst_row=self.row_3)
        except IndexError:
            pass
        return self.args

    def success_all (self, status):
        args = self.args
        self.clearInformation()
        if status == 0:
            args[4] = 'False'
            self.information(date=args[0], instalation_number= args[1], workman= args[2] , address= args[3], success = args[4] )
        elif status == 1:
            args[4] = 'True'
            self.information(date=args[0], instalation_number=args[1], workman=args[2], address=args[3], success = args[4])
        elif status == 2:
            args[4] = ['True', 'False']
            self.information(date=args[0], instalation_number=args[1], workman=args[2], address=args[3],success=args[4])

    def changeFontColor(self, lst_object, lst_row):
        #print(len(lst_object), lst_object)
        tmp =[]
        for i in range(len(lst_row)):
            tmp.append (str(lst_row[i][0]))
        tmp = ','.join(tmp)
        c.execute('SELECT * FROM details_of_installation WHERE id IN (%s)' %tmp)
        details = c.fetchall()
        for i in range(len(lst_object)):
            if details[i][1] == 'False':
                text = lst_object[i][0].text()
                lst_object[i][0].setText('<font color="red">%s</font>' %text)


    def on_ChangedCombobox (self, tmp,i):
        #print(tmp,i)
        if (self.object[i][5].currentIndex() > 0) and (self.object[i][6].currentIndex() > 0):
            self.object[i][9].setCheckState(2)
            self.object[i][2].setEnabled(False)
            self.object[i][3].setEnabled(False)
            self.object[i][5].setEnabled(False)
            self.object[i][6].setEnabled(False)

    def changeActivity (self, i, index='2'):
        #print (i, index)
        if index == 2:
            active = False
        else:
            active = True
        self.object[i][2].setEnabled(active)
        self.object[i][2].setEnabled(active)
        self.object[i][3].setEnabled(active)
        self.object[i][5].setEnabled(active)
        self.object[i][6].setEnabled(active)



    def delLine (self, id, index):
        c = conn.cursor()
        c.execute('DELETE FROM installing WHERE id="%s"' % id)
        conn.commit()#!!!!обязательно закрывать транзакцию SQL

        c = conn.cursor()
        c.execute('DELETE FROM details_of_installation WHERE id="%s"' % id)
        conn.commit()#!!!!обязательно закрывать транзакцию SQL

        c = conn.cursor()
        c.execute('DELETE FROM equipment WHERE id="%s"' % id)
        conn.commit()#!!!!обязательно закрывать транзакцию SQL

        for i in self.object[index]:
            i.deleteLater()
        del self.object[index]

    # вставка данных в определенную ячейку определенной таблицы базы данных valu= значение, i=индекс строки,
    # j=индекс строки заголовка таблицы
    def insertInCell(self,  value,i, j):
        c = conn.cursor()
        c.execute('PRAGMA table_info (installing) ')
        det = c.fetchall()
        if (j == 5) or (j == 6):
            for key, val in self.workman_lst.items():
                if val == value:
                    c = conn.cursor()
                    c.execute('UPDATE installing SET "%s"="%s" WHERE id=%s'% (str(det[j][1]), str(key), self.row_3[i][0] ))
                    conn.commit()#!!!!обязательно закрывать транзакцию SQL
        else:
            c = conn.cursor()
            c.execute('UPDATE installing SET "%s"="%s" WHERE id=%s' % (str(det[j][1]), str(value), self.row_3[i][0]))
            conn.commit()  # !!!!обязательно закрывать транзакцию SQL
    #метод для вызова окна дополнительной информации о инсталяции
    def wakeUpInstalationWindow(self, id):
        self.instalationWindow = Instalation.InstalationWindow(parent=self,id=id)

    # метод для вызова окна сотрудников
    def wakeUpWorkmanWindow(self):
        self.workmanWindow = Workman.WorkmanWindow(self)




    '''def closeEvent(self, event):
        conn.close()
        import ftpconnect
        ftpconnect.fileToFtp('my.db')'''






if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    main = Main()

    sys.exit(app.exec_())
