from maya import cmds
from sgModules import sgHumanRigCommands
import os, json


def makeFolder( pathName ):
    
    pathName = pathName.replace( '\\', '/' )
    splitPaths = pathName.split( '/' )
    
    cuPath = splitPaths[0]
    
    folderExist = True
    for i in range( 1, len( splitPaths ) ):
        checkPath = cuPath+'/'+splitPaths[i]
        if not os.path.exists( checkPath ):
            os.chdir( cuPath )
            os.mkdir( splitPaths[i] )
            folderExist = False
        cuPath = checkPath
        
    if folderExist: return None
        
    return pathName


class Win_Global:
    
    winName = 'sgui_createHumanRig_v01'
    title   = 'UI - Create Human Rig'
    width = 400
    height = 100
    
    infoPath = cmds.about( pd=1 ) + '/sg/sgHumanRigUIInfo.txt'
    makeFolder( os.path.dirname( infoPath ) )
    
    @staticmethod
    def saveInfo():
        controllerSize = cmds.floatFieldGrp( Win_Global.controllerSize, q=1, v=1 )[0]
        numBodyJnts  = cmds.intFieldGrp( Win_Global.numBodyJoints, q=1, v=1 )[0]
        numArmUpperJnts = cmds.intFieldGrp( Win_Global.numArmUpperJnts, q=1, v=1 )[0]
        numArmLowerJnts = cmds.intFieldGrp( Win_Global.numArmLowerJnts, q=1, v=1 )[0]
        numLegUpperJnts = cmds.intFieldGrp( Win_Global.numLegUpperJnts, q=1, v=1 )[0]
        numLegLowerJnts = cmds.intFieldGrp( Win_Global.numLegLowerJnts, q=1, v=1 )[0]
        headType = cmds.intFieldGrp( Win_Global.headType, q=1, v=1 )[0]
        bodyType = cmds.intFieldGrp( Win_Global.bodyType, q=1, v=1 )[0]
        data = [controllerSize, numBodyJnts, numArmUpperJnts, numArmLowerJnts, numLegUpperJnts, numLegLowerJnts, headType, bodyType ]
        
        f = open( Win_Global.infoPath, 'w' )
        json.dump( data, f )
        f.close()
        
    

    @staticmethod
    def loadInfo():
        
        if not os.path.exists( Win_Global.infoPath ): return None
        f = open( Win_Global.infoPath, 'r' )
        data = json.load( f ) 
        f.close()
        
        if type( data ) != list: return None
        if len( data ) != 8: return None
        
        cmds.floatFieldGrp( Win_Global.controllerSize, e=1, v1=data[0] )
        cmds.intFieldGrp( Win_Global.numBodyJoints, e=1, v1=data[1] )
        cmds.intFieldGrp( Win_Global.numArmUpperJnts, e=1, v1=data[2] )
        cmds.intFieldGrp( Win_Global.numArmLowerJnts, e=1, v1=data[3] )
        cmds.intFieldGrp( Win_Global.numLegUpperJnts, e=1, v1=data[4] )
        cmds.intFieldGrp( Win_Global.numLegLowerJnts, e=1, v1=data[5] )
        cmds.intFieldGrp( Win_Global.headType, e=1, v1=data[6] )
        cmds.intFieldGrp( Win_Global.bodyType, e=1, v1=data[7] )



