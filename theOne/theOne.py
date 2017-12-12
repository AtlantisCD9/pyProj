import os
import hashlib
import sqlite3


ENTRY = "./"

BUFF_SIZE = 10240


def main(conn):
	c = conn.cursor()
	for root, dirs, files in os.walk(ENTRY):
		for file in files:
			fullPathName = os.path.join(root, file)
			if os.path.islink(fullPathName):
				continue

			#print fullPathName
			md5 = getFileMd5(fullPathName)

			fullPathName = fullPathName.replace("'", "''")
			sqlStr = "INSERT INTO file_md5 (md5, path_name) VALUES ('{0}', '{1}')"

			c.execute(sqlStr.format(md5, fullPathName))
		conn.commit()


def getFileMd5(fileName):
	fd=open(fileName,'rb')
	#md5=hashlib.md5(fd.read()).hexdigest()
	m = hashlib.md5()

	BUFF = fd.read(BUFF_SIZE)
	while BUFF:
		m.update(BUFF)
		BUFF = fd.read(BUFF_SIZE)

	fd.close()
	md5 = m.hexdigest()

	return md5


def openDB():
	conn = sqlite3.connect('myDB.db3')
	return conn

def closeDB(conn):
	# We can also close the connection if we are done with it.
	# Just be sure any changes have been committed or they will be lost.
	conn.close()


def initDB(conn):
	c = conn.cursor()

	# DROP TABLE
	c.execute('DROP TABLE IF EXISTS file_md5')

	# Create table
	c.execute('CREATE TABLE file_md5(md5 string, path_name string)')

	# Save (commit) the changes
	conn.commit()


if __name__ == "__main__":
	conn = openDB()
	initDB(conn)
	main(conn)
	closeDB(conn)
