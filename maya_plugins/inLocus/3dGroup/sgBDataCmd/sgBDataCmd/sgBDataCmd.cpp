#include  "sgBDataCmd.h"


MStatus getShapeNode( MDagPath& path )
{
	MStatus status;

	if( path.apiType() == MFn::kMesh )
	{
		return MS::kSuccess;
	}

	if( path.apiType() != MFn::kTransform )
	{
		return MS::kFailure;
	}

	unsigned int numShapes;
	path.numberOfShapesDirectlyBelow( numShapes );

	if( !numShapes ) return MS::kFailure;

	for( unsigned int i=0; i< numShapes; i++ )
	{
		status = path.extendToShapeDirectlyBelow( i );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		if( path.apiType() == MFn::kMesh )
		{
			MFnDagNode fnNode = path.node();
			if( !fnNode.isIntermediateObject() )
			{
				return MS::kSuccess;
			}
		}
		path.pop();
	}
	return MS::kFailure;
}



void     writeUnsignedInt( const unsigned int& value, std::ofstream& outFile )
{
	outFile.write( (char*)&value, sizeof( unsigned int ) );
}


void     writeDouble( const double& value, std::ofstream& outFile )
{
	outFile.write( (char*)&value, sizeof( double ) );
}


void     writePointArray( const MFloatPointArray& pointArr, std::ofstream& outFile )
{
	unsigned int length = pointArr.length();
	outFile.write( (char*)&length, sizeof( unsigned int ) );

	float valueX, valueY, valueZ;

	for( unsigned int i=0; i< length; i++ )
	{
		valueX = pointArr[i].x;
		valueY = pointArr[i].y;
		valueZ = pointArr[i].z;
		outFile.write( (char*)&valueX, sizeof( float ) );
		outFile.write( (char*)&valueY, sizeof( float ) );
		outFile.write( (char*)&valueZ, sizeof( float ) );
	}
}


void     writeUnsignedIntArray( const MIntArray& intArr, std::ofstream& outFile )
{
	unsigned int length = intArr.length();
	outFile.write( (char*)&length, sizeof( unsigned int ) );

	unsigned int value;
	for( unsigned int i=0; i< length; i++ )
	{
		value = intArr[i];
		outFile.write( ( char* )&value, sizeof( unsigned int ) );
	}
}



void writeString( const MString& str, std::ofstream& outFile )
{
    unsigned int numChars = str.numChars();
    
    const char* name = str.asChar();
	outFile.write( (char*)&numChars, sizeof(unsigned int) );
    outFile.write( name, sizeof(char) * numChars );
}



void writeMatrix( const MMatrix& mtx, std::ofstream& outFile )
{
	double value;
	for( unsigned int i=0; i< 4; i++ )
	{
		for( unsigned int j=0; j<4; j++ )
		{
			value = mtx( i, j );
			outFile.write( (char*)&value, sizeof( double ) );
		}
	}
}



void writeVector( const MVector& vector, std::ofstream& outFile )
{
	outFile.write( ( char* )&vector.x, sizeof( double ) );
	outFile.write( ( char* )&vector.y, sizeof( double ) );
	outFile.write( ( char* )&vector.z, sizeof( double ) );
}



void writeStringArray( const MStringArray& stringArr, std::ofstream& outFile )
{
	unsigned int length = stringArr.length();
	outFile.write( (char*)&length, sizeof( unsigned int ) );

	for( unsigned int i=0; i< length; i++ )
	{
		writeString( stringArr[i], outFile );
	}
}


void readStringArray( MStringArray& stringArr, std::ifstream& inFile )
{
	unsigned int length;
	inFile.read( (char*)&length, sizeof( unsigned int ) );
	stringArr.setLength( length );

	for( unsigned int i=0; i< length; i++ )
	{
		readString( stringArr[i], inFile );
	}
}


void readUnsignedInt( unsigned int& value, std::ifstream& inFile )
{
	inFile.read( (char*)&value, sizeof( unsigned int ) );
}



void readDouble( double& value, std::ifstream& inFile )
{
	inFile.read( (char*)&value, sizeof( double ) );
}



void readPointArray( MFloatPointArray& pointArr, std::ifstream& inFile )
{
	unsigned int length;
	inFile.read( (char*)&length, sizeof( unsigned int ) );

	pointArr.setLength( length );

	for( unsigned int i=0; i< length; i++ )
	{
		inFile.read( (char*)&pointArr[i].x, sizeof( float ) );
		inFile.read( (char*)&pointArr[i].y, sizeof( float ) );
		inFile.read( (char*)&pointArr[i].z, sizeof( float ) );
	}
}



void   readUnsignedIntArray( MIntArray& intArr, std::ifstream& inFile )
{
	unsigned int length;
	inFile.read( (char*)&length, sizeof( unsigned int ) );
	intArr.setLength( length );

	for( unsigned int i=0; i< length; i++ )
	{
		inFile.read( ( char* )&intArr[i], sizeof( unsigned int ) );
	}
}



