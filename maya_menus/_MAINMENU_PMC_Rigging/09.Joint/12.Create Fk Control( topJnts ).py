from sgMaya import sgCmds, sgModel
import pymel.core

sels = pymel.core.ls( sl=1 )

for sel in sels:
    selChildren = sel.listRelatives( c=1, ad=1 )
    selH = selChildren + [sel]
    selH.reverse()
    
    beforeCtl = None
    ctls = []
    for i in range( len( selH ) ):    
        target = selH[i]
        ctlTarget = sgCmds.makeController( sgModel.Controller.rhombusPoints, 0.5, makeParent=1 )
        ctlTarget.shape_rz.set( 90 )
        ctlP = ctlTarget.getParent()
        pymel.core.xform( ctlP, ws=1, matrix=target.wm.get() )
        if beforeCtl:
            ctlTarget.getParent().setParent( beforeCtl )
        beforeCtl = ctlTarget
        
        if len( selH ) == i+1 or i == 0:
            ctls.append( ctlTarget )
        else:
            ctlPin = sgCmds.makeController( sgModel.Controller.pinPoints, 0.6, makeParent=1 )
            ctlPin.shape_ry.set( 90 )
            ctlPinP = ctlPin.getParent()
            ctlPinP.setParent( ctlTarget )
            sgCmds.setTransformDefault( ctlPinP )
            ctls.append( ctlPin )
    
    for i in range( len( selH )-1 ):
        directionIndex = sgCmds.getDirectionIndex( selH[i+1].t.get() )
        vectorList = [[1,0,0], [0,1,0], [0,0,1], [-1,0,0], [0,-1,0], [0,0,-1]]
        aim = vectorList[ directionIndex ]
        up  = vectorList[ (directionIndex + 1)%6 ]
        pymel.core.aimConstraint( ctls[i+1], selH[i], aim=aim, u=up, wu=up, wut='objectrotation', wuo=ctls[i] )
        sgCmds.constrain_point( ctls[i], selH[i] )
    sgCmds.constrain_parent( ctls[-1], selH[-1] )