#include "sgPolyUnit.h"


MStatus sgPolyUnit::check_and_buildMeshData( MDataBlock& data )
{
	MStatus status;

	MArrayDataHandle hArrInputMeshs = data.inputArrayValue( aInputMeshs );
	int numElement = hArrInputMeshs.elementCount();

	if( m_oArr_inputMesh.length() != numElement )
	{
		m_oArr_inputMesh.setLength( numElement );
		m_mtxArr_inputMesh.setLength( numElement );
		m_intArr_numVertices.setLength( numElement );
		m_intArr_numPolygons.setLength( numElement );
		m_rebuildMeshData = true;
	}

	for( int i=0; i< hArrInputMeshs.elementCount(); i++, hArrInputMeshs.next() )
	{
		MDataHandle hInputMesh = hArrInputMeshs.inputValue();
		MObject oMesh = hInputMesh.asMesh();

		MFnMesh fnMesh( oMesh );
		MDagPath dagPath = fnMesh.dagPath();

		m_oArr_inputMesh[i] = oMesh;
		int numVertices   = fnMesh.numVertices();
		if( m_intArr_numVertices[i] != numVertices )
		{
			m_intArr_numVertices[i] = numVertices;
			m_rebuildMeshData = true;
		}

		int numPolygons   = fnMesh.numPolygons();
		if( m_intArr_numPolygons[i] != numPolygons )
		{
			m_intArr_numPolygons[i] = numPolygons;
			m_rebuildMeshData = true;
		}

		m_mtxArr_inputMesh[i] = dagPath.inclusiveMatrix();
	}

	if( m_rebuildMeshData )
	{
		m_sgBuildMeshData.clear();
		for( int i=0; i< m_oArr_inputMesh.length(); i++ )
		{
			m_sgBuildMeshData.appendMeshData( m_oArr_inputMesh[i], m_mtxArr_inputMesh[i] );
		}
		m_sgBuildMeshData.build();
	}
	else
	{
		int startIndex = 0;

		for( int i=0; i< m_oArr_inputMesh.length(); i++ )
		{
			MFnMesh fnMesh( m_oArr_inputMesh[i] );
			m_sgBuildMeshData.getPositon( m_oArr_inputMesh[i], m_mtxArr_inputMesh[i], startIndex );
			startIndex += fnMesh.numVertices();
		}
		m_sgBuildMeshData.setPosition();
	}

	return MS::kSuccess;
}