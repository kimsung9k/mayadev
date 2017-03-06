#include "sgMeshSnap.h"


MTypeId sgMeshSnap::id( 0x2015070700 );
MObject sgMeshSnap::aSnapMesh;
MObject sgMeshSnap::aIdsMap;


sgMeshSnap::sgMeshSnap()
{
	m_isDirtyIdsMap = true;
}

sgMeshSnap::~sgMeshSnap()
{
}



void* sgMeshSnap::creator()
{
	return new sgMeshSnap();
}


MStatus sgMeshSnap::deform( MDataBlock& data, MItGeometry& itGeo,
	                        const MMatrix& localToWorldMatrix, unsigned int mIndex )
{
	MStatus status;

	float env = data.inputValue( envelope ).asFloat();
	if( env == 0 ) return MS::kSuccess;

	MObject oMesh = data.inputValue( aSnapMesh ).asMesh();
	MFnMesh fnMesh( oMesh, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	fnMesh.getPoints( m_pointsSnap, MSpace::kWorld );

	if( m_isDirtyIdsMap )
	{
		MArrayDataHandle hArrIdsMap = data.inputArrayValue( aIdsMap );
		
		m_indicesSnapVerticesMap.setLength( itGeo.count() );
		for( unsigned int i=0; i< m_indicesSnapVerticesMap.length(); i++ )
		{
			m_indicesSnapVerticesMap[i]= -1;
		}
		for( unsigned int i=0; i< hArrIdsMap.elementCount(); i++, hArrIdsMap.next() )
		{
			m_indicesSnapVerticesMap[hArrIdsMap.elementIndex()] = hArrIdsMap.inputValue().asInt();
		}
	}
	MMatrix mtxWorldToLocal = localToWorldMatrix.inverse();

	MPoint pt;
	unsigned int snapIndex;
	itGeo.reset();
	for( unsigned int i=0; !itGeo.isDone(); itGeo.next(), i++ )
	{
		snapIndex = m_indicesSnapVerticesMap[i];
		if( snapIndex == -1 ) continue;
		pt = m_pointsSnap[ snapIndex ] * mtxWorldToLocal;
		itGeo.setPosition( pt );
	}

	m_isDirtyIdsMap = false;

	return MS::kSuccess;
}



MStatus sgMeshSnap::initialize()
{
	MStatus status;

	MFnTypedAttribute  tAttr;
	MFnNumericAttribute nAttr;

	aSnapMesh = tAttr.create( "snapMesh", "snapMesh", MFnData::kMesh );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aSnapMesh ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aSnapMesh, outputGeom ) );

	aIdsMap   = nAttr.create( "idsMap", "idsMap", MFnNumericData::kInt, -1 );
	nAttr.setArray( true );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aIdsMap ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aIdsMap, outputGeom ) );

	return MS::kSuccess;
}


MStatus sgMeshSnap::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aIdsMap )
	{
		m_isDirtyIdsMap = true;
	}

	return MS::kSuccess;
}