#include "sgDynPointInMesh.h"

MTypeId  sgDynPointInMesh::id( 2015102100 );

MObject  sgDynPointInMesh::aDynamicOn;

MObject  sgDynPointInMesh::aStartTime;
MObject  sgDynPointInMesh::aCurrentTime;

MObject  sgDynPointInMesh::aAttachPercent;
MObject  sgDynPointInMesh::aDecreasePercent;
MObject  sgDynPointInMesh::aBounceRate;
MObject  sgDynPointInMesh::aLockDistance;

MObject  sgDynPointInMesh::aTimeScale;
MObject  sgDynPointInMesh::aSpaceScale;

MObject  sgDynPointInMesh::aInputPoint;
	MObject  sgDynPointInMesh::aInputPointX;
	MObject  sgDynPointInMesh::aInputPointY;
	MObject  sgDynPointInMesh::aInputPointZ;
MObject  sgDynPointInMesh::aLocalMesh;
MObject  sgDynPointInMesh::aMeshMatrix;
MObject  sgDynPointInMesh::aOutputPoint;
	MObject  sgDynPointInMesh::aOutputPointX;
	MObject  sgDynPointInMesh::aOutputPointY;
	MObject  sgDynPointInMesh::aOutputPointZ;

MObject  sgDynPointInMesh::aFrames;
MObject  sgDynPointInMesh::aValues;


sgDynPointInMesh::sgDynPointInMesh()
{
	m_meshChanged = true;
	m_beforeVelocity = MVector( 0,0,0 );
	m_oTrs.clear();
	m_attrModified = false;
}

sgDynPointInMesh::~sgDynPointInMesh()
{
}


void* sgDynPointInMesh::creator()
{
	return new sgDynPointInMesh();
}


MStatus sgDynPointInMesh::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	bool dynamicOn = data.inputValue( aDynamicOn ).asBool();

	MTime timeStart   = data.inputValue( aStartTime ).asTime();
	MTime timeCurrent = data.inputValue( aCurrentTime ).asTime();

	MPoint  inputPoint = data.inputValue( aInputPoint ).asVector();
	MMatrix meshMatrix = data.inputValue( aMeshMatrix ).asMatrix();

	if( timeStart == timeCurrent || !dynamicOn || m_beforeTime == timeCurrent )
	{
		MDataHandle hOutputPoint = data.outputValue( aOutputPoint );
		hOutputPoint.setMVector( inputPoint );
		m_beforePoint  = inputPoint;
		m_beforeMatrix = meshMatrix;
		m_beforeVelocity*=0;
		m_beforeTime = timeStart;
		return MS::kSuccess;
	}
	
	if( timeCurrent < m_beforeTime )
	{
		return MS::kSuccess;
	}
	
	if( m_meshChanged )
	{
		m_oMesh = data.inputValue( aLocalMesh ).asMesh();
		m_fnMesh.setObject( m_oMesh );
	}

	float  attachRate     = pow( (double)( data.inputValue( aAttachPercent ).asFloat() )/100.0f, 0.5 );
	float  decreaseRate   = data.inputValue( aDecreasePercent ).asFloat()/100.0f;
	float  bounceRate     = data.inputValue( aBounceRate ).asFloat()/100.0f;
	double lockDist       = data.inputValue( aLockDistance ).asDouble();

	double timeScale      = data.inputValue( aTimeScale ).asDouble();
	double spaceScale     = data.inputValue( aSpaceScale ).asDouble();

	if( decreaseRate > 1.0f ) decreaseRate = 1;
	decreaseRate *= 0.9f;

	MVector vIncrease = ( inputPoint - m_beforePoint ) * attachRate/timeScale;
	MVector vDecrease = m_beforeVelocity * ( 1.0 - (decreaseRate + 0.1)/timeScale );

	if( vDecrease.length() < lockDist )
		vDecrease *= 0;

	if( ( m_beforeVelocity * vDecrease ) == -1 )
		vDecrease *= 0;

	MVector vVelocity = vIncrease + vDecrease;
	MPoint  pointCurrent = m_beforePoint + vVelocity;

	if( m_fnMesh.numVertices() )
	{
		MMeshIntersector intersector;
		intersector.create( m_oMesh );

		MMatrix localToWorldMatrix = meshMatrix;
		MMatrix worldToLocalMatrix = meshMatrix.inverse();
		
		for( int i=0; i< 2; i++ )
		{
			MPoint  localPoint = pointCurrent * worldToLocalMatrix;
		
			MPointOnMesh pointOnMesh;
			intersector.getClosestPoint( localPoint, pointOnMesh );

			MPoint pointHit = pointOnMesh.getPoint();
			MVector normalHit = pointOnMesh.getNormal().normal();
			MVector currentDir = localPoint - pointHit;

			m_fnNode.setObject( thisMObject() );
			MPlug plugMatrix = m_fnNode.findPlug( aMeshMatrix );

			MPlugArray connections;
			plugMatrix.connectedTo( connections, true, false );

			if( currentDir * normalHit > 0 )
			{
				MVector projV = (currentDir * normalHit) * normalHit;
				MVector verticalV = currentDir - projV;
			
				MVector velNormal = -bounceRate * projV;
				MVector velVertical = verticalV * 0.5;

				vVelocity = (velNormal + velVertical)*localToWorldMatrix;

				if( i == 2 )
				{
					pointCurrent = pointHit * localToWorldMatrix;
				}
				else
				{
					pointCurrent = pointHit * localToWorldMatrix + vVelocity;
				}
			}
			else
			{
				break;
			}
		}
	}
	MDataHandle hOutputPoint = data.outputValue( aOutputPoint );
	hOutputPoint.setMVector( pointCurrent );

	m_beforePoint    = pointCurrent;
	m_beforeMatrix   = meshMatrix;
	m_beforeVelocity = vVelocity;
	m_beforeTime     = timeCurrent;

	return MS::kSuccess;
}



