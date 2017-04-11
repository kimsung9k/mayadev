import maya.cmds as cmds

import allCtls
import initCtls
import chModules.system.mirror as mirror
from ctlsAll import *
from chModules import rigbase

class Mirror( CtlsAll ):
    def __init__(self):
        pass
    
    def mirrorByReplaceString(self, targetList, baseStr, targetStr ):
        namespace = self.getNamespace( targetList[-1] )
        
        for initCtl in targetList:
            if initCtl.find( baseStr ) != -1:
                targetClass = allCtls.AllCtls
                
                initCtlClassName = initCtl.replace( '_L_', '_' ).replace( '_R_', '_' ).replace( namespace, '' )
                if initCtlClassName in dir( initCtls ):
                    exec( "targetClass = initCtls.%s" % initCtlClassName )
                
                try:
                    mirrorType = targetClass.mirrorType
                except: continue
                try:
                    mirrorAxis = targetClass.mirrorAxis
                except: pass
                
                target = initCtl.replace( baseStr, targetStr )
                if mirrorType == 'object':
                    mirror.objectMirror( initCtl, target )
                elif mirrorType == 'axis':
                    if   mirrorAxis == 'x': mirrorVList = [1,0,0]
                    elif mirrorAxis == 'y': mirrorVList = [0,1,0]
                    elif mirrorAxis == 'z': mirrorVList = [0,0,1]
                    mirror.axisMirror( initCtl, target, namespace+'INIT', mirrorVList )

    def mirrorLtoR(self, target, *args ):
        namespace = self.getNamespace( target )
        
        initCtlList = cmds.ls( namespace+'*InitCTL' )
        self.mirrorByReplaceString( initCtlList, '_L_', '_R_' )
    
    def mirrorRtoL(self, target, *args ):
        namespace = self.getNamespace( target )
        
        initCtlList = cmds.ls( namespace+'*InitCTL' )
        self.mirrorByReplaceString( initCtlList, '_R_', '_L_' )
        
class ConAndDiscon( CtlsAll ):
    def __init__(self):
        pass
    
    def isConnect( self, target, *args ):
        namespace = self.getNamespace( target )
        
        allInitCtl = cmds.ls( namespace+'All_InitCTL' )[0]
        initJnt = cmds.listConnections( allInitCtl+'.t', s=0, d=1 )[0]
        
        if cmds.listConnections( initJnt+'.t', s=0, d=1 ):
            return True
        else:
            return False
    
    def connect( self, base, target, *args ):
        baseNamespace = self.getNamespace( base )
        targetNamespace = self.getNamespace( target )
        
        inits = cmds.ls( targetNamespace+'*_Init' )
        
        for init in inits:
            initJnt = init.replace( targetNamespace, baseNamespace ).replace( '_Init', '_InitJnt' )
            cmds.connectAttr( initJnt+'.t', init+'.t', f=1 )
            cmds.connectAttr( initJnt+'.r', init+'.r', f=1 )
    
    def disConnect( self, target, *args ):
        namespace = self.getNamespace( target )
        
        allInitCtl = cmds.ls( namespace+'All_InitCTL' )[0]
        allInitJnt = cmds.listConnections( allInitCtl+'.t', s=0, d=1 )[0]
            
        allInit = cmds.listConnections( allInitJnt+'.t', s=0, d=1 )[0]
        namespace = allInit.replace( 'All_Init', '' )
            
        inits = cmds.ls( namespace+'*_Init', tr=1 )
        inits += cmds.ls( namespace+'*_Init_GRP', tr=1 )
        
        for init in inits:
            cons = cmds.listConnections( init, s=1, d=0, c=1, p=1 )
            
            if not cons: continue
            
            outputs = cons[1::2]
            inputs = cons[::2]
            
            for i in range( len( outputs ) ):
                cmds.disconnectAttr( outputs[i], inputs[i] )
                
