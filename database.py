import mysql.connector

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

#newPosition('Principal')