import maya.cmds as cmds

try:
    sels = cmds.ls( sl=1 )
    posList = []
    
    for sel in sels:
        selShapes = cmds.listRelatives( sel, s=1, f=1 )
    
        for shape in selShapes:
            cvs = cmds.ls( shape + '.cv[*]', fl=1 )
            for cv in cvs:
                pos = cmds.xform( cv, q=1, ws=1, t=1 )[:3]
                posList.append( pos )
    for pos in posList:
        print '[%f, %f, %f],' % ( pos[0], pos[1], pos[2] )
    
except:
    pass