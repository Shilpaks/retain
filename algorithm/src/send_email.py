import imp 
import time
import smtplib

class Email(object):
    def __init__(self, recipient):
        self.recipient = recipient
        self.sender_email_account_credentials = imp.load_source("sender_email_account_credentials", "resources/sender_email_account_credentials.py")

    def send_email(self, subject, body):
        gmail_user = self.sender_email_account_credentials.user
        gmail_pwd = self.sender_email_account_credentials.password
        print gmail_user, gmail_pwd
        FROM = gmail_user
        TO = [self.recipient]
        SUBJECT = subject
        TEXT = body

        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            print "hi"
            server = smtplib.SMTP("smtp.gmail.com", 587)
            print "hi"
            server.ehlo()
            print "hi"
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            print "successful login"
            server.sendmail(FROM, TO, message)
            server.close()
            return True
        except:
            print "Failed to send to ", self.recipient
            return False 

    def robust_send_email(self, subject, body):
        NUM_TRIES = 3
        success = False
        while not success and NUM_TRIES > 0: 
            success = self.send_email(subject, body)
            NUM_TRIES -= 1
            if not success:
                time.sleep(1) # if email fails to send, wait 1 second before resending. this is so we don't overload the SMTP server with requests 
            else: 
                return True 
        return False

email = Email("subrahm2@illinois.edu")
email.send_email("Your Daily Concepts", "Vector Space Model, Pearson Learning Coefficient, and Text Retrieval")