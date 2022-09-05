import time
import pyodbc
import datetime
import os

pathBacthFile = os.getcwd().replace('\\', '/')

cursorUpdate = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=sa; PWD=123456")
cursorUpdate = cursorUpdate.cursor()

# sqlCmdUpdate = 'UPDATE checkProgramsRun SET namePrograms = detectPersonShe WHERE id=1'

# value = 'detectPersonNew'
# cursorUpdate = cursorUpdate.execute('UPDATE checkProgramsRun SET namePrograms = ? WHERE id=1', value)
# cursorUpdate.commit()

while True:
    #connect database
    connectRunPrograms = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=sa; PWD=123456")
    cursorPrograms = connectRunPrograms.cursor()
    sqlCmdSelect = 'SELECT status FROM statusPrograms'
    cursorPrograms.execute(sqlCmdSelect)
    cursorPrograms = cursorPrograms.fetchall()
    for i in cursorPrograms:
        if i[0] == True:
            status = False
            break
        else:
            status = True

    if status == True:
        print('{} >>> ready'.format(datetime.datetime.now()))
        os.system(pathBacthFile + '/groundFloorMixer.bat')
        os.system(pathBacthFile + '/groundFloorPL.bat')
        timeDelay = 600
    else:
        print('{} >>> notReady'.format(datetime.datetime.now()))
        timeDelay = 120

    # time.sleep(timeDelay)
    # time.sleep(5)