# Automating-Email-Sending

This project sends daily scheduled emails with attachement to a list of emails. In addition it writes all the email sending history or errors to a log file.

## Before running

### Install
+ pip install schedule

### Fill the next fields:
++ SENDER_EMAIL
+ SENDER_PSW 
+ MAIL_SERVER 
+ PORT 

### Alter the next files with the desired email template and recievers that you want:
+  email_template.txt
+  recievers.txt

### Create the Report.txt file in order to be attached to the email

### Note: if you are using gmail server generate an app password from your google account

## How to run
+ python '.\Automating Email Sending.py'



