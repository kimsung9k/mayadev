#include "MeshSnapCommand.h"
#include "MeshSnapDeformer.h"


MeshSnapCommand::MeshSnapCommand()
{
}




void* MeshSnapCommand::creator()
{
    return new MeshSnapCommand;
}




bool MeshSnapCommand::isUndoable() const
{
    return true;
}




MSyntax MeshSnapCommand::newSyntax()
{
    MSyntax syntax;
    
    syntax.addFlag( "-n", "-name", MSyntax::kString );
    syntax.setObjectType( MSyntax::kSelectionList, 2, 2 );
    syntax.useSelectionAsDefault( true );

    syntax.enableEdit( false );
    syntax.enableQuery( false );

    return syntax;
}



MStatus MeshSnapCommand::doIt( const MArgList& argList )
{
    MStatus status;

    // Read all the flag arguments
    MArgDatabase argData( syntax(), argList, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    MSelectionList selection;
    status = argData.getObjects( selection );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    status = selection.getDagPath( 0, m_pathBaseMesh );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    status = selection.getDagPath( 1, m_pathSnapMesh );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    status = getShapeNode( m_pathBaseMesh );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    status = getShapeNode( m_pathSnapMesh );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    status = calculateVertexMapping();
    CHECK_MSTATUS_AND_RETURN_IT( status );

    if ( argData.isFlagSet( "-n" ) )
    {
        m_name = argData.flagArgumentString( "-n", 0, &status );
        CHECK_MSTATUS_AND_RETURN_IT( status );
    }
    else
    {
        m_name = "meshSnap#";
    }

    char buffer[512];
    sprintf( buffer, "deformer -type meshSnap -n \"%s\" %s", m_name.asChar(),
        m_pathBaseMesh.partialPathName().asChar() );
    status = m_dgMod.commandToExecute( buffer );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    return redoIt();
}



MStatus MeshSnapCommand::getShapeNode( MDagPath& path )
{
    MStatus status;

    if ( path.apiType() == MFn::kMesh )
    {
        return MS::kSuccess;
    }

    unsigned int numShapes;
    status = path.numberOfShapesDirectlyBelow( numShapes );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    for ( unsigned int i = 0; i < numShapes; ++i )
    {
        status = path.extendToShapeDirectlyBelow( i );
        CHECK_MSTATUS_AND_RETURN_IT( status );

        if ( !path.hasFn( MFn::kMesh ) )
        {
            path.pop();
            continue;
        }

        MFnDagNode fnNode( path, &status );
        CHECK_MSTATUS_AND_RETURN_IT( status );
        if ( !fnNode.isIntermediateObject() )
        {
            return MS::kSuccess;
        }
        path.pop();
    }

    return MS::kFailure;
}



MStatus MeshSnapCommand::calculateVertexMapping()
{
    MStatus status;

    MFnMesh fnBaseMesh( m_pathBaseMesh, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    MPointArray basePoints;
    status = fnBaseMesh.getPoints( basePoints );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    unsigned int numBasePoints = basePoints.length();
    MMeshIntersector intersector;
    MObject oBaseMesh = m_pathBaseMesh.node();
	intersector.create( oBaseMesh );

    MFnMesh fnSnapMesh( m_pathSnapMesh, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    MPointArray snapPoints;
    status = fnSnapMesh.getPoints( snapPoints );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    MPointOnMesh meshPoint;
    double thisDistance;
    int closestVertId, faceIndex;
    double minDistance;
    MIntArray vertexList;
    m_vertexMapping = MIntArray( numBasePoints, -1 );
    MDoubleArray distances( numBasePoints, 9999999.0 );

    for ( unsigned int ii = 0; ii < snapPoints.length(); ii++ )
    {
		MPoint snapPoint = snapPoints[ii];
        status = intersector.getClosestPoint( snapPoint, meshPoint );
        CHECK_MSTATUS_AND_RETURN_IT( status );
        faceIndex = meshPoint.faceIndex();
        fnBaseMesh.getPolygonVertices( faceIndex, vertexList );

        minDistance = 9999999.0;
        for ( unsigned int jj = 0; jj < vertexList.length(); jj++ )
        {
            thisDistance = basePoints[vertexList[jj]].distanceTo( snapPoints[ii] );
            if ( thisDistance < minDistance )
            {
                minDistance = thisDistance;
                closestVertId = vertexList[jj];
            }
        }
        m_vertexMapping[closestVertId] = ii;
        distances[closestVertId] = minDistance;
    }

    return MS::kSuccess;
}



MStatus MeshSnapCommand::redoIt()
{
    MStatus status;

    // Main functionality
    status = m_dgMod.doIt();
    CHECK_MSTATUS_AND_RETURN_IT( status );

    MFnIntArrayData fnIntData;
    MObject oData = fnIntData.create( m_vertexMapping, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    MObject oSnapDeformer;
    status = getSnapDeformerFromBaseMesh( oSnapDeformer );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    MPlug plugVertexMapping( oSnapDeformer, MeshSnap::aMapping );
    plugVertexMapping.setMObject( oData );

    MFnDagNode fnSnapMesh( m_pathSnapMesh, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    MPlug plugWorldMesh = fnSnapMesh.findPlug( "worldMesh", false, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    status = plugWorldMesh.selectAncestorLogicalIndex( 0, plugWorldMesh.attribute() );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    MPlug plugSnapMesh( oSnapDeformer, MeshSnap::aSnapMesh );

    MDGModifier dgMod;
    status = dgMod.connect( plugWorldMesh, plugSnapMesh );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    status = dgMod.doIt();
    CHECK_MSTATUS_AND_RETURN_IT( status );


    return MS::kSuccess;
}



MStatus MeshSnapCommand::getSnapDeformerFromBaseMesh( MObject& oSnapDeformer )
{
    MStatus status;
    MObject oBaseMesh = m_pathBaseMesh.node();
    MItDependencyGraph itGraph( oBaseMesh, MFn::kInvalid, MItDependencyGraph::kUpstream,
        MItDependencyGraph::kDepthFirst, MItDependencyGraph::kNodeLevel, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    while ( !itGraph.isDone() )
    {
        oSnapDeformer = itGraph.currentItem();
        MFnDependencyNode fnNode( oSnapDeformer, &status );
        CHECK_MSTATUS_AND_RETURN_IT( status );
        if ( fnNode.typeId() == MeshSnap::id )
        {
            return MS::kSuccess;
        }
        itGraph.next();
    }
    return MS::kFailure;
}



MStatus MeshSnapCommand::undoIt()
{
    MStatus status;

    // Restore the initial state
    status = m_dgMod.undoIt();
    CHECK_MSTATUS_AND_RETURN_IT( status );
    
    return MS::kSuccess;
}