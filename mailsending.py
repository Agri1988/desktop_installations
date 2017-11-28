# import smtplib
#
# smtpObject = smtplib.SMTP('smtp.yandex.com', 587)
# smtpObject.starttls()
# smtpObject.login('tes.mail2017@yandex.com', '07831505')
# smtpObject.sendmail('tes.mail2017@yandex.com', 'tes.mail2017@yandex.com', msg='xsdfghjk')
#
# print ('hello world')

from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

filepath = "d:/python/instalacji/filename.xls"
basename = os.path.basename(filepath)
address = "tes.mail2017@yandex.com"

# Compose attachment
part = MIMEBase('application', "octet-stream")
part.set_payload(open(filepath,"rb").read() )
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="%s"' % basename)

# Compose message
msg = MIMEMultipart()
msg['From'] = address
msg['To'] = address
msg.attach(part)

# Send mail
smtp = SMTP('smtp.yandex.com', 587)
smtp.starttls()
smtp.login(address, '07831505')
smtp.sendmail(address, address, msg.as_string())
smtp.quit()