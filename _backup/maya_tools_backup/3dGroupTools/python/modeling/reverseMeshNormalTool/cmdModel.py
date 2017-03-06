import maya.OpenMaya as om
import maya.cmds as cmds



def getDagPath( target ):
    selList = om.MSelectionList()
    selList.add( target )
    dagPath = om.MDagPath()
    selList.getDagPath( 0, dagPath )
    return dagPath



def getCurrentCam():
    panel = cmds.getPanel( wf=1 )
    if cmds.getPanel( to=panel ) != "modelPanel": return None
    return cmds.modelEditor( panel, q=1, camera=1 )




def reverseNormalMesh( *args ):
    
    cam = getCurrentCam()
    
    camMtx = getDagPath( cam ).inclusiveMatrix()
    camPos = om.MPoint( camMtx(3,0), camMtx(3,1), camMtx(3,2) )
    
    sels = cmds.ls( sl=1 )
    
    for sel in sels:
        if not cmds.nodeType( sel ) in ['transform', 'mesh']: continue
        if cmds.nodeType( sel ) == 'transform':
            shapes = cmds.listRelatives( sel, s=1 )
            if not shapes: continue
            if cmds.nodeType( shapes[0] ) != 'mesh': continue
            sel = shapes[0]
        
        pathMesh = getDagPath( sel )
        fnMesh = om.MFnMesh( pathMesh )
        pointsMesh = om.MPointArray()
        fnMesh.getPoints( pointsMesh )
        meshMtx = pathMesh.inclusiveMatrix()
        meshMtxInv = pathMesh.inclusiveMatrixInverse()
        
        posLocalCam = camPos* meshMtxInv
        
        #cmds.spaceLocator( p=[posLocalCam.x, posLocalCam.y, posLocalCam.z])
        
        numPolygon = fnMesh.numPolygons()
        
        revFaces = []
        for i in range( numPolygon ):
            normal = om.MVector()
            vertices = om.MIntArray()
            fnMesh.getPolygonNormal( i, normal )
            fnMesh.getPolygonVertices( i, vertices )
            
            avPoint = om.MVector( 0,0,0 )
            for j in range( vertices.length() ):
                avPoint += om.MVector( pointsMesh[ vertices[j] ] )
            avPoint /= vertices.length()
            
            vectorCamPos = om.MVector( posLocalCam - avPoint )
            if vectorCamPos*normal > 0: continue
            
            points = om.MPointArray()
            rayExists = fnMesh.intersect( om.MPoint( avPoint ), om.MVector( vectorCamPos ), points )
            
            if rayExists:
                dist = points[0].distanceTo( om.MPoint( avPoint ) )
                if dist > 0.0001 and dist < 0.0002: continue
            revFaces.append( sel+'.f[%d]' % i )
        
        if not revFaces: continue
        cmds.polyNormal( revFaces, normalMode=0, userNormalMode=0, ch=0 )
            