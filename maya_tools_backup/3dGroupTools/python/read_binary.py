filePath = "X:/Temp/skkim/sceneBakeTest/key/group1.sgKeyData"


f = open( filePath, 'r' )

bytes_read = open(filePath, "rb").read()
for b in bytes_read:
    print b
    break
    
f.close()