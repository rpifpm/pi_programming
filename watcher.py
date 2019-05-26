import smtplib
import os
import time  
import configparser

#functions

def configure():
	conf={}
	#read the ini file
	inifile = '../config/watcher.ini'
	config = configparser.ConfigParser()
	config.read(inifile)
  
	# define attach file
	conf['atfile'] = config['mail']['atfile']
 
  
	# Define email addresses to use
	conf['addr_to']   = config['mail']['addr_to']
	conf['addr_from'] = config['mail']['addr_from']
  
	# Define SMTP email server details
	conf['smtp_server'] = config['mail']['smtp_server']
	conf['smtp_user'] = config['mail']['smtp_user']
	conf['smtp_pass'] = config['mail']['smtp_pass']
	
	return conf
	
def takePhoto(conf):
	atfile = conf.get('atfile')
	stringPhoto = 'fswebcam -r 640x480' + atfile
	os.system(stringPhoto) 
	
	return

def sendMail(conf):	
	msg = MIMEMultipart()
	msg['To'] = conf.get('addr_to')
	msg['From'] = conf.get('addr_from')
	msg['Subject'] = 'Photo Email From RPi'

	body ='Photo from home'

	# Add body to email
	msg.attach(MIMEText(body, "plain"))

	filename = conf.get('atfile')
	
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
	  s = smtplib.SMTP(conf.get('smtp_server'))
	  s.ehlo()
	  s.starttls()
	  s.login(conf.get('smtp_user'),conf.get('smtp_pass'))
	  s.sendmail(conf.get('addr_from'), conf.get('addr_to'), text)
	  s.quit()
	except Exception, ex1:
	  print("There was an error sending the email. Check the smtp settings.")
	  print ex1
	  
	return

# Import the email modules
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase

conf = configure()

#main loop 
while True:
	#takes photo
	takePhoto(conf)
	  
	# send email
	sendMail(conf)

	# wait
	time.sleep(1*60*60)


