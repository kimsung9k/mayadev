#include  "sgHair_cutInfo.h"

MTypeId  sgHair_cutInfo::id( 0x20150205 );

MObject  sgHair_cutInfo::aInputMeshMatrix;
MObject  sgHair_cutInfo::aInputMesh;
MObject  sgHair_cutInfo::aInputCurveMatrix;
MObject  sgHair_cutInfo::aInputCurve;

MObject  sgHair_cutInfo::aOutput;
	MObject  sgHair_cutInfo::aOutU;
	MObject  sgHair_cutInfo::aOutV;
	MObject  sgHair_cutInfo::aOutParam;
	MObject  sgHair_cutInfo::aOutPoint;
		MObject  sgHair_cutInfo::aOutPointX;
		MObject  sgHair_cutInfo::aOutPointY;
		MObject  sgHair_cutInfo::aOutPointZ;


void* sgHair_cutInfo::creator()
{
	return new sgHair_cutInfo();
}


sgHair_cutInfo::sgHair_cutInfo()
{
}

sgHair_cutInfo::~sgHair_cutInfo()
{

}


MStatus sgHair_cutInfo::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	m_mtxInputMesh  = data.inputValue( aInputMeshMatrix ).asMatrix();
	m_mtxInputCurve = data.inputValue( aInputCurveMatrix ).asMatrix();
	m_oMeshBase     = data.inputValue( aInputMesh ).asMesh();
	m_oCurveBase    = data.inputValue( aInputCurve ).asNurbsCurve();

	getOutput();

	MDataHandle hOutU = data.outputValue( aOutU );
	MDataHandle hOutV = data.outputValue( aOutV );
	MDataHandle hOutParam = data.outputValue( aOutParam );
	MDataHandle hOutPoint = data.outputValue( aOutPoint );

	hOutU.set( m_outU );
	hOutV.set( m_outV );
	hOutParam.set( m_outParam );
	hOutPoint.setMVector( m_pointClose );

	data.setClean( plug );

	return MS::kSuccess;
}



MStatus sgHair_cutInfo::initialize()
{
	MStatus status;

	MFnTypedAttribute  tAttr;
	MFnNumericAttribute nAttr;
	MFnMatrixAttribute  mAttr;
	MFnCompoundAttribute cAttr;

	aInputMeshMatrix = mAttr.create( "inputMeshMatrix", "inputMeshMatrix", MFnMatrixAttribute::kDouble, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMeshMatrix ) );

	aInputMesh = tAttr.create( "inputMesh", "inputMesh", MFnData::kMesh, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	tAttr.setStorable( true );
	tAttr.setCached( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputMesh ) );


	aInputCurveMatrix = mAttr.create( "inputCurveMatrix", "inputCurveMatrix", MFnMatrixAttribute::kDouble, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	mAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputCurveMatrix ) );

	aInputCurve = tAttr.create( "inputCurve", "inputCurve", MFnData::kNurbsCurve, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	tAttr.setStorable( true );
	tAttr.setCached( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputCurve ) );

	aOutput = cAttr.create( "output", "output" );

	aOutU = nAttr.create( "outU", "u", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( false );
	aOutV = nAttr.create( "outV", "v", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( false );
	aOutParam = nAttr.create( "outParam", "outParam", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( false );

	aOutPointX = nAttr.create( "outPointX", "outPointX", MFnNumericData::kDouble, 0.0 );
	aOutPointY = nAttr.create( "outPointY", "outPointY", MFnNumericData::kDouble, 0.0 );
	aOutPointZ = nAttr.create( "outPointZ", "outPointZ", MFnNumericData::kDouble, 0.0 );
	aOutPoint  = nAttr.create( "outPoint", "outPoint", aOutPointX, aOutPointY, aOutPointZ );
	nAttr.setStorable( false );

	cAttr.addChild( aOutU );
	cAttr.addChild( aOutV );
	cAttr.addChild( aOutParam );
	cAttr.addChild( aOutPoint );

	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutput ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMesh, aOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputMeshMatrix, aOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurve, aOutput ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurveMatrix, aOutput ) );

	return MS::kSuccess;
}


MStatus  sgHair_cutInfo::setDependentsDirty( const MPlug& plug, MPlugArray& plugArr )
{
	MStatus status;

	return MS::kSuccess;
}