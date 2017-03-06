#include  "assignBlendMeshInfo.h"


assignBlendMeshInfo::assignBlendMeshInfo()
{
}


assignBlendMeshInfo::~assignBlendMeshInfo()
{
}


bool	assignBlendMeshInfo::isUndoable() const
{
	return true;
}


void*	assignBlendMeshInfo::creator()
{
	return new assignBlendMeshInfo();
}


MSyntax	assignBlendMeshInfo::newSyntax()
{
	MSyntax	syntax;

	syntax.setObjectType( MSyntax::kSelectionList, 2, 2 );
	syntax.useSelectionAsDefault( false );

	syntax.enableEdit( false );
	syntax.enableQuery( false );

	return syntax;
}


MStatus	assignBlendMeshInfo::doIt( const MArgList& args )
{
	MStatus status;

	MArgDatabase	argData( syntax(), args, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MSelectionList	selList;
	status = argData.getObjects( selList );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	status = selList.getDagPath( 0, m_pathShape );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = getShapeNode( m_pathShape );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = selList.getDependNode( 1, m_oNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnDependencyNode fnNode = m_oNode;
	if( fnNode.typeName() !="blendAndFixedShape" )
	{
		return MS::kFailure;
	}
	
	MPlug plugBlendMeshInfo = fnNode.findPlug( "blendMeshInfos" );
	m_indexTarget = plugBlendMeshInfo.numElements();

	return redoIt();
}


MStatus	assignBlendMeshInfo::redoIt()
{
	MStatus status;

	MFnDagNode fnShape = m_pathShape.node();
	MPlug plugOutput = fnShape.findPlug( "outMesh" );
	MFnDagNode fnObject = fnShape.parent( 0, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnDependencyNode fnNode = m_oNode;
	MPlug plugElement = fnNode.findPlug( "blendMeshInfos" ).elementByLogicalIndex( m_indexTarget );
	MPlug plugInput   = plugElement.child( 0 );
	MPlug plugMeshName = plugElement.child( 3 );

	m_mdgModifier.connect( plugOutput, plugInput );
	m_mdgModifier.doIt();
	plugMeshName.setString( fnObject.name() );

	return MS::kSuccess;
}


MStatus assignBlendMeshInfo::undoIt()
{
	MStatus status;

	MFnDependencyNode fnNode = m_oNode;
	MPlug plugElement = fnNode.findPlug( "blendMeshInfos" )[ m_indexTarget ];
	char buffer[512];
	sprintf( buffer, "removeMultiInstance %s -b true;", plugElement.name().asChar() );
	MGlobal::executeCommand( buffer );

	return MS::kSuccess;
}


MStatus assignBlendMeshInfo::getShapeNode( MDagPath& path )
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