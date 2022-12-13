import smtplib, psycopg2, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from exchangelib import Credentials, Account, Folder





mylogin = "your login"
passwd = "your password"

##---------------------------------------------------------CONNECTING TO OUR POSTGRES DATABASE---------------------------------------------------------------------##

myhost = 'it relays on you'
conn = psycopg2.connect(
  host = myhost,
  database='your DB',
  user='name of the user',
  password='your password')

##----------------------------------------------------CREATING A CURSOR IN ORDER TO HANDLE OUR DATABASE------------------------------------------------------------##
  
cur = conn.cursor()

##--------------------------------------------------------CREATING A FUNCTION IN ORDER TO SEND MAILS---------------------------------------------------------------##

def sending_mail():
  server = smtplib.SMTP("smtp.'your domain name", 587)
  message = MIMEMultipart()
  message["from"] = "mail of the sender"
  message["to"] = "mail of the recipient"
  message["subject"] = "the subject of the mail"
  message.attach(MIMEText("the body of the mail"))
  server.ehlo()
  server.starttls()
  server.login(mylogin, passwd)
  print("login sucess")
  server.send_message(message)
  print("Email has been sent to", message["to"])
  server.close()

##------------------------------------------------------  CONNECTING TO OUR MAIL ACCOUNT BY USING EXCHANGELIB------------------------------------------------------##

credentials = Credentials(mylogin, passwd)
account = Account('your mail', credentials=credentials, autodiscover=True)

##-------------------------------------------------------------------------CREATING TABLE--------------------------------------------------------------------------##

def creating_table():
  cur.execute('DROP TABLE IF EXISTS Code_n;')   
  cur.execute('CREATE TABLE tables_name (id serial PRIMARY KEY,'
  'code varchar (255),'
  'NOM varchar (255) ,'
  'ADRESSE varchar (255) ,'
  '...'
  'DATE__HEURE varchar(255),'
  'PATH varchar(255));'
)

##------------------------------------------------------------------SETTING AND PULLING DATAS IN THE DB------------------------------------------------------------##

def preparing_and_pulling_datas_in_the_DB():
  for item in account.inbox.all():
    if item.subject.startswith("whatever you want"):
      sep = item.subject.split("_") 
      name_sender = item.sender.name
      date_and_time = item.datetime_received
      mail_sender = item.sender.email_address
      my_path = r'C:\folder\another_folder'
      fpath = os.path.join(my_path, item.subject)
      with open(fpath, 'w') as f:
        f.write(str(item.body))
    # pulling data in the DB
      cur.execute('INSERT INTO tables_name (code, nom, adresse, date__heure, path) VALUES (%s,%s,%s,%s,%s)',(sep[1], name_sender, mail_sender, date_and_time, fpath)) 
      return item

##-----------------------------------------------------------------MOVING MAILS TO ANOTHER FOLDER------------------------------------------------------------------##

def moving_mails_to_our_folder():
  # let's creat a folder in our account 
  myf = Folder(parent = account.inbox, name = "your new folder's name")
### myf.save()
  to_folder = account.inbox / 'your new folder\'s name'
 # Moving mails to myfolder 'Mail_read'
  for item in account.inbox.all():
    if item.subject.startswith("what you chose above"):
      item.move(to_folder)
  return item  


##------------------------------------------------------------------------CALLS OF FUNCTIONS-----------------------------------------------------------------------##

# sending_mail()
### creating_table()

preparing_and_pulling_datas_in_the_DB()
moving_mails_to_our_folder()

##-------------------------IF WE WANT TO UPDATE(PULL NEW DATAS IN THE DB),JUST UNCOMMENT,EXECUTE THE PROGRAM, AND COMMENT AGAIN FOLLOWING LINES--------------------##

# conn.commit()
# conn.close()


