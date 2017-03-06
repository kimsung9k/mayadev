import maya.cmds as cmds
import maya.OpenMaya as om
import sgBFunction_ui
import sgBFunction_mesh




class Window_Global:
    
    winName = 'sgPWindow_set_jointLineOnMesh2'
    title   = 'Edit Joint Line On Mesh2'
    
    fld_baseMesh = ''
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
    def create( *args ):
        
        import sgBFunction_dag
        
        reload( sgBFunction_mesh )
        
        sels = cmds.ls( sl=1 )
        
        baseMesh = cmds.textField( Window_Global.fld_baseMesh, q=1, tx=1 )
        detail   = cmds.intField( Window_Global.fld_detail, q=1, v=1 )
        
        base    = sgBFunction_dag.getShape( baseMesh ) 
        dagPathBase = sgBFunction_dag.getMDagPath( baseMesh )
        oBase = sgBFunction_dag.getMObject( base )
        
        baseMtx = dagPathBase.inclusiveMatrix()
        
        fnBase = om.MFnMesh()
        fnBase.setObject( dagPathBase )
        
        origPointsBase = om.MPointArray()
        multedPointsBase = om.MPointArray()
        fnBase.getPoints( origPointsBase )
        
        multedPointsBase.setLength( origPointsBase.length() )
        for i in range( multedPointsBase.length() ):
            multedPointsBase.set( origPointsBase[i]*baseMtx, i )
        fnBase.setPoints( multedPointsBase )
        
        intersector = om.MMeshIntersector()
        intersector.create( oBase )
        
        topJnts = []
        for sel in sels:
            target  = sgBFunction_dag.getShape( sel )
            
            dagPathMesh = sgBFunction_dag.getMDagPath( target )
            fnMeshTarget = om.MFnMesh( dagPathMesh )
            origPointsTarget = om.MPointArray()
            multedPointsTarget = om.MPointArray()
            fnMeshTarget.getPoints( origPointsTarget )
            
            targetMtx = dagPathMesh.inclusiveMatrix()
            multedPointsTarget.setLength( origPointsTarget.length() )
            for i in range( multedPointsTarget.length() ):
                multedPointsTarget.set( origPointsTarget[i] * targetMtx , i )
            
            minDistIndex = 0
            minDist = 100000.0
            pointOnMesh = om.MPointOnMesh()
            for i in range( multedPointsTarget.length() ):
                intersector.getClosestPoint( multedPointsTarget[i], pointOnMesh )
                pointClose = om.MPoint( pointOnMesh.getPoint() )
                dist = multedPointsTarget[i].distanceTo( pointClose )
                if dist < minDist:
                    minDist = dist
                    minDistIndex = i
                    
            maxDistIndex = 0
            maxDist = 0.0
            for i in range( multedPointsTarget.length() ):
                dist = multedPointsTarget[minDistIndex].distanceTo( multedPointsTarget[i] )
                if maxDist < dist:
                    maxDist = dist
                    maxDistIndex = i
            
            startCenter = om.MPoint( *cmds.xform( target+'.vtx[%d]' % minDistIndex, q=1, ws=1, t=1 ) )
            endCenter = om.MPoint( *cmds.xform( target+'.vtx[%d]' % maxDistIndex, q=1, ws=1, t=1 ) )
                
            jnts = sgBFunction_mesh.createJointLineFromMeshApi( dagPathMesh, startCenter, endCenter, detail )
            topJnts.append( jnts[0] )
        
        fnBase.setPoints( origPointsBase )
        
        cmds.select( topJnts )
    
    
    @staticmethod
    def pickOutJoint( *args ):
        
        import sgBFunction_joint
        sgBFunction_joint.pickOutJoint( cmds.ls( sl=1 ) )
        



class Window:
    
    def __init__(self):
        
        self.width   = 400
        self.height  = 50
        
        self.popupTargetMesh  = sgBFunction_ui.PopupFieldUI( "Base Mesh : ", 'Load Selected', 'single', position = 30 )
        self.intField         = UI_IntField( "Detail : ", 4, 0, 10 )
    
    
    def show(self):
        
        if cmds.window( Window_Global.winName, ex=1 ):
            cmds.deleteUI( Window_Global.winName, wnd=1 )
        cmds.window( Window_Global.winName, title= Window_Global.title )
        
        form = cmds.formLayout()
        
        self.baseMeshForm  = self.popupTargetMesh.create()
        self.detail        = self.intField.create()
        self.pickOut       = cmds.button( l='Pick Out Joint', c= Window_Cmd.pickOutJoint )
        self.btCreate      = cmds.button( l='Create', h=25, c= Window_Cmd.create )
        
        cmds.setParent( '..' )
        
        cmds.formLayout( form, e=1,
                         af = [ ( self.baseMeshForm, 'left', 0 ), ( self.baseMeshForm, 'right', 5 ), ( self.baseMeshForm, 'top', 5 ),
                                ( self.detail, 'left', 100 ),
                                ( self.btCreate, 'left', 0 ), ( self.btCreate, 'right', 0 ) ],
                         ac = [ ( self.detail, 'top', 5, self.baseMeshForm ),
                                ( self.btCreate, 'top', 5, self.detail ),
                                ( self.pickOut, 'left', 10, self.detail ),
                                ( self.pickOut, 'top', 5, self.baseMeshForm ) ] )
        
        cmds.columnLayout()
        cmds.setParent( '..' )
        
        Window_Global.fld_baseMesh = self.popupTargetMesh._field
        Window_Global.fld_detail = self.intField.fld_value
        
        cmds.window( Window_Global.winName, e=1,
                     w = self.width, h = self.height )
        cmds.showWindow( Window_Global.winName )


mc_showWindow = """import sgPWindow_set_jointLineOnMesh2
sgPWindow_set_jointLineOnMesh2.Window().show()"""