void readMatrix( MMatrix& mtx, std::ifstream& inFile )
{
	for( unsigned int i=0; i<4; i++ )
	{
		for( unsigned int j=0; j<4; j++ )
			inFile.read( (char*)&mtx( i, j ), sizeof( double ) );
	}
}



void readVector( MVector& vector, std::ifstream& inFile )
{
	inFile.read( ( char* )&vector.x, sizeof( double ) );
	inFile.read( ( char* )&vector.y, sizeof( double ) );
	inFile.read( ( char* )&vector.z, sizeof( double ) );
}



void readString( MString& str, std::ifstream& inFile )
{
    unsigned int numChars = 0;
    inFile.read( (char*)&numChars, sizeof(unsigned int) );
    char* pStr = new char[numChars + 1];
    inFile.read( pStr, sizeof(char) * numChars );
    pStr[numChars] = '\0';
    str = pStr;
	delete[] pStr;
}



MStatus getParents( const MDagPath& pathMesh, MDagPathArray& dagPathArr )
{
	MStatus status;

	MFnDagNode fnNode( pathMesh );
	unsigned int parentCount = fnNode.parentCount( &status );
	if( !parentCount ) return MS::kSuccess;
	MFnDagNode fnNodeParent( fnNode.parent(0) );
	
	if( fnNodeParent.name() == "world" ) return MS::kSuccess;

	MDagPath pathParent;
	fnNodeParent.getPath( pathParent );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	dagPathArr.insert( pathParent, 0 );
	return getParents( pathParent, dagPathArr );
}



MStatus assignInitialShadingGroup( MObject& oMesh )
{
    MStatus status;

    MSelectionList sList;
    MGlobal::getSelectionListByName( "initialShadingGroup", sList );
    MObject oInitialShadingGroup;
    status = sList.getDependNode( 0, oInitialShadingGroup );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    MFnSet fnShadingGroup( oInitialShadingGroup, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    status = fnShadingGroup.addMember( oMesh );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    return MS::kSuccess;
}



MObject getExistObjectByName( MString fullPathName )
{
	MSelectionList selList;

	MObject oReturn;
	fullPathName.substitute( ":", "_" );
	MGlobal::getSelectionListByName( fullPathName, selList );
	selList.getDependNode( 0, oReturn );

	return oReturn;
}




void writeMatrixArray( const MMatrixArray& matrixArr, std::ofstream& outFile )
{
	writeUnsignedInt( matrixArr.length(), outFile );
	for( unsigned int i=0; i< matrixArr.length(); i++ )
		writeMatrix( matrixArr[i], outFile );
}



void readMatrixArray( MMatrixArray& matrixArr, std::ifstream& inFile )
{
	unsigned int length;
	readUnsignedInt( length, inFile );
	matrixArr.setLength( length );
	for( unsigned int i=0; i< length; i++ )
		readMatrix( matrixArr[i], inFile );
}



void writeVectorArray( const MVectorArray& vectorArr, std::ofstream& outFile )
{
	writeUnsignedInt( vectorArr.length(), outFile );
	for( unsigned int i=0; i< vectorArr.length(); i++ )
		writeVector( vectorArr[i], outFile );
}



void readVectorArray( MVectorArray& vectorArr, std::ifstream& inFile )
{
	unsigned int length;
	readUnsignedInt( length, inFile );
	vectorArr.setLength( length );
	for( unsigned int i=0; i< length; i++ )
		readVector( vectorArr[i], inFile );
}



void     writeFloatArray( const MFloatArray& floatArr, std::ofstream& outFile )
{
	writeUnsignedInt( floatArr.length(), outFile );
	float value;
	for( unsigned int i=0; i< floatArr.length(); i++ )
	{
		value = floatArr[i];
		outFile.write( (char*)&value, sizeof( float ) );
	}
}



void     readFloatArray( MFloatArray& floatArr, std::ifstream& inFile )
{
	unsigned int length;
	readUnsignedInt( length, inFile );
	floatArr.setLength( length );
	for( unsigned int i=0; i< floatArr.length(); i++ )
	{
		inFile.read( (char*)&floatArr[i], sizeof( float ) );
	}
}



void     writeDoubleArray( const MDoubleArray& doubleArr, std::ofstream& outFile )
{
	writeUnsignedInt( doubleArr.length(), outFile );
	double value;
	for( unsigned int i=0; i< doubleArr.length(); i++ )
	{
		value = doubleArr[i];
		outFile.write( (char*)&value, sizeof( double ) );
	}
}



void     readDoubleArray( MDoubleArray& doubleArr, std::ifstream& inFile )
{
	unsigned int length;
	readUnsignedInt( length, inFile );
	doubleArr.setLength( length );
	for( unsigned int i=0; i< doubleArr.length(); i++ )
	{
		inFile.read( (char*)&doubleArr[i], sizeof( double ) );
	}
}



bool plugsHasConnection( const MPlugArray& plugsTarget )
{
	MPlugArray connections;
	for( unsigned int i=0; i< plugsTarget.length(); i++ )
	{
		plugsTarget[i].connectedTo( connections, true, false );
		if( connections.length() ) return true;
	}
	return false;
}