class VisControl( CtlsAll ):
    def __init__(self):
        pass
    
    def getHierarchyInit(self, target ):
        namespace = self.getNamespace(target)
        
        initCtls = cmds.ls( namespace+'*_InitCTL')
        
        initJnt = target.replace( '_InitCTL', '_InitJnt' )
        
        sels = cmds.ls( sl=1 )
        cmds.select( initJnt, hi=1 )
        selJnts = cmds.ls( sl=1, type='joint' )
        cmds.select( sels )
        
        hiInitCtls = []
        for jnt in selJnts:
            hiInitCtls.append( jnt.replace( '_InitJnt', '_InitCTL' ) )
            
        return hiInitCtls
    
    def getParentList(self, target, pList = [] ):
        targetPs = cmds.listRelatives( target, p=1 )
        if targetPs: 
            pList.append( targetPs[0] )
            pList = self.getParentList( targetPs[0], pList )
        return pList
    
    def getVisJntsList(self, target):
        initJnt = target.replace( '_InitCTL', '_InitJnt' )
        visJnts = self.getParentList( initJnt, [] )
        children = cmds.listRelatives( initJnt, c=1, ad=1, type='joint' )
        
        if not children: return None
        children.append( initJnt )
        
        for child in children:
            if child.find( '_InitJnt' ) != -1:
                visJnts.append( child )
        
        return visJnts
    
    def showAll(self, target, *args ):
        namespace = self.getNamespace(target)
        
        for initCtl in cmds.ls( namespace+'*_InitCTL', type='transform' ):
            cmds.setAttr( initCtl+'.dh', 1 )
        for initJnt in cmds.ls( namespace+'*_InitJnt', type='joint' ):
            cmds.setAttr( initJnt+'.v', 1 )
        cmds.setAttr( namespace+'Root_InitJnt.overrideEnabled', 1 )
            
    def showTargetHierarchy(self, target, *args ):
        namespace = self.getNamespace(target)
        
        for initCtl in cmds.ls( namespace+'*_InitCTL', type='transform' ):
            cmds.setAttr( initCtl+'.dh', 0 )
        
        visInitCtlsList = self.getHierarchyInit( target )    
        
        if visInitCtlsList:
            for initCtl in visInitCtlsList:
                if initCtl.find( '_GRP' ) != -1:
                    cmds.setAttr( initCtl+'.dh', 0 )
                else:
                    cmds.setAttr( initCtl+'.dh', 1 )
            
        for initJnt in cmds.ls( namespace+'*_InitJnt', type='joint' ):
            cmds.setAttr( initJnt+'.v', 0 )
            cmds.setAttr( initJnt+'.overrideEnabled', 0 )
        targetInitJnt = target.replace( '_InitCTL', '_InitJnt' )
        rigbase.transformSetColor( targetInitJnt, 22 )
        
        visJntsList = self.getVisJntsList(target)
        
        if visJntsList:
            for initJnt in visJntsList:
                cmds.setAttr( initJnt+'.v', 1 )
            
    def showAllCondition(self, target ):
        namespace = self.getNamespace(target)
        
        for initCtl in cmds.ls( namespace+'*_InitCTL', type='transform' ):
            value = cmds.getAttr( initCtl+'.dh' )
            if value == False: 
                return False
        return True
    
    def hideSelectedHierarchy(self, sels, *args ):
        for sel in sels:
            initJnt = sel.replace( '_InitCTL', '_InitJnt' )
            childJnts = cmds.listRelatives( initJnt, c=1, ad=1, type='joint' )
            cmds.setAttr( initJnt+'.v', 0 )
            
            if not childJnts: childJnts = []
            
            childJnts.append( initJnt )
            
            for jnt in childJnts:
                initCtl = jnt.replace( '_InitJnt', '_InitCTL' )
                cmds.setAttr( initCtl+'.dh', 0 )
    
class Main( Mirror, ConAndDiscon, VisControl ):
    def __init__(self):
        pass