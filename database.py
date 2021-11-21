import mysql.connector
import hashlib


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='weconnect'
)

mydb = mysql.connector.connect(
    host="WeConnect.mysql.pythonanywhere-services.com",
    user="WeConnect",
    password="Shokugeki2021!",
    database='WeConnect$weconnect'
)


def getAll(table):
    mycursor = mydb.cursor()
    mycursor.callproc("SelectAllPostions")
    results = list
    for result in mycursor.stored_results():
        results = result.fetchall()
    mycursor.close()
    return results


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
        mycursor.close()
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
        mycursor.close()
        return True

    mycursor.close()
    return False


def deleteUserDB(id):
    print(id)
    mycursor = mydb.cursor()
    mycursor.callproc("deleteUser", (id, ))
    mydb.commit()
    mycursor.close()
    return "Delete"


def loginDB(email, password):
    # check if Username Exists
    mycursor = mydb.cursor()
    val = (email,)
    mycursor.callproc("SelectUserEmail", val)
    for result in mycursor.stored_results():
        myresult = (result.fetchall())
    if(len(myresult) == 0):
        mycursor.close()
        return "Error"
    realPassword = myresult[0][2]
    # Compare Password
    typedpassword = bytes(password, encoding='utf-8')
    hash_object = hashlib.sha256(str(typedpassword).encode('utf-8'))
    hex_dig = hash_object.hexdigest()
    print(realPassword, hex_dig)
    if(realPassword == hex_dig):
        print(myresult)
        mycursor.close()
        return myresult

    print("Not Equal")
    mycursor.close()
    return "Error"


def getUserData(id):
    mycursor = mydb.cursor()
    val = (id,)
    mycursor.callproc("selectUserID", val)
    results = list
    for result in mycursor.stored_results():
        results = result.fetchall()
    mycursor.close()
    return results
        


def getAllUsers():
    results = list
    mycursor = mydb.cursor()
    mycursor.callproc("SelectAllUsers")
    for result in mycursor.stored_results():
        results = result.fetchall()
    
    mycursor.close()
    return results

def getPosition(positionID):
    mycursor = mydb.cursor()
    val = (positionID,)
    results = list
    mycursor.callproc("selectPositionID", val)
    for result in mycursor.stored_results():
        results = result.fetchall()
    mycursor.close()
    return results

def newPosition(position):
    try:
      mycursor = mydb.cursor()
      val = (position,)
      mycursor.callproc('addPosition', val)
      mydb.commit()
      mycursor.close()
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
