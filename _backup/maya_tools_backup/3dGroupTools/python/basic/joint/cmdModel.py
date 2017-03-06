import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel
import ui.view
import model
import math


mel.eval( 'source "%s"' % model.MelFileInfo._propertiesPath )



def addAngleDriver( target ):
    
    targetP = cmds.listRelatives( target, p=1 )[0]
    baseObject = cmds.createNode( 'transform', n=target.replace( '_BJT', '_DriverBase' ) )
    visObj = cmds.createNode( 'transform', n=target.replace( '_BJT', '_driverVisTr' ) )
    cmds.parent( visObj, baseObject )
    cmds.parent( baseObject, targetP )
    cmds.xform( baseObject, matrix=cmds.getAttr( target+'.m' ) )
    mmtx = cmds.createNode( 'multMatrix', n=target.replace( '_BJT', '_multMtx' ) )
    driver = cmds.createNode( 'angleDriver', n=target.replace( '_BJT', '_angleDriver' ) )
    dcmp = cmds.createNode( 'decomposeMatrix', n=target.replace( '_BJT', '_trDcmp' ) )
    
    cmds.connectAttr( target+'.wm', mmtx+'.i[0]' )
    cmds.connectAttr( baseObject+'.wim', mmtx+'.i[1]' )
    cmds.connectAttr( mmtx+'.matrixSum', driver+'.angleMatrix' )
    cmds.connectAttr( mmtx+'.matrixSum', driver+'.upVectorMatrix' )
    cmds.connectAttr( driver+'.outMatrix', dcmp+'.inputMatrix' )
    cmds.connectAttr( dcmp+'.or', visObj+'.r' )
    
    return visObj



def mmShowCreateJointUI( *args ):
    
    import sgModelFileAndPath
    
    sgModelFileAndPath.autoLoadPlugin( 'sgTools' )
    
    def setTool( *args ):
        if not cmds.contextInfo( "createJointContext1", ex=1 ):
            mel.eval( 'createJointContext createJointContext1' )
        cmds.setToolTo( "createJointContext1" )
    
    inst = ui.view.CreateJointUI()
    inst._cmdSetTool.append( setTool )
    
    inst.create()



def mmShowOnlySelectHierarchy( *args ):
    
    sels = cmds.ls( sl=1, l=1 )
    if not sels: return None
    
    target = sels[-1]

    parent = cmds.listRelatives( target, p=1, f=1 )
    parents = [ target ]
    while parent:
        parents.append( parent[0] )
        parent = cmds.listRelatives( parent, p=1, f=1 )
    
    parents.reverse()
    
    for i in range( len( parents )-1 ):
        children = cmds.listRelatives( parents[i], c=1, f=1 )
        for child in children:
            if child == parents[i+1]: continue
            cmds.setAttr( child + '.v', 0 )



def mmShowAllSelectedHierarchy( *args ):
    
    sels = cmds.ls( sl=1, l=1 )
    if not sels: return None
    
    target = sels[-1]
    
    parent = cmds.listRelatives( target, p=1, f=1 )
    parents = [ target ]
    while parent:
        parents.append( parent[0] )
        parent = cmds.listRelatives( parent, p=1, f=1 )
    
    parents.reverse()
    
    for i in range( len( parents )-1 ):
        children = cmds.listRelatives( parents[i], c=1, f=1 )
        for child in children:
            cmds.setAttr( child+'.v',1 )



def mmSetOrientToTarget( *args ):
    
    sels = cmds.ls( sl=1 )
    
    if len( sels ) < 2: return None
    
    first = sels[0]
    
    rot = cmds.xform( first, q=1, ws=1, ro=1 )[:3]
    
    for sel in sels[1:]:
        cmds.rotate( rot[0], rot[1], rot[2], sel, ws=1, pcp=1 )
    


