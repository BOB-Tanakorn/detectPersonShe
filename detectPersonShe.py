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

countGroundMixer = 0
countGroundPL = 0

startGroundMixer = 12
startGroundPL = 12

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

    countGroundMixer += 1
    countGroundPL += 1
    if status == True:
        
        if countGroundMixer >= startGroundMixer:
            print('{} >>> start process location groundFloorMixer'.title().format(datetime.datetime.now()))
            os.system(pathBacthFile + '/groundFloorMixer.bat')
            time.sleep(3)
            ltGroundFloorMixer = 'groundFloorMixer'
            ltGroundFloorMixer = ltGroundFloorMixer.replace("'", "")
            statusPersonGroundMixer = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=sa; PWD=123456")
            statusPersonGroundMixer = statusPersonGroundMixer.cursor()
            statusPersonGroundMixer = statusPersonGroundMixer.execute('SELECT statusPerson FROM detectPersonShe WHERE location=?', ltGroundFloorMixer)
            statusPersonGroundMixer = statusPersonGroundMixer.fetchone()[0]
            if statusPersonGroundMixer == True:
                startGroundMixer = 60
                countGroundMixer = 0
            else:
                countGroundMixer = 0
            print('{} >>> end process location groundFloorMixer'.title().format(datetime.datetime.now()))
        
        if countGroundPL >= startGroundPL:
            print('{} >>> start process location groundFloorPL'.title().format(datetime.datetime.now()))
            os.system(pathBacthFile + '/groundFloorPL.bat')
            time.sleep(3)
            ltGroundFloorPL = 'groundFloorPL'
            ltGroundFloorPL = ltGroundFloorPL.replace("'", "")
            statusPersonGroundPL = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=sa; PWD=123456")
            statusPersonGroundPL = statusPersonGroundPL.cursor()
            statusPersonGroundPL = statusPersonGroundPL.execute('SELECT statusPerson FROM detectPersonShe WHERE location=?', ltGroundFloorPL)
            statusPersonGroundPL = statusPersonGroundPL.fetchone()[0]
            if statusPersonGroundPL == True:
                startGroundPL = 60
                countGroundPL = 0
            else:
                countGroundPL = 0
            print('{} >>> end process location groundFloorPL'.title().format(datetime.datetime.now()))

    time.sleep(10)
    # time.sleep(5)