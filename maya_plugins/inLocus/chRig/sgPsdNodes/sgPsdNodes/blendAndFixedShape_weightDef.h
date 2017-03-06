#ifndef _blendAndFixedShape_weightDef_h
#define _blendAndFixedShape_weightDef_h

#include "vectorWeight.h"
#include "blendAndFixedShape.h"

/*
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
		float value = fArr0[0] * fArr1[0];
		//if( value < 0 ) return 0.0f;
		dotValue += value;
	}
	return dotValue;
}


MFloatArray getMinVector( MFloatArray& base, MFloatArray& target, bool& success )
{
	MFloatArray fArrResult;

	int arrayLength = base.length();

	float baseLarge   = 0.0f;
	float targetLarge = 0.0f;
	
	float baseSmall   = 1.0f;
	float targetSmall = 1.0f;

	int targetSmallIndex = 0;

	for( int i=0; i< arrayLength; i++ )
	{
		if( base[i] > baseLarge )
			baseLarge   = base[i];
		if( base[i] < baseSmall )
			baseSmall   = base[i];
		if( target[i] > targetLarge )
			targetLarge = target[i];
		if( target[i] < targetSmall )
		{
			targetSmall = target[i];
			targetSmallIndex = i;
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

	float targetMultValue = baseSmall / targetLarge;
	targetSmall *= targetMultValue;
	MFloatArray multTarget = target;

	for( int i=0; i< arrayLength; i++ )
	{
		multTarget[i] *= targetMultValue;
	}

	fArrResult.setLength( arrayLength );
	for( int i=0; i< arrayLength; i++ )
	{
		float divValue = ( base[ targetSmallIndex ] - targetSmall );
		fArrResult[i] = multTarget[i] - ( ( base[i] - multTarget[i] ) * targetSmall ) / divValue;
	}
	fArrResult[targetSmallIndex] = 0.0f;

	return fArrResult; 
}
*/


float  blendAndFixedShape::getWeightFromWeights( MFloatArray& weights, MFloatArray& targetWeights )
{
	int wLength = weights.length();
	
	float smallerWeight = 100.0f;

	bool minusIn = false;
	bool plusIn  = false;

	for( int i=0; i< wLength; i++ )
	{
		float currentWeight = weights[i] / targetWeights[i];
		float absWeight = fabs( currentWeight );

		if( currentWeight < 0 )
			minusIn = true;
		else
			plusIn  = true;

		if( smallerWeight > absWeight )
			smallerWeight = absWeight;
	}

	if( minusIn && plusIn )
		return 0.0f;

	if( smallerWeight == 100.0f )
		return 0.0f;
	
	if( minusIn )
	{
		return 0.0f;
	}
	
	//cout << "return weight : " << smallerWeight << endl;
	return smallerWeight;/**/

	/*
	if( wLength == 1 )
	{
		float result = weights[0] / targetWeights[0];
		if( result > 0 )
			return result;
		else
			return 0.0f;
	}

	bool weightExists;
	for( int i=0; i< weights.length(); i++ )
	{
		if( weights[i] != 0 )
			weightExists = true;
	}
	if( !weightExists )
		return 0.0f;

	float fDistInput;
	float fDistBase;
	float fDistMinVector;
	bool success;
	MFloatArray fArrNInput = normalizeArray( weights, fDistInput );
	MFloatArray fArrNBase  = normalizeArray( targetWeights , fDistBase );

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

	return resultFloat;
	/**/
}



MStatus   blendAndFixedShape::currentWeights_To_task( MArrayDataHandle& hArrDriverWeights )
{
	MStatus status;
	int driverWeightNum = hArrDriverWeights.elementCount();

	if( !driverWeightNum ) return  MS::kSuccess;

	MIntArray indices;
	MFloatArray values;
	indices.setLength( driverWeightNum );
	values.setLength( driverWeightNum );

	int maxIndex = 0;

	hArrDriverWeights.next();
	hArrDriverWeights.jumpToElement( 0 );
	for( int i=0; i<driverWeightNum; i++ )
	{
		hArrDriverWeights.jumpToElement(i);
		MDataHandle hDriverWeight = hArrDriverWeights.inputValue();
		indices[i] = hArrDriverWeights.elementIndex();
		values[i] = hDriverWeight.asFloat();

		if( maxIndex < indices[i] )
		{
			maxIndex = indices[i];
		}
		hArrDriverWeights.next();
	}

	driverWeights.setLength( maxIndex + 1 );

	for( int i=0; i< driverWeightNum; i++ )
	{
		driverWeights[ indices[i] ] = values[i];
	}
	return  MS::kSuccess;
}



