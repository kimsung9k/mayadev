#include "node.h"


bool indexExists( int index, const MIntArray& indices )
{
	for( int i=0; i< indices.length(); i++ )
	{
		if( indices[i] == index )
			return true;
	}
	return false;
}


MMatrix MainNode::getMultMtxDelta( const Weights& weighs )
{
	MMatrix baseMtx;
	baseMtx *= 0.0;

	int logicalIndex;
	int indexMtx;

	for( int i=0; i< weighs.m_logicalIndices.length(); i++ )
	{
		logicalIndex= weighs.m_logicalIndices[i];
		float weight = weighs.m_values[i];
		indexMtx = m_intArrMtxLogicalMap[ logicalIndex ];
		baseMtx += m_mtxArrBindPre[ indexMtx ] * m_mtxArr[ indexMtx ] * weight;
	}

	return baseMtx;
}


MStatus MainNode::chk_updateSkinClusterInfo( const MMatrix& mtx )
{
	MStatus status;

	if( m_plugMtx.isNull() )
	{
		MFnDependencyNode fnNode( thisMObject() );

		MPlug plugMsg = fnNode.findPlug( aMsgSkinCluster );
		MPlugArray connections;
		plugMsg.connectedTo( connections, true, false );
		
		if( !connections.length() )
			return MS::kFailure;

		if( connections[0].node().apiType() == MFn::kSkinClusterFilter )
		{
			MFnDependencyNode fnNode = connections[0].node();

			m_plugMtx = fnNode.findPlug( "matrix" );
			m_plugBindPre = fnNode.findPlug( "bindPreMatrix" );
			MPlug plugWeightList = fnNode.findPlug( "weightList" );

			m_deltaList.setLength( plugWeightList.numElements() );
			m_deltaList.setWLength( plugWeightList.numElements() );

			for( int i=0; i<m_deltaList.length(); i++ )
			{
				MPlug plugWeights = plugWeightList[i].child( 0 );
				//cout << plugWeights.name() << " : " << plugWeights.numElements() << endl;
				for( int j=0; j < plugWeights.numElements(); j++ )
				{
					m_deltaList.m_pWeights[i].append( plugWeights[j].asFloat(), plugWeights[j].logicalIndex() );
				}
			}

			int logicalLength = m_plugMtx[ m_plugMtx.numElements()-1 ].logicalIndex() + 1;

			m_mtxArr.setLength( m_plugMtx.numElements() );
			m_mtxArrBindPre.setLength( m_plugMtx.numElements() );
			m_intArrMtxLogicalMap.setLength( logicalLength );

			for( int i=0; i< m_plugMtx.numElements(); i++ )
			{
				int logicalIndex = m_plugMtx[i].logicalIndex();
				MPlug plugBindPreEl = m_plugBindPre.elementByLogicalIndex( logicalIndex );

				MFnMatrixData fnMtxBindPre = plugBindPreEl.asMObject();
				m_mtxArrBindPre[i] = mtx * fnMtxBindPre.matrix();
				m_intArrMtxLogicalMap[logicalIndex] = i;
			}
		}
		else
		{
			return MS::kFailure;
		}
	}

	for( int i=0; i< m_plugMtx.numElements(); i++ )
	{
		int logicalIndex = m_plugMtx[i].logicalIndex();

		MFnMatrixData fnMtx = m_plugMtx[i].asMObject();
		MFnMatrixData fnBindPre = m_plugBindPre[i].asMObject();
		m_mtxArr[i] = fnMtx.matrix() * mtx.inverse();
		m_mtxArrBindPre[i] = mtx * fnBindPre.matrix();
	}

	return MS::kSuccess;
}


MStatus MainNode::chk_inputGeomPoints( const MItGeometry& itMesh )
{
	if( m_updateInputGeom )
	{
		itMesh.allPositions( m_pointArrBase );
		m_pointArrResult = m_pointArrBase;
		m_multedMtx.setLength( m_pointArrResult.length() );
		m_defaultDeltas.setLength( m_pointArrResult.length() );
		for( int i=0; i< m_defaultDeltas.length(); i++ )
		{
			m_defaultDeltas[i] = MVector(0,0,0);
		}
		m_updateInputGeom = false;
	}
	return MS::kSuccess;
}


MStatus MainNode::chk_deltaInfoAllUpdate( MArrayDataHandle& hArrDeltaInfo, const MMatrix& mat )
{
	MStatus status;

	int numDeltaInfo = hArrDeltaInfo.elementCount();

	MVector delta;
	if( m_numDeltaInfo != numDeltaInfo )
	{
		m_numDeltaInfo = numDeltaInfo; // 다시 업데이트 방지
		m_deltaList.setLength( m_pointArrBase.length() );
		m_weightEachShape.clear();
		m_weightEachShapeLogical.clear();

		for( int i=0; i< numDeltaInfo; i++, hArrDeltaInfo.next() )
		{
			MDataHandle hDeltaInfo = hArrDeltaInfo.inputValue();
			MDataHandle hInputMesh = hDeltaInfo.child( aInputMesh );
			MArrayDataHandle hArrDelta = hDeltaInfo.child( aDelta );
			MDataHandle hWeight = hDeltaInfo.child( aWeight );

			MFnMesh meshInput = hInputMesh.asMesh();
			m_plugDeltaInfo[i].child( aInputMesh ).connectedTo( m_connections, true, false );

			if( !m_connections.length() )
			{
				for( int j=0; j< m_deltaList.length(); j++ )
				{
					m_deltaList[j].append( MVector(0,0,0) );
				}
				for( int j=0; j< hArrDelta.elementCount(); j++, hArrDelta.next() )
				{
					MDataHandle hDelta = hArrDelta.inputValue();
					m_deltaList[ hArrDelta.elementIndex() ].assignLast( hDelta.asVector() );
				}
			}
			else
			{
				MPointArray pointArrInput;
				meshInput.getPoints( pointArrInput );

				if( pointArrInput.length() != m_pointArrBase.length() )
					continue;

				MArrayDataBuilder bArrDelta( aDelta, m_pointArrBase.length() );
				int lengthAppend = 0;
				for( int j=0; j< m_pointArrBase.length(); j++ )
				{
					delta.x = pointArrInput[j].x - m_pointArrBase[j].x;
					delta.y = pointArrInput[j].y - m_pointArrBase[j].y;
					delta.z = pointArrInput[j].z - m_pointArrBase[j].z;
				
					delta *= getMultMtxDelta( m_deltaList.m_pWeights[j] ).inverse();
					m_deltaList[j].append( MVector( 0,0,0 ) );

					if( delta.length() > 0.0001 )
					{
						MDataHandle hDelta = bArrDelta.addElement( j );
						hDelta.setMVector( delta );
						m_deltaList[j].assignLast( delta );
						lengthAppend+=1;
					}
				}
				hArrDelta.set( bArrDelta );
				hArrDelta.setAllClean();
			}
			m_weightEachShape.append( hWeight.asFloat() );
			m_weightEachShapeLogical.append( hArrDeltaInfo.elementIndex() );
		}
	}
	return MS::kSuccess;
}


