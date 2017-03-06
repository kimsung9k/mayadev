import maya.cmds as cmds
import maya.OpenMaya as om
import sgBFunction_ui
import sgBFunction_mesh




class Window_Global:
    
    winName = 'sgPWindow_set_jointLineOnMesh'
    title   = 'Edit Joint Line On Mesh'
    
    fld_targetMesh = ''
    fld_startPoints = ''
    fld_endPoints = ''
    fld_detail = 1

    

class UI_IntField:
    
    def __init__(self, label, defaultValue, minValue, maxValue ):
        
        self.label = label
        self.defaultValue = defaultValue
        self.min = minValue
        self.max = maxValue
    
    def create(self):
        
        form = cmds.formLayout()
        
        tx_label = cmds.text( l= self.label, h=22 )
        fld_value = cmds.intField( min= self.min, max= self.max, v= self.defaultValue, h=22, step=1 )
        
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
    def create( *args ):
        
        strTargetMesh   = cmds.textField( Window_Global.fld_targetMesh, q=1, tx=1 )
        strIndicesStart = cmds.textField( Window_Global.fld_startPoints, q=1, tx=1 )
        strIndicesEnd   = cmds.textField( Window_Global.fld_endPoints, q=1, tx=1 )
        detail          = cmds.intField( Window_Global.fld_detail, q=1, v=1 )
        
        eStrStartIndices = strIndicesStart.split( ',' )
        eStrEndIndices   = strIndicesEnd.split( ',' )
        
        indicesStart = []
        for strIndex in eStrStartIndices:
            indicesStart.append( int( strIndex.strip() ) )
        
        indicesEnd = []
        for strIndex in eStrEndIndices:
            indicesEnd.append( int( strIndex.strip() ) )
        
        import sgBFunction_dag
        
        dagPathMesh = sgBFunction_dag.getMDagPath( strTargetMesh )
        fnMesh = om.MFnMesh( dagPathMesh )
        
        pointsMesh = om.MPointArray()
        fnMesh.getPoints( pointsMesh )
        
        bbStarts = om.MBoundingBox()
        bbEnds   = om.MBoundingBox()
        
        for index in indicesStart:
            bbStarts.expand( pointsMesh[index] )
        
        for index in indicesEnd:
            bbEnds.expand( pointsMesh[index] )
            
        startCenter = bbStarts.center() * dagPathMesh.inclusiveMatrix()
        endCenter   = bbEnds.center() * dagPathMesh.inclusiveMatrix()
        
        sgBFunction_mesh.createJointLineFromMeshApi( dagPathMesh, startCenter, endCenter, detail )
    
    
    @staticmethod
    def loadSelectedStartIndices( *args ):
        
        import sgBFunction_dag
        mesh, indices = sgBFunction_mesh.getMeshAndIndicesPoints( cmds.ls( sl=1 ) )
        cmds.textField( Window_Global.fld_targetMesh, e=1, tx= mesh )
        
        indicesStr = ''
        for i in indices:
            indicesStr += str( i ) + ','
        
        cmds.textField( Window_Global.fld_startPoints, e=1, tx=indicesStr[:-1] )

        fnMesh = om.MFnMesh( sgBFunction_dag.getMDagPath( mesh ) )
        points = om.MPointArray()
        fnMesh.getPoints( points )
        
        bb = om.MBoundingBox()
        
        for i in range( len(indices) ):
            bb.expand( points[indices[i]] )
        
        center = om.MPoint( bb.center() )
        
        farIndex = 0
        farDist = 0.0
        for i in range( points.length() ):
            dist = center.distanceTo( points[i] )
            if farDist < dist:
                farDist = dist
                farIndex = i
        
        print farIndex
        cmds.textField( Window_Global.fld_endPoints, e=1, tx=str(farIndex) )


    @staticmethod
    def loadSelectedEndIndices( *args ):
        
        mesh, indices = sgBFunction_mesh.getMeshAndIndicesPoints( cmds.ls( sl=1 ) )
        cmds.textField( Window_Global.fld_targetMesh, e=1, tx= mesh )
        
        indicesStr = ''
        for i in indices:
            indicesStr += str( i ) + ','
        
        cmds.textField( Window_Global.fld_endPoints, e=1, tx=indicesStr[:-1] )
    
    
    @staticmethod
    def pickOutJoint( *args ):
        
        import sgBFunction_joint
        sgBFunction_joint.pickOutJoint( cmds.ls( sl=1 ) )
        



class Window:
    
    def __init__(self):
        
        self.width   = 400
        self.height  = 50
        
        self.popupTargetMesh  = sgBFunction_ui.PopupFieldUI( "Target Mesh : ", 'Load Selected', 'single', position = 30, olnyAddCmd = True )
        self.popupStartPoints = sgBFunction_ui.PopupFieldUI( 'Start Points : ', 'load Selected', 'multi', 
                                                             Window_Cmd.loadSelectedStartIndices, position = 30, olnyAddCmd = True )
        self.popupEndPoints   = sgBFunction_ui.PopupFieldUI( 'End Points : ', 'load Selected', 'multi', 
                                                             Window_Cmd.loadSelectedEndIndices, position = 30, olnyAddCmd = True )
        self.intField         = UI_IntField( "Detail : ", 4, 1, 10 )
    
    
    def show(self):
        
        if cmds.window( Window_Global.winName, ex=1 ):
            cmds.deleteUI( Window_Global.winName, wnd=1 )
        cmds.window( Window_Global.winName, title= Window_Global.title )
        
        form = cmds.formLayout()
        
        self.targetMeshForm  = self.popupTargetMesh.create()
        self.startPointsFrom = self.popupStartPoints.create()
        self.endPointsFrom   = self.popupEndPoints.create()
        self.detail      = self.intField.create()
        self.pickOut     = cmds.button( l='Pick Out Joint', c= Window_Cmd.pickOutJoint )
        self.btCreate    = cmds.button( l='Create', h=25, c= Window_Cmd.create )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [ ( self.targetMeshForm, 'left', 0 ), ( self.targetMeshForm, 'right', 5 ), ( self.targetMeshForm, 'top', 5 ),
                                ( self.startPointsFrom, 'left', 0 ), ( self.startPointsFrom, 'right', 5 ),
                                ( self.endPointsFrom, 'left', 0 ), ( self.endPointsFrom, 'right', 5 ),
                                ( self.detail, 'left', 100 ),
                                ( self.btCreate, 'left', 0 ), ( self.btCreate, 'right', 0 ) ],
                         ac = [ ( self.startPointsFrom, 'top', 5, self.targetMeshForm ),
                                ( self.endPointsFrom, 'top', 0, self.startPointsFrom ),
                                ( self.detail, 'top', 5, self.endPointsFrom ),
                                ( self.btCreate, 'top', 5, self.detail ),
                                ( self.pickOut, 'left', 10, self.detail ),
                                ( self.pickOut, 'top', 5, self.endPointsFrom ) ] )
        
        cmds.columnLayout()
        cmds.setParent( '..' )
        
        Window_Global.fld_targetMesh = self.popupTargetMesh._field
        Window_Global.fld_startPoints = self.popupStartPoints._field
        Window_Global.fld_endPoints = self.popupEndPoints._field
        Window_Global.fld_detail = self.intField.fld_value
        
        cmds.window( Window_Global.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( Window_Global.winName )


mc_showWindow = """import sgPWindow_set_jointLineOnMesh
sgPWindow_set_jointLineOnMesh.Window().show()"""