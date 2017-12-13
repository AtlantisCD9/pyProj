import os
import hashlib
import sqlite3
import time

ENTRY = "./"
BUFF_SIZE = 10240
DB_NAME = "myDB.db3"
#DB_NAME = ":memory:"

def main():
	dirPath = os.path.abspath(ENTRY)
	for root, dirs, files in os.walk(dirPath):
		for file in files:
			fullPathName = os.path.join(root, file)
			if os.path.islink(fullPathName):
				continue

			cmdStr = "mv \"{0}\" \"{1}\"".format(fullPathName, dirPath)
			os.system(cmdStr)
			print cmdStr

if __name__ == "__main__":
	start = time.clock()
	main()
	elapsed = (time.clock() - start)
	print elapsed, 's'
