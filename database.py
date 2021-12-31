from typing import final
import mysql.connector
import hashlib
from datetime import date, datetime


def connectDb():
    """
    Function used to connecto to database
    """
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database='weconnect'
    )
    # mydb = mysql.connector.connect(
    #     host="WeConnect.mysql.pythonanywhere-services.com",
    #     user="WeConnect",
    #     password="Shokugeki2021!",
    #     database='WeConnect$weconnect'
    # )
    print("Connect")
    return mydb


def getAll(table):
    """
    Get All positions Used for displayingg the list of positions on registration forms
    """
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        mycursor.callproc("SelectAllPostions")
        results = list
        for result in mycursor.stored_results():
            results = result.fetchall()
        return results
    finally:
        mydb.close()
        print('test')


def registerNewUser(email,  password, repeatPass, firstname, lastname, phoneNumber, position):
    """
    Cretes a new user
    """
    try:
        mydb = connectDb()
        # Check if Password are the same
        if(password != repeatPass):
            return("Password not The Same")
        # Hashing
        password = bytes(password, encoding='utf-8')
        hash_object = hashlib.sha256(str(password).encode('utf-8'))
        hex_dig = hash_object.hexdigest()
        try:
            mycursor = mydb.cursor()
            args = (email, hex_dig, firstname,
                    lastname, phoneNumber, position, )
            mycursor.callproc('addUser', args)
            mydb.commit()
            return "Success"
        except Exception as e:
            if "Duplicate entry" in str(e):
                return ("Duplicate error")
    finally:
        mydb.close()


def updateUserDB(id, email, firstName, lastName, phoneNumber, position):
    """
    Update User Details
    """
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (email, firstName, lastName, phoneNumber, position, id, )
        mycursor.callproc("updateUser", val)
        mydb.commit()
        if mycursor.rowcount > 0:
            return True

        return False
    finally:
        mydb.close()


def deleteUserDB(id):
    """
    Delete a User on Database
    """
    try:
        mydb = connectDb()
        print(id)
        mycursor = mydb.cursor()
        mycursor.callproc("deleteUser", (id, ))
        mydb.commit()

        return "Delete"
    finally:
        mydb.close()


def loginDB(email, password):
    try:
        mydb = connectDb()
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

    finally:
        mydb.close()


def getUserData(id):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id,)
        mycursor.callproc("selectUserID", val)
        results = list
        for result in mycursor.stored_results():
            results = result.fetchall()
        mycursor.close()
        return results
    finally:
        mydb.close()

def getTeachers(id):
    try:
        mydb = connectDb()
        results = list
        mycursor = mydb.cursor()
        mycursor.callproc("getTeachers")
        for result in mycursor.stored_results():
            results = result.fetchall()
        return results
    finally:
        mydb.close()

def updateTaskStatus(status,taskID):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (status, taskID)
        mycursor.callproc("updateTaskStatus", val)
        mydb.commit()
        if mycursor.rowcount > 0:
            return True
        return False
    finally:
        mydb.close()


def getAllUsers():
    try:
        mydb = connectDb()
        results = list
        mycursor = mydb.cursor()
        mycursor.callproc("SelectAllUsers")
        for result in mycursor.stored_results():
            results = result.fetchall()
        return results
    finally:
        mydb.close()
        print('test')


def getPosition(positionID):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (positionID,)
        results = list
        mycursor.callproc("selectPositionID", val)
        for result in mycursor.stored_results():
            results = result.fetchall()
        return results
    finally:
        mydb.close()


def newPosition(position):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (position,)
        mycursor.callproc('addPosition', val)
        mydb.commit()
        return True
    except:
        mycursor.close()
        return False
    finally:
        mydb.close()


def saveFiletoDb(filename, filetype, filesize, file_content_type, uploaded_by, share_to_user, share_to_group, deadline, revision,taskID,FilePathName):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        today = datetime.now()
        val = (filename, filetype, filesize, file_content_type, uploaded_by,
               share_to_user, share_to_group, deadline, revision, today,taskID,FilePathName)
        mycursor.callproc('saveFile', val)
        mycursor.lastrowid
        mydb.commit()
        for result in mycursor.stored_results():
            results = result.fetchall()
            return (results)
    except Exception as e:
        mycursor.close()
        print(e)
        return False
    finally:
        mydb.close()


def getFileDb(positionID):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (positionID,)
        results = list
        mycursor.callproc("getFile", val)
        for result in mycursor.stored_results():
            results = result.fetchall()
        return results
    finally:
        mydb.close()


def updateDocDB(id, data):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (data, id)
        mycursor.callproc("updateDOC", val)
        mydb.commit()
        if mycursor.rowcount > 0:
            return True

        return False
    finally:
        mydb.close()


def moveFileToThrash(fileid):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (fileid,)
        mycursor.callproc("moveFileToThrash", val)
        mydb.commit()
        if mycursor.rowcount > 0:
            return True

        return False

    finally:
        mydb.close()


