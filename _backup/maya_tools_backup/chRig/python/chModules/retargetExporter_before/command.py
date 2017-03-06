import os

import mainInfo


def getFiles( targetExtList, fileName = '' ):
    
    motionFiles = []
    
    for root, dirs, files in os.walk( mainInfo.motionExportPath ):
        for eachFile in files:
            joinName = os.path.join( root, eachFile )
            ext = os.path.splitext( joinName )[-1]
            
            onlyName = eachFile.replace( ext, '' ).replace( '.', '' )
            
            if ext in targetExtList and onlyName.find( fileName ) != -1:
                motionFiles.append( joinName )
    
    return motionFiles