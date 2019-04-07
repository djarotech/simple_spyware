# CS361 Spyware project

1. Development done in python3, so install python3
2. install pip3 for dependencies
3. `pip3 install -r requirements.txt`
4. run with parameters. `python3 main.py -h`

## S3 support
1. To run using s3, please set ACCESS_KEY_ID and ACCESS_SECRET_KEY environmental variables
    to whatever credentials you generated on AWS
```
export ACCESS_KEY_ID=AWEUFDADSJHDGJAS <- replace this
export ACCESS_SECRET_KEY=FARUEWRJEWHRJEQFIQEWJFWJQE@#$@#! <- replace this
```
2. install aws-cli
3. now run `aws configure`
4. enter your access keys

5. make a bucket
`aws s3 mb s3://cs361p-spyware`

6. run `python3 main.py --s3_bucket cs361p-spyware`

7. cleanup bucket
`aws s3 rb s3://cs361p-spyware --force`

## IDEAS to work on
1. someone figure out how to run this script upon computer restart and login.
2. Keylogging feature. I was thinking after 10 seconds of no typing, make
a new line in the file
Note: we need to have the datetime at the beginning of each line in
the keylogger file.
