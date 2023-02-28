''' You work at a company that sends daily reports to clients via email. The goal of this project is to automate the process of sending these reports via email.

Here are the steps you can take to automate this process:

    Done - Use the smtplib library to connect to the email server and send the emails.

    Done - Use the email library to compose the email, including the recipient's email address, the subject, and the body of the email.

    Done - Use the os library to access the report files that need to be sent.

    Done - Use a for loop to iterate through the list of recipients and send the email and attachment.

    Done - Use the schedule library to schedule the script to run daily at a specific time.

    Done - You can also set up a log file to keep track of the emails that have been sent and any errors that may have occurred during the email sending process. '''


import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import schedule
import time
import datetime

#pip install schedule

SENDER_EMAIL = '' #add your email
SENDER_PSW = '' #if gmail, generate and add your gmail app password
MAIL_SERVER ='smtp.gmail.com' #change according to your mail account
PORT = 587 #change according to your mail account
EMAIL_TEMPLATE_FILE = 'email_template.txt'
RECIEVERS_EMAILS_FILE = 'recievers.txt'



def sendMail():

    try:

        sender_address = SENDER_EMAIL
        printTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mail_content = open(EMAIL_TEMPLATE_FILE).read()
        receiver_address = open(RECIEVERS_EMAILS_FILE).read().splitlines()# read the emails without \n

        for reciever in receiver_address:
            #Setup the MIME
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = reciever
            message['Subject'] = 'Daily Report'   #The subject line
            
            #attach the Attachement using basename avoiding using relative or path
            filename = 'Report.txt'
            with open(filename, 'r') as f: #open the file
                attachement =  MIMEApplication(f.read(), Name=basename(filename)) #read the contects and define the object
                attachement['Content-Disposition'] = 'attachement; filename="{}"'.format(basename(filename)) #format the contents in thw way that object want
            message.attach(attachement)
            
            #The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))

            #Create SMTP session for sending the mail
            session = smtplib.SMTP(MAIL_SERVER, PORT) #use gmail with port
            session.starttls() #enable security
            session.login(sender_address, SENDER_PSW) #login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, reciever, text)
            session.quit()

            #Write to logs
            log = open("logs.txt", "a+") #create if not exists
            log.write('['+ printTime +'] Email Sent to '+ reciever  + "\n")
            log.close()

    except Exception as e:
        #Write to logs
        log = open("logs.txt", "a+") #create if not exists
        log.write('['+ printTime +'] ERROR: unable to send email '  + "\n" + '['+ printTime +'] ERROR message: ' +str(e) + "\n")
        log.close()




def main():

    # Run daily at 08:00
    schedule.every().day.at("08:00").do(sendMail)

    # Loop so that the scheduling task
    # keeps on running all time.
    while True:
        # Checks whether a scheduled task
        # is pending to run or not
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
