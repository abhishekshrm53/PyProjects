from SendEmails import creds
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path

html = Template(Path('index.html').read_text())
email = EmailMessage()
email['from'] = "abhishekshrm53@live.com"
email['to'] = 'abhishekshrm53@gmail.com'
email['subject'] = 'Sent from python'

email.set_content(html.substitute({'name': 'Abhishek'}), 'html')

with smtplib.SMTP(host="smtp-mail.outlook.com", port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(creds.email, creds.pswrd)
    smtp.send_message(email)
    print('Done')
