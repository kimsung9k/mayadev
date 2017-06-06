import sys
import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaMPx as OpenMayaMPx



def getMObject( nodeName ):
    
    selList = OpenMaya.MSelectionList()
    selList.add( nodeName )
    oNode = OpenMaya.MObject()
    selList.getDependNode( 0, oNode )
    return oNode
    


def float2Ptr():
    util = OpenMaya.MScriptUtil()
    util.createFromList( [0,0], 2 )
    return util.asFloat2Ptr()


def listFromFloat2Ptr( ptr ):
    util = OpenMaya.MScriptUtil()
    v1 = util.getFloat2ArrayItem( ptr, 0, 0 )
    v2 = util.getFloat2ArrayItem( ptr, 0, 1 )
    return [v1, v2]



def shortPtr( intValue = 0 ):
    util = OpenMaya.MScriptUtil()
    util.createFromInt(intValue)
    return util.asShortPtr()

def shortFromShortPtr( ptr ):
    return OpenMaya.MScriptUtil.getShort( ptr )



class Tool_global:
    mouseX = 0
    mouseY = 0



def getSelection():
    sels = cmds.ls( sl=1 )
    for sel in sels:
        if cmds.nodeType( sel ) == 'mesh':
            return sel
        if cmds.nodeType( sel ) != 'transform': continue
        selShapes = cmds.listRelatives( sel, s=1, f=1 )
        for selShape in selShapes:
            if cmds.nodeType( selShape ) == 'mesh': return selShape
    return None



def getDagPath( nodeName ):
    selList = OpenMaya.MSelectionList()
    selList.add( nodeName )
    dagPath = OpenMaya.MDagPath()
    selList.getDagPath( 0, dagPath )
    return dagPath



def getShortPtr( intValue = 0 ):
    util = OpenMaya.MScriptUtil()
    util.createFromInt(intValue)
    return util.asShortPtr()



def getValueFromShortPtr( ptr ):
    return OpenMaya.MScriptUtil().getShort( ptr )



def worldPointToViewPoint( worldPoint ):
    
    activeView = OpenMayaUI.M3dView().active3dView()
    camDagPath = OpenMaya.MDagPath()
    activeView.getCamera( camDagPath )
    
    projectionMatrix = OpenMaya.MMatrix()
    activeView.projectionMatrix(projectionMatrix)
    camInvMatrix = camDagPath.inclusiveMatrixInverse()
    
    viewPoint = worldPoint * camInvMatrix * projectionMatrix
    viewPoint.x = (viewPoint.x/viewPoint.w + 1.0 )/2.0 * activeView.portWidth()
    viewPoint.y = (viewPoint.y/viewPoint.w + 1.0 )/2.0 * activeView.portHeight()
    viewPoint.z = 0
    viewPoint.w = 1
    
    return viewPoint




def printMatrix( mtxValue ):
    
    for i in range( 4 ):
        print "%5.3f, %5.3f, %5.3f, %5.3f" %( mtxValue(i,0), mtxValue(i,1), mtxValue(i,2), mtxValue(i,3) )
    print
    