class Win_Cmd:
    
    @staticmethod
    def createStds( *args ):
        
        from sgModules import sgHumanRigCommands
        sgHumanRigCommands.HumanStdRig()
    
    
    @staticmethod
    def setSymmetry( *args ):
        
        from sgModules import sgHumanRigCommands
        sgHumanRigCommands.StdControl().setSymmetry( cmds.ls( sl=1 )[0] )
    
    
    @staticmethod
    def createRigByStd( *args ):
        
        controllerSize = cmds.floatFieldGrp( Win_Global.controllerSize, q=1, v=1 )[0]
        numBodyJnts  = cmds.intFieldGrp( Win_Global.numBodyJoints, q=1, v=1 )[0]
        numArmUpperJnts = cmds.intFieldGrp( Win_Global.numArmUpperJnts, q=1, v=1 )[0]
        numArmLowerJnts = cmds.intFieldGrp( Win_Global.numArmLowerJnts, q=1, v=1 )[0]
        numLegUpperJnts = cmds.intFieldGrp( Win_Global.numLegUpperJnts, q=1, v=1 )[0]
        numLegLowerJnts = cmds.intFieldGrp( Win_Global.numLegLowerJnts, q=1, v=1 )[0]
        headType = cmds.intFieldGrp( Win_Global.headType, q=1, v=1 )[0]
        bodyType = cmds.intFieldGrp( Win_Global.bodyType, q=1, v=1 )[0]
        
        from sgModules import sgHumanRigCommands
        sgHumanRigCommands.createHumanByStd(controllerSize=controllerSize,
                                            numBodyJnts=numBodyJnts,
                                            numArmUpperJnts=numArmUpperJnts,
                                            numArmLowerJnts=numArmLowerJnts,
                                            numLegUpperJnts=numLegUpperJnts,
                                            numLegLowerJnts=numLegLowerJnts,
                                            headType=headType,
                                            bodyType=bodyType)
        Win_Global.saveInfo()
        
    
    @staticmethod
    def addFollow( *args ):
        
        root  = cmds.checkBox( Win_Global.rootfollow, q=1, v=1 )
        fly   = cmds.checkBox( Win_Global.flyfollow, q=1, v=1 )
        move  = cmds.checkBox( Win_Global.movefollow, q=1, v=1 )
        world = cmds.checkBox( Win_Global.worldfollow, q=1, v=1 )
        
        from sgModules import sgHumanRigCommands
        followList = sgHumanRigCommands.FollowingIk.getFollowList( root=root, fly=fly, move=move, world=world )
        
        sels = cmds.ls( sl=1 )
        for sel in sels:
            targetList = []
            if sel.find( '_IkArm_L_' ) != -1:
                targetList = sgHumanRigCommands.FollowingIk.getLeftArmList()
            if sel.find( '_IkArm_R_' ) != -1:
                targetList = sgHumanRigCommands.FollowingIk.getRightArmList()
            if sel.find( '_IkLeg_L_' ) != -1:
                targetList = sgHumanRigCommands.FollowingIk.getLeftLegList()
            if sel.find( '_IkLeg_R_' ) != -1:
                targetList = sgHumanRigCommands.FollowingIk.getRightLegList()
            sgHumanRigCommands.FollowingIk( *targetList ).create( *followList )


    @staticmethod
    def addIkStretchAndSlide( *args ):
        
        sels = cmds.ls( sl=1 )
        
        for sel in sels:
            topJnt = sel.replace( 'Ctl_Ik', 'IkJnt_' ).replace( '_02', '_00' )
            sgHumanRigCommands.AddAndFixRig.addIkScaleAndSlide( sel, topJnt )
    
    

    @staticmethod
    def addAutoTwistPoleVector( *args ):
        
        sels = cmds.ls( sl=1 )
        for sel in sels:
            sgHumanRigCommands.AddAndFixRig.addAutoTwistPoleVector( sel )



    @staticmethod
    def fixFootPivotCtls( *args ):
        
        sels = cmds.ls( sl=1 )
        for sel in sels:
            sgHumanRigCommands.AddAndFixRig.fixFootAttribute( sel )
    
    
    @staticmethod
    def duplicateStdHand( *args ):
        for sel in cmds.ls( sl=1 ):
            sgHumanRigCommands.duplicateStdHand( sel, ['Grip', 'Spread'] )
    
    
    @staticmethod
    def connectStdRotateToOther( *args ):
        
        sels = cmds.ls( sl=1 )

        for sel in sels:
            firstChildren = cmds.listRelatives( sel, c=1, ad=1, type='joint' )
            
            for firstChild in firstChildren:
                sideName = '_L_'
                if firstChild.find( '_R_' ) != -1:
                    sideName = '_R_'
                
                otherSideName = '_R_'
                if sideName == '_R_':
                    otherSideName = '_L_'
                
                otherTarget = firstChild.replace( sideName, otherSideName )
                if not cmds.objExists( otherTarget ): continue
                cmds.connectAttr( firstChild + '.r', otherTarget + '.r' )
    
    
    @staticmethod
    def mirrorControllerShape( *args ):
        sels = cmds.ls( sl=1 )

        for sel in sels:
            sideName = '_L_'
            otherSideName = '_R_'
            
            if sel.find( '_L_' ) != -1:
                sideName = '_L_'
                otherSideName = '_R_'
            elif sel.find( '_R_' ) != -1:
                sideName = '_R_'
                otherSideName = '_L_'
            cvs = cmds.ls( sel + '.cv[*]', fl=1 )
            poses = []
            for cv in cvs:
                cvPoint = cmds.xform( cv, q=1, ws=1, t=1 )
                poses.append( cvPoint )
            otherCVs = cmds.ls( sel.replace( sideName, otherSideName ) + '.cv[*]', fl=1 )
            for i in range( len( otherCVs ) ):
                cmds.move( -poses[i][0], poses[i][1], poses[i][2], otherCVs[i], ws=1 )
            
    
    



