from maya import cmds
import pymel.core
from functools import partial
from sgMaya import sgCmds


class Win_Global:
    
    winName = 'sg_edgeToJointLine_ui'
    title = "UI - Edge To JointLine"
    width = 300
    height = 50



class Win_Cmd:
    
    @staticmethod
    def create( *args ):
        edges = pymel.core.ls( sl=1 )
        checked = cmds.checkBox( Win_Global.checkBox, q=1, v=1 )
        numEdges = cmds.intField( Win_Global.intField, q=1, v=1 )
        
        separatedEdges = sgCmds.getEachObjectComponents( edges )
        topJoints = []
        for eachEdges in separatedEdges:
            trNodes = sgCmds.edgeToJointLine( eachEdges, numEdges, reverseOrder=checked )
            topJoints.append( trNodes[0] )
        pymel.core.select( topJoints )
    
    @staticmethod
    def close( *args ):
        cmds.deleteUI( Win_Global.winName )
    



class UI_numJoint:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        form = cmds.formLayout()
        text = cmds.text( l='Num Joint : ', w=100, al='left', h=25 )
        intField = cmds.intField(h=25, w=100, v=5 )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [(text,'top',0), (text,'left',20),
                               (intField,'top',0)],
                         ac = [(intField, 'left', 0, text)] )
        
        Win_Global.intField = intField
        
        return form




class UI_Buttons:
    
    def __init__(self):
        
        pass


    def create(self):
        
        form = cmds.formLayout()
        createButton = cmds.button( l='Create', h=25, c=Win_Cmd.create )
        closeButton  = cmds.button( l='Close', h=25,  c=Win_Cmd.close )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af = [( createButton, 'top', 0 ), ( createButton, 'left', 0 ), ( createButton, 'bottom', 0 ),
                               ( closeButton, 'top', 0 ), ( closeButton, 'right', 0 ), ( closeButton, 'bottom', 0 )],
                         ap = [ ( createButton, 'right', 0, 50 ), ( closeButton, 'left', 0, 50 ) ])
    
        return form



class Win:
    
    def __init__(self):
        
        self.ui_numJoint = UI_numJoint()
        self.ui_buttons  = UI_Buttons()


    def create(self):
        
        if cmds.window( Win_Global.winName, q=1, ex=1 ):
            cmds.deleteUI( Win_Global.winName )
        cmds.window( Win_Global.winName, title=Win_Global.title )
        
        form  = cmds.formLayout()
        check = cmds.checkBox( l='Reverse Direction' )
        numJoint = self.ui_numJoint.create()
        button = self.ui_buttons.create()
        cmds.setParent( '..' )

        cmds.formLayout( form, e=1, af=[ (check, 'top', 5 ), (check, 'left', 10 ), (check, 'right', 0 ),
                                         (numJoint, 'left', 10 ), (numJoint, 'right', 5 ),
                                         (button, 'left', 0 ), (button, 'right', 0 ), (button, 'bottom', 0 )],
                                    ac=[ (numJoint, 'top', 5, check), 
                                         (button, 'top', 5, numJoint) ] )
        
        cmds.window( Win_Global.winName, e=1,
                     width = Win_Global.width, height = Win_Global.height,
                     rtf=1 )
        cmds.showWindow( Win_Global.winName )
        
        Win_Global.checkBox = check

