import smtplib
import ssl
import json

port = 465
keys = json.load(open('./.app_info/keys.json'))['gmail']
sender_email = keys['email']
password = keys['password']
reciever_email = 'beekenj@gmail.com'

def send_report(message):
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
	    server.login(sender_email, password)
	    # Send email here
	    server.sendmail(sender_email, reciever_email, message)