class UI_stdArea:
    
    def __init__(self):
        pass
    
    def create(self):
        
        try:frame = cmds.frameLayout( l='Std Area', bgs=1, bgc=[0.4,0.2,0.2] )
        except:frame = cmds.frameLayout( l='Std Area', bgc=[0.4,0.2,0.2] )
        form = cmds.formLayout()
        buttonCreate = cmds.button( l='Create Std', c=Win_Cmd.createStds )
        buttonSymmetry = cmds.button( l='Set Symmetry', c=Win_Cmd.setSymmetry )
        buttonDuStd = cmds.button( l='Duplicate Std Hand( Std_Arm_02 )', c=Win_Cmd.duplicateStdHand )
        buttonConToOther = cmds.button( l='Connect Std Hand Rotate To Other( Std_Arm_02_du )', c=Win_Cmd.connectStdRotateToOther )
        cmds.setParent('..' )
        cmds.setParent('..' )

        cmds.formLayout( form, e=1, 
                         af=[ ( buttonCreate, 'top', 5 ), ( buttonCreate, 'left', 5 ), ( buttonCreate, 'right', 5 ),
                              ( buttonSymmetry, 'left', 5 ), ( buttonSymmetry, 'right', 5 ),
                              ( buttonDuStd, 'left', 5 ), ( buttonDuStd, 'right', 5 ),
                              ( buttonConToOther, 'left', 5 ), ( buttonConToOther, 'right', 5 ) ], 
                         ac=[ ( buttonSymmetry, 'top', 3, buttonCreate ),
                              ( buttonDuStd, 'top', 3, buttonSymmetry ),
                              ( buttonConToOther, 'top', 3, buttonDuStd ) ] )
        
        return frame




class UI_rigArea:
    
    def __init__(self):
        pass
    
    def create(self):
        
        try:frame = cmds.frameLayout( l='Rig Area', bgs=1, bgc=[0.4,0.2,0.2] )
        except:frame = cmds.frameLayout( l='Rig Area', bgc=[0.4,0.2,0.2] )
        form = cmds.formLayout()
        controllerSize = cmds.floatFieldGrp( l='Controller Size : ', v1=1.0 )
        numBodyJoints = cmds.intFieldGrp( l='Num Body Joints : ', v1=5 )
        numArmUpperJnts = cmds.intFieldGrp( l='Num Arm Upper Joints : ', v1=3 )
        numArmLowerJnts = cmds.intFieldGrp( l='Num Arm Lower Joints : ', v1=3 )
        numLegUpperJnts = cmds.intFieldGrp( l='Num Leg Upper Joints : ', v1=3 )
        numLegLowerJnts = cmds.intFieldGrp( l='Num Leg Lower Joints : ', v1=3 )
        headType = cmds.intFieldGrp( l='Head Type : ', v1=1 )
        bodyType = cmds.intFieldGrp( l='Body Type : ', v1=1 )
        button = cmds.button( l='Create', c=Win_Cmd.createRigByStd )
        btConSh = cmds.button( l='Mirror Controller Shape', c= Win_Cmd.mirrorControllerShape )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ (controllerSize, 'top', 0), (controllerSize, 'left', 0), (controllerSize, 'right', 0),
                              (numBodyJoints, 'left', 0), (numBodyJoints, 'right', 0),
                              (numArmUpperJnts, 'left', 0), (numArmUpperJnts, 'right', 0),
                              (numArmLowerJnts, 'left', 0), (numArmLowerJnts, 'right', 0),
                              (numLegUpperJnts, 'left', 0), (numLegUpperJnts, 'right', 0),
                              (numLegLowerJnts, 'left', 0), (numLegLowerJnts, 'right', 0),
                              (headType, 'left', 0), (headType, 'right', 0),
                              (bodyType, 'left', 0), (bodyType, 'right', 0),
                              ( button, 'left', 0 ), ( button, 'right', 0 ),
                              ( btConSh, 'left', 0 ), ( btConSh, 'right', 0 ) ],
                         ac = [( numBodyJoints, 'top', 5, controllerSize ),
                               ( numArmUpperJnts, 'top', 5, numBodyJoints ),
                               ( numArmLowerJnts, 'top', 5, numArmUpperJnts ),
                               ( numLegUpperJnts, 'top', 5, numArmLowerJnts ),
                               ( numLegLowerJnts, 'top', 5, numLegUpperJnts ),
                               ( headType, 'top', 5, numLegLowerJnts ),
                               ( bodyType, 'top', 5, headType ),
                               ( button, 'top', 5, bodyType ),
                               ( btConSh, 'top', 5, button )] )
        
        Win_Global.controllerSize = controllerSize
        Win_Global.numBodyJoints = numBodyJoints
        Win_Global.numArmUpperJnts = numArmUpperJnts
        Win_Global.numArmLowerJnts = numArmLowerJnts
        Win_Global.numLegUpperJnts = numLegUpperJnts
        Win_Global.numLegLowerJnts = numLegLowerJnts
        Win_Global.headType = headType
        Win_Global.bodyType = bodyType
    
        return frame




