import sys, os
    
melFiles = []

for path in sys.path:
    
    path = path.replace( '\\', '/' )
    
    if not os.path.isdir( path ):
        continue
    dirList = os.listdir( path )
    
    if 'basic' in dirList and '_3dGroupTools' in dirList:
        melFiles.append( path+'/basic/skinCluster/ui/setInfluenceSelected.mel' )