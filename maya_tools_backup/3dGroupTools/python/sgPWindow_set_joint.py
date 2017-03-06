import maya.cmds as cmds
from functools import partial



class WinA_Global:
    
    winName = 'sgWindow_joint_slider'
    title   = 'Joint Position Slider'
    width   = 450
    height  = 50
    txf_topJoint = ''
    txf_endJoint = ''
    slider_joint = ''
    button_set   = ''
    
    slider_form = ''
    
    num_original = ''
    num_separate = ''
    frame        = ''
    bt_setEqually  =''
    bt_setNormally = ''
    
    windowPtr = None
    
    globalValueAttr = 'sgJointSliderValueAttr'




class WinA_field_popup:


    def __init__(self, firstLabel, secondLabel ):
        
        import sgBFunction_ui
        self.fieldPopup_first  = sgBFunction_ui.PopupFieldUI( firstLabel, textWidth=120 )
        self.fieldPopup_second = sgBFunction_ui.PopupFieldUI( secondLabel, textWidth=120 )


    
    def create(self):
        
        print "field popup create"
        form = cmds.formLayout()
        fieldPopupFirst_form  = self.fieldPopup_first.create()
        fieldPopupSecond_form = self.fieldPopup_second.create()
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( fieldPopupFirst_form, 'top', 0), ( fieldPopupFirst_form, 'left', 0),
                             ( fieldPopupSecond_form, 'top', 0), ( fieldPopupSecond_form, 'right', 0)],
                         ap=[( fieldPopupFirst_form, 'right', 0, 50 ),
                             ( fieldPopupSecond_form, 'left',  0, 50 )] )
        
        self.form = form
        
        WinA_Global.txf_topJoint = self.fieldPopup_first._field
        WinA_Global.txf_endJoint = self.fieldPopup_second._field
        
        return form




class WinA_frame:
    
    def __init__(self):
        
        pass
    
    
    def create(self):
        
        frame = cmds.frameLayout( l='Separate Joint', cl=1, cll=1, cc= self.cmdCollapse )
        form  = cmds.formLayout()
        tx_origin    = cmds.text( l='Current Joint Number : ', h=25, al='right' )
        inf_origin   = cmds.intField( w= 50 )
        bt_equally  = cmds.button( l='Separate Equally' )
        bt_normally = cmds.button( l='Separate Normally' )
        cmds.setParent( '..' )
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af=[( tx_origin, 'top', 0 ),  ( tx_origin, 'left', 0 ),
                             ( inf_origin, 'top', 0 ),
                             ( bt_equally, 'top', 0 ), ( bt_equally, 'left', 0 ),
                             ( bt_normally, 'top', 0 ), ( bt_normally, 'right', 0 )],
                         ap=[( tx_origin, 'right', 0, 50 ), ( inf_origin, 'left', 0, 50 ),
                             ( bt_equally, 'right', 0, 50 ), ( bt_normally, 'left', 0, 50 )],
                         ac=[( bt_equally, 'top', 0, tx_origin ), ( bt_normally, 'top', 0, tx_origin )])
    
        self.frame = frame
        WinA_Global.num_original = inf_origin
        WinA_Global.bt_setEqually = bt_equally
        WinA_Global.bt_setNormally = bt_normally
    
        return frame

    
    def cmdCollapse(self, *args ):
        
        cmds.window( WinA_Global.winName, e=1, h=50, rtf=1 )
        
        
        



