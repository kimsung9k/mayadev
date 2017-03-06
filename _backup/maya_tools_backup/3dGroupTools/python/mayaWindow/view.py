import maya.cmds as cmds
from model import *
import basic.naming.cmdModel as naming
import basic.skinCluster.cmdModel as skinCluster
import skinCluster.cmdModel as skinCluster2
import basic.controller.cmdModel as controller
import animation.buildCache.cmdModel as buildCache
import animation.importCache.cmdModel as importCache
import finalize.cmdModel as finalize
import animation.cmdModel as animationCmd
import deformer.cmdModel as deformer
import shading.waveLengthCtlCreate.cmdModel as vray
import shading.texture.cmdModel as texture
import shading.cmdModel as shading
import modeling.cmdModel as modeling
import character.dummy.cmdModel as dummyCharacter
import splineRig.cmdModel as splineRig
import fileManager.cmdModel as fileManager
import rigObject.cmdModel as rigObject
import commTeamCostomApp.view as commTeamCostomAppView
import markingMenu.control as markingMenuCtl
import confirm.cmdModel as confirm
import volumeHairTool.ui
import projectFunction.towerOfGod.view as towerOfGodProjFunctionView
import projectFunction.yetiTool.view as yetiToolView
import curve.cmdModel as rigCurve
import sgRigCurve
import sgUIMeshIntersect
import sgUISetAttr
import sgRigController
import sgUIBlendShapeConnectWidthController
import sgRigConnection
import hgCameraBake
import sgRigMesh
import sgRigOptimize
import sgUIsgWobbleCurve
import sgUIMakeCurveDynamic
import sgUICurve_createJoint
import sgRigDag
import sgUISceneBake
import sgRigConnection
import sgFunctionClean
import sgBFunction_scene
import sgPWindow_file_mesh_export
import sgPWindow_file_mesh_import
import sgPWindow_set_joint
import sgPWindow_file_mesh_exportGroup
import sgPWindow_file_mesh_importGroup
import sgPWindow_file_key_export
import sgPWindow_file_key_import
import sgPWindow_file_cache_export
import sgPWindow_file_cache_import
import sgPWindow_file_sceneBakeInfo_export
import sgPWindow_file_sceneBakeInfo_import
import sgPWindow_file_keyAndCache_export
import sgPWindow_file_camera_export
import sgUI_characterBake
import sgBFunction_mesh
import sgPWindow_set_jointNum


from functools import partial



class UIFunctions:
    
    
    def __init__(self):
        
        cmds.setParent( M3DGroupUIInfo._uiName, menu=1 )
    
    
    def dividerMain(self, dividerLabel = '' ):
        
        cmds.setParent( M3DGroupUIInfo._uiName, menu=1 )
        if dividerLabel:
            try:cmds.menuItem( d=1, dl=dividerLabel )
            except:cmds.menuItem( d=1 )
        else:
            cmds.menuItem( d=1 )
    
    def divider(self, dividerLabel='' ):
        
        if dividerLabel:
            try:
                cmds.menuItem( d=1, dl=dividerLabel )
            except:cmds.menuItem( d=1 )
        else:
            cmds.menuItem( d=1 )



class NamingUI( UIFunctions ):
    
    def __init__(self):

        UIFunctions.__init__(self)
        cmds.menuItem( l='Naming', sm=1, to=1  )
        cmds.menuItem( l='Name Numbering UI', c=naming.mmShowNumberingUI )
        cmds.menuItem( l='Name Replace UI',   c=naming.mmShowReplaceNameUI )
        cmds.menuItem( l='Remove Namespace SelH', c=naming.mmRemoveNamespaceSelH )
        cmds.menuItem( l='Rename Shape Selected', c=naming.mmRenameShapeSelected )



class AnimationUI(UIFunctions):
    
    def __init__(self):
        
        UIFunctions.__init__(self)
        cmds.menuItem( l='Animation', sm=1, to=1 )
        cmds.menuItem( l='' )
        self.divider( "Virtual AD" )
        cmds.menuItem( l='Open Virtual AD Tool', c=animationCmd.uiCmd_OpenVirtualAdTool )
        self.divider( "View" )
        cmds.menuItem( l='Create Model Pannel', c=animationCmd.uiCmd_OpenModelPanel )



