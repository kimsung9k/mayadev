#include "sgCurveFromPoints.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>

#include <maya/MGlobal.h>

#define  CREATEBYCV  0
#define  CREATEBYEP  1


MTypeId     sgCurveFromPoints::id( 0x2015052200 );

MObject     sgCurveFromPoints::aCreateType;        
MObject     sgCurveFromPoints::aDegrees;     
MObject     sgCurveFromPoints::aInput;
	MObject     sgCurveFromPoints::aInputMatrix;
	MObject     sgCurveFromPoints::aInputPoint;
		MObject     sgCurveFromPoints::aInputPointX;
		MObject     sgCurveFromPoints::aInputPointY;
		MObject     sgCurveFromPoints::aInputPointZ;
MObject     sgCurveFromPoints::aOutputCurve; 


sgCurveFromPoints::sgCurveFromPoints()
{
	m_isDirtyCreate = true;
	m_isDirtyDegrees = true;
	m_isDirtyNumPoints = true;

	m_createType = 0;
	m_degree    = 3;
}


sgCurveFromPoints::~sgCurveFromPoints()
{
}


MStatus sgCurveFromPoints::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;
	
	MFnDependencyNode fnNode( thisMObject() );
	MPlug plugInput = fnNode.findPlug( aInput );
	int numElement = plugInput.numElements();
	if( m_numPoints != numElement )
	{
		m_isDirtyNumPoints = true;
		m_numPoints = numElement;
	}

	if( m_numPoints < 2 ) return MS::kFailure;

	MArrayDataHandle hArrInput = data.inputArrayValue( aInput );

	m_pointsWorld.setLength( m_numPoints );
	for( unsigned int i=0; i< hArrInput.elementCount(); i++, hArrInput.next() )
	{
		MDataHandle hInput = hArrInput.inputValue();
		MMatrix mtxInput   = hInput.child( aInputMatrix ).asMatrix();
		MPoint  pointInput = hInput.child( aInputPoint ).asVector();
		
		MPoint  pointWorld = pointInput * mtxInput;
		m_pointsWorld.set( pointWorld, i );
	}

	if( m_isDirtyDegrees )
	{
		int enumIndexDegree = data.inputValue( aDegrees ).asUChar();

		switch( enumIndexDegree )
		{
		case 0:
			m_degree = 1; break;
		case 1:
			m_degree = 2; break;
		case 2:
			m_degree = 3; break;
		case 3:
			m_degree = 5; break;
		case 4:
			m_degree = 7; break;
		}

		MFnNurbsCurveData dataCurve;
		m_oCurve = dataCurve.create();
	}

	if( m_isDirtyCreate )
	{
		m_createType = data.inputValue( aCreateType ).asUChar();
	}

	if( m_isDirtyCreate || m_isDirtyDegrees || m_isDirtyNumPoints )
	{
		if( m_createType == CREATEBYCV )
		{
			int modifiedDegree = m_degree;
			if( m_numPoints <= m_degree )
				modifiedDegree = 1;

			//cout << "numPoints : " << m_numPoints << endl;
			//cout << "modifiedDegree : " << modifiedDegree << endl;

			MDoubleArray dArrKnots;
			dArrKnots.setLength( m_numPoints + modifiedDegree - 1 );
			for( int i=0; i< modifiedDegree; i++ )
			{
				//cout << "index : " << i << ", " << 0 << endl;
				dArrKnots[i] = 0;
			}
			for( int i=modifiedDegree; i< m_numPoints-1; i++ )
			{
				//cout << "index : " << i << ",, " << i-(modifiedDegree-1) << endl;
				dArrKnots[i] = i-(modifiedDegree-1);
			}
			for( int i=m_numPoints-1; i< m_numPoints+modifiedDegree-1; i++ )
			{
				//cout << "index : " << i << ",,, " << dArrKnots[m_numPoints-2]+1 << endl;
				dArrKnots[i] = dArrKnots[m_numPoints-2]+1;
			}

			m_fnCreateCurve.create( m_pointsWorld, dArrKnots, modifiedDegree, MFnNurbsCurve::kOpen, false, true, m_oCurve );
			m_fnCreateCurve.setObject( m_oCurve );

			MDataHandle hOutputCurve = data.outputValue( aOutputCurve );
			hOutputCurve.setMObject( m_oCurve );
		}
	}

	if( m_createType == CREATEBYEP )
	{
		m_fnCreateCurve.createWithEditPoints( m_pointsWorld, m_degree, MFnNurbsCurve::kOpen, false, false, true, m_oCurve );
		MDataHandle hOutputCurve = data.outputValue( aOutputCurve );
		hOutputCurve.setMObject( m_oCurve );
	}
	else
	{
		m_fnCreateCurve.setCVs( m_pointsWorld );
	}

	data.setClean( plug );

	m_isDirtyCreate = false;
	m_isDirtyDegrees = false;
	m_isDirtyNumPoints = false;

	return MS::kSuccess;
}


void* sgCurveFromPoints::creator()
{
	return new sgCurveFromPoints();
}


MStatus sgCurveFromPoints::initialize()	
{
	MStatus status;

	MFnTypedAttribute   tAttr;
	MFnMatrixAttribute  mAttr;
	MFnNumericAttribute nAttr;
	MFnCompoundAttribute cAttr;
	MFnEnumAttribute eAttr;

	aCreateType = eAttr.create( "createType", "createType" );
	eAttr.addField( "CV Points", 0 );
	eAttr.addField( "EP Points", 1 );
	eAttr.setKeyable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aCreateType ) );

	aDegrees = eAttr.create( "degrees", "degrees" );
	eAttr.setKeyable( true );
	eAttr.addField( "1", 0 );
	eAttr.addField( "2", 1 );
	eAttr.addField( "3", 2 );
	eAttr.addField( "5", 3 );
	eAttr.addField( "7", 4 );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aDegrees ) );

	aInput = cAttr.create( "input", "input" );

	aInputMatrix = mAttr.create( "inputMatrix", "inputMatrix" );
	aInputPointX = nAttr.create( "inputPointX", "inputPointX", MFnNumericData::kDouble, 0.0 );
	aInputPointY = nAttr.create( "inputPointY", "inputPointY", MFnNumericData::kDouble, 0.0 );
	aInputPointZ = nAttr.create( "inputPointZ", "inputPointZ", MFnNumericData::kDouble, 0.0 );
	aInputPoint  = nAttr.create( "inputPoint", "inputPoint", aInputPointX, aInputPointY, aInputPointZ );

	cAttr.addChild( aInputMatrix );
	cAttr.addChild( aInputPoint );
	cAttr.setArray( true );
	cAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInput ) );

	aOutputCurve = tAttr.create( "outputCurve", "outputCurve", MFnData::kNurbsCurve );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputCurve ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aCreateType, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aDegrees, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInput, aOutputCurve ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInput, aOutputCurve ) );

	return MS::kSuccess;
}


MStatus  sgCurveFromPoints::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	if( plug == aCreateType )
	{
		m_isDirtyCreate = true;
	}
	else if( plug == aDegrees )
	{
		m_isDirtyDegrees = true;
	}
	else if( plug == aInputPoint || plug == aInputMatrix )
	{
		MFnDependencyNode fnNode( thisMObject() );
		MPlug plugInput = fnNode.findPlug( aInput );
		int numElement = plugInput.numElements();
		if( m_numPoints != numElement )
		{
			m_isDirtyNumPoints = true;
			m_numPoints = numElement;
		}
	}

	return MS::kSuccess;
}