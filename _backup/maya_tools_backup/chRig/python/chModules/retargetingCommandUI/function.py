import os, glob

def getNewCPoseName( path ):
    
    largeNum = 0
    for root, dirs, names in os.walk( path ):
        for name in names:
            if len( name ) < 11: continue
            digitPart = name[4:-6]
            if digitPart.isdigit():
                if largeNum < int( digitPart ):
                    largeNum = int( digitPart )
        break
    
    return "pose%d.cpose" % ( largeNum +1 )


def getNewCAnimName( path ):
    
    largeNum = 0
    for root, dirs, names in os.walk( path ):
        for name in dirs:
            if len( name ) < 11: continue
            digitPart = name[4:-6]
            if digitPart.isdigit():
                if largeNum < int( digitPart ):
                    largeNum = int( digitPart )
        break
    
    return "anim%d.canim" % ( largeNum +1 )