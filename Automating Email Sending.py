import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import schedule
import time
import datetime

SENDER_EMAIL = '' #add your email
SENDER_PSW = '' #if gmail, generate and add your gmail app password
MAIL_SERVER ='smtp.gmail.com' #change according to your mail account
PORT = 587 #change according to your mail account
EMAIL_TEMPLATE_FILE = 'email_template.txt'
RECIEVERS_EMAILS_FILE = 'recievers.txt'



def sendMail():

    try:
        
        printTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mail_content = open(EMAIL_TEMPLATE_FILE).read()
        receiver_address = open(RECIEVERS_EMAILS_FILE).read().splitlines()# read the emails without \n

        for reciever in receiver_address:
            #Setup the MIME
            message = MIMEMultipart()
            message['From'] = SENDER_EMAIL
            message['To'] = reciever
            message['Subject'] = 'Daily Report'
            
            #Attach the attachement using basename avoiding using relative or absolute path
            filename = 'Report.txt'
            with open(filename, 'r') as f: #open the file
                attachement =  MIMEApplication(f.read(), Name=basename(filename)) #read the contects and define the object
                attachement['Content-Disposition'] = 'attachement; filename="{}"'.format(basename(filename)) #format the contents in thw way that object want
            message.attach(attachement)
            
            #The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))

            #Create SMTP session and send the email
            session = smtplib.SMTP(MAIL_SERVER, PORT) #use gmail with port
            session.starttls() #enable security
            session.login(SENDER_EMAIL, SENDER_PSW) #login with mail_id and password
            text = message.as_string()
            session.sendmail(SENDER_EMAIL, reciever, text)
            session.quit()

            #Write to logs
            log = open("logs.txt", "a+") #create if not exists
            log.write('['+ printTime +'] Email sent to '+ reciever  + "\n")
            log.close()

    except Exception as e:
        #Write to logs
        log = open("logs.txt", "a+") #create if not exists
        log.write('['+ printTime +'] ERROR: unable to send email '  + "\n" + '['+ printTime +'] ERROR message: ' +str(e) + "\n")
        log.close()




def main():

    # Run daily at 08:00
    schedule.every().day.at("08:00").do(sendMail)

    # Loop so that the scheduling task keeps on running all time.
    while True:
        # Checks whether a scheduled task is pending to run or not
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