class OptimizeUI(UIFunctions):
    
    def __init__(self):
        UIFunctions.__init__(self)
        cmds.menuItem( l='Optimize', sm=1, to=1 )
        
        cmds.menuItem( l='Clean Mesh', c= sgBFunction_scene.mc_cleanMesh )
        cmds.menuItem( l="Clean UV Sets", c= sgBFunction_mesh.mc_cleanUVSets )
        cmds.menuItem( l='Delete Unused', c= sgRigOptimize.mc_deleteUnused )
        
        self.divider()
        
        cmds.menuItem( l='Delete Unknown', c= sgFunctionClean.mc_deleteUnknown )
        cmds.menuItem( l='Delete Turtle', c= sgBFunction_scene.mc_turtleClear )
        
        self.divider( "Delete SG Nodes" )
        
        cmds.menuItem( l='Delete Sg Nodes', c= sgFunctionClean.mc_deleteSgNodes )



class FinalizeUI(UIFunctions):
    
    def __init__(self):
        
        UIFunctions.__init__(self)
        cmds.menuItem( l='Finalize', sm=1, to=1 )
        
        cmds.menuItem( l='UI Import Cache', c=finalize.uiCmd_OpenImportCacheUI )
        cmds.menuItem( l='UI Build Cache( stand alone )', c=finalize.uiCmd_OpenBuildCacheUI )
        cmds.menuItem( l='UI Character Bake', c= sgUI_characterBake.mc_showWindow )
        cmds.menuItem( l='UI SCene Bake', c=sgUISceneBake.mc_showWindow )
        
        self.divider( "Export New" )
        cmds.menuItem( l='Export Camera',     c= sgPWindow_file_camera_export.mc_showWindow )
        cmds.menuItem( l='Export Mesh Group', c= sgPWindow_file_mesh_exportGroup.mc_showWindow )
        cmds.menuItem( l='Export Key',        c= sgPWindow_file_key_export.mc_showWindow )
        cmds.menuItem( l='Export Cache',      c= sgPWindow_file_cache_export.mc_showWindow )
        cmds.menuItem( l='Export Key And Cache', c= sgPWindow_file_keyAndCache_export.mc_showWindow )
        cmds.menuItem( l='Export Scene Bake Info', c= sgPWindow_file_sceneBakeInfo_export.mc_showWindow )
        
        self.divider( "Import New" )
        cmds.menuItem( l='Import Mesh Group', c= sgPWindow_file_mesh_importGroup.mc_showWindow )
        cmds.menuItem( l="Import Key", c= sgPWindow_file_key_import.mc_showWindow )
        cmds.menuItem( l='Import Cache',      c= sgPWindow_file_cache_import.mc_showWindow )
        cmds.menuItem( l='Import Scene Bake Info', c= sgPWindow_file_sceneBakeInfo_import.mc_showWindow )
        
        self.divider( "Other Method" )
        cmds.menuItem( l='Combine Mesh Safety', c='import maya.mel as mel; mel.eval( "_combineMesh" )' )
        



class Modeling(UIFunctions):
    
    def __init__(self):
        
        UIFunctions.__init__(self)
        cmds.menuItem( l='Modeling', sm=1, to=1 )

        cmds.menuItem( l='Open Smooth Mark UI', c=modeling.uiCmd_OpenSubTagingUI )
        cmds.menuItem( l='Create Sliding Deformer', c=deformer.uiCmd_createSlidingDeformer )
        self.divider("Polygon")
        cmds.menuItem( l='Export Mesh UI', c= sgPWindow_file_mesh_export.mc_showWindow )
        cmds.menuItem( l='Import Mesh UI', c= sgPWindow_file_mesh_import.mc_showWindow )
        self.divider("Polygon Group")
        cmds.menuItem( l='Export Mesh Group UI', c= sgPWindow_file_mesh_exportGroup.mc_showWindow )
        cmds.menuItem( l='Import Mesh Group UI', c= sgPWindow_file_mesh_importGroup.mc_showWindow )
        




class UserUpdateCodeUI(UIFunctions):

    def __init__(self):
        
        UIFunctions.__init__(self)
        cmds.menuItem( l='User Update APP', sm=1, to=1 )
        
        cmds.menuItem( l='Update APP UI', c=commTeamCostomAppView.mc_checkIdAndOpenWindow )
        self.divider()
        #cmds.menuItem( l='Show User Update App', c=commTeamCostomAppView.MayaMenu().create )
        cmds.menuItem( l='Show User Update App', c=commTeamCostomAppView.mc_showUserSetupMenu )
        cmds.menuItem( l='Category Editor', c=commTeamCostomAppView.mc_showCategoryEditor )
        cmds.menuItem( l='Id Editor', c=commTeamCostomAppView.mc_showIdEditor )

        
        

class AttributeUI(UIFunctions):
    
    def __init__(self):
        
        UIFunctions.__init__(self)
        cmds.menuItem( l='Attribute', sm=1, to=1 )
        
        cmds.menuItem( l='UI Set Attribute', c= sgUISetAttr.mc_showWindow  )


        
