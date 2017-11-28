from zipfile import ZipFile
import os
import shutil
import re
def inf_whith_documents():
    file_lst = []
    dict = {}
    for count, file in enumerate(os.listdir('.')):
        if file[-3:] == 'xps':
            dict[count] = []
            file_lst.append(file)
            z = ZipFile('%s' %file, 'r')
            z.extract('Documents/1/Pages/1.fpage', './')
            z.close()
            f = open('Documents/1/Pages/1.fpage', 'r', encoding='utf-8')
            f = f.read()
            f = f.replace('\xa0', '')
            f = ''.join(re.findall(r'UnicodeString="(.+?)" Indices', f))
            dict[count].append(''.join(re.findall(r'Zlecenie instalacji nr:(.+?)Zlecenie złożone nr:', f)))
            dict[count].append(''.join(re.findall(r'Adres lokalizacji:(.+?)15-', f)))
            dict[count].append(''.join(re.findall(r'klienta/użytkownika:(.+?)Segment właściciela', f)))
            dict[count].append(''.join(re.findall(r'Planowana data:(.+?)Typ usługi:', f)))
            dict[count].append(file[:2])
            dict[count].append(file[2:4])
            dict[count].append(file[4])
            #print(lst)
            shutil.rmtree('Documents')
            os.remove('%s' % file)
    return (dict)
# dict = (inf_whith_documents())
# for key, value in dict.items():
#     print(value)




