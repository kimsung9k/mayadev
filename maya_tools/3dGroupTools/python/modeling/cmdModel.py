import maya.cmds as cmds
import maya.OpenMaya as om
import model


def getMObject( target ):
    
    selList = om.MSelectionList()
    selList.add( target )
    
    mObj = om.MObject()
    selList.getDependNode( 0, mObj )
    
    return mObj


def setMesh( first, second ):
    
    model.MeshInfo.fnFirstMesh = om.MFnMesh( getMObject(first) )
    model.MeshInfo.fnSecondMesh = om.MFnMesh( getMObject(second) )
    
    model.MeshInfo.fnFirstMesh.getUVs( model.MeshInfo.firstUs, model.MeshInfo.firstVs )
    model.MeshInfo.fnSecondMesh.getUVs( model.MeshInfo.secondUs, model.MeshInfo.secondVs )
    
    


def setUVs( selUVs ):
    
    firstMeshName = model.MeshInfo.fnFirstMesh.name()
    firstMeshName = cmds.listRelatives( firstMeshName, p=1 )[0]
    secondMeshName = model.MeshInfo.fnSecondMesh.name()
    secondMeshName = cmds.listRelatives( secondMeshName, p=1 )[0]
    
    firstUVs = []
    secondUVs = []
    for uv in selUVs:
        if uv.find( firstMeshName ) != -1:
            firstUVs.append( int( uv.split( '[' )[1].replace( ']', '' ) ) )
        else:
            secondUVs.append( int( uv.split( '[' )[1].replace( ']', '' ) ) )
    
    print firstUVs, secondUVs
            
    for i in range( len( firstUVs ) ):
        
        closeDist = 100000.0
        closeIndex = 0
        
        closeDiffU = 0
        closeDiffV = 0
        
        fUs = model.MeshInfo.firstUs[ firstUVs[i] ]
        fVs = model.MeshInfo.firstVs[ firstUVs[i] ]
        
        for j in range( len( secondUVs ) ):
            sUs = model.MeshInfo.secondUs[ secondUVs[j] ]
            sVs = model.MeshInfo.secondVs[ secondUVs[j] ]
            
            diffU = fUs-sUs
            diffV = fVs-sVs
            dist = ( diffU**2 + diffV**2 )**0.5
            if dist < closeDist :
                closeDist = dist
                closeIndex = j
                closeDiffU = diffU
                closeDiffV = diffV
        
        cmds.polyEditUV( secondMeshName + '.map[%d]' % secondUVs[closeIndex], u=closeDiffU, v=closeDiffV ) 
        


uiCmd_OpenSubTagingUI="""import modeling.subTagging.view
modeling.subTagging.view.showUI()"""