class MatchMoveUI(UIFunctions):

    def __init__(self):

        UIFunctions.__init__(self)
        cmds.menuItem( l='Match Move', sm=1, to=1 )
        cmds.menuItem( l='UI Create Mesh Intersect Object', c= sgUIMeshIntersect.mc_showWindow )




class RiggingUI(UIFunctions):
    
    def __init__(self):
        
        UIFunctions.__init__(self)
        cmds.menuItem( l='Rigging', sm=1, to=1 )
        cmds.menuItem( l='' )
        self.divider( "Joint" )
        cmds.menuItem( l="Joint Position Slider", c= sgPWindow_set_joint.mc_showWindow )
        self.divider( "Skin Cluster" )
        cmds.menuItem( l='Skin Cluster Edit UI', c=skinCluster.mmShowSkinWeightEditUI )
        cmds.menuItem( l='Replace Object Skined', c=skinCluster2.mc_replaceObjectSkined )
        self.divider( "Controller" )
        cmds.menuItem( l='Build Controller UI', c=controller.mc_OpenBuildControllerUI )
        cmds.menuItem( l='Color Override UI', c=controller.mc_OpenColorOverride )
        cmds.menuItem( l='Combine Multi Curve Shapes', c=sgRigController.mc_combineMultiShapes )
        self.divider( "Rig Object" )
        cmds.menuItem( l='Open Create Aim Object UI', c=rigObject.uiCmd_OpenCreateAimObjectUI )
        cmds.menuItem( l='Create Middle Joint UI', c=rigObject.uiCmd_OpenCreateMiddleJointUI )
        cmds.menuItem( l='Open Mesh Rivet UI', c=rigObject.uiCmd_OpenMeshRivetUI )
        self.divider( "Curve" )
        cmds.menuItem( l='Create Point On Curve', c=sgRigCurve.mc_createPointOnCurve )
        cmds.menuItem( l='Create Curve On Selected Points', c=sgRigCurve.mc_createCurveOnTargetPoints )
        cmds.menuItem( l='Create Curve On Selected Joints', c=sgRigCurve.mc_createCurveOnSelJoints )
        cmds.menuItem( l='Create Bend To Curve', c=sgRigCurve.mc_createBendToCurve )
        cmds.menuItem( l='UI Create Sg Wobble Curve', c=sgUIsgWobbleCurve.mc_showWindow )
        cmds.menuItem( l='UI Make Curve Dynamic', c=sgUIMakeCurveDynamic.mc_showWindow )
        cmds.menuItem( l='UI Create Joint On Curve', c=sgUICurve_createJoint.mc_showWindow )
        self.divider( "Connection" )
        cmds.menuItem( l='UI Blend Shape Connect Width Controller', c=sgUIBlendShapeConnectWidthController.mc_showWindow )
        cmds.menuItem( l='Copy Attr And Connect', c=sgRigConnection.mc_copyAttributeAndConnect )
        cmds.menuItem( l='Set Orig Normal Soft', c=sgRigMesh.mc_setOrigNormalSoft )
        self.divider( "Transform" )
        cmds.menuItem( l='Set Matrix To Target', c=sgRigDag.mc_setMatrixToTarget )
        cmds.menuItem( l='Duplicate Object To Target', c=sgRigDag.mc_duplicateObjectToTarget )
        cmds.menuItem( l='Replace Object', c=sgRigDag.mc_replaceObject )




class CharacterUI(UIFunctions):
    
    def __init__(self):
        UIFunctions.__init__(self)
        cmds.menuItem( l='Character', sm=1, to=1 )
        
        fileList = dummyCharacter.getFileList()
        for i in range( len( fileList ) ):
            cmds.menuItem( l=fileList[i], c= partial( dummyCharacter.mmOpenDummyCharacter, i ) )





class ShadingUI(UIFunctions):
    
    def __init__(self):
        
        UIFunctions.__init__(self)
        cmds.menuItem( l='Shading', sm=1, to=1 )
        cmds.menuItem( l='Wave Length Ctl Create UI', c=shading.uiCmd_OpenWaveLengthCtlCreate )
        cmds.menuItem( l='File Texture Manager UI', c=texture.mc_OpenFileTextureManager )
        cmds.menuItem( l='Open Make Shader As Reference UI', c=shading.uiCmd_OpenMakeShadderAsReference )
        cmds.menuItem( l='Vray Proxy Controller Source', c=shading.uiCmd_OpenVrayProxyControllerSource )
        self.divider( 'Copy Shader' )
        cmds.menuItem( l='Copy Shader', c=sgRigConnection.mc_copyShader )
        cmds.menuItem( l='Copy Shader Hierarchy', c=sgRigConnection.mc_copyShaderHierarchy )
        




