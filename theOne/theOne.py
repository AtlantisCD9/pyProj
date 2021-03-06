import os
import hashlib
import sqlite3
import time


ENTRY = "./"
BUFF_SIZE = 10240
DB_NAME = "myDB.db3"
#DB_NAME = ":memory:"


def main(conn):
	c = conn.cursor()
	dirPath = os.path.abspath(ENTRY)
	for root, dirs, files in os.walk(dirPath):
		for file in files:
			fullPathName = os.path.join(root, file)
			if os.path.islink(fullPathName):
				continue

			#print fullPathName
			md5 = getFileMd5(fullPathName)
			print md5

			fullPathName = fullPathName.replace("'", "''")
			sqlStr = "INSERT INTO file_md5 (md5, path_name) VALUES ('{0}', '{1}')"

			c.execute(sqlStr.format(md5, fullPathName))
		print 'commit'
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
	conn = sqlite3.connect(DB_NAME)
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

def dumpFile(conn):
	fd=open("dumpFile",'wb')

	c = conn.cursor()

	sqlStr ='''SELECT md5, path_name FROM file_md5 WHERE md5 IN(
	SELECT md5 FROM file_md5 GROUP BY md5 HAVING COUNT(*) > 1
	) ORDER BY md5, path_name'''

	for row in c.execute(sqlStr):
		content = ' rm "'.join(row)
		content += '"'
		fd.write(content.encode('utf-8'))
		fd.write("\n")

def dumpFileFilter(conn):
	fd=open("dumpFileFilter",'wb')

	c = conn.cursor()

	sqlStr ='''SELECT md5, path_name FROM file_md5 WHERE md5 IN(
	SELECT md5 FROM file_md5 GROUP BY md5 HAVING COUNT(*) > 1
	) ORDER BY md5, path_name'''

	tmp = ""
	for row in c.execute(sqlStr):
		if row[0] == tmp:
			content = 'rm "' + row[1] + '"'
			fd.write(content.encode('utf-8'))
			fd.write("\n")
		else:
			tmp = row[0]
			continue

if __name__ == "__main__":
	start = time.clock()
	conn = openDB()
	initDB(conn)
	main(conn)
	dumpFile(conn)
	dumpFileFilter(conn)
	closeDB(conn)
	elapsed = (time.clock() - start)
	print elapsed, 's'
