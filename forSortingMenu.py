import sqlite3

conn = sqlite3.connect('my.db')
def year_month_day ():
    c = conn.cursor()
    c.execute('SELECT date FROM installing')
    year_dict = {}
    #print (c.fetchall())
    for i in c.fetchall():
        if i[0][0:4] not in year_dict:
            year_dict[i[0][0:4]]= {}
        if i[0][5:7] not in year_dict[i[0][0:4]]:
            year_dict[i[0][0:4]][i[0][5:7]] = []
        if i[0][-2:] not in year_dict[i[0][0:4]][i[0][5:7]]:
            year_dict[i[0][0:4]][i[0][5:7]].append(i[0][-2:])
    return (year_dict)
print (year_month_day())

def month_name (number):
    c = conn.cursor()
    c.execute('SELECT * FROM month')
    for i in c.fetchall():
        if str(number) == i[0]:
            return i[1]


def sort_year(year_dict):
    years_lst = []
    for keys in year_dict.keys():
        years_lst.append(keys)
    years_lst.sort()
    return years_lst

def sort_months (year):
    months_lst = []
    for month in year_month_day()[year].keys():
        months_lst.append(month)
        months_lst.sort()
    return months_lst


#print(year_month_day(), '\n', sort_year(year_month_day()))