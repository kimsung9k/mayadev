import maya.cmds as cmds
from functools import partial
import sgBFunction_ui
import cPickle
import sgBFunction_fileAndPath


class WinA_Global:
    
    winName = 'sgAimConstraint'
    title   = 'Aim Constraint'
    width   = 300
    height  = 50

    chk_autoAxis = ''
    omg_aimAxis  = ''
    chk_createUp = ''
    chk_editUp   = ''
    sep_00       = ''
    chk_mo       = ''
    but_const    = ''

    infoPath = sgBFunction_fileAndPath.getLocusCommPackagePrefsPath() + '/sgAimConstraint/info.txt'




class WinA_Cmd:
    
    @staticmethod
    def updateWindowFromInfo():
        
        sgBFunction_fileAndPath.makeFile( WinA_Global.infoPath, False )
        f = open( WinA_Global.infoPath, 'r' )
        data = cPickle.load( f )
        f.close()
        if not data: return None
        
        try:
            autoAxis, aimIndex, createUp, editUpObject, maintainOffset = data
        except: return None
        
        cmds.checkBox(      WinA_Global.chk_autoAxis, e=1, v=autoAxis )
        cmds.optionMenuGrp( WinA_Global.omg_aimAxis,  e=1, sl=aimIndex )
        cmds.checkBox(      WinA_Global.chk_createUp, e=1, v=createUp )
        cmds.checkBox(      WinA_Global.chk_editUp,   e=1, v=editUpObject )
        cmds.checkBox(      WinA_Global.chk_mo,       e=1, v=maintainOffset )
        WinA_Cmd.updateUICondition()
    
    
    @staticmethod
    def updateInfoFromWindow():
        
        autoAxis       = cmds.checkBox(      WinA_Global.chk_autoAxis, q=1, v=1 )
        axisIndex      = cmds.optionMenuGrp( WinA_Global.omg_aimAxis,  q=1, sl=1 )
        createUp       = cmds.checkBox(      WinA_Global.chk_createUp,   q=1, v=1 )
        editUp         = cmds.checkBox(      WinA_Global.chk_editUp,   q=1, v=1 )
        maintainOffset = cmds.checkBox(      WinA_Global.chk_mo,       q=1, v=1 )
        
        data = [ autoAxis, axisIndex, createUp, editUp, maintainOffset ]
        f = open( WinA_Global.infoPath, 'w' )
        cPickle.dump( data, f )
        f.close()
    
    
    
    @staticmethod
    def updateUICondition( *args ):
        
        autoAxis = cmds.checkBox( WinA_Global.chk_autoAxis, q=1, v=1 )
        if autoAxis:
            cmds.optionMenuGrp( WinA_Global.omg_aimAxis, e=1, en=0 )
        else:
            cmds.optionMenuGrp( WinA_Global.omg_aimAxis, e=1, en=1 )
        
        createUp = cmds.checkBox( WinA_Global.chk_createUp, q=1, v=1 )
        if createUp:
            cmds.checkBox( WinA_Global.chk_editUp, e=1, en=1 )
        else:
            cmds.checkBox( WinA_Global.chk_editUp, e=1, en=0 )



    @staticmethod
    def uicmdConstraint( *args ):
        
        import sgBFunction_connection
        
        autoAxis       = cmds.checkBox(      WinA_Global.chk_autoAxis, q=1, v=1 )
        axisIndex      = cmds.optionMenuGrp( WinA_Global.omg_aimAxis,  q=1, sl=1 )
        createUp       = cmds.checkBox(      WinA_Global.chk_createUp, q=1, v=1 )
        editUp         = cmds.checkBox(      WinA_Global.chk_editUp,   q=1, v=1 )
        maintainOffset = cmds.checkBox(      WinA_Global.chk_mo,       q=1, v=1 )

        sels = cmds.ls( sl=1 )

        aimTarget = sels[0]
        constTarget = sels[1]

        sgBFunction_connection.aimConstraintByAimObjectMatrix( aimTarget, constTarget, autoAxis, maintainOffset, createUp, editUp, axisIndex-1 )
        WinA_Cmd.updateInfoFromWindow()


    @staticmethod
    def cmdConstraint():

        import sgBFunction_connection
        
        sgBFunction_fileAndPath.makeFile( WinA_Global.infoPath, False )
        f = open( WinA_Global.infoPath, 'r' )
        data = cPickle.load( f )
        f.close()
        
        if not data:
            autoAxis = True
            axisIndex = 0
            createUp = False
            editUp = True
            maintainOffset = False
        else:
            try:
                autoAxis, axisIndex, createUp, editUp, maintainOffset = data
            except: 
                autoAxis = True
                axisIndex = 0
                createUp = False
                editUp = True
                maintainOffset = False
        
        sels = cmds.ls( sl=1 )

        aimTarget = sels[0]
        constTarget = sels[1]
        sgBFunction_connection.aimConstraintByAimObjectMatrix( aimTarget, constTarget, autoAxis, maintainOffset, createUp, editUp, axisIndex-1 )
        WinA_Cmd.updateInfoFromWindow()





class WinA:

    
    def __init__(self):
        
        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height
        


    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )

        form = cmds.formLayout()
        chk_autoAxis = cmds.checkBox( l='Auto Axis', v=1, cc=WinA_Cmd.updateUICondition )
        omg_aimAxis  = cmds.optionMenuGrp( l='Aim Axis', cw=[(1,60),(2,40)], en=0 )
        chk_createUp = cmds.checkBox( l='Create Up Object', v=0, cc=WinA_Cmd.updateUICondition  )
        chk_editUp   = cmds.checkBox( l='Edit Up Object Position', v=1, en=0 )
        sep_00       = cmds.separator()
        chk_mo       = cmds.checkBox( l='Maintain Offset', v=0 )
        but_const    = cmds.button( l='C O N S T R A I N T', h=25, c= WinA_Cmd.uicmdConstraint )
        
        cmds.menuItem( l='X' );  cmds.menuItem( l='Y' );  cmds.menuItem( l='Z' )
        cmds.menuItem( l='-X' ); cmds.menuItem( l='-Y' ); cmds.menuItem( l='-Z' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[ ( chk_autoAxis, 'top', 5 ), ( chk_autoAxis, 'left', 20 ),
                              ( omg_aimAxis, 'top', 5 ),  ( omg_aimAxis, 'left', 120 ),
                              ( chk_createUp, 'top', 5 + 22 ), ( chk_createUp, 'left', 20 ),
                              ( chk_editUp, 'top', 5 + 22 ), ( chk_editUp, 'left', 140 ),
                              ( sep_00, 'top', 5 + 22 * 2 ), ( sep_00, 'left', 0 ), ( sep_00, 'right', 0 ),
                              ( chk_mo, 'top', 5 + 22 * 2 + 10 ), ( chk_mo, 'left', 20 ),
                              ( but_const, 'top', 5 + 22 * 3 + 10 ), ( but_const, 'left', 0 ), ( but_const, 'right', 0 ) ] )
        
        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )
        
        WinA_Global.chk_autoAxis = chk_autoAxis
        WinA_Global.omg_aimAxis  = omg_aimAxis
        WinA_Global.chk_createUp = chk_createUp
        WinA_Global.chk_editUp   = chk_editUp
        WinA_Global.sep_00       = sep_00
        WinA_Global.chk_mo       = chk_mo
        WinA_Global.but_const    = but_const
        
        WinA_Cmd.updateWindowFromInfo()