class HairUI(UIFunctions):
    
    def __init__(self):
        
        import sgBRig_hair
        import sgBFunction_hair
        import sgPWindow_curve_sgWobbleCurve
        
        UIFunctions.__init__(self)
        cmds.menuItem( l='Hair', sm=1, to=1 )
        
        cmds.menuItem( l='HSBVC Tool', c=volumeHairTool.ui.mc_showHSBVCTool )
        cmds.menuItem( l='Build Curve Based On Mesh', c=towerOfGodProjFunctionView.mc_showWindow )
        cmds.menuItem( l='Yeti View', c=yetiToolView.mc_showWindow )
        
        self.divider( 'Joint Part' )
        cmds.menuItem( l="Tool Create Joint On Mesh", c=sgBRig_hair.setTool_createJointOnMesh )
        cmds.menuItem( l="UI Create Joint Line", c=sgBRig_hair.showUi_createJointLineOnMesh )
        cmds.menuItem( l="UI Create Joint Line2", c=sgBRig_hair.showUi_createJointLineOnMesh2 )
        cmds.menuItem( l="UI Set Joint Num", c=sgPWindow_set_jointNum.mc_showWindow )
        cmds.menuItem( l="UI Create Joint On Curve", c=sgBRig_hair.showUi_createJointOnCurve )
        cmds.menuItem( l="Make Control Joints", c=sgBRig_hair.mc_makeControlJointOnCurve )
        cmds.menuItem( l="Create Editable Joints", c=sgBRig_hair.mc_createEditableJoints )
        self.divider( "Curve Part" )
        cmds.menuItem( l="Make Curve From Joint", c=sgBRig_hair.mc_createCurveFromJoint )
        cmds.menuItem( l="Create Curve On Line Mesh", c=sgBRig_hair.mc_createCurveOnLineMesh )
        cmds.menuItem( l='Set Center Curve Rig', c=sgBRig_hair.mc_setCurvesAsRadiusCurve )
        cmds.menuItem( l="Cut Curve By Mesh", c=sgBRig_hair.mc_cutCurveByCutInfo )
        self.divider( "Simulation Part" )
        cmds.menuItem( l="Create Follicle By CutInfo", c=sgBRig_hair.mc_createFollicleByCutInfo )
        cmds.menuItem( l="UI SG Wobble Curve", c= sgPWindow_curve_sgWobbleCurve.mc_showWindow )
        cmds.menuItem( l="UI Dynamic Curve", c= sgBRig_hair.showUi_createDynamicCurve )
        cmds.menuItem( l="Set Simulation Transform Mult", c=sgBRig_hair.mc_setSimulationTransformMult )
        
        




class FileManagerUI(UIFunctions):
    
    def __init__(self):
        
        UIFunctions.__init__(self)
        cmds.menuItem( l='File Manager', sm=1, to=1 )
        cmds.menuItem( l='Asset Reference', c=fileManager.openAssetReference_ui )
        cmds.menuItem( l='Recent File Browser', c=fileManager.openRecentFileBrowser_ui )




class ConfirmUI(UIFunctions):
    
    def __init__(self):
        
        UIFunctions.__init__(self)
        cmds.menuItem( l='Confirm', sm=1, to=1 )
        cmds.menuItem( l='Confirm UI', c=confirm.uiCmd_OpenConfirmUI )




class MarkingMenuUI( UIFunctions ):

    def __init__(self):

        UIFunctions.__init__(self)
        cmds.menuItem( l='Marking Menu', sm=1, to=1 )
        cmds.menuItem( l='Clear', c=markingMenuCtl.deleteAllTools )
        self.divider()
        cmds.menuItem( l='Rig Tool ( Ctrl+Alt+RMB )', c=markingMenuCtl.mc_createRigTool )
        cmds.menuItem( l='Rig Tool2 ( Ctrl+Alt+RMB )', c=markingMenuCtl.mc_createRigTool2 )
        cmds.menuItem( l='Anim Tool ( Ctrl+Alt+RMB )', c=markingMenuCtl.mc_createAnimTool )



class M3DGroupUI( UIFunctions ):
    
    def __init__(self):
        
        NamingUI()
        AttributeUI()
        Modeling()
        RiggingUI()
        OptimizeUI()
        MatchMoveUI()
        HairUI()
        AnimationUI()
        ShadingUI()
        CharacterUI()
        FileManagerUI()
        ConfirmUI()
        FinalizeUI()
        
        self.dividerMain()
        
        UserUpdateCodeUI()
        MarkingMenuUI()


    