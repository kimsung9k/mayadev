import maya.cmds as cmds
import bake as mainCmd
import chModules.retargetTool.functions as fnc
import chModules.retargetTool.topInfo as topInfo
import chModules.retargetTool.topInfoEdit as topInfoEdit
import chModules.retargetTool.distObjInfo as distObjInfo
import os



class CreateDGTransform:
    
    def __init__(self, worldCtl, ctls = [] ):
        
        topInfoEdit.EditNameSpaceInfo( worldCtl, worldCtl)
        
        self._namespace = worldCtl.replace( 'World_CTL', '' )
        
        self._trs = []
        
        self.getNeedTransforms( ctls )
        self.doIt()
        
        
    def getNeedTransforms(self, ctls = [] ):
        
        if ctls:
            appended = []
            
            for ctl in ctls:
                
                if not ctl in appended:
                    self._trs.append( ctl )
                    appended.append( ctl )
                
                topInfoEdit.EditCtlInfo( ctl )
                
                for parent in topInfo.parentList:
                    if not self._namespace+parent in appended:
                        self._trs.append( self._namespace+parent )
                        appended.append( parent )
                if topInfo.orientOrigin and not topInfo.orientOrigin in appended:
                    self._trs.append( self._namespace+topInfo.orientOrigin )
                    appended.append( topInfo.orientOrigin )
                if topInfo.transParent and not topInfo.transParent in appended:
                    self._trs.append( self._namespace+topInfo.transParent )
                    appended.append( topInfo.transParent )
                
                
                distObjs = distObjInfo.getDistObjByName( ctl.replace( self._namespace, '' ) )
                if distObjs:
                    distObjs = distObjs[:-1]
                else:
                    continue
                
                for distObj in distObjs:
                    distObj = self._namespace+distObj
                    if not distObj in appended:
                        self._trs.append( distObj )
                        appended.append( distObj )
                    
        else:
            self._trs = cmds.ls( self._namespace+'*_CTL', tr=1 )
            self._trs.append( self._namespace+'Chest_CTL_Origin' )
            self._trs += cmds.ls( self._namespace+'Arm_*_CU0' )
            self._trs += cmds.ls( self._namespace+'Arm_*_CU1' )
            self._trs += cmds.ls( self._namespace+'Arm_*_CU2' )
            self._trs += cmds.ls( self._namespace+'Leg_*_CU0' )
            self._trs += cmds.ls( self._namespace+'Leg_*_CU1' )
            self._trs += cmds.ls( self._namespace+'Leg_*_CU2' )
            self._trs += cmds.ls( self._namespace+'Hip_*_Const' )
            
            leg_distObj  = ['Knee_*_Init', 'Ankle_*_Init']
            arm_distObj  = ['Elbow_*_Init', 'Wrist_*_Init']
            body_distObj = ['Waist_Init', 'Chest_Init']
            head_distObj = ['NeckMiddle_Init', 'Head_Init']
            
            sideDistObj = []
            centerDistObj = []
            
            sideDistObj += leg_distObj
            sideDistObj += arm_distObj
            centerDistObj += body_distObj
            centerDistObj += head_distObj
            
            for distObj in sideDistObj:
                left = distObj.replace( '*', 'L' )
                right = distObj.replace( '*', 'R' )
                
                self._trs.append( self._namespace+left )
                self._trs.append( self._namespace+right )
                
            for distObj in centerDistObj:
                self._trs.append( self._namespace+distObj )
                
        self._trs = list( set( self._trs ) )


    def doIt(self):
        
        cmds.undoInfo( swf=0 )
        for tr in self._trs:
            
            dgtrName = 'DGTR_'+tr.replace( self._namespace, '' )
            
            if cmds.listConnections( tr, s=0, d=1, type='dgTransform' ):
                continue
            
            dgTransform = cmds.createNode( 'dgTransform', n= dgtrName.replace( self._namespace, self._namespace[:-1]+'_DGTR'+self._namespace[-1] ) )
            decomposeMatrix = cmds.createNode( 'decomposeMatrix', n=dgTransform+'_DCMP' )
            cmds.connectAttr( tr+'.pm', decomposeMatrix+'.inputMatrix' )
            
            attrList = ['tx','ty','tz','rx','ry','rz','sx','sy','sz']
            
            for attr in attrList:
                cmds.connectAttr( decomposeMatrix+'.o'+attr, dgTransform+'.i'+attr )
                cmds.connectAttr( tr+'.'+attr, dgTransform+'.'+attr )
            
            if cmds.nodeType( tr ) == 'joint':
                cmds.connectAttr( tr+'.jox', dgTransform+'.jox' )
                cmds.connectAttr( tr+'.joy', dgTransform+'.joy' )
                cmds.connectAttr( tr+'.joz', dgTransform+'.joz' )
        cmds.undoInfo( swf=1 )


class ExportSelected:
    
    def __init__(self, worldCtl, filePath, timeRange):
        
        self._worldCtl = worldCtl
        self._timeRange = timeRange
        self._filePath = filePath
        
        self._sels = cmds.ls( sl=1 )
        
        if self._worldCtl in self._sels:
            self._sels.remove( self._worldCtl )
        
        cmds.undoInfo( swf=0 )
        self.createDGTransform()
        self.bakeToAnimCurve()
        self.exportFile()
        cmds.undoInfo( swf=1 )
        
    
    def createDGTransform(self):
    
        dgTransData = CreateDGTransform( self._worldCtl, self._sels )
        
        self._dgTransform = []
        self._decomposeMatrix =[]
        
        for tr in dgTransData._trs:
            
            dgTransCons = cmds.listConnections( tr, s=0, d=1, type='dgTransform' )
            
            
            if dgTransCons:
                self._dgTransform.append( dgTransCons[0] )
                decomposeCons = cmds.listConnections( dgTransCons[0], s=1, d=0, type='decomposeMatrix' )
                self._decomposeMatrix.append( decomposeCons[0] )
                
        self._trs = dgTransData._trs
                
                
    def bakeToAnimCurve(self):
        
        #attrs = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz','itx', 'ity', 'itz', 'irx', 'iry', 'irz']
        
        for i in range( len( self._trs ) ):
            tr = self._trs[i]
            dg = self._dgTransform[i]
            
            udAttrs = cmds.listAttr( tr, k=1, ud=1 )
            
            if not udAttrs: continue
            
            for attr in udAttrs:
                attrType = cmds.attributeQuery( attr, node= tr, attributeType=True )
                cmds.addAttr( dg, ln=attr, at=attrType )
                cmds.setAttr( dg+'.'+attr, e=1, k=1 )
                
                cmds.connectAttr( tr+'.'+attr, dg+'.'+attr )
        
        mainCmd.Bake().exportBake( self._dgTransform, self._timeRange )
        

    def exportFile(self):
        
        cmds.select( self._dgTransform )
        
        if fnc.checkFilePath( self._filePath ):
            cmds.refresh()
            cmds.file( self._filePath, force=1, options="v=0;", typ="mayaBinary", pr=1, es=1 )
            
            if os.path.exists( self._filePath ):
                os.remove( self._filePath )
            os.rename( self._filePath+'.mb', self._filePath )
        else:
            cmds.error( 'Path Name is wrong' )