#include "MeshSnapDeformer.h"

MTypeId MeshSnap::id( 0x0000001234 );
MObject MeshSnap::aSnapMesh;
MObject MeshSnap::aMapping;

MeshSnap::MeshSnap()
{
}


MeshSnap::~MeshSnap()
{
}


void* MeshSnap::creator() { return new MeshSnap; }


MStatus MeshSnap::deform( MDataBlock &data, MItGeometry &itGeo, const MMatrix &localToWorldMatrix, unsigned int mIndex )
{
    MStatus status; 
    float env = data.inputValue( envelope ).asFloat();

    // Get the snap mesh
    MObject oMesh = data.inputValue( aSnapMesh ).asMesh();

    // Get the vertex mapping
    MObject oMapData = data.inputValue( aMapping ).data();
    
    if ( oMesh.isNull() || env == 0.0f || oMapData.isNull() )
    {
        return MS::kSuccess;
    }

    MFnIntArrayData intData( oMapData, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    MIntArray vertexMapping = intData.array();

    // Get vertices to snap to from snap mesh
    MFnMesh fnMesh( oMesh, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    MPointArray snapVertices;
    fnMesh.getPoints( snapVertices, MSpace::kWorld );
    unsigned int numSnapVerts = snapVertices.length();

    MMatrix worldToLocalMatrix = localToWorldMatrix.inverse();
    MPoint pt;
    unsigned int snapVertexIndex;
    for ( itGeo.reset(); !itGeo.isDone(); itGeo.next() )
    {
        pt = itGeo.position();
        snapVertexIndex = vertexMapping[itGeo.index()];
        if ( snapVertexIndex != -1 )
        {
            pt = pt + ( ( (snapVertices[snapVertexIndex] * worldToLocalMatrix) - pt) * env );
            //pt = (snapVertices[snapVertexIndex] * worldToLocalMatrix);
        }
        itGeo.setPosition( pt );
    }
    return MS::kSuccess;
}


MStatus MeshSnap::initialize()
{
    MFnTypedAttribute tAttr;

    aSnapMesh = tAttr.create( "snapMesh", "snapMesh", MFnData::kMesh );
    addAttribute( aSnapMesh );
    attributeAffects( aSnapMesh, outputGeom );

    aMapping = tAttr.create( "vertexMapping", "vertexMapping", MFnData::kIntArray );
    tAttr.setHidden( true );
    tAttr.setConnectable( false );
    addAttribute( aMapping );
    attributeAffects( aMapping, outputGeom );

    return MS::kSuccess;
}