# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
import smtplib

EMAIL = 'deafoyatalk@gmail.com'
PASSWORD = 'czzceszhsoihatwj'
TO = 'deafoyatalk@gmail.com'

msg = MIMEText('This is a test')

msg['Subject'] = 'Test Mail Subject'
msg['From'] = EMAIL
msg['To'] = TO

s = smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(EMAIL, PASSWORD)
s.sendmail(EMAIL, TO, msg.as_string())
s.quit()