def getNumberOfFilesUploaded(id):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id,)
        results = list
        mycursor.callproc("getNumberOfFilesUploaded", val)
        resultsArray = []
        for result in mycursor.stored_results():
            results = result.fetchall()
            # print(results)
            # resultsArray.append(results)

        # print(len(results))
        return results
    finally:
        mydb.close()


def getNumberOfFilesPassed(id):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id,)
        results = list
        mycursor.callproc("getNumberOfFilesPassed", val)
        for result in mycursor.stored_results():
            results = result.fetchall()
            # print(results)
            # resultsArray.append(results)

        # print(len(results))
        return results
    finally:
        mydb.close()


def getNumberOfFilesDeadline(id):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id,)
        results = list
        mycursor.callproc("number_of_files_deadline", val)
        for result in mycursor.stored_results():
            results = result.fetchall()
            # print(results)
            # resultsArray.append(results)

        # print(len(results))
        return results
    finally:
        mydb.close()


def getNumberOfFilesNearDeadline(id):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id,)
        results = list
        mycursor.callproc("number_of_files_nearing_Deadline", val)
        for result in mycursor.stored_results():
            results = result.fetchall()
            # print(results)
            # resultsArray.append(results)

        # print(len(results))
        return results
    finally:
        mydb.close()


def getNFiles(id, number):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id, number,)
        results = list
        mycursor.callproc("getNFiles", val)
        for result in mycursor.stored_results():
            results = result.fetchall()
            # print(results)
            # resultsArray.append(results)

        # print(len(results))
        return results
    finally:
        mydb.close()


def getAllFilesUser(id):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id,)
        results = list
        mycursor.callproc("getAllFiles", val)
        for result in mycursor.stored_results():
            results = result.fetchall()
            # print(results)
            # resultsArray.append(results)

        # print(len(results))
        return results
    finally:
        mydb.close()


def restoreFileDB(id):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id,)
        mycursor.callproc("Restore", val)
        mydb.commit()
        if mycursor.rowcount > 0:
            return True

        return False

    finally:
        mydb.close()


def emptyTrashDb(id):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id,)
        mycursor.callproc("emptyTrash", val)
        mydb.commit()
        if mycursor.rowcount > 0:
            return True

        return False

    finally:
        mydb.close()


def setStatusPinned(id, status):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id, status)
        mycursor.callproc("SetPinned", val)
        mydb.commit()
        if mycursor.rowcount > 0:
            return True

        return False

    finally:
        mydb.close()


def getAllFilesForAdmin():
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        # val = (id,)
        results = list
        mycursor.callproc("getAllFilesForAdmin")
        for result in mycursor.stored_results():
            results = result.fetchall()
            # print(results)
            # resultsArray.append(results)

        # print(len(results))
        return results
    finally:
        mydb.close()


def deleteFileDB(id):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id,)
        mycursor.callproc("deleteFile", val)
        mydb.commit()
        if mycursor.rowcount > 0:
            return True

        return False

    finally:
        mydb.close()
    
def addTask(taskName,taskImage, taskCreatedBy, taskDeadline, taskDescription,schedule):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor(buffered=True)
        today = datetime.now()
        status = 'Pending Teachers'
        val = (taskName,taskCreatedBy,today, taskDeadline, taskDescription,status ,schedule)
        mycursor.callproc('AddTask', val)
        mycursor.lastrowid
        mydb.commit()
        for result in mycursor.stored_results():
            results = result.fetchall()
        return ("ok")
    except Exception as e:
        mycursor.close()
        print(e)
        return False
    finally:
        mydb.close()

def getAllTask():
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        # val = (id,)
        results = list
        mycursor.callproc("SelectAllTask")
        for result in mycursor.stored_results():
            results = result.fetchall()
            # print(results)
            # resultsArray.append(results)
        # print(len(results))
        return results
    finally:
        mydb.close()

def getOneTask(id):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (id,)
        results = list
        mycursor.callproc("SelectOneTask", val)
        for result in mycursor.stored_results():
            results = result.fetchall()
        return results
    finally:
        mydb.close()

def checkIfUserUploadedDB(userID, taskID):
    try:
        mydb = connectDb()
        mycursor = mydb.cursor()
        val = (userID,taskID,)
        results = list
        mycursor.callproc("checkUserUpload", val)
        for result in mycursor.stored_results():
            results = result.fetchall()
        return results
    finally:
        mydb.close()



# ==========================================
# TESTING FUNCTIONS


# def hashtest(password, password2):
#     hash_object = hashlib.sha256(password)
#     hex_dig = hash_object.hexdigest()

#     a = hashlib.sha1(password2)
#     ahex = a.hexdigest()

#     print(ahex == hex_dig)


# hashtest(b'pass1', b'pass1')


# def getusers():
#     mydb = connectDb()
#     mycursor = mydb.cursor()
#     mycursor.callproc("selectUser", ['admin@gmail.com', ])
#     for result in mycursor.stored_results():
#         result = (result.fetchall())

#     print(result)


# print(registerNewUser('test3','test1','test1','test1','test','test',1))
# print(getusers())
# print(deleteUserDB(85))
# print(newPosition('test'))