class UI_FollowArea:
    
    def __init__(self):
        pass
    
    def create(self):
        
        try:frame = cmds.frameLayout( l='Follow Area', bgs=1, bgc=[0.2,0.2,.4] )
        except:frame = cmds.frameLayout( l='Follow Area', bgc=[0.2,0.2,.4] )
        form = cmds.formLayout()
        text  = cmds.text( l='Select Ik And Set' )
        root  = cmds.checkBox( l='Root', v=1 )
        fly   = cmds.checkBox( l='Fly', v=1 )
        move  = cmds.checkBox( l='Move', v=1 )
        world = cmds.checkBox( l='World', v=1 )
        btSet = cmds.button( l='Set', c= Win_Cmd.addFollow )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ ( text, 'left', 0 ), ( text, 'right', 0 ), ( text, 'top', 0 ),
                              ( root, 'left', 0 ), ( world, 'right', 0 ),
                              ( btSet, 'left', 0 ), ( btSet, 'right', 0 ) ],
                         ac=[ ( root, 'top', 5, text ), ( fly, 'top', 5, text ), ( move, 'top', 5, text ), ( world, 'top', 5, text ),
                              ( btSet, 'top', 5, move ) ],
                         ap=[ ( root, 'right', 0, 25 ), 
                              ( fly, 'left', 0, 25 ), ( fly, 'right', 0, 50 ),
                              ( move, 'left', 0, 50 ), ( move, 'right', 0, 75 ),
                              ( world, 'left', 0, 75 ) ] )
        
        Win_Global.rootfollow = root
        Win_Global.flyfollow = fly
        Win_Global.movefollow = move
        Win_Global.worldfollow = world
        
        return frame




class UI_AddRigArea:
    
    def __init__(self):
        pass
    
    
    def create(self):
        
        try:frame = cmds.frameLayout( l='Add Rig Area', bgs=1, bgc=[0.2, 0.5, 0.5] )
        except:frame = cmds.frameLayout( l='Add Rig Area', bgc=[0.2, 0.5, 0.5] )
        form = cmds.formLayout()
        btIkScaleOption = cmds.button( l='Add Ik Scale Options( ikCtls )', c = Win_Cmd.addIkStretchAndSlide )
        btAddAutoTwist  = cmds.button( l='Add Auto Twist PoleVector( ikCtls )', c = Win_Cmd.addAutoTwistPoleVector )
        btFixFootPivAttribute  = cmds.button( l='Fix Foot Pivot Ctls( FootPivCtls )', c = Win_Cmd.fixFootPivotCtls )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[(btIkScaleOption,'top',3), (btIkScaleOption,'left',0), (btIkScaleOption,'right',0),
                             (btAddAutoTwist,'left',0), (btAddAutoTwist,'right',0),
                             (btFixFootPivAttribute,'left',0), (btFixFootPivAttribute,'right',0)],
                         ac=[(btAddAutoTwist,'top',3,btIkScaleOption),
                             (btFixFootPivAttribute,'top',3,btAddAutoTwist)],
                         ap=[] )
        
        return frame
    





class Win:
    
    def __init__(self ):
        
        self.stdArea = UI_stdArea()
        self.rigArea = UI_rigArea()
        self.followArea = UI_FollowArea()
        self.addRigArea = UI_AddRigArea()
    
    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        
        cmds.window( Win_Global.winName, title= Win_Global.title )
        
        formOuter = cmds.formLayout()
        stdForm = self.stdArea.create()
        rigForm = self.rigArea.create()
        followForm = self.followArea.create()
        addRigForm = self.addRigArea.create()
        cmds.setParent( '..' )

        cmds.formLayout( formOuter, e=1, 
                         af = [ (stdForm, 'left', 5), (stdForm, 'right', 5), (stdForm, 'top', 5),
                                (rigForm, 'left', 5), (rigForm, 'right', 5),
                                (followForm, 'left', 5), (followForm, 'right', 5),
                                (addRigForm, 'left', 5), (addRigForm, 'right', 5), (addRigForm, 'bottom', 5) ],
                         ac = [ (rigForm, 'top', 5, stdForm ),
                                (followForm, 'top', 5, rigForm ),
                                (addRigForm, 'top', 5, followForm )] )
        
        cmds.window( Win_Global.winName, e=1, width = Win_Global.width, height= Win_Global.height )
        cmds.showWindow( Win_Global.winName )
        
        Win_Global.loadInfo()
        
        
    