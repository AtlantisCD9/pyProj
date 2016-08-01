import pySend
import pyGetFile

if __name__ == '__main__':
    fileName = pyGetFile.getFile()
    pySend.sendMail(fileName)
