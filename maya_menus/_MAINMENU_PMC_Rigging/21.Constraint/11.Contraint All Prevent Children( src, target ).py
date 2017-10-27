from sgMaya import sgCmds
import pymel.core

sels = pymel.core.ls( sl=1 )
controlObj = sels[0]
target = sels[1]
if target.getShape():
    sgCmds.setGeometryMatrixToTarget( target, controlObj )
else:
    children = target.listRelatives( c=1, type='transform' )
    childrenPoses = [ child.wm.get() for child in children ]
    pymel.core.xform( target, ws=1, matrix=controlObj.wm.get() )
    for i in range( len( children ) ):
        pymel.core.xform( children[i], ws=1, matrix= childrenPoses[i] )
sgCmds.constrain_all( controlObj, target )