import pyReceive
import pySend
import pyGetFile
import time

if __name__ == '__main__':
    loopFLag = True

    while loopFLag:
        subject = pyReceive.receiveMail()
        print subject
        if 'takePhoto' == subject:
            fileName = pyGetFile.getFile()
            pySend.sendMail(fileName)
        time.sleep(10)

    exit(0)

