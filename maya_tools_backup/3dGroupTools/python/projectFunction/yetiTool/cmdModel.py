import maya.OpenMaya as om
import maya.cmds as cmds
import maya.mel as mel


def getFnNode( node ):
    
    selList = om.MSelectionList()
    selList.add( node )
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    return om.MFnDependencyNode( mObj )



def makeSetSelectedGroup( grp ):
    
    setName = grp+'_set'
    children = cmds.listRelatives( grp, f=1, ad=1 )
    nurbsCurves = []
    for child in children:
        if cmds.getAttr( child+'.io' ): continue
        if cmds.nodeType( child ) == 'nurbsCurve':
            crvObj = cmds.listRelatives( child, p=1 )[0]
            nurbsCurves.append( crvObj )
    return cmds.sets( nurbsCurves, n=setName )



def connectSetToYeti( setName, yetiNode ):
    
    if cmds.nodeType( yetiNode ) == 'transform':
        yetiNode = cmds.listRelatives( yetiNode, s=1 )[0]
    
    sets = cmds.listConnections( yetiNode+'.guideSets' )
    if sets:
        if setName in sets: 
            cmds.warning(  '"%s" is aleady Connected to "%s"' %( setName, yetiNode ) )
            return None
    
    mel.eval( 'pgYetiAddGuideSet("%s","%s");' %( setName, yetiNode ) )
    
    print  '"%s" Connected to "%s"' %( setName, yetiNode )

    
    
    
def createGroomAndConnect( setName, mesh ):
    
    yetiGroomNode = cmds.createNode( 'pgYetiGroom' )
    yetiGroomObj = cmds.listRelatives( yetiGroomNode, p=1 )[0]
    yetiGroomObj = cmds.rename( yetiGroomObj, setName.replace( '_set', '_groom' ) )
    yetiGroomNode = cmds.listRelatives( yetiGroomObj, s=1 )[0]
    yetiGroomNode = cmds.rename( yetiGroomNode, yetiGroomObj+'Shape' )
    
    if cmds.nodeType( mesh ) == 'transform':
        mesh = cmds.listRelatives( mesh, s=1 )[0]
    
    cmds.connectAttr( mesh+'.worldMesh[0]', yetiGroomNode+'.inputGeometry' )
    cmds.connectAttr( 'time1.outTime', yetiGroomNode+'.currentTime' )
    
    mel.eval( "pgYetiCommand -convertFromCurves %s %s;" %( setName, yetiGroomNode ) )
    
    yetiMaya = cmds.listConnections( mesh, type='pgYetiMaya', shapes=1 )
    if not yetiMaya: return None
    yetiMaya = yetiMaya[0]
    mel.eval( 'pgYetiAddGroom("%s","%s")' %(yetiGroomNode,yetiMaya) )
    


def processAll( groups, yetiNode, mesh ):
    
    setNames = []
    for group in groups:
        setName = makeSetSelectedGroup( group )
        setNames.append( setName )
    
    for setName in setNames:
        connectSetToYeti( setName, yetiNode )
        createGroomAndConnect( setName, mesh )