import ftplib
import os


class fileToFtp:
    def __init__(self, name):
        self.name = str(name)
        host = "ftp.agri.bplaced.net"
        ftp_user = "agri"
        ftp_password = "07831505"
        filename = ("%s" % self.name)

        con = ftplib.FTP(host, ftp_user, ftp_password)
        # Открываем файл для передачи в бинарном режиме
        f = open(filename, "rb")
        # Передаем файл на сервер
        send = con.storbinary("STOR " + filename, f)
        f.close()
        # Закрываем FTP соединение
        con.close
        #os.remove(self.name)
class fileWithFtp:
    def __init__(self):
        #self.name = str(name)
        host = "ftp.agri.bplaced.net"
        ftp_user = "agri"
        ftp_password = "07831505"

        con = ftplib.FTP(host, ftp_user, ftp_password)
        lst = sorted(con.nlst())
        #f = open(str(lst[3:]), 'wb')
        print(lst)
        print (lst[3:])
        '''for i in lst[3:]:
            f = open(str(i), 'wb')
            index = lst.index(i)
            con.retrbinary('RETR %s' % str(lst[index]),f.write)
            f.close()
            #con.delete(str(lst[index]))'''

fileWithFtp()


