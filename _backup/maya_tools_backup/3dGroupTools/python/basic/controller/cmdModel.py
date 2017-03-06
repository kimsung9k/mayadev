import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import basic.baseFunctions as baseFunctions
import math
import model

mel.eval( 'source "%s"' % model.MelFileInfo._colorOverridePath )


def makeGRP( target ):
    
    targetP = cmds.listRelatives( target, p=1 )
    
    mtx = cmds.getAttr( target +'.wm' )
    grp = cmds.createNode( 'transform', n='P'+target )
    cmds.xform( grp, ws=1, matrix=mtx )
    target = cmds.parent( target, grp )[0]
    
    if cmds.nodeType( target ) == 'joint':
        jntMtx = cmds.getAttr( target+'.m' )
        mMtx = om.MMatrix()
        om.MScriptUtil.createMatrixFromList( jntMtx, mMtx )
        trMtx = om.MTransformationMatrix( mMtx )
        rotV = trMtx.eulerRotation().asVector()
        rot = [math.degrees( rotV.x),  math.degrees( rotV.y ), math.degrees( rotV.z )]
        cmds.setAttr( target+'.r', 0,0,0 )
        cmds.setAttr( target+'.jo', *rot )
    
    if targetP:
        cmds.parent( grp, targetP[0] )
        
    return target



def mirrorController( target ):
    
    mtx = cmds.getAttr( target + '.wm' )

    targetShapes = cmds.listRelatives( target, s=1, f=1 )
    if cmds.nodeType( target ) == 'joint':
        emptyCtl = cmds.createNode( 'joint' )
        cmds.setAttr( emptyCtl+'.radius', 0 )
    else:
        emptyCtl = cmds.createNode( 'transform' )

    for shape in targetShapes:
        cmds.parent( shape, emptyCtl, add=1, shape =1 )
    ctl = cmds.duplicate( emptyCtl )[0]; cmds.delete( emptyCtl )
    
    for i in range( 3 ):
        mtx[ i*4 + 1 ] *= -1
        mtx[ i*4 + 2 ] *= -1
    mtx[3*4+0] *= -1
        
    if target.find( '_L_' ) != -1:
        replaceName = target.replace( '_L_', '_R_' )
    elif target.find( '_R_' ) != -1:
        replaceName = target.replace( '_R_', '_L_' )
    else:
        replaceName = 'newObject'
        
    ctl = cmds.rename( ctl, replaceName )
    
    cmds.xform( ctl, ws=1, matrix=mtx )
    ctlShapes = cmds.listRelatives( ctl, s=1, f=1 )
    
    for ctlShape in ctlShapes:
        fnCurve = om.MFnNurbsCurve( baseFunctions.getMObject( ctlShape ) )
        points = om.MPointArray()
        fnCurve.getCVs( points )
        for i in range( points.length() ):
            points[i].x *= -1
            points[i].y *= -1
            points[i].z *= -1
        fnCurve.setCVs( points )
        cmds.rename( ctlShape, ctl+'Shape' )

    makeGRP( ctl )




def mmMakeGRP( *args ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        makeGRP( sel )




def mmMirrorController( *args ):
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        mirrorController( sel )




def mmAddShape( *args ):
    
    sels = cmds.ls( sl=1 )
    
    first = sels[0]
    others = sels[1:]
    
    for target in others:
        duObj = cmds.duplicate( first )[0]
        duShapes = cmds.listRelatives( duObj, s=1, f=1 )
        if not duShapes: break
        for shape in duShapes:
            shapeName = cmds.parent( shape, target, add=1, shape=1 )
            cmds.rename( shapeName, target+'Shape' )
        cmds.delete( duObj )
        
        

class MmSetOrder:
    
    def __init__(self):
        
        self._sels = cmds.ls( sl=1 )
    
    
    def xyz_0(self, *args ):
        for sel in self._sels:
            cmds.setAttr( sel + '.rotateOrder', 0 )
            
    def yzx_1(self, *args ):
        for sel in self._sels:
            cmds.setAttr( sel + '.rotateOrder', 1 )
            
    def zxy_2(self, *args ):
        for sel in self._sels:
            cmds.setAttr( sel + '.rotateOrder', 2 )
            
    def xzy_3(self, *args ):
        for sel in self._sels:
            cmds.setAttr( sel + '.rotateOrder', 3 )
            
    def yxz_4(self, *args ):
        for sel in self._sels:
            cmds.setAttr( sel + '.rotateOrder', 4 )
            
    def zyx_5(self, *args ):
        for sel in self._sels:
            cmds.setAttr( sel + '.rotateOrder', 5 )
            
            
            
def mmIkHandle( *args ):
    
    sels = cmds.ls( sl=1 )
    
    handles = []
    for sel in sels:
        selChildren = cmds.listRelatives( sel, c=1, ad=1 )
        lastChild = selChildren[0]
        
        handle = cmds.ikHandle( sj=sel, ee=lastChild, sol='ikRPsolver' )
        
    handles.append( handle )
    


mc_OpenBuildControllerUI = """import basic.controller.ui.view
basic.controller.ui.view.CreateControllerUI().show()"""
    
    
    
mc_OpenColorOverride = """import maya.mel as mel
mel.eval( 'colorOverrideProc' )"""