import os
import smtplib
from dotenv import load_dotenv 
from fastapi.responses import JSONResponse

load_dotenv()

GMAIL_USER = os.environ.get("GMAIL_USER") 
GMAIL_PASS = os.environ.get("GMAIL_PASS") 

def send_mail(subject, to, body_text):  
    
    sent_from = GMAIL_USER  

    email_text = """\
    From: {}
    To: {}
    Subject: {}

    {}
    """.format(sent_from, ", ".join(to), subject, body_text)

    try: 
        server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(sent_from, to, email_text)
        server.close()
        
    except: 

        return JSONResponse(
            status_code=400,
            content= {
                "message": f"Failed to send the mail.",  
            }
        )      
