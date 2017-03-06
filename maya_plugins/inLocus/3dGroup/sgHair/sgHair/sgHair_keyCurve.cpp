#include "sgHair_keyCurve.h"


MTypeId sgHair_keyCurve::id( 0x2015060300 );

MObject sgHair_keyCurve::aBaseLocalMatrix;
MObject sgHair_keyCurve::aTime;
MObject sgHair_keyCurve::aKeys;
	MObject sgHair_keyCurve::aKeyframe;
	MObject sgHair_keyCurve::aBaseMatrix;
	MObject sgHair_keyCurve::aInputCurve;


sgHair_keyCurve::sgHair_keyCurve()
{
	m_isDirtyKeys = true;
	m_isDirtyInputGeom = true;
}

sgHair_keyCurve::~sgHair_keyCurve()
{
}


void* sgHair_keyCurve::creator()
{
	return new sgHair_keyCurve();
}



MStatus sgHair_keyCurve::deform( MDataBlock& data, MItGeometry& itGeo,
	                             const MMatrix& mtxGeo, unsigned int multIndex )
{
	MStatus status;

	MFnDependencyNode fnThisNode( thisMObject() );
	MPlug env = fnThisNode.findPlug( envelope );
	float envValue = env.asFloat();
	if( !envValue ) return MS::kSuccess;

	itGeo.allPositions( m_inputPoints );
	m_outputPoints = m_inputPoints;

	if( m_isDirtyKeys )
	{
		MArrayDataHandle hArrKeys = data.inputArrayValue( aKeys );

		unsigned int lengthKeys = hArrKeys.elementCount();
		m_keys.setLength( lengthKeys );
		
		m_timesSorted.clear();
		m_indicesSorted.clear();
		for( int i=0; i< lengthKeys; i++, hArrKeys.next() )
		{
			MDataHandle      hKeys     = hArrKeys.inputValue();
			MDataHandle      hKeyframe = hKeys.child( aKeyframe );
			MDataHandle      hBaseMatrix = hKeys.child( aBaseMatrix );
			MDataHandle      hInputCurve = hKeys.child( aInputCurve );

			MTime& m_keyTime = m_keys.getTime( i );
			m_keyTime = hKeys.asTime();
			MMatrix& m_mtxBase = m_keys.getMatrix( i );
			m_mtxBase = hBaseMatrix.asMatrix();
			MFnNurbsCurve fnInputCurve( hInputCurve.asNurbsCurve() );

			bool inserted = false;
			for( int j=0; j< m_timesSorted.length(); j++ )
			{
				if( m_keyTime < m_timesSorted[j] )
				{
					m_timesSorted.insert( m_keyTime, j );
					m_indicesSorted.insert( i, j );
					inserted = true;
					break;
				}
			}
			if( !inserted )
			{
				//cout << "appended : " << m_keyTime.value() << endl;
				m_timesSorted.append( m_keyTime );
				m_indicesSorted.append( i );
			}
			
			MPointArray& m_keyVectors = m_keys.getPoints( i );

			MPointArray pointsCurve;
			fnInputCurve.getCVs( pointsCurve );

			m_keyTime.setValue( hKeyframe.asDouble() );
			m_keyVectors.setLength( fnInputCurve.numCVs() );

			for( int j=0; j< fnInputCurve.numCVs(); j++ )
			{
				MPoint point = pointsCurve[j];
				m_keyVectors.set( point, j );
			}
		}
	}
	MDataHandle hBaseMatrix = data.inputValue( aBaseLocalMatrix );
	MMatrix mtxBase = hBaseMatrix.asMatrix();

	MDataHandle hTime = data.inputValue( aTime );
	MTime time = hTime.asTime();

	getOutputPoints( m_inputPoints, m_outputPoints, mtxBase, time, m_keys,
		 m_timesSorted, m_indicesSorted, envValue );

	itGeo.setAllPositions( m_outputPoints );

	m_isDirtyKeys = false;
	m_isDirtyInputGeom = false;

	return MS::kSuccess;
}



MStatus sgHair_keyCurve::initialize()
{
	MStatus status;

	MFnNumericAttribute  nAttr;
	MFnUnitAttribute     uAttr;
	MFnMatrixAttribute   mAttr;
	MFnEnumAttribute     eAttr;
	MFnCompoundAttribute cAttr;
	MFnTypedAttribute    tAttr;

	aBaseLocalMatrix = mAttr.create( "baseLocalMatrix", "baseLocalMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBaseLocalMatrix ) );

	aTime      = uAttr.create( "time", "time", MFnUnitAttribute::kTime );
	uAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aTime ) );

	aKeys      = cAttr.create( "keys", "keys" );
		aKeyframe   = uAttr.create( "keyframe", "keyframe", MFnUnitAttribute::kTime );
		aBaseMatrix = mAttr.create( "baseMatrix", "baseMatrix" );
		aInputCurve = tAttr.create( "inputCurve", "inputCurve", MFnData::kNurbsCurve );
		nAttr.setArray( true );

	cAttr.addChild( aKeyframe );
	cAttr.addChild( aBaseMatrix );
	cAttr.addChild( aInputCurve );
	cAttr.setStorable( true );
	cAttr.setArray( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aKeys ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aTime,       outputGeom ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aKeys,       outputGeom ) );

	return MS::kSuccess;
}


MStatus sgHair_keyCurve::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aKeyframe || plug == aInputCurve )
	{
		m_isDirtyKeys = true;
	}
	if( plug == inputGeom )
	{
		m_isDirtyInputGeom = true;
	}
	if( plug == aBaseMatrix )
	{
		m_isDirtyKeys = true;
	}
	return MS::kSuccess;
}