class WinA_Cmd:
    

    def __init__(self, ptr_window ):
        
        import maya.OpenMaya
        import math
        
        self.openMaya = maya.OpenMaya
        self.ptr_w = ptr_window
        self.oCurve = None
        self.numPoints = 0
        self.jntH = []
        self.sin  = math.sin
        self.maxRadValue = math.pi / 2.0
        
        self.dragOn = False
        self.beforeValue = 0
        
        cmds.scriptJob( e=['Undo', self.setUndo ], p= self.ptr_w.winName )
        cmds.scriptJob( e=['Redo', self.setRedo ], p= self.ptr_w.winName )
        
        self.setGlobalValue( 0 )
        


    def getGlobalAttr(self):
        
        import sgBFunction_attribute
        
        globalValueAttrs = cmds.ls( '*.' + WinA_Global.globalValueAttr )
        if not globalValueAttrs:
            cmds.undoInfo( swf=1 )
            node = cmds.createNode( 'addDoubleLinear' )
            sgBFunction_attribute.addAttr( node, ln= WinA_Global.globalValueAttr )
            globalValueAttrs = [node + '.' + WinA_Global.globalValueAttr]
        return globalValueAttrs[0]
    


    def getGlobalValue(self):
        
        return cmds.getAttr( self.getGlobalAttr() )
    

    
    def setGlobalValue(self, value ):
        
        return cmds.setAttr( self.getGlobalAttr(), value )


    def updateJointNum(self, *args ):
        
        topJoint = cmds.textField( WinA_Global.txf_topJoint, q=1, tx=1 )
        endJoint = cmds.textField( WinA_Global.txf_endJoint, q=1, tx=1 )
        
        endJoint = cmds.ls( endJoint, l=1 )[0]
        jntChildren = cmds.listRelatives( topJoint, c=1, ad=1, f=1 )
        jntChildren.append( topJoint )
        jntChildren.reverse()
        
        if not endJoint in jntChildren:
            cmds.frameLayout( WinA_Global.frame, e=1, en=0 )
            cmds.floatSliderGrp( WinA_Global.slider_joint, e=1, v=0 )
            return False
        
        index = jntChildren.index( endJoint )
        self.jntH = jntChildren[:index+1]
        self.numPoints = len( self.jntH )
        
        cmds.intField( WinA_Global.num_original, e=1, v=self.numPoints )

    
    def setEditMode(self, topJoint, endJoint, curveEdit=True ):

        self.dragOn = False

        endJoint = cmds.ls( endJoint, l=1 )[0]
        jntChildren = cmds.listRelatives( topJoint, c=1, ad=1, f=1 )
        jntChildren.append( topJoint )
        jntChildren.reverse()
        
        if not endJoint in jntChildren:
            cmds.frameLayout( WinA_Global.frame, e=1, en=0 )
            cmds.floatSliderGrp( WinA_Global.slider_joint, e=1, v=0 )
            return False
        
        index = jntChildren.index( endJoint )
        self.jntH = jntChildren[:index+1]
        self.numPoints = len( self.jntH )
        
        cmds.intField( WinA_Global.num_original, e=1, v=self.numPoints )
        cmds.floatSliderGrp( WinA_Global.slider_joint, e=1, v=0 )
        
        self.editCurveByPosition()
        self.setGlobalValue( self.getGlobalValue() )
        
        return True
    
    
    
    def editCurveByPosition(self):
        
        fnCurve = self.openMaya.MFnNurbsCurve()
        fnCurveData = self.openMaya.MFnNurbsCurveData()
        self.oCurve = fnCurveData.create()
        
        points = self.openMaya.MPointArray()
        points.setLength( self.numPoints )
        for i in range( points.length() ):
            points.set( self.openMaya.MPoint( *cmds.xform( self.jntH[i], q=1, ws=1, t=1 ) ), i )
        
        fnCurve.createWithEditPoints( points, 3, 1, 0, 0, 1, self.oCurve )
        fnCurve.setObject( self.oCurve )
        
        self.fnCurve = fnCurve
    


    def getPositionFromCurve(self, numPoint, equally=False ):
        
        crvLength = self.fnCurve.length()
        originParam = self.fnCurve.findParamFromLength( crvLength )
        
        points = []
        
        if equally:
            eacheLengthValue = crvLength / float( numPoint-1 )
            
            for i in range( numPoint ):
                point = self.openMaya.MPoint()
                paramValue = self.fnCurve.findParamFromLength( eacheLengthValue * i )
                self.fnCurve.getPointAtParam( paramValue, point )
                points.append( point )
        else:
            eacheParamValue = originParam / float( numPoint-1 )    
            
            for i in range( numPoint ):
                point = self.openMaya.MPoint()
                paramValue = eacheParamValue * i
                self.fnCurve.getPointAtParam( paramValue, point )
                points.append( point )
        
        return points
    
    

    def setJointNum( self, topJoint, endJoint, num, equally ):
        
        import sgBFunction_dag
        import maya.OpenMaya as om
        
        jntFnH = [ None for i in self.jntH ]
        
        sels = cmds.ls( sl=1 )
        
        originLength = len( jntFnH )
        for i in range( originLength ):
            jntFnH[i] = om.MFnDagNode( sgBFunction_dag.getMObject( self.jntH[i] ) )
        
        diff = num - originLength
        if diff < 0:
            for jntFn in jntFnH[diff-1:-1]:
                jntChildren = cmds.listRelatives( jntFn.fullPathName(), c=1, f=1 )
                for child in jntChildren:
                    cmds.parent( child, w=1 )
                cmds.delete( jntFn.fullPathName() )
            jntFnH = jntFnH[:diff-1]+[jntFnH[-1]]
            cmds.parent( jntFnH[-1].fullPathName(), jntFnH[-2].fullPathName() )
        elif diff > 0:
            cmds.select( jntFnH[-2].fullPathName() )
            rad = cmds.getAttr( jntFnH[-2].fullPathName()+'.radius' )
            for i in range( diff ):
                jntFnH.insert( -1, om.MFnDagNode(sgBFunction_dag.getMObject( cmds.joint( rad=rad ) )) )
            cmds.parent( jntFnH[-1].fullPathName(), jntFnH[-2].fullPathName() )
        
        positions = self.getPositionFromCurve( num, equally )
        
        for i in range( 1, len( jntFnH )-1 ):
            cmds.move( positions[i].x, positions[i].y, positions[i].z, jntFnH[i].fullPathName(), ws=1, pcp=1 )
        
        self.setEditMode( topJoint, endJoint )
        self.setGlobalValue( self.getGlobalValue() )
        
        if sels:
            existObjs = []
            for sel in sels:
                if cmds.objExists( sel ):
                    existObjs.append( sel )
            cmds.select( existObjs )


    def setPositionByValue(self, value, drag=False ):
        
        #poweredValues.append( self.numPoints-1 )
        if drag and not self.dragOn:
            self.dragOn = True
            cmds.undoInfo( swf=0 )
        
        if not drag and self.dragOn:
            self.setValueOlny( self.getGlobalValue() )
            self.dragOn = False
            cmds.undoInfo( swf=1 )
            self.setGlobalValue( value )
        
        self.setValueOlny( value )
        


    def setValueOlny( self, value ):
        
        divValue = float(self.numPoints-1)
        eacheRadValue = self.maxRadValue / divValue
        
        poweredValues = []
        
        for i in range( self.numPoints ):
            cuRadValue = i * eacheRadValue
            eacheValue   = self.sin( cuRadValue ) * divValue
            origValue    = i
            poweredValues.append( eacheValue * value + origValue *( 1-value ) )
        
        for i in range( 1, self.numPoints-1 ):
            point = self.openMaya.MPoint()
            self.fnCurve.getPointAtParam( poweredValues[i], point )
            cmds.move( point.x, point.y, point.z, self.jntH[i], ws=1, pcp=1 )
    

    
    def setUndo(self, *args ):
        
        cmds.floatSliderGrp( self.ptr_w.slider.slider, e=1, v= self.getGlobalValue() )
        self.updateJointNum()
        self.editCurveByPosition()

    
    def setRedo(self, *args ):
        
        cmds.floatSliderGrp( self.ptr_w.slider.slider, e=1, v= self.getGlobalValue() )
        self.updateJointNum()
        self.editCurveByPosition()



    def set(self):
        
        pass





