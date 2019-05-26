#!/home/servidor/env/bin/python2.7
########### OBSERVER 1 ################################### THIS PROCCESS WILL WATCH FOR NEW EMAIL REQUESTS ##################


# connect to database
# read for new requests by field marcado
# marcado = 0 is new
# marcado = 1 is not new
# will generate emails and sent the requester on the field correo
import mysql.connector
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

class Obsr:
    def __init__(self,username = None,password = None,server = None,database = None):
        self.username = username
        self.password = password
        self.server = server
        self.database = database
        self.mydb = None

    def dbconnection(self):
        mydb = mysql.connector.connect(
        host=self.server,
        user=self.username,
        passwd=self.password,
        database=self.database
        )
        self.mydb = mydb
    
    def getPendings(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM registro where marcado IS NULL ")
        myresult = mycursor.fetchall()
        return myresult

    def marcarComoCreado(self,id):
        mycursor = self.mydb.cursor()
        sql = "UPDATE registro SET marcado = 'True'"
        mycursor.execute(sql)
        self.mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

    def generateEmails(self,nombre,idd):
        ############# este correo debe de ser generado por el servidor de correos ##########
        ############# aqui solo ponemos una funcion ejemplo #####################
        nombre = re.sub('[^A-Za-z0-9]+', '', nombre) 
        correo = nombre+"_"+str(idd)+"@itt.mx"
        return correo


    def sendemail_local(self,to = None,subject = "Nuevo Correo",text = "Tu Nuevo correo"):                   
        # me == my email address
        # you == recipient's email address
        me = "ittadmins@itt.mx"                
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = to

        # Create the body of the message (a plain-text and an HTML version).        
        html = '<p>' + str(text) + '</p>'

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        
        try:
            # Send the message via local SMTP server.
            s = smtplib.SMTP('localhost')
            # sendmail function takes 3 arguments: sender's address, recipient's address
            # and message to send - here it is sent as one string.
            resp = s.sendmail(me, to, msg.as_string())
            s.quit() 
        except Exception,e:
            return False
        return True

    def send_email(self,to = None,subject = "Nuevo Correo",text = "Tu Nuevo correo"):
        gmail_user = 'autoemailstec@gmail.com'  
        gmail_password = 'registros'

        sent_from = gmail_user  
        to = to  
        subject = 'Su Correo Esta Listo'  
        body = 'Hola su correo esta listo: ' + str(text)

        email_text = """\  
        From: %s  
        To: %s  
        Subject: %s
        %s
        """ % (sent_from, ", ".join(to), subject, body)

        try:  
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            resp = server.sendmail(sent_from, to, email_text)
            server.close()

            return str(resp)
        except Exception,e:  
            return str(e)







if __name__ == "__main__":
	while(True):
	    # create connection
		obr = Obsr(username = "root", password = "toor",server = "localhost",database = "kenya")
		obr.dbconnection()
		rpnedings = obr.getPendings()
		print "executing " + str(len(rpnedings))
		textemail = """
			Favor de pasar al departamento de Centro de Computo despues de 
			24 horas en un horario de 9am-12pm y de 1pm-3pm" + "Llevar con sigo una copia de su credencial de Estudiante"
		"""
		for r in rpnedings:
			resp = obr.send_email(to = r[7],subject = "Tu solicitud de correo ha sido aceptada", text = textemail)
			if resp:
				obr.marcarComoCreado(r[0])	
		time.sleep(60) # se va a dormir cada 300 segundos 5 minutos

