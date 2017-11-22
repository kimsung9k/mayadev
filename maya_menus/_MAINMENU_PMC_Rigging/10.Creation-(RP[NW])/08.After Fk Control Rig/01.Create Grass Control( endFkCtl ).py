import pymel.core
from sgMaya import sgCmds, sgModel

sels = pymel.core.ls( sl=1 )
for sel in sels:
    endCtl = sel
    bb = pymel.core.exactWorldBoundingBox( endCtl )
    
    bbmin = sgCmds.getMPoint( bb[:3] )
    bbmax = sgCmds.getMPoint( bb[3:] )
    
    dist = bbmin.distanceTo( bbmax )
    
    mainCtl = sgCmds.makeController( sgModel.Controller.diamondPoints, dist/4.0, makeParent=1 )
    pMainCtl = mainCtl.getParent()
    pymel.core.xform( pMainCtl, ws=1, matrix= sels[0].wm.get() )
    
    mainCtl.rename( '_'.join( endCtl.split( '_' )[:-1] )  + '_main' )
    
    firstCtl = pymel.core.ls( '_'.join( endCtl.split( '_' )[:-1] ) + '_0' )[0]
    pFirstCtl = firstCtl.getParent()
    base = pFirstCtl.getParent()
    pMainCtl.setParent( base )
    
    lookAtBase = pymel.core.createNode( 'transform', n= 'lookAtBase_' + firstCtl )
    pymel.core.xform( lookAtBase, ws=1, matrix= firstCtl.wm.get() )
    lookAtChild = sgCmds.makeLookAtChild( mainCtl, lookAtBase )
    lookAtChild.rename( 'lookAtChild_' + firstCtl )
    
    lookAtBase.setParent( base )
    pFirstCtl.setParent( lookAtChild )
    
    joints = sgCmds.createFkControlJoint( pFirstCtl )
    joints[0].v.set( 0 )
    
    mainCtlFriend = pymel.core.createNode( 'transform' )
    pMainCtl = mainCtl.getParent()
    mainCtlFriend.setParent( pMainCtl )
    
    sgCmds.setTransformDefault( mainCtlFriend )
    
    blendNode = sgCmds.createBlendTwoMatrixNode( mainCtlFriend, mainCtl, local=1 )
    dcmp = sgCmds.getDecomposeMatrix( blendNode.matrixSum )
    
    for joint in joints[1:]:
        dcmp.outputRotate >> joint.r
    
    sgCmds.addOptionAttribute( mainCtl )
    sgCmds.addAttr( mainCtl, ln='showDetail', min=0, max=1, at='long', cb=1 )
    mainCtl.attr( 'showDetail' ) >> pFirstCtl.v