#!/usr/bin/env python

import smtplib as smtp
def send_mail(sent_to,sent_body,location):
    gmail_user = <Email Address>
    gmail_password = <password>
    sent_subject = "Top 10 Resturant at "+location.capitalize()

    email_text = """From: %s
To: %s
Subject: %s
    
%s
""" % (gmail_user, sent_to, sent_subject, sent_body)

    try:
        server = smtp.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, sent_to, email_text)
        server.close()
    except:
        print('Somthing Went Wrong')

