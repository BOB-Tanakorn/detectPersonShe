Set oShell = CreateObject ("Wscript.Shell")
Dim strCMD
strCMD = "cmd cd /c C:\Users\PTF\she_objectdetection\com_vision_she.bat"
oShell.Run strCMD, 0, false