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
def getAll(table):
  mycursor = mydb.cursor()
  sql = "SELECT * FROM position"
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  print(myresult)
  return myresult


def registerNewUser(username,email,  password, repeatPass, name, phoneNumber, position):
  #Check if Password are the same
  if(password != repeatPass):
    return("Password not The Same")
  #Hashing
  password = bytes(password, encoding= 'utf-8')
  hash_object = hashlib.sha1(str(password).encode('utf-8'))
  hex_dig = hash_object.hexdigest()
  try:
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (Username,Email, Password, Name, PhoneNumber, Position) VALUES ('%s','%s','%s','%s','%s','%s')"
    val = (username, email, hex_dig, name, phoneNumber, position)
    print(val)
    mycursor.execute(sql % (val))
    print(mycursor.rowcount, "Records Added")
    mydb.commit()
    return "Success"
  except Exception as e:
    if "Duplicate entry" in str(e):
      return ("Duplicate error")


def loginDB(username, password):
  #check if Username Exists
  mycursor = mydb.cursor()
  sql = "SELECT * FROM users WHERE username = '%s'"
  val = (username)
  mycursor.execute(sql % (val))
  myresult = mycursor.fetchall()
  if(len(myresult)== 0):
    return "Error"
  realPassword = myresult[0][3]
  #Compare Password
  typedpassword = bytes(password, encoding= 'utf-8')
  hash_object = hashlib.sha1(str(typedpassword).encode('utf-8'))
  hex_dig = hash_object.hexdigest()

  if(realPassword == hex_dig):
    print(myresult)
    return myresult
  
  return "Error"


def getUserData(id):
  mycursor = mydb.cursor()
  sql = "SELECT * FROM users WHERE id = '%s'"
  val = (id)
  mycursor.execute(sql % (val))
  myresult = mycursor.fetchall()
  return myresult

def getPosition(positionID):
  mycursor = mydb.cursor()
  sql = "SELECT * FROM position WHERE id ='%s'"
  val = (positionID)
  print(sql % (val))
  mycursor.execute(sql % (val))
  myresult = mycursor.fetchone()
  return myresult[1]


def newPosition(position):
  mycursor = mydb.cursor()
  sql = "INSERT INTO position (position_name) VALUES ('%s')"
  val = (position)
  print(sql % (val))
  mycursor.execute(sql % (val))
  mydb.commit()
  print(mycursor.rowcount, "record inserted.")


def hashtest(password, password2):
  hash_object = hashlib.sha256(password)
  hex_dig = hash_object.hexdigest()

  a = hashlib.sha1(password2)
  ahex = a.hexdigest()
  
  print (ahex == hex_dig)

hashtest(b'pass1',b'pass1')
  
