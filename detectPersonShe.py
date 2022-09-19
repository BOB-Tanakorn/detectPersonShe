import time
import pyodbc
import datetime
import os

pathBacthFile = os.getcwd().replace('\\', '/')

cursor = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=comVision; PWD=123456")

locationMixer =  'groundFloorMixer'
locationMixer = locationMixer.replace("'", "")
cursorMixer = cursor.cursor()
cursorstart = cursorMixer.execute('UPDATE statusPrograms SET status=? WHERE programs=?',(False, locationMixer))
cursorstart.commit()

locationPL = 'groundFloorPL'
locationPL = locationPL.replace("'", "")
cursorPL = cursor.cursor()
cursorPL = cursorPL.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (False, locationPL))
cursorPL.commit()

countGroundMixer = 0
countGroundPL = 0

startGroundMixer = 12
startGroundPL = 12

while True:
    countGroundMixer += 1
    countGroundPL += 1

    if countGroundMixer >= startGroundMixer:
        runGroundMixer = True
        while runGroundMixer:
            timeLoopMixer = 5
            #connect database
            connectRunPrograms = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=comVision; PWD=123456")
            cursorPrograms = connectRunPrograms.cursor()
            runGoundMixer = connectRunPrograms.cursor()
            sqlCmdSelect = 'SELECT status FROM statusPrograms'
            cursorPrograms.execute(sqlCmdSelect)
            cursorPrograms = cursorPrograms.fetchall()
            
            ltMixer = []
            for iGroundMixer in cursorPrograms:
                ltMixer.append(iGroundMixer[0])

            if True in ltMixer:
                statusGrounsMixer = False
            else:
                statusGrounsMixer = True
                timeLoopMixer = 1
                break
            time.sleep(timeLoopMixer)

        if statusGrounsMixer == True:
            programsName = 'groundFloorMixer'
            programsName = programsName.replace("'", "")
            runGoundMixer = runGoundMixer.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (True, programsName))
            runGoundMixer.commit()
            print('{} >>> start process location groundFloorMixer'.title().format(datetime.datetime.now()))
            os.system(pathBacthFile + '/groundFloorMixer.bat')
            time.sleep(3)
            ltGroundFloorMixer = 'groundFloorMixer'
            ltGroundFloorMixer = ltGroundFloorMixer.replace("'", "")
            statusPersonGroundMixer = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=comVision; PWD=123456")
            statusPersonGroundMixer = statusPersonGroundMixer.cursor()
            statusPersonGroundMixer = statusPersonGroundMixer.execute('SELECT statusPerson FROM detectPersonShe WHERE location=?', ltGroundFloorMixer)
            statusPersonGroundMixer = statusPersonGroundMixer.fetchone()[0]
            if statusPersonGroundMixer == True:
                startGroundMixer = 600
                countGroundMixer = 0
                timeDelay = 1
            else:
                startGroundMixer = 120
                countGroundMixer = 0

            print('{} >>> end process location groundFloorMixer'.title().format(datetime.datetime.now()))
            runGoundMixer = runGoundMixer.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (False, programsName))
            runGoundMixer.commit()
            runGroundMixer = False
      
    if countGroundPL >= startGroundPL:
        runGroundPL = True
        while runGroundPL:
            timeLoopPL = 5
            #connect database
            connectGroundPL = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=comVision; PWD=123456")
            cursorGroundPL = connectGroundPL.cursor()
            runGroundPL = connectGroundPL.cursor()
            cmdGroundPL = 'SELECT status FROM statusPrograms'
            cursorGroundPL.execute(cmdGroundPL)
            cursorGroundPL = cursorGroundPL.fetchall()

            ltPL = []
            for iGroundPL in cursorGroundPL:
                ltPL.append(iGroundPL[0])

            if True in ltPL:
                statusGroundPL = False
            else:
                statusGroundPL = True
                timeLoopPL = 1
                break
            time.sleep(timeLoopPL)

        if statusGroundPL == True:
            programsName = 'groundFloorPL'
            programsName = programsName.replace("'", "")
            runGroundPL = runGroundPL.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (True, programsName))
            runGroundPL.commit()

            print('{} >>> start process location groundFloorPL'.title().format(datetime.datetime.now()))
            os.system(pathBacthFile + '/groundFloorPL.bat')
            time.sleep(3)
            ltGroundFloorPL = 'groundFloorPL'
            ltGroundFloorPL = ltGroundFloorPL.replace("'", "")
            statusPersonGroundPL = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server}; SERVER=localhost; DATABASE=projectComputerVision; UID=comVision; PWD=123456")
            statusPersonGroundPL = statusPersonGroundPL.cursor()
            statusPersonGroundPL = statusPersonGroundPL.execute('SELECT statusPerson FROM detectPersonShe WHERE location=?', ltGroundFloorPL)
            statusPersonGroundPL = statusPersonGroundPL.fetchone()[0]
            if statusPersonGroundPL == True:
                startGroundPL = 600
                countGroundPL = 0
            else:
                startGroundPL = 120
                countGroundPL = 0
                
            print('{} >>> end process location groundFloorPL'.title().format(datetime.datetime.now()))
            runGroundPL = runGroundPL.execute('UPDATE statusPrograms SET status=? WHERE programs=?', (False, programsName))
            runGroundPL.commit()
            runGroundPL = False

    time.sleep(1)
    # time.sleep(5)