MStatus sgDynPointInMesh::initialize()
{
	MStatus status;

	MFnTypedAttribute tAttr;
	MFnUnitAttribute  uAttr;
	MFnMatrixAttribute mAttr;
	MFnNumericAttribute nAttr;

	aDynamicOn = nAttr.create( "dynamicOn", "on", MFnNumericData::kBoolean );
	nAttr.setChannelBox( true );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aDynamicOn ) );

	aStartTime = uAttr.create( "startTime", "startTime", MFnUnitAttribute::kTime, 1 );
	uAttr.setChannelBox( true );
	uAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aStartTime ) );
	aCurrentTime = uAttr.create( "currentTime", "currentTime", MFnUnitAttribute::kTime );
	uAttr.setKeyable( true );
	uAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aCurrentTime ) );


	aAttachPercent = nAttr.create( "attachPercent", "ap", MFnNumericData::kFloat, 25 );
	nAttr.setMin( 1 );
	nAttr.setMax( 99 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aAttachPercent ) );
	aDecreasePercent = nAttr.create( "decreasePercent", "dp", MFnNumericData::kFloat, 25 );
	nAttr.setMin( 0.0 );
	nAttr.setMax( 100 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aDecreasePercent ) );
	aBounceRate = nAttr.create( "bounce", "bounce", MFnNumericData::kFloat, 10 );
	nAttr.setMin( 0 );
	nAttr.setMax( 99 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aBounceRate ) );
	aLockDistance = nAttr.create( "lockDistance", "lockDistance", MFnNumericData::kDouble, 0.001 );
	nAttr.setMin( 0.00001 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aLockDistance ) );


	aTimeScale  = nAttr.create( "timeScale", "timeScale", MFnNumericData::kDouble, 1.0 );
	nAttr.setMin( 0.01 );
	nAttr.setMax( 100 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aTimeScale ) );
	aSpaceScale = nAttr.create( "spaceScale", "spaceScale", MFnNumericData::kDouble, 1.0 );
	nAttr.setMin( 0.01 );
	nAttr.setMax( 100 );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aSpaceScale ) );


	aInputPointX = nAttr.create( "inputPointX", "ipx", MFnNumericData::kDouble, 0.0 );
	aInputPointY = nAttr.create( "inputPointY", "ipy", MFnNumericData::kDouble, 0.0 );
	aInputPointZ = nAttr.create( "inputPointZ", "ipz", MFnNumericData::kDouble, 0.0 );
	aInputPoint = nAttr.create( "inputPoint", "ip", aInputPointX, aInputPointY, aInputPointZ );
	nAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputPoint ) );

	aLocalMesh = tAttr.create( "localMesh", "lm", MFnData::kMesh );
	tAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aLocalMesh ) );

	aMeshMatrix = mAttr.create( "meshMatrix", "mm" );
	mAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aMeshMatrix ) );

	aOutputPointX = nAttr.create( "outputPointX", "opx", MFnNumericData::kDouble );
	aOutputPointY = nAttr.create( "outputPointY", "opy", MFnNumericData::kDouble );
	aOutputPointZ = nAttr.create( "outputPointZ", "opz", MFnNumericData::kDouble );
	aOutputPoint = nAttr.create( "outputPoint", "op", aOutputPointX, aOutputPointY, aOutputPointZ );
	nAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputPoint ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aStartTime, aOutputPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aCurrentTime, aOutputPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aAttachPercent, aOutputPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aDecreasePercent, aOutputPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aBounceRate, aOutputPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aLockDistance, aOutputPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aTimeScale, aOutputPoint ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputPoint, aOutputPoint ) );

	aFrames = uAttr.create( "frames", "frames", MFnUnitAttribute::kTime );
	uAttr.setArray( true );
	uAttr.setHidden( true );
	uAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aFrames ) );

	aValues = nAttr.create( "values", "values", MFnNumericData::k3Double );
	nAttr.setArray( true );
	nAttr.setHidden( true );
	uAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aValues ) );

	return MS::kSuccess;
}


MStatus sgDynPointInMesh::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aLocalMesh )
	{
		m_meshChanged = true;
	}
	if( plug == aLocalMesh || plug == aAttachPercent || plug == aDecreasePercent ||
		plug == aBounceRate || plug == aLockDistance || plug == aTimeScale )
	{
		m_attrModified = true;
	}

	return MS::kSuccess;
}