import mysql.connector
import hashlib


# mydb = mysql.connector.connect(
#   host="paulian829.mysql.pythonanywhere-services.com",
#   user="paulian829",
#   password="Shokugeki2021!",
#   database='paulian829$weconnect'
# )

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database='weconnect'
)



def registerNewUser(email):
  print(email)
  mycursor = mydb.cursor()
  sql = "INSERT INTO users (Email, Password, Name, PhoneNumber, Position) VALUES ('%s')"
  val = ("'John'")
  mycursor.execute(sql % (email))
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")

def newPosition(position):
  mycursor = mydb.cursor()
  sql = "INSERT INTO position (position_name) VALUES ('%s')"
  val = (position)
  print(sql % (val))
  mycursor.execute(sql % (val))
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")


def hashtest(password, password2):
  hash_object = hashlib.sha1(password)
  hex_dig = hash_object.hexdigest()
  print(hex_dig)

  a = hashlib.sha1(password2)
  ahex = hash_object.hexdigest()
  
  print (ahex == hex_dig)
  



vartest = b'password'
varb = b'password'
hashtest(vartest,varb)