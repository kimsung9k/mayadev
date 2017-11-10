#include "sgSmoothWeightCommand.h"
#include "SGPrintf.h"

MObject sgSmoothWeightCommand::m_oSkinCluster;
MDagPath sgSmoothWeightCommand::m_pathMesh;
MPlug sgSmoothWeightCommand::m_plugWeightList;
ConnectedIndices sgSmoothWeightCommand::m_connectedIndices;

MStatus sgSmoothWeightCommand::getShapeNode( MDagPath& path )
{
	MStatus status;

	if( path.apiType() == MFn::kMesh )
	{
		return MS::kSuccess;
	}

	if( path.apiType() != MFn::kTransform )
	{
		return MS::kFailure;
	}

	unsigned int numShapes;
	path.numberOfShapesDirectlyBelow( numShapes );

	if( !numShapes ) return MS::kFailure;

	for( int i=0; i< numShapes; i++ )
	{
		status = path.extendToShapeDirectlyBelow( i );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		if( path.apiType() == MFn::kMesh )
		{
			MFnDagNode fnNode = path.node();
			if( !fnNode.isIntermediateObject() )
			{
				return MS::kSuccess;
			}
		}
		path.pop();
	}
	return MS::kFailure;
}


MStatus sgSmoothWeightCommand::getSkinClusterNode( MDagPath& path, MObject& oNode )
{
	MStatus status;

	MItDependencyGraph itGraph( path.node(), MFn::kInvalid, MItDependencyGraph::kUpstream );

	while( !itGraph.isDone() )
	{
		oNode = itGraph.currentItem();

		if( oNode.apiType() == MFn::kSkinClusterFilter )
		{
			return MS::kSuccess;
		}

		itGraph.next();
	}

	return MS::kFailure;
}


MStatus sgSmoothWeightCommand::getWeightValueAndIndices( MPlug& plugWeightList,
	MIntArray& indicesWeights, MFloatArray& valuesWeights )
{
	MStatus status;

	MPlug plugWeights = plugWeightList.child( 0 );
	int numElements = plugWeights.numElements();

	indicesWeights.setLength( numElements );
	valuesWeights.setLength( numElements );

	for( int i=0; i<numElements ; i++ )
	{
		indicesWeights[i] = plugWeights[i].logicalIndex();
		valuesWeights[i]  = plugWeights[i].asFloat();
	}
	return MS::kSuccess;
}


MIntArray sgSmoothWeightCommand::getConnectedIndices( const MDagPath& pathMesh, int index )
{
	MFnSingleIndexedComponent vertices;
	const int indices[1] = { index };
	MIntArray elements( indices, 1 );

	MObject components = vertices.create( MFn::kMeshVertComponent );
	vertices.addElements( elements );

	MItMeshVertex itMeshVtx( pathMesh, components );
	int getIndex;
	itMeshVtx.setIndex( index, getIndex );

	MIntArray intArrConnected;
	itMeshVtx.getConnectedVertices( intArrConnected );

	return intArrConnected;
}


void  sgSmoothWeightCommand::normalizeWeights( MFloatArray& valuesWeights )
{
	int length = valuesWeights.length();

	float sumWeights = 0.0f;
	for( int i=0; i< length; i++ )
	{
		sumWeights += valuesWeights[i];
	}
	for( int i=0; i< length; i++ )
	{
		valuesWeights[i] /= sumWeights;
	}
}


void  sgSmoothWeightCommand::getSmoothWeight( MPlug& plugWeightList, int indexTarget, 
	                            MIntArray& indicesGet, MFloatArray& valuesGet )
{
	MIntArray& indicesConnected = m_connectedIndices.p_indices[indexTarget];

	int lengthIndices = indicesConnected.length();

	indicesGet.clear();
	valuesGet.clear();

	for( int i=0; i<lengthIndices; i++ )
	{
		MPlug plugWeights = plugWeightList.elementByLogicalIndex( indicesConnected[i] ).child(0);
		for( int j=0; j<plugWeights.numElements(); j++ )
		{
			int logical = plugWeights[j].logicalIndex();
			float value = plugWeights[j].asFloat();

			bool assigned = false;
			for( int k=0; k<indicesGet.length(); k++ )
			{
				if( indicesGet[k] == logical )
				{
					valuesGet[k] += value / lengthIndices;
					assigned = true;
					break;
				}
			}
			if( !assigned )
			{
				indicesGet.append( logical );
				valuesGet.append( value / lengthIndices );
			}
		}
	}
	float sumValue = 0.0;
	normalizeWeights( valuesGet );
}


