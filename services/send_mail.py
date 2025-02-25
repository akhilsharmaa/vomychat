import os
import smtplib
from dotenv import load_dotenv 

load_dotenv()
 

GMAIL_USER = os.environ.get("GMAIL_USER") 
GMAIL_PASS = os.environ.get("GMAIL_PASS") 

def send_mail():  
    
    sent_from = GMAIL_USER

    to = ['akhil.sudo@gmail.com', 'akhilsharma3332@gmail.com']
    subject = 'Message subject'
    body = "Hey, what's up?\n\n- You"

    email_text = """\
    From: {}
    To: {}
    Subject: {}

    {}
    """.format(sent_from, ", ".join(to), subject, body)

    server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
    server.ehlo()
    server.login(GMAIL_USER, GMAIL_PASS)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print('Email sent!') 
        
send_mail()