import pymel.core
from sgMaya import sgCmds

sels = pymel.core.ls( sl=1 )

ctl = sels[0]
mesh = sels[1]

blShapeNodes = sgCmds.getNodeFromHistory( mesh, 'blendShape' )

for blendNode in blShapeNodes:
    for i in range( blendNode.w.numElements() ):
        wPlug = blendNode.w[i]
        attrName = cmds.ls( wPlug.name() )[0].split( '.' )[-1]
            
        try:sgCmds.addAttr( ctl, ln=attrName, k=1, min=0, max=1 ) 
        except:continue
        ctl.attr( attrName ) >> wPlug