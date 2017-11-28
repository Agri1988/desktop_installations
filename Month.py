import main
class Month:
    conn = sqlite3.connect('my.db')
    c = conn.cursor()
    c.execute('SELECT * FROM month')
    self.row_2 = c.fetchall()
    # print (self.row_2)
    self.btn_2 = []
    for i in range(len(self.row_2)):
        self.btn_2.append(QtGui.QRadioButton(str(self.row_2[i][1])))
        self.mainLayout.addWidget(self.btn_2[i], i + 1, 0)