MStatus   blendAndFixedShape::setBlendMeshWeightByAnimCurve()
{
	MStatus status;

	MFloatArray& blendMeshWeights = pTaskData->blendMeshWeights;
	MObjectArray& oArrAnimCurve  = pTaskData->oArrAnimCurve;

	for( int i=0; i< blendMeshWeights.length(); i++ )
	{
		MFnAnimCurve anim( oArrAnimCurve[i], &status );
		if( !status ) continue;
		
		double getWeight;
		anim.evaluate( blendMeshWeights[i], getWeight );
		blendMeshWeights[i] = getWeight;
	}

	return MS::kSuccess;
}



void   blendAndFixedShape::weightAttrs_To_task( MArrayDataHandle& hArrBlendMeshInfos )
{
	int blendMeshNum = hArrBlendMeshInfos.elementCount();

	targetIndicesArray.resize( blendMeshNum );
	targetWeightsArray.resize( blendMeshNum );

	int targetWeightNum;
	int overIndicesNum;

	MFnDependencyNode fnThisNode( thisMObject() );
	MPlug plugBlendMeshInfos = fnThisNode.findPlug( aBlendMeshInfos );
	MPlugArray cons;
	MObjectArray& oArrAnimCurve = pTaskData->oArrAnimCurve;
	
	oArrAnimCurve.clear();
	oArrAnimCurve.setLength( blendMeshNum );
	
	for( int i=0; i< blendMeshNum; i++ )
	{
		hArrBlendMeshInfos.jumpToElement( i );
		MDataHandle hBlendMeshInfo = hArrBlendMeshInfos.inputValue();
		MArrayDataHandle hArrTargetWeights = hBlendMeshInfo.child( aTargetWeights );
		MDataHandle hAnimCurveMsg = hBlendMeshInfo.child( aAnimCurve );

		MPlug plugBlendMeshInfoElement = plugBlendMeshInfos[i];
		MPlug animCurvePlug = plugBlendMeshInfoElement.child( aAnimCurve );
		animCurvePlug.connectedTo( cons, true, false );
		if( cons.length() )
		{
			oArrAnimCurve[i] = cons[0].node();
		}

		targetWeightNum = hArrTargetWeights.elementCount();

		targetIndicesArray[i].setLength( targetWeightNum );
		targetWeightsArray[i].setLength( targetWeightNum );

		hArrTargetWeights.jumpToArrayElement( 0 );
		for( int j=0; j< targetWeightNum; j++ )
		{
			MDataHandle hTargetWeight = hArrTargetWeights.inputValue();
			targetIndicesArray[i][j] = hArrTargetWeights.elementIndex();
			targetWeightsArray[i][j] = hTargetWeight.asFloat();
			hArrTargetWeights.next();
		}
		//cout << "targetIndicesArray[" << i << "] : " << targetIndicesArray[i] << endl;
	}
}



void blendAndFixedShape::getBlendMeshWeight()
{
	int blendMeshNum = targetIndicesArray.size();

	pTaskData->blendMeshWeights.setLength( blendMeshNum );
	pTaskData->largeOverValues.setLength( blendMeshNum );

	for( int i=0; i< blendMeshNum; i++ )
	{
		MIntArray& targetIndices = targetIndicesArray[i];
		MFloatArray& targetWeights = targetWeightsArray[i];

		MFloatArray eachDriverWeights;
		eachDriverWeights.setLength( targetIndices.length() );

		for( int j=0; j< targetIndices.length(); j++ )
		{
			if( driverWeights.length() <= targetIndices[j] )
			{
				driverWeights.setLength( targetIndices[j] +1 );
				driverWeights[ targetIndices[j] ] = 0.0f;
			}
			eachDriverWeights[j] = driverWeights[ targetIndices[j] ];
		}
		pTaskData->blendMeshWeights[i] = envValue * getWeightFromWeights( eachDriverWeights, targetWeights );
		pTaskData->largeOverValues[i] = 0.0f;
	}
}


bool isOverAble( MIntArray& first, MIntArray& second )
{
	int firstCount = first.length();
	int secondCount = second.length();

	if( firstCount > secondCount ) return false;

	for( int i=0; i< firstCount; i++ )
	{
		bool sameExists = false;
		for( int j=0; j< secondCount; j++ )
		{
			if( first[i] == second[j] )
				sameExists = true;
		}
		if( !sameExists )
			return false;
	}
	return true;
}


