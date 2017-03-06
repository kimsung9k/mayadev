import maya.cmds as cmds
import maya.OpenMaya as om
import sgBFunction_ui
import sgBFunction_mesh




class Window_Global:
    
    winName = 'sgPWindow_set_jointNum'
    title   = 'Set Joint Num'
    
    ui_popupJnts = ''
    fld_targetJoints = ''
    fld_min = ''
    fld_max = ''

    

class UI_IntField:
    
    def __init__(self, label, defaultValue, minValue, maxValue ):
        
        self.label = label
        self.defaultValue = defaultValue
        self.min = minValue
        self.max = maxValue
        
    
    def create(self):
        
        form = cmds.formLayout()
        
        tx_label = cmds.text( l= self.label, h=22 )
        fld_value = cmds.intField( v= self.defaultValue, h=22, min=self.min, max=self.max )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1, 
                         af=[( tx_label, 'left', 0 ), ( tx_label, 'top', 0 ),
                             ( fld_value, 'top', 0 )],
                         ac=[( fld_value, 'left', 0, tx_label ) ] )
        
        self.fld_value = fld_value
        self.form = form
        return form




class Window_Cmd:
    
    @staticmethod
    def cmdSet( *args ):
        
        import sgBFunction_joint

        jnts = Window_Global.ui_popupJnts.getFieldTexts()
        
        instJointSets = []
        minLength = 100000000.0
        maxLength = 0.0
        for topJnt in jnts:
            instJointSet = sgBFunction_joint.JointLineSet( topJnt )
            length = instJointSet.getLength()
            instJointSets.append( instJointSet )
            
            if length < minLength:
                minLength =length
            if length > maxLength:
                maxLength = length
        
        lengthDiff = maxLength - minLength
        diffRate = 1.0
        
        minJntNum = cmds.intField( Window_Global.fld_min, q=1, v=1 )
        maxJntNum = cmds.intField( Window_Global.fld_max, q=1, v=1 )
        
        jntNumDiff = maxJntNum-minJntNum
        if jntNumDiff != 0:
            diffRate = lengthDiff / jntNumDiff
        
        for instJointSet in instJointSets:
            lengthDiff = instJointSet.getLength()-minLength
            addJntNum = lengthDiff / diffRate
            
            num = int( minJntNum + addJntNum )
            
            instJointSet.setJointNum( instJointSet.jntH[0], instJointSet.jntH[-1], num )
        



class Window:
    
    def __init__(self):
        
        self.width   = 400
        self.height  = 50
        
        self.popupTargetJoints  = sgBFunction_ui.PopupFieldUI( "Target Joints : ", 'Load Selected', 'multi', position = 30 )
        Window_Global.ui_popupJnts = self.popupTargetJoints
        self.minNum           = UI_IntField( "min joint num : ", 2, 2, 500 )
        self.maxNum           = UI_IntField( "max joint num: ",  2, 2, 1000 )
    
    
    def show(self):
        
        if cmds.window( Window_Global.winName, ex=1 ):
            cmds.deleteUI( Window_Global.winName, wnd=1 )
        cmds.window( Window_Global.winName, title= Window_Global.title )
        
        form = cmds.formLayout()
        
        self.targetJointsForm  = self.popupTargetJoints.create()
        self.minJointNum        = self.minNum.create()
        self.maxJointNum        = self.maxNum.create()
        self.btCreate      = cmds.button( l='Create', h=25, c= Window_Cmd.cmdSet )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [ ( self.targetJointsForm, 'left', 0 ), ( self.targetJointsForm, 'right', 5 ), ( self.targetJointsForm, 'top', 5 ),
                                ( self.minJointNum, 'left', 50 ),
                                ( self.btCreate, 'left', 0 ), ( self.btCreate, 'right', 0 ) ],
                         ac = [ ( self.minJointNum, 'top', 5, self.targetJointsForm ),
                                ( self.maxJointNum, 'top', 5, self.targetJointsForm ),( self.maxJointNum, 'left', 20, self.minJointNum ),
                                ( self.btCreate, 'top', 5, self.minJointNum ) ] )
        
        cmds.columnLayout()
        cmds.setParent( '..' )
        
        Window_Global.fld_targetJoints = self.popupTargetJoints._field
        Window_Global.fld_min        = self.minNum.fld_value
        Window_Global.fld_max        = self.maxNum.fld_value
        
        cmds.window( Window_Global.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( Window_Global.winName )


mc_showWindow = """import sgPWindow_set_jointNum
sgPWindow_set_jointNum.Window().show()"""