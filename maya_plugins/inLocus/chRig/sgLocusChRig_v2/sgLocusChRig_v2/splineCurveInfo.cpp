#include "splineCurveInfo.h"

#include <maya/MPlug.h>
#include <maya/MMatrix.h>
#include <maya/MPoint.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MArrayDataBuilder.h>
#include <maya/MPxTransformationMatrix.h>

#include <maya/MFnNurbsCurve.h>

MTypeId splineCurveInfo::id( 0xc8c911 );

MObject  splineCurveInfo::aInputCurve;
MObject  splineCurveInfo::aTurnOnPercentage;
MObject  splineCurveInfo::aParamFromLength;

MObject  splineCurveInfo::aStartTransform;
MObject  splineCurveInfo::aEndTransform;

MObject  splineCurveInfo::aStartUpAxis;
MObject  splineCurveInfo::aEndUpAxis;

MObject  splineCurveInfo::aTargetAimAxis;
MObject  splineCurveInfo::aTargetUpAxis;

MObject  splineCurveInfo::aParameter;

MObject  splineCurveInfo::aOutput;
	MObject  splineCurveInfo::aDistance;
	MObject  splineCurveInfo::aBetweenDistance;

	MObject  splineCurveInfo::aRotateByTangent;

	MObject  splineCurveInfo::aPosition;
		MObject  splineCurveInfo::aPositionX;
		MObject  splineCurveInfo::aPositionY;
		MObject  splineCurveInfo::aPositionZ;
	MObject  splineCurveInfo::aRotate;
		MObject  splineCurveInfo::aRotateX;
		MObject  splineCurveInfo::aRotateY;
		MObject  splineCurveInfo::aRotateZ;

splineCurveInfo::splineCurveInfo() {};
splineCurveInfo::~splineCurveInfo() {};