void blendAndFixedShape::separateSameChannelIndices()
{
	sameChannelIndicesArray.clear();

	for( int i=0; i< targetIndicesArray.size(); i++ )
	{
		int targetIndicesLength = targetIndicesArray[i].length();
		
		//cout << "check " << i << " Array : " << targetIndicesArray[i] << endl;

		for( int j=0; j< targetIndicesArray.size(); j++ )
		{
			if( i == j ) continue;
			
			if( isOverAble( targetIndicesArray[i], targetIndicesArray[j] ) &&
				isOverAble( targetIndicesArray[j], targetIndicesArray[i] ) )
			{
				bool arrayExists = false;
				for( int k=0; k < sameChannelIndicesArray.size(); k++ )
				{
					bool iExists = false;
					bool jExists = false;
					for( int m=0; m< sameChannelIndicesArray[k].length(); m++ )
					{
						if( i == sameChannelIndicesArray[k][m] )
							iExists = true;
						if( j == sameChannelIndicesArray[k][m] )
							jExists = true;
					}
					if( iExists && !jExists )
						sameChannelIndicesArray[k].append( j );
					if( !iExists && jExists )
						sameChannelIndicesArray[k].append( i );

					if( iExists || jExists )
					{
						arrayExists = true;
						break;
					}
				}

				if( arrayExists )
				{
					break;
				}
				{
					MIntArray newArray;
					newArray.setLength( 2 );
					newArray[0] = i;
					newArray[1] = j;

					sameChannelIndicesArray.push_back( newArray );
				}
			}
		}
	}
}


MFloatArray getWeightFromOneChannel( MFloatArray& weights, float weight )
{
	MFloatArray reOrderWeights;
	reOrderWeights.append( weights[0] );

	for( int i=1; i< weights.length(); i++ )
	{
		bool isInsulted = false;
		for( int j=0; j< reOrderWeights.length(); j++ )
		{
			if( reOrderWeights[j] == weights[i] )
			{
				isInsulted = true;
				break;
			}
			if( reOrderWeights[j] > weights[i] )
			{
				reOrderWeights.insert( weights[i], j );
				isInsulted = true;
				break;
			}
		}
	
		if( !isInsulted )
			reOrderWeights.append( weights[i] );
	}

	for( int i=0; i< reOrderWeights.length(); i++ )
	{
		if( reOrderWeights[i] > 0 )
		{
			reOrderWeights.insert( 0.0f, i );
			break;
		}
	}

	MFloatArray returnArray;
	returnArray.setLength( weights.length() );

	//cout << "reOrder Weights : " << reOrderWeights << endl;
	
	for( int i=0; i< weights.length(); i++ )
	{
		if( reOrderWeights[0] >= weight )
		{
			if( reOrderWeights[0] == 0 )
			{
				returnArray[i] = 0.0f;
			}
			else
			{
				if( weights[i] == reOrderWeights[0] )
					returnArray[i] = weight / reOrderWeights[0];
				else
					returnArray[i] = 0.0f;
			}
			continue;
		}

		bool setValued = false;
		for( int j=1; j<reOrderWeights.length(); j++ )
		{
			if( reOrderWeights[j] >= weight )
			{
				float minValue = reOrderWeights[j-1];
				float maxValue = reOrderWeights[j];

				if( maxValue == weights[i] )
					returnArray[i] = ( weight - minValue ) / ( maxValue - minValue );
				else if( minValue == weights[i] )
					returnArray[i] = 1 - ( weight - minValue ) / ( maxValue - minValue );
				else
					returnArray[i] = 0.0f;

				setValued = true;
				break;
			}
		}

		if( !setValued )
		{
			if( reOrderWeights[ reOrderWeights.length() -1 ] == weights[i] )
				returnArray[i] = weight / weights[i];
			else
				returnArray[i] = 0.0f;
		}
	}

	//cout << "reOrderWeights : " << reOrderWeights << endl;
	//cout << "weights : " << weights << " , " << weight << endl;
	//cout << "returns : " << returnArray << endl;
	//cout << endl;

	return returnArray;
}


