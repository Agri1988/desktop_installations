import sqlite3
conn = sqlite3.connect('my.db')
from datetime import datetime, timedelta
import xlwt

def by_address(address):
    c = conn.cursor()
    c.execute('SELECT * FROM installing WHERE address = "%s"' % address)
    installing = c.fetchall()
    return installing
    #print(installing)

def all_address ():
    c = conn.cursor()
    c.execute('SELECT address FROM installing')
    addresses = c.fetchall()
    new_addresses = []
    for address in addresses:
        new_addresses.append(address[0])
    return new_addresses

    #print(new_addresses)
#all_address()

def bydate (date = ''):
    c = conn.cursor()
    c.execute('SELECT id, date, address FROM installing WHERE date = "%s"' % date)
    installing = c.fetchall()
    #print(installing)


def byworkman (workman= '', day = "__",month = "__",year="____"):
    c = conn.cursor()
    c.execute('SELECT date,address FROM installing WHERE (workman1 = "%s" OR workman2 = "%s") '
              'AND (date LIKE "%s.%s.%s") AND (id IN (SELECT id FROM details_of_installation WHERE success = "True")) ORDER BY date'
              %(workman, workman, year, month, day))
    installing = c.fetchall()
    #print (installing)
    return installing


def allDB (month = '03', year='2017', workmans=''):
    workman_lst = workmans
    keys = []
    values = []
    for key,value in workman_lst.items():
        keys.append(key)
        values.append(value)
    raport = []
    for id in range(len(keys)):
        raport.append(byworkman(workman='%s' %keys[id], month = month, year=year))
    #print (raport)
    # Создаем книку
    book = xlwt.Workbook('utf8')

    # Создаем шрифт
    borders = xlwt.Borders()
    borders.bottom = xlwt.Borders.THIN
    borders.top = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN

    # font = xlwt.easyxf('font: height 240,name Arial,colour_index black, bold off,\
    #         italic off; align: wrap on, vert top, horiz left;\
    #         pattern: pattern solid, fore_colour red;')

    style = xlwt.XFStyle()
    style.borders = borders



    # Добавляем лист
    sheet = book.add_sheet('sheetname')
    r = 1
    for i in range(len(values)):
        # Заполняем ящейку (Строка, Колонка, Текст, Шрифт)
        sheet.write(r, 0, values[i], style)
        iterr = 1
        for j in range(len(raport[i])):
            sheet.write(r, 1, iterr, style)
            #print (raport[i][j])
            iterr +=1
            for x in range(len(raport[i][j])):
                sheet.write(r, x+2, raport[i][j][x], style)
            r+=1
        r+=1

    # Высота строки
    sheet.row(1).height = 250

    # Ширина колонки
    sheet.col(0).width = 5000
    sheet.col(1).width = 1000
    sheet.col(2).width = 2600
    sheet.col(3).width = 8000


    # Лист в положении "альбом"
    sheet.portrait = True

    # Масштабирование при печати
    sheet.set_print_scaling(120)

    # Сохраняем в файл
    book.save('filename.xls')
    # запуск файла из питона
    cmd = 'ping yandex.ru -c 5'
    import subprocess
    subprocess.call("filename.xls", shell=True)


'''
# Создаем книку
book = xlwt.Workbook('utf8')

# Создаем шрифт
font = xlwt.easyxf('font: height 240,name Arial,colour_index black, bold off,\
    italic off; align: wrap on, vert top, horiz left;\
    pattern: pattern solid, fore_colour red;')

# Добавляем лист
sheet = book.add_sheet('sheetname')
# Заполняем ящейку (Строка, Колонка, Текст, Шрифт)
sheet.write(0, 0, 'text', font)

# Высота строки
sheet.row(1).height = 2500

# Ширина колонки
sheet.col(0).width = 1450

# Лист в положении "альбом"
sheet.portrait = False

# Масштабирование при печати
sheet.set_print_scaling(85)

# Сохраняем в файл
book.save('filename.xls')
# запуск файла из питона
cmd = 'ping yandex.ru -c 5'
import subprocess
subprocess.call("filename.xls", shell=True)'''