class WinA:

    
    def __init__(self):
        
        import sgBFunction_ui
        self.winName = WinA_Global.winName
        self.title   = WinA_Global.title
        self.width   = WinA_Global.width
        self.height  = WinA_Global.height
        
        self.jointTxfPopup = WinA_field_popup( 'Top Joint : ', 'End Joint : ' )
        self.frame         = WinA_frame()
        self.slider        = sgBFunction_ui.Slider( min=-1, max=1, v=0, pre=2, f=1 )
        
        WinA_Global.windowPtr = self
        


    def create(self):
        
        if cmds.window( self.winName, ex=1 ):
            cmds.deleteUI( self.winName, wnd=1 )
        cmds.window( self.winName, title=self.title )
        
        self.cmd     = WinA_Cmd( self )
        
        form = cmds.formLayout()
        fieldForm  = self.jointTxfPopup.create()
        frame      = self.frame.create()
        sliderForm = self.slider.create()
        button     = cmds.button( l='SET' )
        cmds.setParent( '..' )
        cmds.formLayout( form, e=1,
                         af=[ (fieldForm, 'top',5 ), (fieldForm,'left', 0), (fieldForm,'right',0),
                              (sliderForm, 'left', 0), (sliderForm, 'right', 0),
                              (frame, 'left', 0), (frame, 'right', 0),
                              (button, 'left',0), (button, 'right',0)],
                         ac=[ (frame, 'top', 5, fieldForm),
                              (sliderForm, 'top', 0, frame ),
                              (button, 'top', 0, sliderForm)] )
        
        cmds.window( self.winName, e=1, wh=[ self.width, self.height ], rtf=1 )
        cmds.showWindow( self.winName )
        
        WinA_Global.slider_joint = self.slider.slider
        
        WinA_Global.slider_form = sliderForm
        self.buttonForm = button
        
        self.conditionControl( 'default' )
        
        cmds.button( button, e=1, c= self.cmdSet )
        cmds.floatSliderGrp( self.slider.slider, e=1, cc=self.cmdSetPointByChangeValue )
        cmds.floatSliderGrp( self.slider.slider, e=1, dc=self.cmdSetPointByDragValue )
        
        cmds.button( WinA_Global.bt_setEqually, e=1, c= self.cmdButtonSetEqually )
        cmds.button( WinA_Global.bt_setNormally, e=1, c= self.cmdButtonSetNormally )

        self.jointTxfPopup.fieldPopup_first._addCommand.append( self.updateFirstJoint )
        self.jointTxfPopup.fieldPopup_second._addCommand.append( self.updateSecondJoint )


    def cmdButtonSetEqually( self, *args ):
        
        topJoint = cmds.textField( WinA_Global.txf_topJoint, q=1, tx=1 )
        endJoint = cmds.textField( WinA_Global.txf_endJoint, q=1, tx=1 )
        num      = cmds.intField( WinA_Global.num_original, q=1, v=1 )
        self.cmd.setJointNum( topJoint, endJoint, num, True )
    
    
    def cmdButtonSetNormally(self, *args ):
        
        topJoint = cmds.textField( WinA_Global.txf_topJoint, q=1, tx=1 )
        endJoint = cmds.textField( WinA_Global.txf_endJoint, q=1, tx=1 )
        num      = cmds.intField( WinA_Global.num_original, q=1, v=1 )
        self.cmd.setJointNum( topJoint, endJoint, num, False )



    def cmdSet(self, *args ):
        
        self.conditionControl( 'edit' )
        self.cmdSetEditMode()



    def cmdSetEditMode( self ):

        topJnt = cmds.textField( WinA_Global.txf_topJoint,  q=1, tx=1 )
        endJnt = cmds.textField( WinA_Global.txf_endJoint, q=1, tx=1 )
        if not topJnt: return None
        if not cmds.objExists( topJnt ): return None
        if not endJnt: return None
        if not cmds.objExists( endJnt ): return None
        return self.cmd.setEditMode(topJnt, endJnt)



    def cmdSetPointByChangeValue( self, *args ):
        
        value = cmds.floatSliderGrp( WinA_Global.slider_joint, q=1, v=1 )
        self.cmd.setPositionByValue( value )
    


    def cmdSetPointByDragValue(self, *args ):
        
        value = cmds.floatSliderGrp( WinA_Global.slider_joint, q=1, v=1 )
        self.cmd.setPositionByValue( value, True )
    
    

    def conditionControl(self, mode='edit', *args ):
        
        if mode == 'default':
            cmds.floatSliderGrp( WinA_Global.slider_joint, e=1, v=0 )
            cmds.formLayout( WinA_Global.slider_form, e=1, en=0 )
        elif mode == 'edit':
            cmds.floatSliderGrp( WinA_Global.slider_joint, e=1, v=0 )
            cmds.formLayout( WinA_Global.slider_form, e=1, en=1 )
    

    
    def updateFirstJoint( self ):
        
        lastJnt = cmds.listRelatives( cmds.ls( sl=1 ), c=1, ad=1, f=1 )[0]
        cmds.textField( WinA_Global.txf_endJoint, e=1, tx=cmds.ls( lastJnt )[0]  )
        cmds.intField( WinA_Global.num_original, e=1, v=1 )
        self.cmdSetEditMode()
        self.conditionControl( 'edit' )
    
    
    def updateSecondJoint( self ):
        
        if self.cmdSetEditMode():
            self.conditionControl( 'edit' )


mc_showWindow = """import sgPWindow_set_joint
sgPWindow_set_joint.WinA().create()"""