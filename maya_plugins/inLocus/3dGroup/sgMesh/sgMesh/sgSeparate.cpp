#include "sgSeparate.h"


MTypeId sgSeparate::id( 0x2015061600 );

MObject sgSeparate::aInputMeshs;
MObject sgSeparate::aElements;
	MObject sgSeparate::aElementIndices;
MObject sgSeparate::aOutputMeshs;


void* sgSeparate::creator()
{
	return new sgSeparate();
}


sgSeparate::sgSeparate()
{
	m_isDirty_inputMesh = true;
	m_isDirty_element = true;
	m_require_update = true;
	m_elementNum = 0;

	m_pTask = new sgSeparate_TaskData;
	MThreadPool::init();
}


sgSeparate::~sgSeparate()
{
	delete m_pTask;
	MThreadPool::release();
}


MStatus sgSeparate::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	if( m_isDirty_inputMesh )
	{
		MArrayDataHandle hArrInputMeshs = data.inputArrayValue( aInputMeshs );

		int length = hArrInputMeshs.elementCount();
		
		if( m_numVertices_inputs.length() != length )
		{
			m_require_update = true;
			m_numVertices_inputs.setLength( length );
			m_numPolygons_inputs.setLength( length );
			for( int i=0; i< length; i++ )
			{
				m_numVertices_inputs[i] = 0;
				m_numPolygons_inputs[i] = 0;
			}
		}

		m_oArrMeshs.setLength( hArrInputMeshs.elementCount() );
		for( int i=0; i< hArrInputMeshs.elementCount(); i++, hArrInputMeshs.next() )
		{
			MDataHandle hInputMesh = hArrInputMeshs.inputValue();
			MObject oMesh = hInputMesh.asMesh();

			MFnMesh fnMesh( oMesh );
			int numVertices_input = fnMesh.numVertices();
			int numPolygons_input = fnMesh.numPolygons();

			if( numVertices_input != m_numVertices_inputs[i] || numPolygons_input != m_numPolygons_inputs[i] )
			{
				m_numVertices_inputs[i] = numVertices_input;
				m_numPolygons_inputs[i] = numPolygons_input;
				m_require_update = true;
			}
			m_oArrMeshs[i] = oMesh;
		}
		if( m_require_update ){
			m_meshDataArray.clear();
			for( int i=0; i< m_oArrMeshs.length(); i++ )
				separateEachElement( m_oArrMeshs[i], i );
		}
	}

	if( m_require_update || m_isDirty_element )
	{
		int sepLength = m_meshDataArray.length();

		m_meshDataArray_output.clear();
		MArrayDataHandle hArrElements = data.inputArrayValue( aElements );
		for( int i=0; i< hArrElements.elementCount(); i++, hArrElements.next() )
		{
			MDataHandle hElement = hArrElements.inputValue();
			MArrayDataHandle hArrElementIndices = hElement.child( aElementIndices );
			
			sgBuildMeshData buildMeshData;
			for( int j=0; j< hArrElementIndices.elementCount(); j++, hArrElementIndices.next() )
			{
				int indexElement = hArrElementIndices.inputValue().asInt()-1;
				if( indexElement < 0) continue;
				if( sepLength <= indexElement ) continue;
				buildMeshData.appendMeshData( m_meshDataArray[ indexElement ] );
				buildMeshData.m_appendedIndices.append( indexElement );
			}
			m_meshDataArray_output.append( buildMeshData );
		}
	}

	m_elementNum = m_meshDataArray_output.length();

	setThread();
	if( m_require_update )
	{
		//m_pTask->m_pMeshDataArray_output = &m_meshDataArray_output;
		//MThreadPool::newParallelRegion( parallelCompute_build, (void*)m_pThread );
		for( int i=0; i< m_elementNum; i++ )
			m_meshDataArray_output[i].build();
	}
	else
	{
		vector<MPointArray> pointArraysInput;
		MMatrixArray mtxArrInput;
		pointArraysInput.resize( m_oArrMeshs.length() );
		mtxArrInput.setLength( m_oArrMeshs.length() );
		for( int i=0; i< m_oArrMeshs.length(); i++ )
		{
			MFnMesh fnMesh( m_oArrMeshs[i] );
			fnMesh.getPoints( pointArraysInput[i] );
			mtxArrInput[i] = fnMesh.dagPath().inclusiveMatrix();
		}

		//m_pTask->m_pMeshDataArray_input = &m_meshDataArray;
		//m_pTask->m_pPointArraysInput    = &pointArraysInput;
		//m_pTask->m_pMtxArrInput         = &mtxArrInput;
		//MThreadPool::newParallelRegion( parallelCompute_setPosition, (void*)m_pThread );
		
		for( int i=0; i< m_elementNum; i++ )
		{
			int numVertices_output = 0;
			MIntArray& appendedIndices = m_meshDataArray_output[i].m_appendedIndices;

			for( int j=0; j< appendedIndices.length(); j++ )
			{
				int appendedIndex = m_meshDataArray_output[i].m_appendedIndices[j];
				sgBuildMeshData& targetMeshData = m_meshDataArray[ appendedIndex ];

				int numVertices = targetMeshData.m_numVertices;
				numVertices_output += numVertices;
			}
			MFnMesh fnMesh;
			int currentIndex = 0;
			MIntArray& originalIndices = m_meshDataArray_output[i].m_appendedIndices;
			MPointArray& pointArray_output = m_meshDataArray_output[i].m_points;

			for( int j=0; j< originalIndices.length(); j++ )
			{
				int appendedIndex = originalIndices[j];
				int inputMeshIndex = m_meshDataArray[ appendedIndex ].m_inputMeshIndex;
				MMatrix& mtxInputMesh = mtxArrInput[ inputMeshIndex ];

				fnMesh.setObject( m_meshDataArray[ appendedIndex ].m_oMesh );
				MMatrix mtxMesh = fnMesh.dagPath().inclusiveMatrix();

				MPointArray& basePoints = pointArraysInput[ inputMeshIndex ];
				MIntArray&   verticeIndices = m_meshDataArray[ appendedIndex ].m_originalVerticesIndices;
				for( int k=0; k< verticeIndices.length(); k++ )
				{
					pointArray_output[ currentIndex ] = basePoints[ verticeIndices[k] ] * mtxInputMesh;
					currentIndex++;
				}
			}
			MFnMesh fnMesh_output( m_meshDataArray_output[i].m_oMesh );
			fnMesh_output.setPoints( pointArray_output );
		}
	}
	//endThread();

	MArrayDataHandle hArrOutputMesh = data.outputArrayValue( aOutputMeshs );
	MArrayDataBuilder builder( aOutputMeshs, m_elementNum );
	for( int i=0; i< m_elementNum; i++ )
	{
		MDataHandle hOutputMesh = builder.addElement( i );
		hOutputMesh.set( m_meshDataArray_output[i].m_oMesh );
	}
	hArrOutputMesh.set( builder );
	hArrOutputMesh.setAllClean();

	m_isDirty_inputMesh = false;
	m_isDirty_element = false;
	m_require_update = false;

	return MS::kSuccess;
}



MStatus sgSeparate::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnTypedAttribute   tAttr;
	MFnCompoundAttribute cAttr;

	aInputMeshs = tAttr.create( "inputMeshs", "inputMeshs", MFnData::kMesh );
	tAttr.setStorable( true );
	tAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMeshs ) );

	aElements  = cAttr.create( "elements", "elements" );
	aElementIndices   = nAttr.create( "elementIndices", "elementIndices", MFnNumericData::kInt, 0 );
	nAttr.setArray( true );

	cAttr.addChild( aElementIndices );
	cAttr.setStorable( true );
	cAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aElements ) );

	aOutputMeshs = tAttr.create( "outputMeshs", "outputMeshs", MFnData::kMesh );
	tAttr.setStorable( false );
	tAttr.setArray( true );
	tAttr.setUsesArrayDataBuilder( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputMeshs ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMeshs, aOutputMeshs ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aElements, aOutputMeshs ) );

	return MS::kSuccess;
}



MStatus sgSeparate::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aInputMeshs )
	{
		m_isDirty_inputMesh = true;
	}

	if( plug == aElementIndices )
	{
		m_isDirty_element = true;
	}

	return MS::kSuccess;
}