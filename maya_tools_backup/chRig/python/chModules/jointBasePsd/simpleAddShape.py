import maya.cmds as cmds
import copy

class simpleCommands:
    
    def getTargetSkinCluster(self, targetObj ):
    
        hists = cmds.listHistory( targetObj, pdo=1 )
        
        if not hists: return None
        for hist in hists:
            if cmds.nodeType( hist ) == 'skinCluster':
                return hist
        
    
    def duplicateObj( self, targetObj, skinNode, addName='_add' ):
        
        if cmds.nodeType( targetObj ) != 'transform':
            targetObj = cmds.listRelatives( targetObj, p=1 )
            
            if targetObj: targetObj = targetObj [0]
            else: return None
        targetShape = cmds.listRelatives( targetObj, s=1 )[0]
        targetAttr = targetShape+'.outMesh'
        outputAttr = cmds.listConnections( skinNode+'.input[0].inputGeometry', s=1, d=0, p=1, c=1 )[1]
        
        secondMesh = cmds.createNode( 'mesh' )
        thirdMesh  = cmds.createNode( 'mesh' )
        
        secondObj = cmds.listRelatives( secondMesh, p=1 )[0]
        thirdObj  = cmds.listRelatives( thirdMesh, p=1 )[0]
        
        cmds.connectAttr( targetAttr, secondMesh+'.inMesh' )
        cmds.connectAttr( outputAttr, thirdMesh +'.inMesh' )
        
        cmds.refresh()
        
        cmds.disconnectAttr( targetAttr, secondMesh+'.inMesh' )
        cmds.disconnectAttr( outputAttr, thirdMesh +'.inMesh' )
        
        secondObj = cmds.rename( secondObj, targetObj+addName )
        thirdObj  = cmds.rename( thirdObj , targetObj+addName+'_inv' )
        
        return secondObj, thirdObj
        
    
    def getDuPosition(self, targetObj ):
        
        if cmds.nodeType( targetObj ) != 'transform':
            targetObj = cmds.listRelatives( targetObj, p=1 )
            
            if targetObj: targetObj = targetObj [0]
            else: return None
        
        origMtx = cmds.xform( targetObj, q=1, ws=1, matrix=1 )
        secondPos = copy.copy( origMtx )
        thirdPos  = copy.copy( origMtx )

        minValue = cmds.getAttr( targetObj+'.boundingBoxMin' )[0][0]
        maxValue = cmds.getAttr( targetObj+'.boundingBoxMax' )[0][0]

        width = maxValue - minValue
        addDist = width * 1.05

        secondPos[12] += addDist
        thirdPos[12]  += addDist*2
        
        return secondPos, thirdPos
        

class Cmd:
    
    def __init__(self):
        
        self._cmd = simpleCommands()
    
    
    def createCmd(self, *args ):
        
        sels = cmds.ls( sl=1 )
        
        if not sels: return None
        
        targetObj = sels[0]
        
        skinNode = self._cmd.getTargetSkinCluster( targetObj )
    
        if not skinNode : return None
        
        duObjs = self._cmd.duplicateObj( targetObj, skinNode )
        
        print duObjs
        
        if duObjs: secondObj = duObjs[0]; thirdObj = duObjs[1]
        else: return None
        
        secondShape = cmds.listRelatives( secondObj, s=1 )[0]
        
        inverseSkinCluster = cmds.deformer( thirdObj, type='inverseSkinCluster' )[0]
        cmds.connectAttr( secondShape+'.outMesh', inverseSkinCluster+'.inMesh' )
        cmds.connectAttr( skinNode+'.message', inverseSkinCluster+'.targetSkinCluster' )
        cmds.connectAttr( targetObj+'.wm', inverseSkinCluster+'.geomMatrix')
        
        pos1, pos2 = self._cmd.getDuPosition( targetObj )
    
        cmds.xform( secondObj, ws=1, matrix=pos1 )
        cmds.xform( thirdObj, ws=1, matrix=pos2 )
        
        cmds.sets( secondObj, thirdObj, e=1, forceElement = "initialShadingGroup" )
        
        cmds.select( secondObj )
    
    
    
class Show( Cmd ):
    
    def __init__(self):
        
        self._winName = "simpleAddInversedShape_ui"
        self._title   = "Simple Add PSD Shape"
        
        self._width = 300
        self._height = 100
        self._sideWidth = 10
        self._mainWidth = self._width - self._sideWidth*2
        
        self.core()
        Cmd.__init__( self )
        
    
    def core(self):
        
        if cmds.window( self._winName, ex=1 ):
            cmds.deleteUI( self._winName, wnd=1 )
            
        cmds.window( self._winName, title= self._title )
        
        cmds.columnLayout()
        
        cmds.text( l='', h=15 )
        
        cmds.rowColumnLayout( nc=1, cw=( 1, self._width ) )
        cmds.text( l='Select Skin Cluter Mesh' )
        cmds.setParent( '..' )
        
        cmds.text( l='', h=20 )
        
        cmds.rowColumnLayout( nc=3, cw=[(1,self._sideWidth), (2,self._mainWidth)] )
        cmds.text( l='' )
        cmds.button( l='Create', c=self.createCmd, h=30 )
        cmds.setParent( '..' )
        
        cmds.window( self._winName, e=1, wh=[ self._width, self._height ] )
        cmds.showWindow( self._winName )