class Functions:
    
    @staticmethod
    def getIntersectPoint( meshDagPath, mouseX, mouseY ):
        
        meshMatrix = meshDagPath.inclusiveMatrix()
        invMtx = meshDagPath.inclusiveMatrixInverse()
        
        activeView = OpenMayaUI.M3dView().active3dView()
        nearPoint = OpenMaya.MPoint()
        farPoint  = OpenMaya.MPoint()
        activeView.viewToWorld( mouseX, mouseY, nearPoint, farPoint )
        
        nearPoint *= invMtx
        farPoint  *= invMtx
        
        fnMesh = OpenMaya.MFnMesh( meshDagPath )
        intersectPoints = OpenMaya.MPointArray()
        
        fnMesh.intersect( nearPoint, farPoint - nearPoint, intersectPoints )
        
        if not intersectPoints.length(): return None
        
        if intersectPoints.length() == 1:
            return intersectPoints[0] * meshMatrix
        elif intersectPoints.length() > 1:
            pointCenter = OpenMaya.MPoint( ( intersectPoints[0].x + intersectPoints[1].x )/2.0, 
                                           ( intersectPoints[0].y + intersectPoints[1].y )/2.0,
                                           ( intersectPoints[0].z + intersectPoints[1].z )/2.0 ) 
            return pointCenter * meshMatrix
    
    
    @staticmethod
    def getTransform( mouseX, mouseY ):
        
        transform = cmds.createNode( 'joint' )
        return transform
    
    
    @staticmethod
    def setOrientByChild( targetJnt ):
        
        childJnt = cmds.listRelatives( targetJnt, c=1, f=1 )
        if not childJnt:
            return None
        
        targetParent = cmds.listRelatives( targetJnt, p=1, f=1 )
        
        if not targetParent:
            activeView = OpenMayaUI.M3dView().active3dView()
            dagCam = OpenMaya.MDagPath()
            activeView.getCamera( dagCam )
            mtx = dagCam.inclusiveMatrix()
            camPos = OpenMaya.MPoint( mtx(3,0), mtx(3,1), mtx(3,2))
            targetPos = OpenMaya.MPoint( *cmds.xform( targetJnt, q=1, ws=1, t=1 ) )
            childPos = OpenMaya.MPoint( *cmds.xform( childJnt[0], q=1, ws=1, t=1 ) )
            aimVector = childPos - targetPos
            upVector  = camPos - targetPos
            crossVector = aimVector ^ upVector
            
            aimVector.normalize()
            upVector.normalize()
            crossVector.normalize()
        else:
            parentMtx = cmds.getAttr( targetParent[0] + '.wm' )
            
            targetPos = OpenMaya.MPoint( *cmds.xform( targetJnt, q=1, ws=1, t=1 ) )
            childPos  = OpenMaya.MPoint( *cmds.xform( childJnt[0], q=1, ws=1, t=1 ) )
            
            aimVector = childPos - targetPos
            upVector  = OpenMaya.MVector( parentMtx[4], parentMtx[5], parentMtx[6] )
            crossVector = aimVector ^ upVector
            
            aimVector.normalize()
            upVector.normalize()
            crossVector.normalize()
            
        mtxList = [ aimVector.x, aimVector.y, aimVector.z, 0,
                  upVector.x, upVector.y, upVector.z, 0,
                  crossVector.x, crossVector.y, crossVector.z, 0,
                  targetPos.x, targetPos.y, targetPos.z, 1 ]
        
        childJntMtx = cmds.getAttr( childJnt[0] + '.wm' )
        cmds.xform( targetJnt, ws=1, matrix=mtxList )
        cmds.xform( childJnt[0], ws=1, matrix=childJntMtx )
        cmds.scale( 1,1,1, targetJnt, pcp=1 )
        cmds.setAttr( childJnt[0] + '.s', 1,1,1 )



