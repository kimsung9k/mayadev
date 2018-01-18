from maya import cmds, OpenMaya
import pymel.core
from functools import partial


class Win_Global:
    
    winName = 'sg_edgeToJointLine_ui'
    title = "UI - Edge To JointLine"
    width = 300
    height = 50




class sgCmds:
    
    
    @staticmethod
    def getMObject( inputTarget ):
        target = pymel.core.ls( inputTarget )[0]
        mObject = OpenMaya.MObject()
        selList = OpenMaya.MSelectionList()
        selList.add( target.name() )
        selList.getDependNode( 0, mObject )
        return mObject
    
    
    @staticmethod
    def getDagPath( inputTarget ):
        target = pymel.core.ls( inputTarget )[0]
        dagPath = OpenMaya.MDagPath()
        selList = OpenMaya.MSelectionList()
        selList.add( target.name() )
        try:
            selList.getDagPath( 0, dagPath )
            return dagPath
        except:
            return None



    @staticmethod
    def getPointAtParam( inputCurveObj, paramValue ):
    
        curveObj = pymel.core.ls( inputCurveObj )[0]
        if curveObj.nodeType() == 'nurbsCurve':
            curveShape = curveObj
        else:
            curveShape = curveObj.getShape()
        
        fnCurve = OpenMaya.MFnNurbsCurve( sgCmds.getDagPath( curveShape ) )
        point = OpenMaya.MPoint()
        fnCurve.getPointAtParam( paramValue, point, OpenMaya.MSpace.kWorld )
        return [ point.x, point.y, point.z ]
    
    
    @staticmethod
    def getTangetAtParam( inputCurveObj, paramValue ):
    
        curveObj = pymel.core.ls( inputCurveObj )[0]
        if curveObj.nodeType() == 'nurbsCurve':
            curveShape = curveObj
        else:
            curveShape = curveObj.getShape()
        
        fnCurve = OpenMaya.MFnNurbsCurve( sgCmds.getDagPath( curveShape ) )
        tangent = fnCurve.tangent( paramValue, OpenMaya.MSpace.kWorld )
        return [ tangent.x, tangent.y, tangent.z ]



    @staticmethod
    def getNormalAtPoint( inputMesh, inputPoint ):
    
        if type( inputPoint ) in [ list, tuple ]:
            point = OpenMaya.MPoint( *inputPoint )
        else:
            point = inputPoint
        
        mesh = pymel.core.ls( inputMesh )[0]
        if mesh.nodeType() == 'transform':
            meshShape = mesh.getShape()
        else:
            meshShape = mesh
        
        dagPath = sgCmds.getDagPath( meshShape.name() )
        intersector = OpenMaya.MMeshIntersector()
        intersector.create( sgCmds.getMObject( meshShape ) )
        
        pointOnMesh = OpenMaya.MPointOnMesh()
        intersector.getClosestPoint( point * dagPath.inclusiveMatrixInverse(), pointOnMesh )
        normal = OpenMaya.MVector( pointOnMesh.getNormal() ) * dagPath.inclusiveMatrix()
        
        return [ normal.x, normal.y, normal.z ]

    
    @staticmethod
    def createJointLineOnEdge( edges, numJoint, **options ):
    
        reverseOrder = False
        if options.has_key( 'reverseOrder' ):
            reverseOrder = options['reverseOrder']
        print "reverseOrder :", reverseOrder
        
    
        pymel.core.select( edges )
        curve = pymel.core.ls( pymel.core.polyToCurve( form=2, degree=3 )[0] )[0]
        curveShape = curve.getShape()
        maxValue = curveShape.maxValue.get()
        eachParam = maxValue / numJoint
        
        targetMeshShape = pymel.core.ls( edges[0] )[0].node()
        targetMesh = targetMeshShape.getParent()
        
        matricies = []
        meshIntersector = OpenMaya.MMeshIntersector()
        meshIntersector.create( sgCmds.getMObject( targetMeshShape ) )
        
        for i in range( numJoint+1 ):
            point   = sgCmds.getPointAtParam( curve, i*eachParam )
            tangent = sgCmds.getTangetAtParam( curve, i*eachParam )
            normal  = OpenMaya.MVector( *sgCmds.getNormalAtPoint( targetMesh, point ) )
            if reverseOrder:
                tangent = [ value * -1 for value in tangent ]
            vTangent = OpenMaya.MVector( *tangent )
            vNormal = OpenMaya.MVector( *normal )
            vBNormal = vTangent ^ vNormal
            vANormal = vBNormal ^ vTangent
            vTangent.normalize()
            vANormal.normalize()
            vBNormal.normalize()
            matrix = [ vTangent.x, vTangent.y, vTangent.z, 0,
              vANormal.x, vANormal.y, vANormal.z, 0, 
              vBNormal.x, vBNormal.y, vBNormal.z, 0,
              point[0], point[1], point[2], 1 ]
            matricies.append( matrix )
        
        if reverseOrder:
            matricies.reverse()
        
        pymel.core.select( d=1 )
        trNodes = []
        for matrix in matricies:
            trNode = pymel.core.joint()
            pymel.core.xform( trNode, ws=1, matrix=matrix )
            trNodes.append( trNode )
        
        pymel.core.delete( curve )
        
        return trNodes




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


def show():
    
    Win().create()



if __name__ == '__main__':
    show()