MStatus splineCurveInfo::initialize()
{
	MStatus stat;

	MFnCompoundAttribute cAttr;
	MFnNumericAttribute nAttr;
	MFnTypedAttribute tAttr;
	MFnEnumAttribute eAttr;
	MFnUnitAttribute uAttr;
	MFnMatrixAttribute mAttr;

	aInputCurve = tAttr.create( "inputCurve", "ic", MFnData::kNurbsCurve );
	tAttr.setStorable( true );
	tAttr.setWritable( true );
	aTurnOnPercentage = nAttr.create( "turnOnPercentage", "top", MFnNumericData::kBoolean, true );
	nAttr.setStorable( true );
	nAttr.setWritable( true );
	aParamFromLength = nAttr.create( "paramFromLength", "pfl", MFnNumericData::kBoolean, true );
	nAttr.setStorable( true );
	nAttr.setWritable( true );

	aStartTransform = mAttr.create( "startTransform", "st" );
	mAttr.setStorable( true );
	mAttr.setWritable( true );
	aEndTransform = mAttr.create( "endTransform", "et" );
	mAttr.setStorable( true );
	mAttr.setWritable( true );

	aStartUpAxis = eAttr.create( "startUpAxis", "sua" );
		eAttr.addField(" X Axis", 0 );
		eAttr.addField(" Y Axis", 1 );
		eAttr.addField(" Z Axis", 2 );
		eAttr.addField("-X Axis", 3 );
		eAttr.addField("-Y Axis", 4 );
		eAttr.addField("-Z Axis", 5 );
		eAttr.setStorable(true);
	aEndUpAxis = eAttr.create( "endUpAxis", "eua" );
		eAttr.addField(" X Axis", 0 );
		eAttr.addField(" Y Axis", 1 );
		eAttr.addField(" Z Axis", 2 );
		eAttr.addField("-X Axis", 3 );
		eAttr.addField("-Y Axis", 4 );
		eAttr.addField("-Z Axis", 5 );
		eAttr.setStorable(true);

	aTargetAimAxis = eAttr.create( "targetAimAxis", "taa" );
		eAttr.addField(" X Axis", 0 );
		eAttr.addField(" Y Axis", 1 );
		eAttr.addField(" Z Axis", 2 );
		eAttr.addField("-X Axis", 3 );
		eAttr.addField("-Y Axis", 4 );
		eAttr.addField("-Z Axis", 5 );
		eAttr.setStorable(true);
	aTargetUpAxis = eAttr.create( "targetUpAxis", "tua" );
		eAttr.addField(" X Axis", 0 );
		eAttr.addField(" Y Axis", 1 );
		eAttr.addField(" Z Axis", 2 );
		eAttr.addField("-X Axis", 3 );
		eAttr.addField("-Y Axis", 4 );
		eAttr.addField("-Z Axis", 5 );
		eAttr.setStorable(true);

	aParameter = nAttr.create( "parameter", "pr", MFnNumericData::kDouble, 0.0 );
	nAttr.setArray( true );
	nAttr.setStorable( true );
	nAttr.setWritable( true );

	aDistance = nAttr.create( "distance", "dis", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( false );
	nAttr.setWritable( false );
	aBetweenDistance = nAttr.create( "betweenDistance", "bd", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( false );
	nAttr.setWritable( false );

	aRotateByTangent = nAttr.create( "rotateByTangent", "rbt", MFnNumericData::kBoolean, false );
	nAttr.setStorable( true );
	nAttr.setWritable( true );

	aPositionX = nAttr.create( "positionX", "px", MFnNumericData::kDouble, 0.0 );
	aPositionY = nAttr.create( "positionY", "py", MFnNumericData::kDouble, 0.0 );
	aPositionZ = nAttr.create( "positionZ", "pz", MFnNumericData::kDouble, 0.0 );
	aPosition = nAttr.create( "position", "p", aPositionX, aPositionY, aPositionZ );
	nAttr.setStorable( false );
	nAttr.setWritable( false );
	aRotateX = uAttr.create( "rotateX", "rx", MFnUnitAttribute::kAngle, 0.0 );
	aRotateY = uAttr.create( "rotateY", "ry", MFnUnitAttribute::kAngle, 0.0 );
	aRotateZ = uAttr.create( "rotateZ", "rz", MFnUnitAttribute::kAngle, 0.0 );
	aRotate = nAttr.create( "rotate", "r", aRotateX, aRotateY, aRotateZ );
	nAttr.setStorable( false );
	nAttr.setWritable( false );

	aOutput = cAttr.create( "output", "o" );
	cAttr.setArray( true );
	cAttr.setUsesArrayDataBuilder( true );
	cAttr.setStorable( false );
	cAttr.setWritable( false );
	cAttr.addChild( aDistance );
	cAttr.addChild( aBetweenDistance );
	cAttr.addChild( aRotateByTangent );
	cAttr.addChild( aPosition );
	cAttr.addChild( aRotate );

	stat = addAttribute( aInputCurve );
	if( !stat ){ stat.perror( "addAttribute : inputCurve" ); return stat; }
	stat = addAttribute( aStartTransform );
	if( !stat ){ stat.perror( "addAttribute : upAxis" ); return stat; }
	stat = addAttribute( aEndTransform );
	if( !stat ){ stat.perror( "addAttribute : upAxis" ); return stat; }
	stat = addAttribute( aStartUpAxis );
	if( !stat ){ stat.perror( "addAttribute : upAxis" ); return stat; }
	stat = addAttribute( aEndUpAxis );
	if( !stat ){ stat.perror( "addAttribute : endUpAxis" ); return stat; }
	stat = addAttribute( aTargetAimAxis );
	if( !stat ){ stat.perror( "addAttribute : aimAxis" ); return stat; }
	stat = addAttribute( aTargetUpAxis );
	if( !stat ){ stat.perror( "addAttribute : aimAxis" ); return stat; }
	stat = addAttribute( aTurnOnPercentage );
	if( !stat ){ stat.perror( "addAttribute : top" ); return stat; }
	stat = addAttribute( aParamFromLength );
	if( !stat ){ stat.perror( "addAttribute : pfl" ); return stat; }
	stat = addAttribute( aParameter );
	if( !stat ){ stat.perror( "addAttribute : top" ); return stat; }
	stat = addAttribute( aOutput );
	if( !stat ){ stat.perror( "addAttribute : pi" ); return stat; }

	stat = attributeAffects( aInputCurve, aOutput );
	if( !stat ){ stat.perror( "attributeAffects :inputCurve" ); return stat; }
	stat = attributeAffects( aParameter, aOutput );
	if( !stat ){ stat.perror( "attributeAffects :Param" ); return stat; }
	stat = attributeAffects( aTurnOnPercentage, aOutput );
	if( !stat ){ stat.perror( "attributeAffects :top" ); return stat; }
	stat = attributeAffects( aParamFromLength, aOutput );
	if( !stat ){ stat.perror( "attributeAffects :pfl" ); return stat; }
	stat = attributeAffects( aStartUpAxis, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : startUp" ); return stat; }
	stat = attributeAffects( aEndUpAxis, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : endUp" ); return stat; }
	stat = attributeAffects( aTargetAimAxis, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : targetAim" ); return stat; }
	stat = attributeAffects( aTargetUpAxis, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : targetUp" ); return stat; }
	stat = attributeAffects( aStartTransform, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : startTransform" ); return stat; }
	stat = attributeAffects( aEndTransform, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : endTransform" ); return stat; }
	stat = attributeAffects( aRotateByTangent, aRotate );
	if( !stat ){ stat.perror( "attributeAffects : endTransform" ); return stat; }

	return MS::kSuccess;
}
MVector getVectorByAxis( MMatrix mmtx, short axis )
{
	int axisNum = axis%3;

	MVector vector( mmtx( axisNum, 0 ), mmtx( axisNum, 1 ), mmtx( axisNum, 2 ) );

	if( axis >= 3 )
		vector *= -1;

	return vector;
}

MVector getRotateByAimUp( MVector aim, MVector up, short aimAxis, short upAxis )
{
	double matrix[4][4];

	int aimNum = aimAxis%3;
	int upNum = upAxis%3;
	int otherNum = 3 - aimNum - upNum;

	if( aimAxis >= 3 )
		aim *= -1;
	if( upAxis >= 3 )
		up *= -1;

	MVector cross = aim^up;
	up = cross^aim;


	matrix[aimNum][0] = aim.x; matrix[aimNum][1] = aim.y; matrix[aimNum][2] = aim.z;
	matrix[upNum][0] = up.x; matrix[upNum][1] = up.y; matrix[upNum][2] = up.z;
	matrix[otherNum][0] = cross.x; matrix[otherNum][1] = cross.y; matrix[otherNum][2] = cross.z;

	MMatrix mmtx( matrix );
	MPxTransformationMatrix mpxTrMtx( mmtx );

	return mpxTrMtx.eulerRotation().asVector();
}

MStatus splineCurveInfo::compute( const MPlug& plug, MDataBlock& block )
{
	MStatus stat;

	MDataHandle hInputCurve = block.inputValue( aInputCurve );
	MDataHandle hTurnOnPercent = block.inputValue( aTurnOnPercentage );
	MDataHandle hParamFromLength = block.inputValue( aParamFromLength );

	MArrayDataHandle hArrParameter = block.inputArrayValue( aParameter );

	MFnNurbsCurve curve = hInputCurve.asNurbsCurve();
	bool rotatePlugOn = plug == aRotate || plug == aRotateX || plug == aRotateY || plug == aRotateZ;

	MVector startUpVector;
	MVector endUpVector;
	short targetAimAxis;
	short targetUpAxis;

	if( rotatePlugOn )
	{
		MDataHandle hStartTransform = block.inputValue( aStartTransform );
		MDataHandle hEndTransform = block.inputValue( aEndTransform );
		MDataHandle hStartUpAxis = block.inputValue( aStartUpAxis );
		MDataHandle hEndUpAxis = block.inputValue( aEndUpAxis );
		MDataHandle hAimAxis = block.inputValue( aTargetAimAxis );
		MDataHandle hUpAxis = block.inputValue( aTargetUpAxis );

		startUpVector = getVectorByAxis( hStartTransform.asMatrix(), hStartUpAxis.asShort() );
		endUpVector = getVectorByAxis( hEndTransform.asMatrix(), hEndUpAxis.asShort() );

		targetAimAxis = hAimAxis.asShort();
		targetUpAxis = hUpAxis.asShort();
	}

	bool top = hTurnOnPercent.asBool();
	bool pfl = hParamFromLength.asBool();
	double maxValue = curve.knot( curve.numCVs() );
	double dist = curve.length();
	double multMaxDist;

	if( dist == 0 || multMaxDist == 0 )
		multMaxDist = 1;
	else
		multMaxDist = maxValue/dist;

	unsigned int elementCount = hArrParameter.elementCount();

	MArrayDataHandle  hArrOutput = block.outputArrayValue( aOutput );
	MArrayDataBuilder bArrOutput( aOutput, elementCount+1, &stat );

	MDataHandle* hRotateByTangentPtr = new MDataHandle[ elementCount ];
	MDataHandle* hDistancePtr =        new MDataHandle[ elementCount ];
	MDataHandle* hBetweenDistancePtr = new MDataHandle[ elementCount ];
	MDataHandle* hPositionPtr =        new MDataHandle[ elementCount ];
	MDataHandle* hRotatePtr =          new MDataHandle[ elementCount ];

	MPoint* pointPtr = new MPoint[ elementCount+1 ];
	MVector* offsetPtr = new MVector[ elementCount+1 ];
	double* paramPtr = new double[ elementCount ];

	MDataHandle hInput;
	for( int i=0; i< elementCount; i++ )
	{
		MDataHandle hParameter = hArrParameter.inputValue();

		paramPtr[i] = hParameter.asDouble();

		if( top )
			paramPtr[i] *= maxValue;
		if( pfl )
			paramPtr[i] = curve.findParamFromLength( paramPtr[i]/multMaxDist, &stat );

		stat = curve.getPointAtParam( paramPtr[i], pointPtr[i] );

		MDataHandle hOutput = bArrOutput.addElement( hArrParameter.elementIndex(), &stat );

		hRotateByTangentPtr[i] = hOutput.child( aRotateByTangent );
		hDistancePtr[i]        = hOutput.child( aDistance );
		hBetweenDistancePtr[i] = hOutput.child( aBetweenDistance );
		hPositionPtr[i]        = hOutput.child( aPosition );
		hRotatePtr[i]          = hOutput.child( aRotate );

		hArrParameter.next();
	}

	stat = curve.getPointAtParam( maxValue, pointPtr[elementCount] );
	
	MPoint currentPoint( 0,0,0 );
	for( int i=0; i< elementCount; i++ )
	{
		MVector rotate( 0,0,0 );
		if( rotatePlugOn )
		{
			float endWeight = paramPtr[i]/maxValue;
			float startWeight = 1-endWeight;

			MVector aimVector;
			if( hRotateByTangentPtr[i].asBool() )
				aimVector = curve.tangent( paramPtr[i] );
			else
				aimVector = pointPtr[i+1] - pointPtr[i];
			MVector upVector = startUpVector*startWeight + endUpVector*endWeight;

			rotate = getRotateByAimUp( aimVector, upVector, targetAimAxis, targetUpAxis );
		}
		double distance = paramPtr[i]/multMaxDist;
		double betweenDistance = currentPoint.distanceTo( pointPtr[i] );
		currentPoint = pointPtr[i];

		hDistancePtr[i].set( distance );
		hBetweenDistancePtr[i].set( betweenDistance );
		hPositionPtr[i].setMVector( pointPtr[i] );
		hRotatePtr[i].set( rotate );
	}

	hArrOutput.set( bArrOutput );
	hArrOutput.setAllClean();
	
	block.setClean( plug );

	delete []hRotateByTangentPtr;
	delete []hDistancePtr;
	delete []hBetweenDistancePtr;
	delete []hPositionPtr;
	delete []hRotatePtr;
	delete []pointPtr;
	delete []paramPtr;

	return MS::kSuccess;
}

void* splineCurveInfo::creator()
{
	return new splineCurveInfo();
}