void  sgSmoothWeightCommand::getHardWeight( MPlug& plugWeightList, int indexTarget, 
	                            const MIntArray& indicesBefore, const MFloatArray& valuesBefore,
								MIntArray& indicesAfter, MFloatArray& valuesAfter )
{
	indicesAfter.clear();
	valuesAfter.clear();

	valuesAfter.setLength( valuesBefore.length() );
	for( int i=0; i< valuesBefore.length(); i++ )
	{
		valuesAfter[i] = pow( valuesBefore[i], 2 );
	}

	indicesAfter = indicesBefore;
	
	normalizeWeights( valuesAfter );
}

void sgSmoothWeightCommand::editAfterValueByWeight( MIntArray& indicesBefore, MFloatArray& valuesBefore,
	                                              MIntArray& indicesAfter, MFloatArray& valuesAfter, float weight )
{
	float invWeight = 1.0f-weight;

	MIntArray indices;
	MFloatArray values;

	for( int i=0; i< indicesBefore.length(); i++ )
	{
		bool exists = false;
		for( int j=0; j< indices.length(); j++ )
		{
			if( indices[j] == indicesBefore[i] )
			{
				values[j] += valuesBefore[i]*invWeight;
				exists = true;
				break;
			}
		}
		if( !exists )
		{
			indices.append( indicesBefore[i] );
			values.append( valuesBefore[i]*invWeight );
		}
	}

	for( int i=0; i< indicesAfter.length(); i++ )
	{
		bool exists = false;
		for( int j=0; j< indices.length(); j++ )
		{
			if( indices[j] == indicesAfter[i] )
			{
				values[j] += valuesAfter[i]*weight;
				exists = true;
				break;
			}
		}
		if( !exists )
		{
			indices.append( indicesAfter[i] );
			values.append( valuesAfter[i]*weight );
		}
	}

	indicesAfter = indices;
	valuesAfter  = values;
}


void sgSmoothWeightCommand::setWeightValue( MPlug& plugWeightList,
		                        const MIntArray& indices, const MFloatArray& values )
{
	int numElement = plugWeightList.array().numElements();
	if (numElement <= plugWeightList.logicalIndex()) {
		return;
	}

	MPlug plugWeights = plugWeightList.child(0);

	MIntArray beforeIndices;
	MFloatArray beforeValues;

	for( int i=0; i< plugWeights.numElements(); i++ )
	{
		beforeIndices.append( plugWeights[i].logicalIndex() );
		beforeValues.append( plugWeights[i].asFloat() );
	}
	/*
	cout << "-----------------------------" << endl;
	for( int i=0; i< beforeIndices.length(); i++ )
	{
		printf(" %6d ", beforeIndices[i] );
	}
	printf( "\n" );
	for( int i=0; i< beforeValues.length(); i++ )
	{
		printf(" %5.4f ", beforeValues[i] );
	}
	printf( "\n" );
	for( int i=0; i< indices.length(); i++ )
	{
		printf(" %6d ", indices[i] );
	}
	printf( "\n" );
	for( int i=0; i< values.length(); i++ )
	{
		printf(" %5.4f ", values[i] );
	}
	printf( "\n" );
	cout << "-----------------------------" << endl;
	*/
	for( int i=0; i< indices.length(); i++ )
	{
		plugWeights.elementByLogicalIndex( indices[i] ).setFloat( values[i] );
	}
}


MStatus sgSmoothWeightCommand::getInfomaiton( const MArgDatabase& argData )
{
	MStatus status;

	MSelectionList selList;
	status = argData.getObjects( selList );

	selList.getDagPath( 0, m_pathMesh );

	getShapeNode( m_pathMesh );
	getSkinClusterNode( m_pathMesh, m_oSkinCluster );

	m_plugWeightList = MFnDependencyNode( m_oSkinCluster ).findPlug( "weightList" );

	MFnMesh fnMesh = m_pathMesh;

	m_connectedIndices.setLength( fnMesh.numVertices() );
	for( int i=0; i<fnMesh.numVertices(); i++ )
	{
		m_connectedIndices.p_indices[i] = getConnectedIndices( m_pathMesh, i );
	}

	return MS::kSuccess;
}



void sgSmoothWeightCommand::removeMultiInstance( const MIntArray& beforeIndices, const MIntArray& afterIndices )
{
	MPlug plugWeights = m_plugWeightList.elementByLogicalIndex( m_index ).child( 0 );

	char buffer[512];

	for( int i=0; i< afterIndices.length(); i++ )
	{
		bool exists = false;
		for( int j=0; j< beforeIndices.length(); j++ )
		{
			if( beforeIndices[j] == afterIndices[i] )
				exists = true;
		}
		if( !exists )
		{
			sprintf( buffer, "removeMultiInstance %s;" , plugWeights.elementByLogicalIndex( afterIndices[i] ).name().asChar() );
			MGlobal::executeCommand( buffer );
		}
	}
}