void blendAndFixedShape::shareWeightBySameChannel()
{
	for( int i=0; i< sameChannelIndicesArray.size(); i++ )
	{
		//cout << "-------------" <<endl;
		MIntArray& currentChannelIndices = sameChannelIndicesArray[i];

		vector< MFloatArray > weightDimensions;

		int targetWeightIndex = currentChannelIndices[0];
		int weightArrayLength = targetWeightsArray[ targetWeightIndex ].length();

		if( weightArrayLength != 1 ) continue;
		weightDimensions.resize( weightArrayLength );
		/*
		for( int j=0; j< targetWeightsArray.size(); j++ )
		{
			cout << "targetWeights " << j << " : " << targetWeightsArray[j] << endl;
		}
		*/
		for( int j=0; j< weightArrayLength; j++ )
		{
			weightDimensions[j].setLength( currentChannelIndices.length() );

			for( int k=0; k<currentChannelIndices.length(); k++ )
			{
				targetWeightIndex = currentChannelIndices[k];
				float currentWeight = targetWeightsArray[ targetWeightIndex ][j];
				weightDimensions[j][k] = currentWeight;
			}
		}

		//cout << "-----------------" << endl;
		//cout << "currentChannelIndices : " << currentChannelIndices << endl;
		for( int j=0; j< weightDimensions.size(); j++ )
		{
			//cout << "cuChannel : " << currentChannelIndices[j] << endl;
			weightDimensions[j] = getWeightFromOneChannel( weightDimensions[j], driverWeights[targetIndicesArray[currentChannelIndices[j]][j]] );
		}
		//cout << "-----------------" << endl;

		vector< MFloatArray > eachChannelValuesArray;
		eachChannelValuesArray.resize( weightDimensions[0].length() );

		for( int j=0; j<eachChannelValuesArray.size(); j++ )
		{
			eachChannelValuesArray[j].setLength( weightDimensions.size() );

			for( int k=0; k < eachChannelValuesArray[j].length(); k++ )
				eachChannelValuesArray[j][k] = weightDimensions[k][j];
		}
		/*
		for( int j=0; j< weightDimensions.size(); j++ )
		{
			cout << "wDimention : " << j << " : " << weightDimensions[j] << endl;
		}
		for( int j=0; j< eachChannelValuesArray.size(); j++ )
		{
			cout << "eachValue  : " << currentChannelIndices[j] << " : " << eachChannelValuesArray[j] << endl;
		}
		*/
		for( int j=0; j < currentChannelIndices.length(); j++ )
		{
			int index = currentChannelIndices[j];
			float weight = eachChannelValuesArray[j][0];

			bool plusValue = false;
			bool minusValue = false;

			if( weight >= 0 )
				plusValue = true;
			else
				minusValue = true;

			for( int k=1; k<eachChannelValuesArray[j].length(); k++ )
			{
				if( eachChannelValuesArray[j][k] >= 0 )
					plusValue = true;
				else
					minusValue = true;

				if( plusValue && minusValue )
				{
					weight = 0.0f;
					break;
				}

				if( fabs( eachChannelValuesArray[j][k] ) < fabs( weight ) )
					weight = eachChannelValuesArray[j][k];
			}
			pTaskData->blendMeshWeights[ index ] = weight;
		}
		//cout << "-------------" <<endl;
	}
}


void blendAndFixedShape::setOverIndicesArray( MArrayDataHandle& hArrBlendMeshInfos )
{
	int blendMeshInfoCount = hArrBlendMeshInfos.elementCount();

	overIndicesArray.resize( blendMeshInfoCount );

	for( int i=0; i< blendMeshInfoCount; i++ )
	{
		int targetIndicesCount = targetIndicesArray[i].length();
		
		if( targetIndicesCount == 1 ) continue;

		overIndicesArray[i].clear();
		for( int j=0; j< blendMeshInfoCount; j++ )
		{
			if( j==i ) continue;
			
			if ( isOverAble( targetIndicesArray[j], targetIndicesArray[i] ) &&
				 !isOverAble( targetIndicesArray[i], targetIndicesArray[j] ) )
			{
				overIndicesArray[i].append( j );
			}
		}
	}
}


void blendAndFixedShape::setOverWeights()
{
	int blendMeshNum = targetIndicesArray.size();
	float minusValue;
	
	for( int i=0; i< blendMeshNum; i++ )
	{
		MIntArray& overIndices = overIndicesArray[i];
		minusValue = pow( pTaskData->blendMeshWeights[i], 2.0f );

		for( int j=0; j< overIndices.length(); j++ )
		{
			int targetIndex = overIndices[j];

			pTaskData->blendMeshWeights[targetIndex] -= minusValue;
			if( pTaskData->blendMeshWeights[targetIndex] < 0 )
				pTaskData->blendMeshWeights[targetIndex] =0;
		}
	}
}


void  blendAndFixedShape::setEnvWeights()
{
	for( int i=0; i< pTaskData->blendMeshWeights.length(); i++ )
		pTaskData->blendMeshWeights[i] *= envValue;
}


#endif