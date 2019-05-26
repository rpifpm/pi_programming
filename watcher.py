import smtplib
import os
import time  
import configparser

#functions

def configure():
	#read the ini file
	inifile = '../config/watcher.ini'
	config = configparser.ConfigParser()
	config.read(inifile)
  
	# define attach file
	atfile = '/home/pi/foto2.jpg'  
 
  
	# Define email addresses to use
	addr_to   = config['mail']['addr_to']
	addr_from = config['mail']['addr_from']
  
	# Define SMTP email server details
	smtp_server = config['mail']['smtp_server']
	smtp_user = config['mail']['smtp_user']
	smtp_pass = config['mail']['smtp_pass']
	
	return

# Import the email modules
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase

configure()

while True:
	#takes photo
	os.system('fswebcam -r 640x480 /home/pi/foto2.jpg') 
	  
	# Construct email
	msg = MIMEMultipart()
	msg['To'] = addr_to
	msg['From'] = addr_from
	msg['Subject'] = 'Photo Test Email From RPi'

	body ='Prueba de envio de fotografia'

	# Add body to email
	msg.attach(MIMEText(body, "plain"))

	filename = atfile  

	# Open file in binary mode
	with open(filename, "rb") as attachment:
		# Add file as application/octet-stream
		# Email client can usually download this automatically as attachment
		part = MIMEBase("application", "octet-stream")
		part.set_payload(attachment.read())

	# Encode file in ASCII characters to send by email    
	encoders.encode_base64(part)

	# Add header as key/value pair to attachment part
	part.add_header(
		"Content-Disposition",
		"attachment; filename= foto.jpg",
	)

	# Add attachment to message and convert message to string
	msg.attach(part)
	text = msg.as_string()
	  
	# Send the message via an SMTP server
	try:
	  s = smtplib.SMTP(smtp_server)
	  s.ehlo()
	  s.starttls()
	  s.login(smtp_user,smtp_pass)
	  s.sendmail(addr_from, addr_to, text)
	  s.quit()
	except Exception, ex1:
	  print("There was an error sending the email. Check the smtp settings.")
	  print ex1

	time.sleep(1*60*60)