MStatus MainNode::chk_deltaInfoMovedUpdate( MArrayDataHandle& hArrDeltaInfo, const MMatrix& meshMatrix )
{
	MStatus status;

	MVector delta;
	
	for( int i=0; i< hArrDeltaInfo.elementCount(); i++, hArrDeltaInfo.next() )
	{
		int logicalIndex = hArrDeltaInfo.elementIndex();

		if( !indexExists( logicalIndex, m_indicesUpdateMesh ) ) continue;

		MDataHandle hDeltaInfo = hArrDeltaInfo.inputValue();
		MDataHandle hInputMesh = hDeltaInfo.child( aInputMesh );
		MArrayDataHandle hArrDelta = hDeltaInfo.child( aDelta );
		MDataHandle hWeight = hDeltaInfo.child( aWeight );

		MFnMesh meshInput = hInputMesh.asMesh();
		MPointArray pointArrInput;
		meshInput.getPoints( pointArrInput );

		if( pointArrInput.length() != m_pointArrBase.length() )
		{
			if( hArrDelta.elementCount() == 0 )
			{
				char buffer[512];
				sprintf( buffer, "removeMultiInstance %s[%d]", m_plugDeltaInfo.name().asChar(), logicalIndex );
				MGlobal::executeCommand( buffer );
			}
			continue;
		}

		MArrayDataBuilder bArrDelta( aDelta, m_pointArrBase.length() );
		for( int j=0; j< m_pointArrBase.length(); j++ )
		{
			delta.x = pointArrInput[j].x - m_pointArrBase[j].x;
			delta.y = pointArrInput[j].y - m_pointArrBase[j].y;
			delta.z = pointArrInput[j].z - m_pointArrBase[j].z;
			
			delta *= getMultMtxDelta( m_deltaList.m_pWeights[j] ).inverse();
			m_deltaList[j].pointsEachChannel[i] = delta;

			if( delta.length() > 0.0001 )
			{
				MDataHandle hDelta = bArrDelta.addElement( j );
				hDelta.setMVector( delta );
			}
		}
		hArrDelta.set( bArrDelta );
		hArrDelta.setAllClean();

		m_weightEachShape[i] = hWeight.asFloat();
	}

	m_indicesUpdateMesh.clear();

	return MS::kSuccess;
}


MStatus MainNode::chk_updateWeights( MArrayDataHandle& hArrDeltaInfo )
{
	MStatus status;
	for( int i=0; i< hArrDeltaInfo.elementCount(); i++, hArrDeltaInfo.next() )
	{
		int logicalIndex = hArrDeltaInfo.elementIndex();
		MDataHandle hDeltaInfo = hArrDeltaInfo.inputValue();
		MDataHandle hWeight    = hDeltaInfo.child( aWeight );

		for( int j=0; j< m_weightEachShapeLogical.length(); j++ )
		{
			if( logicalIndex == m_weightEachShapeLogical[j] )
			{
				m_weightEachShape[j] = hWeight.asFloat();
			}
		}
	}
	return MS::kSuccess;
}


MStatus MainNode::caculate()
{
	MStatus status;

	m_pointArrResult = m_pointArrBase;

	bool weightExists = false;
	for( int i=0; i< m_weightEachShape.length(); i++ )
	{
		if( m_weightEachShape[i] ) weightExists = true;
	}

	if( !weightExists ) return MS::kSuccess;
	m_addedDeltas = m_defaultDeltas;

	if( m_numBeforeDeltaInfo != m_numDeltaInfo )
	{
		m_numBeforeDeltaInfo = m_numDeltaInfo;
	}

	for( int i=0; i< m_deltaList.length(); i++ )
	{
		Weights& weights = m_deltaList.m_pWeights[i];
		m_multedMtx[i] = getMultMtxDelta( weights );
	}

	for( int i=0; i< m_weightEachShape.length(); i++ )
	{
		if( !m_weightEachShape[i] ) continue;
		for( int j=0; j< m_deltaList.length(); j++ )
		{
			Delta& delta = m_deltaList[j];
			m_addedDeltas[j] += delta.pointsEachChannel[i]* m_weightEachShape[i];
		}
	}

	for( int i=0; i< m_deltaList.length(); i++ )
	{
		m_pointArrResult[i] += m_addedDeltas[i] * m_multedMtx[i];
	}

	return MS::kSuccess;
}