def mmMirrorJoint( *args ):
    
    sels= cmds.ls( sl=1 )
    
    for sel in sels:
        
        srcStr = ''
        trgStr = ''
        if sel.find( '_L_' ) != -1:
            other = sel.replace( '_L_', '_R_' )
            srcStr = '_L_'
            trgStr = '_R_'
        elif sel.find( '_R_' ) != -1:
            other = sel.replace( '_R_', '_L_' )
            srcStr = '_R_'
            trgStr = '_L_'
        else:
            continue
        
        if not cmds.objExists( other ):
            cmds.mirrorJoint( sel, mirrorYZ=1, mirrorBehavior=1, searchReplace=["_L_", "_R_"] )
        else:
            mtxTop = cmds.getAttr( sel+'.wm' )
            mtxTop[1] *= -1; mtxTop[ 2] *= -1
            mtxTop[5] *= -1; mtxTop[ 6] *= -1
            mtxTop[9] *= -1; mtxTop[10] *= -1
            mtxTop[12] *= -1
            cmds.xform( other, ws=1, matrix=mtxTop )
            
            children = cmds.listRelatives( sel, c=1, ad=1 )
            for child in children:
                mtx = cmds.getAttr( child+'.m' )
                mtx[12] *= -1; mtx[13] *= -1; mtx[14] *= -1
                otherChild = child.replace( srcStr, trgStr )
                cmds.xform( otherChild, matrix=mtx )
    
    
    
def mmShowSetJointOrientUI( *args ):
    
    ui.view.SetJointOrientUI().Show()
    
    
    
def mmParentSelectedOrder( *args ):
    
    sels = cmds.ls( sl=1 )
    
    for i in range( len( sels )-1 ):
        cmds.parent( sels[i], sels[i+1] )
        
        if cmds.nodeType( sels[i] ) == "joint":
            cmds.makeIdentity( sels[i], apply=1, t=0, r=1, s=0, n=0 )
            
            
            
            
def mmAddAngleDriver( *args ):
    
    sels = cmds.ls( sl=1 )
    
    visObjs = []
    for sel in sels:
        visObjs.append( addAngleDriver( sel ) )
    
    cmds.select( visObjs )
    


def mmInsertJoint( *args ):
    
    def normalize(vector_value):
        length = math.sqrt(vector_value[0]**2 + vector_value[1]**2 + vector_value[2]**2)
        x = vector_value[0]/length
        y = vector_value[1]/length
        z = vector_value[2]/length
        result = [x, y, z]
        return result
    
    num_joints =input(10)
    num_joints = num_joints+1
    joint_list = cmds.ls(sl=True)
    
    for r in joint_list:
    
        first_joint_trans = cmds.xform(r, q=True, ws=True, t=True)
        first_joint_ori = cmds.xform(r, q=True, ws=True, ro=True)
        end_joint = cmds.listRelatives(r, f=True, c=True)
        end_joint_rename=cmds.rename(end_joint[0], "end_to_delete______yeah")
        end_joint_trans = cmds.xform(end_joint_rename, q=True, ws=True, t=True)
        end_joint_ori = cmds.xform(end_joint_rename, q=True, ws=True, ro=True)
        
        between_vector = [-(first_joint_trans[0]-end_joint_trans[0]),-(first_joint_trans[1]-end_joint_trans[1]),-(first_joint_trans[2]-end_joint_trans[2])]
        vector_length = mel.eval(("mag(<<"+str(between_vector[0])+","+str(between_vector[1])+","+str(between_vector[2])+">>)"))
        vector_normalize = normalize(between_vector)
        
        for i in range(num_joints):
                vector_to_add = [(vector_normalize[0]*((vector_length/num_joints)*((num_joints-float(i))))),(vector_normalize[1]*((vector_length/num_joints)*((num_joints-float(i))))),(vector_normalize[2]*((vector_length/num_joints)*((num_joints-float(i)))))]
                inset_joint = cmds.insertJoint(r)
                cmds.joint(inset_joint, e=True, co=True, o=(0,0,0), p=((first_joint_trans[0]+vector_to_add[0]), (first_joint_trans[1]+vector_to_add[1]), (first_joint_trans[2]+vector_to_add[2])))
        cmds.delete(end_joint_rename)
        



def mmFreezeJointOrient( *args ):
    
    sels = cmds.ls( sl=1 )
    
    
    for sel in sels:
        
        mtx = cmds.getAttr( sel+'.m' )
        
        mmtx = om.MMatrix()
        om.MScriptUtil.createMatrixFromList( mtx, mmtx )
        
        trMtx = om.MTransformationMatrix( mmtx )
        
        euler = trMtx.eulerRotation().asVector()
        
        rotX = math.degrees( euler.x )
        rotY = math.degrees( euler.y )
        rotZ = math.degrees( euler.z )
        
        cmds.setAttr( sel+'.jo', rotX, rotY, rotZ )
        cmds.setAttr( sel+'.r', 0,0,0 )