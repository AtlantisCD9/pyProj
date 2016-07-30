import os

def deleteNullDir(dirEntry):  
    if os.path.isdir(dirEntry):  
        for subDir in os.listdir(dirEntry):
            subDirEntry = os.path.join(dirEntry,subDir)
            if (os.path.isdir(subDirEntry) == True):  
                deleteNullDir(subDirEntry)  
    if not os.listdir(dirEntry):  
        #os.rmdir(dirEntry)  
        print 'Deleted Dir: ', dirEntry  


if __name__ == '__main__':
    dirEntry = os.path.abspath('/home/atlantis/Documents/PhoneTest/Android')
    print dirEntry
    deleteNullDir(dirEntry)
