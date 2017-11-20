import maya.api.OpenMaya as mayaApi

selList = mayaApi.MSelectionList()

selList.add( 'pSphereShape1' )
fnMesh = mayaApi.MFnMesh( selList.getDagPath( 0 ) )

fnMesh.getUVSetNames()

uArray = mayaApi.MFloatArray()
vArray = mayaApi.MFloatArray()
uvCounts = mayaApi.MIntArray()
uvIds    = mayaApi.MIntArray()