#include "vectorWeight.h"

MObject vectorWeight::aInputVector;
MObject vectorWeight::aBaseVector;
MObject vectorWeight::aOutMinVector;
MObject vectorWeight::aOutputWeight;

MTypeId vectorWeight::id( 0x123457 );

vectorWeight::vectorWeight(){}
vectorWeight::~vectorWeight(){}


void* vectorWeight::creator()
{
	return new vectorWeight();
}


float getFloatDist( MFloatArray& fArr )
{
	float addValue = 0.0f;
	for( int i=0; i< fArr.length(); i++ )
	{
		addValue += pow( fArr[i], 2 );
	}
	return sqrt( addValue );
}


MFloatArray normalizeArray( MFloatArray& fArr, float& dist )
{
	MFloatArray fArrNormal = fArr;
	dist = getFloatDist( fArr );

	for( int i=0; i< fArrNormal.length(); i++ )
	{
		fArrNormal[i] /= dist;
	}
	return fArrNormal;
}


float dotProductFloat( MFloatArray& fArr0, MFloatArray& fArr1 )
{
	float dotValue = 0.0f;
	for( int i=0; i< fArr0.length(); i++ )
	{
		float value = fArr0[i] * fArr1[i];
		dotValue += value;
	}
	return dotValue;
}


MFloatArray getMinVector( MFloatArray& base, MFloatArray& target, bool& success )
{
	MFloatArray fArrResult;

	int arrayLength = base.length();
	fArrResult.setLength( arrayLength );

	MIntArray invIndices;
	invIndices.setLength( arrayLength );
	for( int i=0; i<arrayLength; i++ )
	{
		if( (target[i] < 0 && base[i] > 0) || (target[i] > 0 && base[i] < 0) )
		{
			success = false;
			return fArrResult;
		}
		else
		{
			if( target[i] < 0 )
			{
				target[i] *= -1;
				base[i] *= -1;
				invIndices[i] = 1;
			}
			else
			{
				invIndices[i] = 0;
			}
		}
	}

	float baseLarge   = 0.0f;
	float targetLarge = 0.0f;
	
	float baseSmall   = 10.0f;
	float targetSmall = 10.0f;

	for( int i=0; i< arrayLength; i++ )
	{
		if( base[i] > baseLarge )
			baseLarge   = base[i];
		if( base[i] < baseSmall )
			baseSmall   = base[i];
		if( target[i] > targetLarge )
			targetLarge = target[i];
		if( target[i] < targetSmall )
			targetSmall = target[i];
	}

	int targetSmallIndex = 0;
	int targetLargeIndex = 0;
	float largerDiv  = 0.0f; 
	float smallerDiv = 1000000.0f;
	for( int i=0; i< arrayLength; i++ )
	{
		float divValue = target[i]/base[i];
		if( divValue < smallerDiv )
		{
			smallerDiv = divValue;
			targetSmallIndex = i;
		}
		if( divValue > largerDiv )
		{
			largerDiv = divValue;
			targetLargeIndex = i;
		}
	}

	if( !targetLarge )
	{
		success = false;
		return fArrResult;
	}
	else
	{
		success = true;
	}

	float targetMultValue = base[ targetSmallIndex ] / target[ targetLargeIndex ];
	MFloatArray multTarget = target;

	for( int i=0; i< arrayLength; i++ )
	{
		multTarget[i] *= targetMultValue;
	}

	for( int i=0; i< arrayLength; i++ )
	{
		float divValue = ( base[ targetSmallIndex ] - multTarget[ targetSmallIndex ] );
		fArrResult[i] = multTarget[i] - ( ( base[i] - multTarget[i] ) * multTarget[ targetSmallIndex ] ) / divValue;
		if( fArrResult[i] < 0 )
			fArrResult[i] *= -1;
		if( invIndices[i] )
			fArrResult[i] *= -1;
	}
	fArrResult[targetSmallIndex] = 0.0f;

	return fArrResult; 
}


MStatus vectorWeight::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hInputVector = data.inputValue( aInputVector );
	MDataHandle hBaseVector  = data.inputValue( aBaseVector );

	MFloatVector vectorInput = hInputVector.asFloatVector();
	MFloatVector vectorBase  = hBaseVector.asFloatVector();

	MFloatArray fArrInput, fArrBase, fArrResult;
	fArrInput.setLength( 3 );
	fArrBase.setLength( 3 );
	fArrResult.setLength( 3 );

	fArrInput[0] = vectorInput.x;
	fArrInput[1] = vectorInput.y;
	fArrInput[2] = vectorInput.z;

	fArrBase[0]  = vectorBase.x;
	fArrBase[1]  = vectorBase.y;
	fArrBase[2]  = vectorBase.z;

	float fDistInput;
	float fDistBase;
	float fDistMinVector;
	bool success;
	MFloatArray fArrNInput = normalizeArray( fArrInput, fDistInput );
	MFloatArray fArrNBase  = normalizeArray( fArrBase , fDistBase );

	MFloatArray minVector  = normalizeArray( getMinVector( fArrNBase, fArrNInput, success ),fDistMinVector );
	
	float resultFloat;
	if( !success )
	{
		for( int i=0; i<minVector.length(); i++ )
			minVector[i] = 0.0f;
		resultFloat = 0.0f;
	}
	else
	{
		float maxAngle = acos( dotProductFloat( minVector, fArrNBase ) );
		float cuAngle  = acos( dotProductFloat( minVector, fArrNInput ) );

		resultFloat = fDistInput/fDistBase*cuAngle/maxAngle;
	}
	MDataHandle hOutMinVector = data.outputValue( aOutMinVector );
	hOutMinVector.set3Float( minVector[0], minVector[1], minVector[2] );
	MDataHandle hOutputWeight = data.outputValue( aOutputWeight );
	hOutputWeight.setFloat( resultFloat );

	data.setClean( plug );

	return MS::kSuccess;
}

MStatus vectorWeight::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnTypedAttribute tAttr;

	aOutMinVector = nAttr.create( "outMinVector", "outMinVector", MFnNumericData::k3Float );
	addAttribute( aOutMinVector );
	aOutputWeight = nAttr.create( "outputWeight", "outputWeight", MFnNumericData::kFloat );
	addAttribute( aOutputWeight );

	aInputVector = nAttr.create( "inputVector", "inputVector", MFnNumericData::k3Float );
	addAttribute( aInputVector );
	aBaseVector  = nAttr.create( "baseVector", "baseVector", MFnNumericData::k3Float );
	addAttribute( aBaseVector );

	attributeAffects( aInputVector, aOutMinVector );
	attributeAffects( aBaseVector,  aOutMinVector );
	attributeAffects( aInputVector, aOutputWeight );
	attributeAffects( aBaseVector,  aOutputWeight );

	return MS::kSuccess;
}