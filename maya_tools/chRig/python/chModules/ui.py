import set.initrigset as initrigset
import set.allset as allset
import set.headrigset as headrigset
import set.torsorigset as torsorigset
import set.armandlegrigset as armandlegrigset
import set.bjtset as bjtset
import set.repairSet as repairSet
import rigbase
import set.fingerrigset as fingerrigset
import chModules

import maya.cmds as cmds

import pickle
from functools import partial


class LocusHumanRig_ui:
    
    def followMenuVisSet( self, *args ):
        worldEx = cmds.objExists( 'World_CTL' )
        if worldEx:
            cmds.window( self.win, e=1, w=425 )
            for field in self.fieldGrp:
                cmds.intField( field, e=1, en=0 )
            cmds.button( self.setButton, e=1, vis=0 )
            cmds.button( self.backButton, e=1, vis=1 )
        else:
            cmds.window( self.win, e=1, w=313 )
            for field in self.fieldGrp:
                cmds.intField( field, e=1, en=1 )
            cmds.button( self.setButton, e=1, vis=1 )
            cmds.button( self.backButton, e=1, vis=0 )
    
    
    def scriptJobSetting(self):
        cmds.scriptJob( e=['Undo', self.followMenuVisSet ], p=self.win )
        cmds.scriptJob( e=['Redo', self.followMenuVisSet ], p=self.win )
    
    
    def __init__(self, *args ):
        if not cmds.objExists( 'All_InitCTL' ):
            self.rigInitCtl_inst = initrigset.RigAll()
            self.rigInitCtl_inst.putInitCtl()
            self.rigInitCtl_inst.doIt()

            try:
                f = open( "pickle.dat", 'w' )
                pickle.dump( self.rigInitCtl_inst, f )
                f.close()
            except: pass
        else:
            try:
                f = open( "pickle.dat", 'r' )
                self.rigInitCtl_inst = pickle.load(f)
                f.close()
            except: pass
        
        win = rigbase.createWindow( 'locusHumanRig_ui', title='Locus Human Rig' )
        
        form = cmds.formLayout()
        cmds.image( image = chModules.chRiggingImagePath )
        cmds.popupMenu()
        cmds.menuItem( l='Mirror <<' )
        cmds.menuItem( l='Mirror >>' )
        
        self.neckField  = cmds.intField( v=4, min=3 )
        self.bodyField  = cmds.intField( v=5, min=3 )
        self.armLUField = cmds.intField( v=5, min=3 )
        self.armLLField = cmds.intField( v=5, min=3 )
        self.armRUField = cmds.intField( v=5, min=3 )
        self.armRLField = cmds.intField( v=5, min=3 )
        self.legLUField = cmds.intField( v=5, min=3 )
        self.legLLField = cmds.intField( v=5, min=3 )
        self.legRUField = cmds.intField( v=5, min=3 )
        self.legRLField = cmds.intField( v=5, min=3 )
        
        self.fieldGrp = [ self.neckField, self.bodyField, 
                          self.armLUField, self.armLLField, self.armRUField, self.armRLField, 
                          self.legLUField, self.legLLField, self.legRUField, self.legRLField ]
        
        self.headFollow = cmds.frameLayout( l='Head Follow', w=100 )
        cmds.checkBox( l='Neck', v=1, onc= partial( self.followAttrVis, ['Head_CTL'] , 'neckFollow', True ),
                                      ofc= partial( self.followAttrVis, ['Head_CTL'], 'neckFollow', False ) )
        cmds.checkBox( l='Chest',v=1, onc= partial( self.followAttrVis, ['Head_CTL'], 'chestFollow', True ),
                                      ofc= partial( self.followAttrVis, ['Head_CTL'], 'chestFollow', False ) )
        cmds.checkBox( l='Root', onc= partial( self.followAttrVis, ['Head_CTL'], 'rootFollow', True ),
                                 ofc= partial( self.followAttrVis, ['Head_CTL'], 'rootFollow', False ) )
        cmds.checkBox( l='Move', onc= partial( self.followAttrVis, ['Head_CTL'], 'moveFollow', True ),
                                 ofc= partial( self.followAttrVis, ['Head_CTL'], 'moveFollow', False ) )
        cmds.setParent('..')
        
        self.collarFollow = cmds.frameLayout( l='Collar Follow', w=100 )
        cmds.checkBox( l='Chest', onc= partial( self.followAttrVis, ['Collar_L_CTL','Collar_R_CTL'], 'chestFollow', True ),
                                  ofc= partial( self.followAttrVis, ['Collar_L_CTL','Collar_R_CTL'], 'chestFollow', False ) )
        cmds.checkBox( l='Root', onc= partial( self.followAttrVis, ['Collar_L_CTL','Collar_R_CTL'], 'rootFollow', True ),
                                 ofc= partial( self.followAttrVis, ['Collar_L_CTL','Collar_R_CTL'], 'rootFollow', False ) )
        cmds.checkBox( l='Move', onc= partial( self.followAttrVis, ['Collar_L_CTL','Collar_R_CTL'], 'moveFollow', True ),
                                 ofc= partial( self.followAttrVis, ['Collar_L_CTL','Collar_R_CTL'], 'moveFollow', False ) )
        cmds.setParent('..')
        
        self.armFollow = cmds.frameLayout( l='Arm Follow', w=100 )
        cmds.checkBox( l='Collar', onc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'collarFollow', True ),
                                   ofc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'collarFollow', False ) )
        cmds.checkBox( l='Head', onc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'headFollow', True ),
                                 ofc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'headFollow', False ) )
        cmds.checkBox( l='Chest',v=1, onc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'chestFollow', True ),
                                      ofc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'chestFollow', False ) )
        cmds.checkBox( l='Hip', onc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'hipFollow', True ),
                                ofc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'hipFollow', False ) )
        cmds.checkBox( l='Root',v=1, onc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'rootFollow', True ),
                                     ofc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'rootFollow', False ) )
        cmds.checkBox( l='Move', onc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'moveFollow', True ),
                                 ofc= partial( self.followAttrVis, ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], 'moveFollow', False ) )
        cmds.setParent('..')
        
        self.legFollow = cmds.frameLayout( l='Leg Follow', w=100 )
        cmds.checkBox( l='Hip', onc= partial( self.followAttrVis, ['Leg_L_Switch_CTL','Leg_R_Switch_CTL'], 'hipFollow', True ),
                                ofc= partial( self.followAttrVis, ['Leg_L_Switch_CTL','Leg_R_Switch_CTL'], 'hipFollow', False ) )
        cmds.checkBox( l='Root',v=1, onc= partial( self.followAttrVis, ['Leg_L_Switch_CTL','Leg_R_Switch_CTL'], 'rootFollow', True ),
                                     ofc= partial( self.followAttrVis, ['Leg_L_Switch_CTL','Leg_R_Switch_CTL'], 'rootFollow', False ) )
        cmds.checkBox( l='Move', onc= partial( self.followAttrVis, ['Leg_L_Switch_CTL','Leg_R_Switch_CTL'], 'moveFollow', True ),
                                 ofc= partial( self.followAttrVis, ['Leg_L_Switch_CTL','Leg_R_Switch_CTL'], 'moveFollow', False ) )
        cmds.setParent('..')
        
        dfFollowButton = cmds.button( l='Default Follow', w=100, h=30, c= self.defaultFollow )
        self.setButton = cmds.button( l='SET', c=self.setCmd, w=60, h=30, bgc=[.308-.1,.312-.1,.292-.1] )
        self.backButton = cmds.button( l='BACK', c=self.backCmd, vis=0,  w=60, h=30, bgc=[.308-.1,.312-.1,.292-.1] )
        
        empty = cmds.text(l='')
        #mirrorLButton = cmds.button( l='>>',  w=30, h=80 )
        #mirrorRButton  = cmds.button( l='<<', w=30, h=80 )
        cmds.frameLayout( self.collarFollow, q=1, ca=1 )
        
        cmds.formLayout( form, e=1,
                         attachForm = [ ( self.neckField, 'top', 80 ),( self.neckField, 'left', 130 ),
                                        ( self.bodyField, 'top', 195 ),( self.bodyField, 'left', 150 ),
                                        ( self.armLUField, 'top', 170 ),( self.armLUField, 'left', 200 ),
                                        ( self.armLLField, 'top', 235 ),( self.armLLField, 'left', 215 ),
                                        ( self.armRUField, 'top', 170 ),( self.armRUField, 'left', 65 ),
                                        ( self.armRLField, 'top', 235 ),( self.armRLField, 'left', 50 ),
                                        ( self.legLUField, 'top', 350 ),( self.legLUField, 'left', 175 ),
                                        ( self.legLLField, 'top', 465 ),( self.legLLField, 'left', 165 ),
                                        ( self.legRUField, 'top', 350 ),( self.legRUField, 'left', 105 ),
                                        ( self.legRLField, 'top', 470 ),( self.legRLField, 'left', 85  ),
                                        
                                        ( self.headFollow, 'top', 15 ),( self.headFollow, 'left', 320  ),
                                        ( self.collarFollow, 'top', 150 ),( self.collarFollow, 'left', 320  ),
                                        ( self.armFollow, 'top', 265 ),( self.armFollow, 'left', 320  ),
                                        ( self.legFollow, 'top', 440 ),( self.legFollow, 'left', 320  ),
                                        ( dfFollowButton, 'top', 560 ), ( dfFollowButton, 'left', 320 ),
                                        ( self.setButton, 'top', 560 ), ( self.setButton, 'left', 250 ),
                                        ( self.backButton, 'top', 560 ), ( self.backButton, 'left', 250 ),
                                        ( empty, 'top', 0 ) ] )
        
        cmds.window( win, e=1, wh=[313,595], s=0 )
        
        try:
            from BorderlessFrame import BorderlessFrame, toQtObject
            dlg = toQtObject(win)
            self._win = BorderlessFrame()
            self._win.setContent(dlg)
            self._win.setTitle( 'Locus Human Rig' )
            self._win.show()
            self._win.move(214, 223)
        except:
            cmds.showWindow( win )
        
        self.win = win
        
        self.followMenuVisSet()
        self.scriptJobSetting()
    
        
    def setCmd(self, *args ):
        neckJntNum = cmds.intField( self.neckField, q=1, v=1 )
        bodyJntNum = cmds.intField( self.bodyField, q=1, v=1 )
        armLUJntNum = cmds.intField( self.armLUField, q=1, v=1 )
        armLLJntNum = cmds.intField( self.armLLField, q=1, v=1 )
        armRUJntNum = cmds.intField( self.armRUField, q=1, v=1 )
        armRLJntNum = cmds.intField( self.armRLField, q=1, v=1 )
        legLUJntNum = cmds.intField( self.legLUField, q=1, v=1 )
        legLLJntNum = cmds.intField( self.legLLField, q=1, v=1 )
        legRUJntNum = cmds.intField( self.legRUField, q=1, v=1 )
        legRLJntNum = cmds.intField( self.legRLField, q=1, v=1 )
        
        allInst = allset.RigAll( self.rigInitCtl_inst )
        allInst.allSet()
        
        torsoInst = torsorigset.RigAll( self.rigInitCtl_inst )
        torsoInst.allSet( bodyJntNum, 2 )
        
        headInst = headrigset.RigAll( self.rigInitCtl_inst )
        headInst.allSet( neckJntNum )
        
        armIkInst = armandlegrigset.RigAll( self.rigInitCtl_inst )
        armIkInst.allSet( armLUJntNum,armLLJntNum,armRUJntNum,armRLJntNum,legLUJntNum,legLLJntNum,legRUJntNum,legRLJntNum )
        
        frInst = fingerrigset.RigAll( self.rigInitCtl_inst )
        frInst.allSet()
        
        cmds.setAttr( 'INIT.v', 0 )

        bjtset.createBjt(  'Spline0_RJT' )
        bjtset.flyFollowRepair()
        bjtset.markingMenuSet( self.rigInitCtl_inst )
        repairSet.ikTip_repairSet()
        repairSet.poleV_repairSet()
        repairSet.waist_repairSet()
        repairSet.armPoleV_repairSet()
        repairSet.legPoleV_repairSet()
        repairSet.waistVector_repairSet()
        repairSet.chestOrigin_repairSet()
        repairSet.ikStretch_repairSet()
        repairSet.ankleItp_repairSet()
        repairSet.legPoleV_repairSet2()
        repairSet.flyCtlRepairSet()
        repairSet.legTwistRepairSet()
        repairSet.circleCheckRepairSet()
        repairSet.shoulderRepairSet()
        
        rigbase.repairConstraint()
        
        cmds.window( self.win, e=1, w=425 )
        
        for field in self.fieldGrp:
            cmds.intField( field, e=1, en=0 )
        
        cmds.button( self.setButton, e=1, vis=0 )
        cmds.button( self.backButton, e=1, vis=1 )
    
        
    def backCmd(self, *args ):
        cmds.delete( 'RIG', 'SKIN' )
        cmds.window( self.win, e=1, w=313 )
        
        cmds.setAttr( 'INIT.v', 1 )
        for field in self.fieldGrp:
            cmds.intField( field, e=1, en=1 )
        
        cmds.button( self.setButton, e=1, vis=1 )
        cmds.button( self.backButton, e=1, vis=0 )
        
        attrs = cmds.listAttr( self.rigInitCtl_inst.rObj )
        cmds.lockNode( self.rigInitCtl_inst.rObj, lock=0 )
        for attr in attrs:
            if attr.find( '_CTL' ) != -1:
                cmds.deleteAttr( self.rigInitCtl_inst.rObj+'.'+attr )
        cmds.lockNode( self.rigInitCtl_inst.rObj, lock=1 )
    
                
    def followAttrVis(self, ctlNameList, attrName, onOff, *args ):
        if onOff == True:
            for ctlName in ctlNameList:
                cmds.setAttr( ctlName+'.'+attrName, e=1, k=1 )
        else:
            for ctlName in ctlNameList:
                cmds.setAttr( ctlName+'.'+attrName, e=1, k=0 )
    
                
    def defaultFollow(self, *args):
        headChildrenLay = cmds.frameLayout( self.headFollow, q=1, ca=1 )
        collarChildrenLay = cmds.frameLayout( self.collarFollow, q=1, ca=1 )
        armChildrenLay = cmds.frameLayout( self.armFollow, q=1, ca=1 )
        legChildrenLay = cmds.frameLayout( self.legFollow, q=1, ca=1 )
        
        for head in headChildrenLay:
            followName = cmds.checkBox( head, q=1, l=1 )
            if followName in ['Neck', 'Chest', 'Fly']:
                cmds.checkBox( head, e=1, v=1 )
                self.followAttrVis( ['Head_CTL'], followName.lower()+'Follow', True )
            else:
                cmds.checkBox( head, e=1, v=0 )
                self.followAttrVis( ['Head_CTL'], followName.lower()+'Follow', False )
        
        for collar in collarChildrenLay:
            followName = cmds.checkBox( collar, q=1, l=1 )
            if followName in ['Fly']:
                cmds.checkBox( collar, e=1, v=1 )
                self.followAttrVis( ['Collar_L_CTL','Collar_R_CTL'], followName.lower()+'Follow', True )
            else:
                cmds.checkBox( collar, e=1, v=0 )
                self.followAttrVis( ['Collar_L_CTL','Collar_R_CTL'], followName.lower()+'Follow', False )
                
        for arm in armChildrenLay:
            followName = cmds.checkBox( arm, q=1, l=1 )
            if followName in ['Chest', 'Root', 'Fly' ]:
                cmds.checkBox( arm, e=1, v=1 )
                self.followAttrVis( ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], followName.lower()+'Follow', True )
            else:
                cmds.checkBox( arm, e=1, v=0 )
                self.followAttrVis( ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], followName.lower()+'Follow', False )
                
        for leg in legChildrenLay:
            followName = cmds.checkBox( leg, q=1, l=1 )
            if followName in ['Root', 'Fly' ]:
                cmds.checkBox( leg, e=1, v=1 )
                self.followAttrVis( ['Leg_L_Switch_CTL','Leg_R_Switch_CTL'], followName.lower()+'Follow', True )
            else:
                cmds.checkBox( leg, e=1, v=0 )
                self.followAttrVis( ['Leg_L_Switch_CTL','Leg_R_Switch_CTL'], followName.lower()+'Follow', False )
    
                
    def setAllFollow( self, *args ):
        headChildrenLay = cmds.frameLayout( self.headFollow, q=1, ca=1 )
        collarChildrenLay = cmds.frameLayout( self.collarFollow, q=1, ca=1 )
        armChildrenLay = cmds.frameLayout( self.armFollow, q=1, ca=1 )
        legChildrenLay = cmds.frameLayout( self.legFollow, q=1, ca=1 )
        
        for head in headChildrenLay:
            followName = cmds.checkBox( head, q=1, l=1 )
            if cmds.checkBox( head, q=1, v=1 ):
                self.followAttrVis( ['Head_CTL'], followName.lower()+'Follow', True )
        
        for collar in collarChildrenLay:
            followName = cmds.checkBox( collar, q=1, l=1 )
            if cmds.checkBox( collar, q=1, v=1 ):
                self.followAttrVis( ['Collar_L_CTL','Collar_R_CTL'], followName.lower()+'Follow', True )
                
        for arm in armChildrenLay:
            followName = cmds.checkBox( arm, q=1, l=1 )
            if cmds.checkBox( arm, e=1, v=1 ):
                self.followAttrVis( ['Arm_L_Switch_CTL','Arm_R_Switch_CTL'], followName.lower()+'Follow', True )
                
        for leg in legChildrenLay:
            followName = cmds.checkBox( leg, q=1, l=1 )
            if cmds.checkBox( leg, e=1, v=1 ):
                self.followAttrVis( ['Leg_L_Switch_CTL','Leg_R_Switch_CTL'], followName.lower()+'Follow', True )