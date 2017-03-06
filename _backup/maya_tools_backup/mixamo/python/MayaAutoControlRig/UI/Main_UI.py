'''
UI.Main_UI
Handles:
    Creation of main UI
'''
import os
import maya.cmds as mayac
import maya.mel as mel
import Version_Info
import MayaAutoControlRig.DJB_Character as DJB_Character
from AssortedFunctions import *
import MayaAutoControlRig.Utils.General as General

FBXpluginLoaded = mayac.pluginInfo("fbxmaya", query = True, loaded = True)
if not FBXpluginLoaded:
    mayac.loadPlugin( "fbxmaya")

class MIXAMO_AutoControlRig_UI:
    def __init__(self):
        self.file1Dir = None
        self.name = "MIXAMO_AutoControlRig_UI"
        self.title = "MIXAMO Auto-Control-Rig v. %s" % (Version_Info.VERSION)

        # Begin creating the UI
        if (mayac.window(self.name, q=1, exists=1)): mayac.deleteUI(self.name)
        self.window = mayac.window(self.name, title=self.title, menuBar=True)
        
        #menu
        mayac.menu( label='Help', helpMenu=True )
        mayac.menuItem(l='Tutorials Site', command = lambda *args: goToWebpage("tutorials")) 
        mayac.menuItem( label='Bugs, Feature Requests, Confusions, Praise, Support', command = lambda *args: goToWebpage("community"))
        mayac.menuItem( label='About', command = self.showAboutWindow)
        
        
        #forms
        self.form = mayac.formLayout(w=650)
        mayac.columnLayout(adjustableColumn = True, w=650)
        mayac.text( label=' Thank you for trying the Mixamo Maya Auto-Control-Rig!', align='center' )
        mayac.text( label=' Please send Bugs, Feature Requests, Confusions, and/or Praise', align='center' )
        supportText = mayac.text( label=' to our community site.(Link in Help menu)', align='center' )
        mayac.popupMenu(parent=supportText, ctl=False, button=1) 
        
        mayac.menuItem(l='Go to community site', command = lambda *args: goToWebpage("community")) 
        mayac.text( label='', align='left' )
        happyAnimatingText = mayac.text( label='  Happy Animating! www.mixamo.com', align='center' )
        mayac.popupMenu(parent=happyAnimatingText, ctl=False, button=1) 
        mayac.menuItem(l='Go to Mixamo.com', command = lambda *args: goToWebpage("mixamo")) 
        mayac.text( label='', align='left' )
        
        
        mayac.setParent( '..' )
        
        self.tabs = mayac.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        self.layout = mayac.formLayout( self.form, edit=True, attachForm=((self.tabs, 'top', 90), (self.tabs, 'left', 0), (self.tabs, 'bottom', 0), (self.tabs, 'right', 0)) )
        
        #Rig Tab
        self.child1 = mayac.columnLayout(adjustableColumn = True)
        mayac.text( label='', align='left' )
        autoSkinnerText = mayac.text( label='  Import your downloaded MIXAMO character in Original Pose or T-Pose and then press the button below.', align='left' )
        mayac.popupMenu(parent=autoSkinnerText, ctl=False, button=1) 
        mayac.menuItem(l='Go to Mixamo Auto-Rigger webpage', command = lambda *args: goToWebpage("autoRigger"))
        self.setupControls_button = mayac.button(label='Rig Character', w=100, c=self.setupControls_function)
        
        mayac.separator( height=15, style='in' )
        mayac.text( label='Advanced Options', align='center' )
        mayac.text( label='The following option will change the base skeleton.', align='left')
        self.hulaOptionCheckBox = mayac.checkBox(label = 'Add Pelvis ("hula") Control', align='left' )
        mayac.separator( height=15, style='in' )
        
        mayac.text( label='Control Sizing Helper', align='center')
        '''mayac.text( label='  If the character has unusual proportions or large appendages, the button below will create a cube that you may scale to', align='center' )
        mayac.text( label='compensate for the unusual proportions.', align='center' )'''
        self.fakeBB_button = mayac.button(label='Create override Bounding Box', w=100, c=self.createOverrideBB_function)
        mayac.text( label='', align='left' )
        
        
        
        mayac.text( label='', align='left' )
        mayac.setParent( '..' )
        
        
        #Animate Tab
        self.child2 = mayac.columnLayout(adjustableColumn = True)
        mayac.text( label='', align='left' )
        mayac.text( label="**Please note that the animation data functionality is only designed to work with animations retargeted to your character's skeleton**", align='left' )
        mayac.text( label='', align='left' )
        mayac.text( label='', align='left' )
        animationText = mayac.text( label='  Apply downloaded MIXAMO animation to rig (will pop up file browser to choose animation file).', align='left' )
        mayac.popupMenu(parent=animationText, ctl=False, button=1) 
        mayac.menuItem(l='Go to Mixamo Motions webpage', command = lambda *args: goToWebpage("motions")) 
        mayac.button(label='Import Animation to Control Rig', w=100, c=self.importAnimation_function)
        #might want to bring the separated ability back at some point.  Simplifying interface
        '''self.browseMotions_button = mayac.button(label='Import Animation', w=100, c=self.browseMotions_function)
        mayac.text( label='', align='left' )
        mayac.text( label='  Select the "Hips" joint of the imported motion and then press the button below.', align='left' )
        mayac.button(label='Copy Animation to Rig (for imported animation)', w=100, c=self.copyAnimationToRig_function)
        mayac.text( label='', align='left' )
        mayac.button(label='Direct Connect Animation to Rig (for referenced animation)', w=100, c=self.connectAnimationToRig_function)'''
        mayac.text( label='', align='left' )
        mayac.text( label='', align='left' )
        mayac.text( label='Here you can bake the animation to the controls and/or revert to clean controls at any time.', align='center' )
        controlRigText = mayac.text( label="For more details see the documentation or www.mixamo.com/c/auto-control-rig-for-maya", align='center' )
        mayac.popupMenu(parent=controlRigText, ctl=False, button=1) 
        mayac.menuItem(l='Go to Auto-Control-Rig webpage', command = lambda *args: goToWebpage("autoControlRig")) 
        mayac.text( label='', align='left' )
        self.bakeAnimation_button = mayac.button(label='Bake Animation to Controls (imported anim only)', w=100, c=self.bakeAnimation_function)
        mayac.text( label='', align='left' )
        self.bakeAnimation_button = mayac.button(label='Clear Animation Controls (imported anim only)', w=100, c=self.clearAnimation_function)
        mayac.text( label='', align='left' )
        mayac.text( label='', align='left' )
        #auto-deleting original animation as part of simplification
        '''mayac.text( label='  Note: The original animation resides in the scene on its own layer until deleted.', align='left' )
        mayac.text( label='', align='left' )
        self.deleteOrigAnimation_button = mayac.button(label='Delete Original Animation (imported anim only)', w=100, c=self.deleteOrigAnimation_function)
        mayac.text( label='', align='left' )'''
        mayac.setParent( '..' )
        
        
        #Export Tab
        self.child3 = mayac.columnLayout(adjustableColumn = True)
        mayac.text( label='', align='left' )
        mayac.text( label='General Options', align='center')
        self.removeEndJointsCheckBox = mayac.checkBox(label = 'Remove End Joints', align='left')
        self.reduceNonEssentialJointsCheckBox = mayac.checkBox(label = 'Reduce Keyframes on Non-Essential Joints', align='left' )
        self.exportWithMeshOptionCheckBox = mayac.checkBox(label = 'Export Mesh with Skeleton*', align='left' )
        mayac.text( label='*Referenced rigs with facial blendshapes will not export correctly with mesh*', align='left')
        
        mayac.separator( height=15, style='in' )
        mayac.text( label='Dynamics Options', align='center')
        self.dynamicsFadeFramesSlider = mayac.intSliderGrp( field=True, label='Pose-Match Frame', minValue=0, maxValue=50, value=0, columnAttach3=("both","both","both"))
        mayac.separator( height=15, style='in' )
        self.exportBakedSkeleton_button = mayac.button(label='Export Baked Skeleton', w=100, c=self.exportBakedSkeleton_function)
        mayac.text( label='', align='left' )
        mayac.setParent( '..' )
        
        
        #Batch Tab
        self.child4 = mayac.columnLayout(adjustableColumn = True)
        mayac.text( label='', align='left' )
        mayac.text( label='**Note that Batching uses settings from the Rig and Export tabs**', align='left' )
        
        self.batchtabs = mayac.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        self.batchchild1 = mayac.columnLayout(adjustableColumn = True)
        mayac.text( label='', align='left' )
        self.batchImport_RigPath = mayac.textFieldButtonGrp( label='FBX or Control Rig File', text='', buttonLabel='Browse', buttonCommand = self.batchImport_RigPath_function)
        mayac.separator( height=15, style='in')
        mayac.text( label='Animation FBX files', align='center' )
        mayac.button(label = "Browse", w=15, c=self.batchImport_Animations_browse_function)
        mayac.button(label = "Select All", w=30, c=self.batchImport_Animations_selectAll_function)
        self.batchImport_Animations_ScrollField = mayac.textScrollList( numberOfRows=15, allowMultiSelection=True, height = 180)
        mayac.separator( height=15, style='in')
        self.batchImport_savePath_textFieldButtonGrp = mayac.textFieldButtonGrp( label='Finished Files Save Path', text='', buttonLabel='Browse', buttonCommand = self.batchImport_savePath_function)
        mayac.separator( height=15, style='in')
        mayac.text( label='', align='left' )
        mayac.button(label = "Batch Import", w=15, c=self.batchImport_function)

        mayac.setParent( '..' )
        self.batchchild2 = mayac.columnLayout(adjustableColumn = True)
        mayac.text( label='', align='left' )
        mayac.text( label='Animated Control Rig Files', align='center' )
        mayac.button(label = "Browse", w=15, c=self.batchExport_Animations_browse_function)
        mayac.button(label = "Select All", w=30, c=self.batchExport_Animations_selectAll_function)
        self.batchExport_Animations_ScrollField = mayac.textScrollList( numberOfRows=15, allowMultiSelection=True, height = 180)
        mayac.separator( height=15, style='in')
        self.batchExport_playblast_checkbox = mayac.checkBox(label="Playblast", v = True)
        self.batchExport_playblastPath_textFieldButtonGrp = mayac.textFieldButtonGrp( label='Playblast Save Path', text='', buttonLabel='Browse', buttonCommand = self.batchExport_playblastPath_function)
        mayac.separator( height=15, style='in' )
        self.batchExport_savePath_textFieldButtonGrp = mayac.textFieldButtonGrp( label='Export Path', text='', buttonLabel='Browse', buttonCommand = self.batchExport_savePath_function)
        mayac.text( label='', align='left' )
        self.batchButton = mayac.button(label = "Batch Export", w=15, c=self.batchExport_function)
        mayac.text( label='', align='left' )        
        mayac.setParent( '..' )
        mayac.setParent( '..' )
        mayac.setParent( '..' )
        

        #Utilities Tab
        self.child5 = mayac.columnLayout(adjustableColumn = True)
        mayac.text( label='', align='left' )
        mayac.text( label="If you've added a skinned mesh to your rig, ", align='center')
        mayac.text( label="the button below will let the system know about it for exports.", align='center' )
        self.batch_startFileOption = mayac.button(label='Remake Mesh Infonode', w=100, c=self.remakeMeshInfoNode_function)
        mayac.text( label='', align='left' )
        mayac.text( label="If you've added joints to your rig, ", align='center')
        mayac.text( label="select them and click the button below.", align='center' )
        self.makeExtraJointsInfoNode_button = mayac.button(label='Make Extra Joints Infonode from selection', w=100, c=self.makeExtraJointsInfoNode_function)
        mayac.text( label='', align='left' )
        mayac.text( label="If you've added joints that you wish to have dynamic, ", align='center')
        mayac.text( label="select them and click the button below for automatic followthrough.", align='center' )
        mayac.text( label="(powered by ZV Dynamics by Paolo Dominici)", align='center')
        self.makeDynamicChainRigFromSelection_button = mayac.button(label='Make Dynamic Chain Rig from selection', w=100, c=self.makeDynamicChainRigFromSelection_function)
        
        
        mayac.setParent( '..' )
        
        mayac.tabLayout( self.batchtabs, edit=True, tabLabel=((self.batchchild1, 'Batch Import'), (self.batchchild2, 'Batch Export')) )
        mayac.tabLayout( self.tabs, edit=True, tabLabel=((self.child1, 'Rig'), (self.child2, 'Animate'), (self.child3, 'Export'), (self.child4, 'Batching'), (self.child5, 'Utilities')) )
        mayac.window(self.window, e=1, w=650, h=575, sizeable = 0) #580,560
        mayac.showWindow(self.window)
            

    def showAboutWindow(self, arg = None):
        if (mayac.window("DJB_MACR_About", q=1, exists=1)): mayac.deleteUI("DJB_MACR_About")
        about_window = mayac.window("DJB_MACR_About", title="About %s" % (self.title))
        about_form = mayac.formLayout()
        about_tabs = mayac.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        about_layout = mayac.formLayout( about_form, edit=True, attachForm=((about_tabs, 'top', 0), (about_tabs, 'left', 0), (about_tabs, 'bottom', 0), (about_tabs, 'right', 0)) )
        #About Tab
        child1 = mayac.columnLayout(adjustableColumn = True)
        mayac.scrollField( editable=False, wordWrap=False, text= Version_Info.ABOUT_TEXT, h=450, w=750)
        mayac.setParent( '..' )
        #Changelog Tab
        child2 = mayac.columnLayout(adjustableColumn = True)
        mayac.scrollField( editable=False, wordWrap=False, text= Version_Info.CHANGELOG_TEXT, h=450, w=750)
        mayac.setParent( '..' )
        mayac.tabLayout( about_tabs, edit=True, tabLabel=((child1, 'General'), (child2, 'Changelog')) )
         
        mayac.window(about_window, e=1, w=650, h=450, sizeable = 0) #580,560
        mayac.showWindow(about_window)


    def createOverrideBB_function(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        if not DJB_CharacterInstance:
            oldCubes = mayac.ls("*Bounding_Box_Override_Cube*")
            if oldCubes:
                for cube in oldCubes:
                    if mayac.objExists(cube):
                        mayac.delete(cube)
            DJB_Character_ProportionOverrideCube = mayac.polyCube(n = "Bounding_Box_Override_Cube", ch = False)[0]
            
            #get default proportions
            mesh = []
            temp = mayac.ls(geometry = True)
            shapes = []
            for geo in temp:
                if "ShapeOrig" not in geo:
                    shapes.append(geo)
                    transform = mayac.listRelatives(geo, parent = True)[0]
            for geo in shapes:
                parent = mayac.listRelatives(geo, parent = True, path=True)[0]
                mesh.append(mayac.listRelatives(parent, children = True, type = "shape", path=True)[0])
            #place and lock up cube
            BoundingBox = mayac.exactWorldBoundingBox(mesh)
            mayac.move(BoundingBox[0], BoundingBox[1], BoundingBox[5], "%s.vtx[0]" % (DJB_Character_ProportionOverrideCube), absolute = True)
            mayac.move(BoundingBox[3], BoundingBox[1], BoundingBox[5], "%s.vtx[1]" % (DJB_Character_ProportionOverrideCube), absolute = True)
            mayac.move(BoundingBox[0], BoundingBox[4], BoundingBox[5], "%s.vtx[2]" % (DJB_Character_ProportionOverrideCube), absolute = True)
            mayac.move(BoundingBox[3], BoundingBox[4], BoundingBox[5], "%s.vtx[3]" % (DJB_Character_ProportionOverrideCube), absolute = True)
            mayac.move(BoundingBox[0], BoundingBox[4], BoundingBox[2], "%s.vtx[4]" % (DJB_Character_ProportionOverrideCube), absolute = True)
            mayac.move(BoundingBox[3], BoundingBox[4], BoundingBox[2], "%s.vtx[5]" % (DJB_Character_ProportionOverrideCube), absolute = True)
            mayac.move(BoundingBox[0], BoundingBox[1], BoundingBox[2], "%s.vtx[6]" % (DJB_Character_ProportionOverrideCube), absolute = True)
            mayac.move(BoundingBox[3], BoundingBox[1], BoundingBox[2], "%s.vtx[7]" % (DJB_Character_ProportionOverrideCube), absolute = True)
            pivotPointX = ((BoundingBox[3] - BoundingBox[0]) / 2) + BoundingBox[0]
            pivotPointY = BoundingBox[1]
            pivotPointZ = ((BoundingBox[5] - BoundingBox[2]) / 2) + BoundingBox[2]
            mayac.move(pivotPointX, pivotPointY, pivotPointZ, "%s.scalePivot" % (DJB_Character_ProportionOverrideCube), "%s.rotatePivot" % (DJB_Character_ProportionOverrideCube), absolute = True)
            mayac.setAttr("%s.tx" % (DJB_Character_ProportionOverrideCube),lock = True)
            mayac.setAttr("%s.ty" % (DJB_Character_ProportionOverrideCube),lock = True)
            mayac.setAttr("%s.tz" % (DJB_Character_ProportionOverrideCube),lock = True)
            mayac.setAttr("%s.rx" % (DJB_Character_ProportionOverrideCube),lock = True)
            mayac.setAttr("%s.ry" % (DJB_Character_ProportionOverrideCube),lock = True)
            mayac.setAttr("%s.rz" % (DJB_Character_ProportionOverrideCube),lock = True)
            
        else:
            OpenMaya.MGlobal.displayError("You must create and scale the override cube before rigging the character.")
        mayac.select(clear = True)
        
            
    def setupControls_function(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        if not DJB_CharacterInstance:
            joints = mayac.ls(type = "joint")
            if not joints:
                OpenMaya.MGlobal.displayError("There must be a Mixamo Autorigged character in the scene.")
            else:
                hulaValue = mayac.checkBox(self.hulaOptionCheckBox, query = True, value = True)
                DJB_CharacterInstance.append(DJB_Character.Character.DJB_Character(hulaOption_ = hulaValue))
        else:
            OpenMaya.MGlobal.displayError("There is already a rig in the scene")
        mayac.select(clear = True)
        
        
    def browseMotions_function(self, arg = None):
        mayac.Import()
    
    def connectAnimationToRig_function(self, arg = None):
        selection = mayac.ls(selection = True)
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        
        if not DJB_CharacterInstance:
            OpenMaya.MGlobal.displayError("You must rig a character first")
        elif len(selection) == 0 or mayac.nodeType(selection[0]) != "joint":
            OpenMaya.MGlobal.displayError("You must select the 'Hips' Joint of the imported animation")
        elif len(DJB_CharacterInstance) == 1:
            if DJB_CharacterInstance[0].Hips.Bind_Joint:
                isCorrectRig = DJB_CharacterInstance[0].checkSkeletonProportions(selection[0])
                if isCorrectRig:
                    DJB_CharacterInstance[0].connectMotionToAnimDataJoints(selection[0])
                else:
                    OpenMaya.MGlobal.displayError("Imported Skeleton does not match character!")
        else: #more than one character, spawn a choice window
            mayac.select(selection, r=True)
            ACR_connectAnimationToRigWindow()
        
        
    def importAnimation_function(self, arg=None, importFile = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        stuffInScene = mayac.ls()
        if not DJB_CharacterInstance:
            OpenMaya.MGlobal.displayError("You must rig a character first")
        if not importFile:
            importFile = mayac.Import()
        if importFile:
            mayac.file(importFile, i=True, force=True)
        stuffInSceneAfterImport = mayac.ls()
        #Did anything Import??  Probably cancelled if not
        if len(stuffInSceneAfterImport)-len(stuffInScene):
            allJoints = mayac.ls(type="joint")
            HipsJoint = None
            for joint in allJoints:
                if ("Hips" in joint or "Root" in joint) and "Bind" not in joint and "AnimData" not in joint and "IK_Dummy" not in joint:
                    HipsJoint = joint
                    break
            if not HipsJoint:
                OpenMaya.MGlobal.displayError("No compatible skeleton found in imported file.")
                return
            if len(DJB_CharacterInstance) == 1:
                if DJB_CharacterInstance[0].Hips.Bind_Joint:
                    isCorrectRig = DJB_CharacterInstance[0].checkSkeletonProportions(HipsJoint)
                    if isCorrectRig:
                        DJB_CharacterInstance[0].transferMotionToAnimDataJoints(HipsJoint, newStartTime = 0, mixMethod = "insert")
                        self.deleteOrigAnimation_function()
                    else:
                        OpenMaya.MGlobal.displayError("Imported Skeleton does not match character!")
            else: #more than one character, spawn a choice window
                mayac.select(HipsJoint, r=True)
                ACR_copyAnimationToRigWindow()
                self.deleteOrigAnimation_function()
        
        
          
    def copyAnimationToRig_function(self, arg = None):
        selection = mayac.ls(selection = True)
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        
        if not DJB_CharacterInstance:
            OpenMaya.MGlobal.displayError("You must rig a character first")
        elif len(selection) == 0 or mayac.nodeType(selection[0]) != "joint":
            OpenMaya.MGlobal.displayError("You must select the 'Hips' Joint of the imported animation")
        elif len(DJB_CharacterInstance) == 1:
            if DJB_CharacterInstance[0].Hips.Bind_Joint:
                isCorrectRig = DJB_CharacterInstance[0].checkSkeletonProportions(selection[0])
                if isCorrectRig:
                    DJB_CharacterInstance[0].transferMotionToAnimDataJoints(selection[0], newStartTime = 0, mixMethod = "insert")
                else:
                    OpenMaya.MGlobal.displayError("Imported Skeleton does not match character!")
        else: #more than one character, spawn a choice window
            mayac.select(selection, r=True)
            ACR_copyAnimationToRigWindow()
            
    def deleteOrigAnimation_function(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        if not DJB_CharacterInstance:
            OpenMaya.MGlobal.displayError("No Character Found!")
        else:
            if DJB_CharacterInstance[0].origAnim:
                DJB_CharacterInstance[0].deleteOriginalAnimation()
            else:
                OpenMaya.MGlobal.displayError("No Original Animation Found!")
            
    def bakeAnimation_function(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        if DJB_CharacterInstance:
            DJB_CharacterInstance[0].bakeAnimationToControls()
        else:
            OpenMaya.MGlobal.displayError("No Character Found!")
        
    def clearAnimation_function(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        if DJB_CharacterInstance:
            DJB_CharacterInstance[0].clearAnimationControls()
        else:
            OpenMaya.MGlobal.displayError("No Character Found!")
                     
    def exportBakedSkeleton_function(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        if DJB_CharacterInstance:
            keepMesh = mayac.checkBox(self.exportWithMeshOptionCheckBox, query = True, value = True)
            reduce = mayac.checkBox(self.reduceNonEssentialJointsCheckBox, query = True, value = True)
            removeEndJoints = mayac.checkBox(self.removeEndJointsCheckBox, query = True, value = True)
            dynamicsFadeFrames = mayac.intSliderGrp(self.dynamicsFadeFramesSlider, query = True, value = True)
            DJB_CharacterInstance[0].createExportSkeleton(keepMesh_ = keepMesh, dynamicsToFK = dynamicsFadeFrames, reduceNonEssential = reduce, removeEndJoints = removeEndJoints)
            if arg:
                DJB_CharacterInstance[0].exportSkeleton(arg)
            else:
                DJB_CharacterInstance[0].exportSkeleton()
            version = mel.eval("float $ver = `getApplicationVersionAsFloat`;")
            if version != 2010.0:
                DJB_CharacterInstance[0].deleteExportSkeleton()
            if version == 2010.0:
                OpenMaya.MGlobal.displayInfo("You may delete the newly created geometry and joints after exporting is complete")
        else:
            OpenMaya.MGlobal.displayError("No Character Found!")
     
     
    def remakeMeshInfoNode_function(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        if DJB_CharacterInstance:
            DJB_CharacterInstance[0].remakeMeshInfoNode()
        else:
            OpenMaya.MGlobal.displayError("No Character Found!")   
    
    
    def makeExtraJointsInfoNode_function(self, arg = None):
        sel = mayac.ls(sl=True)
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        if DJB_CharacterInstance:
            if sel:
                DJB_CharacterInstance[0].makeExtraJointsInfoNode(sel)
            else:
                OpenMaya.MGlobal.displayError("Extra Joints Must Be Selected!")  
        else:
            OpenMaya.MGlobal.displayError("No Character Found!")  
            
    def makeDynamicChainRigFromSelection_function(self, arg = None):
        sel = mayac.ls(sl=True)
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        
        if DJB_CharacterInstance:
            if sel:
                for cur in sel:
                    mayac.select(cur, replace = True)
                    mayac.select(hierarchy = True)
                    chain = mayac.ls(sl=True)
                    DJB_CharacterInstance[0].makeDynamicChainRig(chain, dynamic_ = "ZV", control_ = "FK") #need to add checks for eligible joint chain
            else:
                OpenMaya.MGlobal.displayError("Eligible Joints Must Be Selected!")
        else:
            OpenMaya.MGlobal.displayError("No Character Found!")
    def batchImport_function(self, arg=None):
        rigFile = mayac.textFieldButtonGrp(self.batchImport_RigPath, q=True, text=True)
        savePath = mayac.textFieldButtonGrp(self.batchImport_savePath_textFieldButtonGrp, q=True, text=True)
        if not rigFile:
            mayac.error("Please supply control rig file.")
            return
        charName, fileExtension = os.path.splitext(os.path.basename(rigFile))
        if not savePath:
            savePath = validateFolder(os.path.join(self.importFileDir,"%s_Batch"%charName), create=True)
        filesShort = mayac.textScrollList(self.batchImport_Animations_ScrollField, query = True, selectItem = True)
        if not filesShort:
            mayac.error("Please select animation files to batch.")
        #iterate through top level files
        for file in filesShort:
            mayac.file(new=True, force=True)
            fileName, fileExtension = os.path.splitext(file)
            file = os.path.join(self.importFileDir, file)
            #open rig file...may not be rigged
            mayac.file( rigFile, o=True, force = True )
            DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
            #if no rig, rig and save temprig
            if not DJB_CharacterInstance:
                joints = mayac.ls(type = "joint")
                if not joints:
                    OpenMaya.MGlobal.displayError("There must be a Mixamo Autorigged character in the Control Rig File field.")
                else:
                    hulaValue = mayac.checkBox(self.hulaOptionCheckBox, query = True, value = True)
                    DJB_CharacterInstance.append(DJB_Character.Character.DJB_Character(hulaOption_ = hulaValue))
                    rigFile =  os.path.join(savePath, charName+"_ControlRig.ma")
                    mayac.file( rename=rigFile)
                    mayac.file( save=True, type='mayaAscii' )
            #import and apply animation
            self.importAnimation_function(self, importFile = file)
            #save or bake and export
            saveFile = os.path.join(savePath,"%s.ma"%fileName)
            mayac.file( rename= saveFile )
            mayac.file( save=True, type='mayaAscii', force=True )
            OpenMaya.MGlobal.displayInfo("Process Complete.  Saved all files to %s"%savePath)
            


    def batchImport_RigPath_function(self, arg=None):
        path = DJB_BrowserWindow(filter_ = "Maya_FBX", caption_ = "Browse for playblast folder", fileMode_ = "File")
        if path:
            mayac.textFieldButtonGrp(self.batchImport_RigPath, edit = True, text = path)
        else:
            mayac.textFieldButtonGrp(self.batchImport_RigPath, edit = True, text = "")
    def batchImport_Animations_browse_function(self, arg = None):
        self.importFileDir = path = DJB_BrowserWindow(filter_ = "FBX", caption_ = "Browse for character files directory", fileMode_ = "directory")
        filesRaw = os.listdir(path)
        filesRaw.sort()
        mayac.textScrollList(self.batchImport_Animations_ScrollField, edit = True, removeAll = True)
        for file in filesRaw:
            if ".fbx" in file:
                mayac.textScrollList(self.batchImport_Animations_ScrollField, edit = True, append = file)
    def batchImport_Animations_selectAll_function(self, arg = None):
        allItems = mayac.textScrollList(self.batchImport_Animations_ScrollField, query = True, allItems = True)
        if not allItems:
            OpenMaya.MGlobal.displayError("Nothing to select")
        else:
            for item in allItems:
                mayac.textScrollList(self.batchImport_Animations_ScrollField, edit = True, selectItem = item)
    def batchImport_savePath_function(self, arg=None):   
        savePath = DJB_BrowserWindow(filter_ = None, caption_ = "Browse for save folder", fileMode_ = "directory")
        if savePath:
            mayac.textFieldButtonGrp(self.batchImport_savePath_textFieldButtonGrp, edit = True, text = savePath)
        else:
            mayac.textFieldButtonGrp(self.batchImport_savePath_textFieldButtonGrp, edit = True, text = "")
    
    
    def batchExport_function(self, arg = None):
        #get all options
        savePath = mayac.textFieldButtonGrp(self.batchExport_savePath_textFieldButtonGrp, q=True, text=True)
        if not savePath:
            savePath = validateFolder(os.path.join(self.exportFileDir,"Batch"), create=True)
        filesShort = mayac.textScrollList(self.batchExport_Animations_ScrollField, query = True, selectItem = True)
        if not filesShort:
            mayac.error("Please select animation files to batch.")
        keepMesh = mayac.checkBox(self.exportWithMeshOptionCheckBox, query = True, value = True)
        blastPath = mayac.textFieldButtonGrp(self.batchExport_playblastPath_textFieldButtonGrp, query = True, text = True)
        if not blastPath:
            blastPath = validateFolder(os.path.join(savePath,"Playblasts"), create=True)
        
        #iterate through top level files
        for file in filesShort:
            fileName, fileExtension = os.path.splitext(file)
            file = os.path.join(self.exportFileDir, file)
            #open top level
            mayac.file( file, o=True, force = True )
            #if rig replace
            '''rigReplace = mayac.checkBox(self.batch_replaceRigReference_checkbox, query = True, value = True)
            references = None
            if rigReplace:
                references=mayac.file(q=True, reference = True)[0]
            if references:
                ref = mayac.referenceQuery(references, rfn = True)
                newRef = mayac.textFieldButtonGrp(self.batch_replaceRigReference_textFieldButtonGrp, query = True, text = True)
                if ".ma" in newRef:
                    mayac.file(newRef, loadReference = ref, type = "mayaAscii", options = ("v=0"))
                else:
                    mayac.file(newRef, loadReference = ref, type = "mayaBinary", options = ("v=0"))'''
            
            #save or bake and export
            DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
            if not DJB_CharacterInstance:
                mayac.error("No Control Rig found in scene.")
                return
            saveFile = os.path.join(savePath,fileName).replace("\\","/")
            for i in range(0,10):
                mayac.currentTime( i, edit=True )
            mayac.currentTime( 0, edit=True )
            self.exportBakedSkeleton_function(arg = saveFile)
            playblast = mayac.checkBox(self.batchExport_playblast_checkbox, query = True, value = True)
            if playblast:
                controlLayer = General.DJB_addNameSpace(DJB_CharacterInstance[0].characterNameSpace, "ControlLayer")
                mayac.setAttr("%s.visibility" %(controlLayer), 1)
                for i in range(0,10):
                    mayac.currentTime( i, edit=True )
                mayac.currentTime( 0, edit=True )
                
                blastFile = os.path.join(blastPath,fileName).replace("\\","/")
                mayac.setAttr("persp.tx",-0.358)
                mayac.setAttr("persp.ty",86.261)
                mayac.setAttr("persp.tz",503.388)
                mayac.setAttr("persp.rx",-.338)
                mayac.setAttr("persp.ry",-2.4)
                mayac.setAttr("persp.rz",0)
                mayac.setAttr("perspShape.farClipPlane", 100000)
                mayac.setAttr("perspShape.nearClipPlane", 100)
                #viewport = mayac.getPanel( withFocus = True)
                mayac.modelEditor( "modelPanel4", edit=True, 
                                   camera="persp", rnm="base_OpenGL_Renderer", 
                                   nurbsCurves=False, joints=False, cameras=False, 
                                   grid=False, ikh=False, deformers=False, 
                                   dynamics=False, nParticles = False, follicles=False, 
                                   locators=False, activeView=True, 
                                   displayAppearance='smoothShaded', displayTextures=True )
                mel.eval('playblast  -format avi -filename "%s" -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 0 -offScreen  -fp 4 -percent 100 -compression "XVID" -quality 70 -widthHeight 1280 720;'%(blastFile))
        OpenMaya.MGlobal.displayInfo("Process Complete.  Exported files to %s"%savePath)
        
    def batchExport_Animations_browse_function(self, arg = None):
        self.exportFileDir = path = DJB_BrowserWindow(filter_ = "FBX", caption_ = "Browse for character files directory", fileMode_ = "directory")
        filesRaw = os.listdir(path)
        filesRaw.sort()
        mayac.textScrollList(self.batchExport_Animations_ScrollField, edit = True, removeAll = True)
        for file in filesRaw:
            if ".ma" in file or ".mb" in file:
                mayac.textScrollList(self.batchExport_Animations_ScrollField, edit = True, append = file)
    def batchExport_Animations_selectAll_function(self, arg = None):
        allItems = mayac.textScrollList(self.batchExport_Animations_ScrollField, query = True, allItems = True)
        if not allItems:
            OpenMaya.MGlobal.displayError("Nothing to select")
        else:
            for item in allItems:
                mayac.textScrollList(self.batchExport_Animations_ScrollField, edit = True, selectItem = item)   
    '''def batch_replaceRigReferencePath_function(self, arg = None):
        replaceRigReferencePath = DJB_BrowserWindow(filter_ = "Maya", caption_ = "Browse for rig reference replacement", fileMode_ = "Maya")
        if replaceRigReferencePath:
            mayac.textFieldButtonGrp(self.batch_replaceRigReference_textFieldButtonGrp, edit = True, text = replaceRigReferencePath)
        else:
            mayac.textFieldButtonGrp(self.batch_replaceRigReference_textFieldButtonGrp, edit = True, text = "")'''
    def batchExport_playblastPath_function(self, arg = None):
        playblastPath = DJB_BrowserWindow(filter_ = None, caption_ = "Browse for playblast folder", fileMode_ = "directory")
        if playblastPath:
            mayac.textFieldButtonGrp(self.batchExport_playblastPath_textFieldButtonGrp, edit = True, text = playblastPath)
        else:
            mayac.textFieldButtonGrp(self.batchExport_playblastPath_textFieldButtonGrp, edit = True, text = "")
    def batchExport_savePath_function(self, arg = None):
        savePath = DJB_BrowserWindow(filter_ = None, caption_ = "Browse for export folder", fileMode_ = "directory")
        if savePath:
            mayac.textFieldButtonGrp(self.batchExport_savePath_textFieldButtonGrp, edit = True, text = savePath)
        else:
            mayac.textFieldButtonGrp(self.batchExport_savePath_textFieldButtonGrp, edit = True, text = "")
          

class ACR_connectAnimationToRigWindow:
    def __init__(self):
        self.file1Dir = None
        self.name = "Connect Animation to Rig"
        self.title = "Connect Animation to Rig"

        # Begin creating the UI
        if (mayac.window(self.name, q=1, exists=1)): 
            mayac.deleteUI(self.name)
        self.window = mayac.window(self.name, title=self.title, menuBar=True)
        #forms
        self.form = mayac.formLayout(w=650)
        mayac.columnLayout(adjustableColumn = True, w=650)
        mayac.text( label='', align='left' )
        self.characters_ScrollList = mayac.textScrollList( numberOfRows=5, allowMultiSelection=False)
        mayac.separator( height=40, style='in' )
        mayac.text( label='', align='left' )
        self.batchButton = mayac.button(label = "Connect Animation to selected Character", w=15, c=self.connectFunction)
        mayac.text( label='', align='left' )
        
        self.populateScrollField()
        mayac.window(self.window, e=1, w=650, h=515, sizeable = 1) #580,560
        mayac.showWindow(self.window)
        
    def populateScrollField(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        for char in DJB_CharacterInstance:
            mayac.textScrollList(self.characters_ScrollList, edit = True, append = char.name)
        mayac.textScrollList(self.characters_ScrollList, edit=True, selectIndexedItem = 1)
        
    def connectFunction(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        selection = mayac.ls(sl=True)
        selectedIndex = mayac.textScrollList(self.characters_ScrollList, query=True, selectIndexedItem = True)
        #print selectedIndex
        
        DJB_CharacterInstance[selectedIndex[0]-1].connectMotionToAnimDataJoints(selection[0])
        
class ACR_copyAnimationToRigWindow():
    def __init__(self):
        self.file1Dir = None
        self.name = "Copy Animation to Rig"
        self.title = "Copy Animation to Rig"

        # Begin creating the UI
        if (mayac.window(self.name, q=1, exists=1)): 
            mayac.deleteUI(self.name)
        self.window = mayac.window(self.name, title=self.title, menuBar=True)
        #forms
        self.form = mayac.formLayout(w=650)
        mayac.columnLayout(adjustableColumn = True, w=650)
        mayac.text( label='', align='left' )
        self.characters_ScrollList = mayac.textScrollList( numberOfRows=5, allowMultiSelection=False)
        mayac.separator( height=40, style='in' )
        mayac.text( label='', align='left' )
        self.batchButton = mayac.button(label = "Copy Animation to selected Character", w=15, c=self.copyFunction)
        mayac.text( label='', align='left' )
        
        self.populateScrollField()
        mayac.window(self.window, e=1, w=650, h=515, sizeable = 1) #580,560
        mayac.showWindow(self.window)
    def populateScrollField(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        for char in DJB_CharacterInstance:
            mayac.textScrollList(self.characters_ScrollList, edit = True, append = char.name)
        mayac.textScrollList(self.characters_ScrollList, edit=True, selectIndexedItem = 1)
        
    def copyFunction(self, arg = None):
        DJB_CharacterInstance = DJB_Character.Character.createCharacterClassInstance()
        selection = mayac.ls(sl=True)
        selectedIndex = mayac.textScrollList(self.characters_ScrollList, query=True, selectIndexedItem = True)
        DJB_CharacterInstance[selectedIndex[0]-1].transferMotionToAnimDataJoints(selection[0], newStartTime = 0, mixMethod = "insert")
        
if __name__ == "__main__":
    DJB_MIX_ACS_UI = MIXAMO_AutoControlRig_UI()