class PutObjectContext( OpenMayaMPx.MPxSelectionContext ):

    contextName = 'sgPutJointLineContext'
    
    def __init__(self):
        OpenMayaMPx.MPxSelectionContext.__init__( self )


    def toolOnSetup(self, *args, **kwargs ):
        
        meshShape = getSelection()
        if not meshShape:
            cmds.error( "Select mesh first" )
        
        self.meshName = meshShape
        self.dagPath = getDagPath( meshShape )
        self.meshMatrix = self.dagPath.inclusiveMatrix()
        self.meshMatrixInv = self.dagPath.inclusiveMatrixInverse()
        
        OpenMayaMPx.MPxSelectionContext.toolOnSetup( self, *args, **kwargs )
        
        self.beforeJoint = None
    

    def toolOffCleanup( self, *args, **kwargs ):
        OpenMayaMPx.MPxSelectionContext.toolOffCleanup(self, *args, **kwargs )


    def className( self, *args, **kwargs):
        OpenMayaMPx.MPxSelectionContext.className(self, *args, **kwargs)
        
    
    
    def getMouseXY(self, event ):
        argX = OpenMaya.MScriptUtil()
        argX.createFromInt(0)
        argXPtr = argX.asShortPtr()
        argY = OpenMaya.MScriptUtil()
        argY.createFromInt(0)
        argYPtr = argY.asShortPtr()
        event.getPosition(argXPtr, argYPtr)
        mouseX = OpenMaya.MScriptUtil(argXPtr).asShort()
        mouseY = OpenMaya.MScriptUtil(argYPtr).asShort()
        return mouseX, mouseY
    
    
    def doPress( self, event ):
        
        if event.mouseButton() == OpenMayaUI.MEvent.kMiddleMouse: 
            cmds.select( d=1 )
            self.beforeJoint = None
            return None
        
        self.transform = None
        mouseX, mouseY = self.getMouseXY( event )

        intersectPoint = Functions.getIntersectPoint( self.dagPath, mouseX, mouseY )
        if not intersectPoint: 
            return None
        
        if not self.beforeJoint:
            cmds.select( d=1 )
        self.transform = cmds.joint()    
        cmds.select( self.transform )
        self.beforePosition = cmds.xform( self.transform, q=1, ws=1, t=1 )[:3]
        cmds.undoInfo( swf=0 )
        cmds.move( intersectPoint.x, intersectPoint.y, intersectPoint.z, self.transform, ws=1 )
        self.currentPosition = [intersectPoint.x, intersectPoint.y, intersectPoint.z]
        
        if self.beforeJoint:
            Functions.setOrientByChild( self.beforeJoint )
            cmds.setAttr( self.transform + '.r', 0,0,0 )
        
        cmds.refresh()
    

    def doDrag(self, event ):
        if not self.transform: return None
        mouseX, mouseY = self.getMouseXY( event )

        intersectPoint = Functions.getIntersectPoint( self.dagPath, mouseX, mouseY )
        if not intersectPoint: 
            return None
        
        cmds.move( intersectPoint.x, intersectPoint.y, intersectPoint.z, self.transform, ws=1 )
        self.currentPosition = [intersectPoint.x, intersectPoint.y, intersectPoint.z]
        
        if self.beforeJoint:
            Functions.setOrientByChild( self.beforeJoint )
            cmds.setAttr( self.transform + '.r', 0,0,0 )
        
        cmds.refresh()


    def doRelease(self, event ):
        cmds.move( self.beforePosition[0], self.beforePosition[1], self.beforePosition[2], self.transform, ws=1 )
        cmds.undoInfo( swf=1 )
        cmds.move( self.currentPosition[0], self.currentPosition[1], self.currentPosition[2], self.transform, ws=1 )
        
        self.beforeJoint = self.transform
        pass




class PutObjectContextCommand( OpenMayaMPx.MPxContextCommand ):
    
    commandName = "sgPutJointLineContextCommand"
    def __init__(self):
        OpenMayaMPx.MPxContextCommand.__init__( self )
        self.m_pContext = 0
        
    @staticmethod
    def creator():
        return OpenMayaMPx.asMPxPtr( PutObjectContextCommand() )
    
    def doEditFlags( self ):
        return OpenMayaMPx.MPxContextCommand.doEditFlags( self )
    
    def doQueryFlags( self ):
        return OpenMayaMPx.MPxContextCommand.doQueryFlags( self )
    
    def appendSyntax( self ):
        return OpenMayaMPx.MPxContextCommand.appendSyntax( self )
    
    def makeObj(self):
        return OpenMayaMPx.asMPxPtr( PutObjectContext() )



# initialize the script plug-in
def initializePlugin(mobject):
    import maya.mel as mel
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Autodesk", "1.0", "Any")
    mplugin.registerContextCommand( PutObjectContextCommand.commandName,
                                    PutObjectContextCommand.creator )
    
    mel.eval( "%s %s1" %( PutObjectContextCommand.commandName, PutObjectContext.contextName ))



# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    import maya.mel as mel
    
    mel.eval( "deleteUI %s1" %( PutObjectContext.contextName ) )
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    mplugin.deregisterContextCommand( PutObjectContextCommand.commandName )
