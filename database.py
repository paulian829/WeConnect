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
    mycursor.callproc("SelectAllPostions")
    for result in mycursor.stored_results():
        return (result.fetchall())


def registerNewUser(email,  password, repeatPass, firstname, lastname, phoneNumber, position):
    # Check if Password are the same
    if(password != repeatPass):
        return("Password not The Same")
    # Hashing
    password = bytes(password, encoding='utf-8')
    hash_object = hashlib.sha256(str(password).encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    try:
        mycursor = mydb.cursor()
        args = (email, hex_dig, firstname, lastname, phoneNumber, position, )
        mycursor.callproc('addUser', args)
        mydb.commit()
        return "Success"
    except Exception as e:
        if "Duplicate entry" in str(e):
            return ("Duplicate error")


def updateUserDB(id, email, firstName, lastName, phoneNumber, position):
    mycursor = mydb.cursor()
    val = (email, firstName, lastName, phoneNumber, position, id, )
    mycursor.callproc("updateUser", val)
    mydb.commit()
    if mycursor.rowcount > 0:
        return True
    return False


def deleteUserDB(id):
    print(id)
    mycursor = mydb.cursor()
    mycursor.callproc("deleteUser", (id, ))
    mydb.commit()
    return "Delete"


def loginDB(email, password):
    # check if Username Exists
    mycursor = mydb.cursor()
    val = (email,)
    mycursor.callproc("SelectUserEmail", val)
    for result in mycursor.stored_results():
        myresult = (result.fetchall())
    if(len(myresult) == 0):

        return "Error"
    realPassword = myresult[0][2]
    # Compare Password
    typedpassword = bytes(password, encoding='utf-8')
    hash_object = hashlib.sha256(str(typedpassword).encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    print(realPassword, hex_dig)
    if(realPassword == hex_dig):
        print(myresult)
        return myresult

    print("Not Equal")
    return "Error"


def getUserData(id):
    mycursor = mydb.cursor()
    val = (id,)
    mycursor.callproc("selectUserID", val)
    for result in mycursor.stored_results():
        return (result.fetchall())


def getAllUsers():
    mycursor = mydb.cursor()
    mycursor.callproc("SelectAllUsers")
    for result in mycursor.stored_results():
        return (result.fetchall())


def getPosition(positionID):
    mycursor = mydb.cursor()
    val = (positionID,)
    mycursor.callproc("selectPositionID", val)
    for result in mycursor.stored_results():
        return (result.fetchall())


def newPosition(position):
    try:
      mycursor = mydb.cursor()
      val = (position,)
      mycursor.callproc('addPosition', val)
      mydb.commit()
      return True
    except:
      return False

    

    

# ==========================================
# TESTING FUNCTIONS
def hashtest(password, password2):
    hash_object = hashlib.sha256(password)
    hex_dig = hash_object.hexdigest()

    a = hashlib.sha1(password2)
    ahex = a.hexdigest()

    print(ahex == hex_dig)


hashtest(b'pass1', b'pass1')


def getusers():
    mycursor = mydb.cursor()
    mycursor.callproc("selectUser", ['admin@gmail.com', ])
    for result in mycursor.stored_results():
        result = (result.fetchall())

    print(result)


# print(registerNewUser('test3','test1','test1','test1','test','test',1))
# print(getusers())
# print(deleteUserDB(85))
# print(newPosition('test'))
