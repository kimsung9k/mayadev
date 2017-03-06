import functions.capture as capture
import functions.render as render
import maya.cmds as cmds




def setMatrix( first, second ):
    
    mtx = cmds.getAttr( first+'.wm' )
    cmds.xform( second, ws=1, matrix=mtx )
    pivot = cmds.xform( first, q=1, ws=1, piv=1 )[:3]
    print pivot
    cmds.xform( second, ws=1, piv=pivot )



def getBBC( target ):
    
    bbmin = cmds.getAttr( target + '.boundingBoxMin' )[0]
    bbmax = cmds.getAttr( target + '.boundingBoxMax' )[0]
    
    bbcenter = []
    for i in range( 3 ):
        bbcenter.append( (bbmin[i] + bbmax[i])/2.0 )
    return bbcenter
    
    
    
def getSizeXYZ( target ):
    
    bbmin = cmds.getAttr( target + '.boundingBoxMin' )[0]
    bbmax = cmds.getAttr( target + '.boundingBoxMax' )[0]
    
    sizeX = bbmax[0] - bbmin[0]
    sizeY = bbmax[1] - bbmin[1]
    sizeZ = bbmax[2] - bbmin[2]
    
    return sizeX, sizeY, sizeZ
    


def getHierarchyObjects( target ):
    
    fullPathName = cmds.ls( target, l=1 )[0]
    
    sepNames = fullPathName.split( '|' )[1:]
    
    hierarchy = []
    for i in range( len( sepNames ) ):
        trNode = '|' + '|'.join( sepNames[:i+1] )
        hierarchy.append( trNode )
    
    #hierarchy.reverse()
    return hierarchy
    
    

def checkItHasKey( target ):
    if cmds.listConnections( target, type='animCurve' ):
        return True
    else:
        return False




def copyKeyframe( first, second ):

    animCons = cmds.listConnections( first, s=1, d=0, p=1, c=1, type='animCurve' )

    outputs = animCons[1::2]
    inputs  = animCons[::2]

    for i in range( len( outputs ) ):
        animNode = cmds.duplicate( outputs[i].split( '.' )[0] )[0]
        cmds.connectAttr( animNode+'.output', second + '.' + inputs[i].split( '.' )[1] )
        


def offsetGrpFromFirstToSecond( grp, first, second ):
    
    firstBBC   = getBBC( first )
    secondBBC  = getBBC( second )
    firstSize  = getSizeXYZ( first )
    secondSize = getSizeXYZ( second )
    
    if secondSize[1] == 0:
        yRate = 1.0
    else:
        yRate = secondSize[1]/firstSize[1]
    
    origP = cmds.listRelatives( grp, p=1 )
    grpP = cmds.createNode( 'transform' )
    cmds.setAttr( grpP+'.t', *firstBBC )
    grp = cmds.parent( grp, grpP )[0]
    cmds.setAttr( grpP+'.s', yRate, yRate, yRate )
    cmds.setAttr( grpP+'.t', *secondBBC )
    
    if origP:
        cmds.parent( grp, origP[0] )
    else:
        cmds.parent( grp, w=1 )
    
    cmds.delete( grpP )




def deleteKey( target ):
    
    animCurves = cmds.listConnections( target, s=1, d=0, type='animCurve' )
    
    cmds.delete( animCurves)




def buildHierarchyToSecond( first, second ):

    firstH = getHierarchyObjects( first )
    
    secondH = []
    for i in range( len( firstH )-1 ):
        grp = cmds.createNode( 'transform' )
        setMatrix( firstH[i], grp )
        cmds.makeIdentity( grp, apply=1, t=1, r=1, s=1 )
        if secondH:
            cmds.parent( grp, secondH[-1] )
        secondH.append( grp )
        
    offsetGrpFromFirstToSecond( secondH[0], first, second )
    cmds.parent( second, secondH[-1] )
    cmds.makeIdentity( second, apply=1, t=1, r=1, s=1 )
    secondH.append( second )
    
    return secondH
    
    
    
def keyCopyFirstHToSecondH( first, second ):
    
    deleteKey( second )
    
    firstH  = getHierarchyObjects( first )
    secondH = buildHierarchyToSecond( first, second )
    
    for i in range( len( firstH ) ):
        animCons = cmds.listConnections( firstH[i], type='animCurve', s=1, d=0, c=1, p=1 )
        if not animCons: continue
        
        outputs= animCons[1::2]
        inputs = animCons[::2]
        
        for j in range( len( outputs ) ):
            animNode = outputs[j].split( '.' )[0]
            duAnimNode = cmds.duplicate( animNode )[0]
            
            cmds.connectAttr( duAnimNode+'.output', secondH[i] + '.' + inputs[j].split('.')[1], f=1 )