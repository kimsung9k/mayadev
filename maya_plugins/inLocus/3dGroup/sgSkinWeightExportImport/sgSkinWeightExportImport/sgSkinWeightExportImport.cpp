#include "sgSkinWeightExportImport.h"


sgSkinWeightExportImport::sgSkinWeightExportImport()
{
}

sgSkinWeightExportImport::~sgSkinWeightExportImport()
{
}

void* sgSkinWeightExportImport::creator()
{
	return new sgSkinWeightExportImport();
}

bool  sgSkinWeightExportImport::canBeOpened() const
{
	return false;
}

bool  sgSkinWeightExportImport::haveReadMethod() const
{
	return true;
}

bool  sgSkinWeightExportImport::haveWriteMethod() const
{
	return true;
}

MString  sgSkinWeightExportImport::defaultExtension() const
{
	return "weight";
}

MPxFileTranslator::MFileKind  sgSkinWeightExportImport::identifyFile(
	const  MFileObject& fileName,
	const  char* buffer,
	short  size ) const
{
	MStatus  status;
	MString  name = fileName.name();

	unsigned int nameLength  = name.numChars();
	name.toLowerCase();
	MStringArray tokens;
	status = name.split( '.', tokens );
	CHECK_MSTATUS( status );
	MString  lastToken = tokens[tokens.length()-1];

	if( nameLength > 4 && lastToken == defaultExtension() )
	{
		return MPxFileTranslator::kIsMyFileType;
	}
	else
	{
		return MPxFileTranslator::kNotMyFileType;
	}
}


MStatus  sgSkinWeightExportImport::writer(
	const MFileObject& file,
	const MString& optionsString,
	FileAccessMode  mode )
{
	MStatus  status;

	status = parseOptionsString( optionsString );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	const char* fileName = file.fullName().asChar();
	std::ofstream  output( fileName, ios::binary );
	if( !output.is_open() )
	{
		return MS::kFailure;
	}

	if( mode == MPxFileTranslator::kExportActiveAccessMode )
	{
		status = exportSelected( output );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	output.close();
	return MS::kSuccess;
}


MStatus  sgSkinWeightExportImport::parseOptionsString( const MString& optionsString )
{
	MStatus status;
	/*
    m_exportNormals = false;
    m_exportUVs = false;

    if ( optionsString.numChars() > 0 )
    {
        MStringArray optionList;
        MStringArray currentOption;
        optionsString.split( ';', optionList );

        for ( unsigned int i = 0; i < optionList.length(); ++i )
        {
            currentOption.clear();
            optionList[i].split( '=', currentOption );
            if ( currentOption.length() != 2 )
            {
                continue;
            }
            if ( currentOption[0] == "normals" && currentOption[1].asInt() )
            {
                m_exportNormals = true;
            }
            if ( currentOption[0] == "uvs" && currentOption[1].asInt() )
            {
                m_exportUVs = true;
            }
        }
    }
	*/
	return MS::kSuccess;
}


MStatus  sgSkinWeightExportImport::exportSelected( std::ofstream& output )
{
	MStatus status;

	MSelectionList sList;
	MGlobal::getActiveSelectionList( sList );
	if( sList.length() == 0 )
	{
		return MS::kFailure;
	}
	MItSelectionList itList( sList );

	MDagPath pathDag;
	for( ; !itList.isDone(); itList.next() )
	{
		status = itList.getDagPath( pathDag );
		if( MFAIL( status ) )
		{
			continue;
		}
		status = exportWeightInfo( pathDag, output );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}
	return MS::kSuccess;
}


MStatus  sgSkinWeightExportImport::exportWeightInfo( 
	      MDagPath& pathDag, std::ofstream& output )
{
	MStatus status;
	
	MMatrix transformMatrix = pathDag.inclusiveMatrix();
	float writeMatrix[16];
	for( int i=0; i<4; i++ )
	{
		for( int j=0; j<4; j++ )
			writeMatrix[i*4+j] = (float)transformMatrix( i, j );
	}

	MFnDependencyNode fnSkinClusterNode;
	status = getSkinClusterNodeFromPath( pathDag, fnSkinClusterNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MPlug matrixPlug = fnSkinClusterNode.findPlug( "matrix" );
	unsigned int numJoint = matrixPlug.numElements();

	MMatrix eachMatrix;
	MPoint  eachPoint;
	MFnMatrixData eachMatrixData;

	output.write( (char*)writeMatrix, sizeof( float ) * 16 );
	output.write( (char*)&numJoint, sizeof( unsigned int ) );
	int logicalIndex =0;
	double point[3];
	for( unsigned int i=0; i<numJoint; i++ )
	{
		logicalIndex = matrixPlug[i].logicalIndex();
		eachMatrixData.setObject( matrixPlug[i].asMObject() );
		eachMatrix = eachMatrixData.matrix();
		point[0] = eachMatrix(3,0);
		point[1] = eachMatrix(3,1);
		point[2] = eachMatrix(3,2);

		output.write( (char*)&logicalIndex, sizeof( unsigned int ) );
		output.write( (char*)point, sizeof( double )*3 );
	}

	MPointArray shapeVtxPoints;
	MFnMesh fnMesh( pathDag, &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );

    unsigned int numVertices = fnMesh.numVertices();
    unsigned int numPolygons = fnMesh.numPolygons();
    unsigned int numFaceVertices = fnMesh.numFaceVertices();
    const float* points = fnMesh.getRawPoints( &status );
    CHECK_MSTATUS_AND_RETURN_IT( status );
    int* polyCounts = new int[numPolygons];
    int* faceVertices = new int[numFaceVertices];
    MIntArray vertexList;
    int index = 0;
    for ( unsigned int i = 0; i < numPolygons; i++ )
    {
        status = fnMesh.getPolygonVertices( i, vertexList );
        CHECK_MSTATUS_AND_RETURN_IT( status );
        polyCounts[i] = (int)vertexList.length();
        for ( unsigned int j = 0; j < vertexList.length(); j++ )
        {
            faceVertices[index++] = vertexList[j];
        }
    }

    output.write( (char*)&numVertices, sizeof(unsigned int) );
    output.write( (char*)&numPolygons, sizeof(unsigned int) );
    output.write( (char*)points, sizeof(float) * numVertices * 3 );
    output.write( (char*)polyCounts, sizeof(int) * numPolygons );
    output.write( (char*)&numFaceVertices, sizeof(unsigned int) );
    output.write( (char*)faceVertices, sizeof(int) * numFaceVertices );

	MPlug weightListPlug = fnSkinClusterNode.findPlug( "weightList" );

	unsigned int numVtx = weightListPlug.numElements();
	for( unsigned int i=0; i< numVtx; i++ )
	{
		MPlug plugWeights = weightListPlug[i].child(0);
		unsigned int numElements = plugWeights.numElements();
		output.write( (char*)&numElements, sizeof( unsigned int ) );
		unsigned int logicalIndex;
		float weight;
		for( unsigned int j=0; j< plugWeights.numElements(); j++ )
		{
			logicalIndex = plugWeights[j].logicalIndex();
			weight       = plugWeights[j].asFloat();
			output.write( (char*)&logicalIndex, sizeof( unsigned int ) );
			output.write( (char*)&weight, sizeof( float ) );
		}
	}

	return MS::kSuccess;
}



MStatus  sgSkinWeightExportImport::reader( const MFileObject& file,
        const MString& optionsString,
        FileAccessMode mode )
{
	MStatus status;
	const char* fileName = file.fullName().asChar();
	std::ifstream inFile( fileName, ios::binary );

	if( !inFile.is_open() )
	{
		return MS::kFailure;
	}

	std::streamoff current = inFile.tellg();
	inFile.seekg( 0, ios::end );
	std::streamoff length = inFile.tellg();
	inFile.seekg( 0, ios::beg );

	MSelectionList selList;
	MGlobal::getActiveSelectionList( selList );

	if( !selList.length() )
		return MS::kFailure;

	MDagPath mDagPath;
	for( int i=0; i<selList.length(); i++ )
	{
		selList.getDagPath( i, mDagPath );
		status = importWeightInfo( inFile, mDagPath );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}
	return MS::kSuccess;
}


MStatus  sgSkinWeightExportImport::getShape( MDagPath& targetPath )
{
	MStatus status;
	MDagModifier mdagModifier;

	unsigned int numShape;
	targetPath.numberOfShapesDirectlyBelow( numShape );

	bool shapeExists = false;
	for( int i=0; i<numShape; i++ )
	{
		status = targetPath.extendToShapeDirectlyBelow( i );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		if( targetPath.apiType() == MFn::kMesh )
		{
			return MS::kSuccess;
		}
		targetPath.pop();
	}
	return MS::kFailure;
}



MStatus  sgSkinWeightExportImport::importWeightInfo( std::ifstream& inFile, MDagPath& targetPath )
{
	MStatus status;
	MDagModifier mdagModifier;

	MMatrix targetMatrix;
	fileInfo weightInfo;
	MFnTransform tempTransform;
	tempTransform.create( MObject::kNullObj, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	status = getFileInfo( inFile, &weightInfo, tempTransform, targetMatrix );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MObject oTempMesh = tempTransform.child( 0, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	MFnTransform targetNode = targetPath.node();
	status = getShape( targetPath );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MTransformationMatrix transformMtx( targetMatrix );
	tempTransform.set( transformMtx );

	char deformBuffer[512];
	sprintf( deformBuffer, "deformer -type skinCluster %s;", tempTransform.fullPathName().asChar() );
	MGlobal::executeCommand( deformBuffer );

	MDagPath tempTransformPath;
	status = tempTransform.getPath( tempTransformPath );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnDependencyNode skinNode;
	status = getSkinClusterNodeFromPath( tempTransformPath, skinNode );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MObjectArray oJoints;
	status = setInfoToSkinNode( weightInfo, skinNode, oJoints );
	char copySkinBuffer[512];
	sprintf( copySkinBuffer, "copySkinWeights -noMirror -surfaceAssociation closestPoint -influenceAssociation closestJoint -normalize %s %s;",
		 tempTransform.fullPathName().asChar(), targetNode.fullPathName().asChar() );
	MGlobal::executeCommand( copySkinBuffer );
	
	MDagModifier modifier;
	modifier.deleteNode( tempTransform.object() );

	for( int i=0; i< oJoints.length(); i++ )
		modifier.deleteNode( oJoints[i] );
	modifier.doIt();
	
	return MS::kSuccess;
}


MStatus sgSkinWeightExportImport::setInfoToSkinNode( fileInfo& weightInfo,
	                                               MFnDependencyNode& skinNode, MObjectArray& oJoints )
{
	MStatus status;

	MDagModifier dagModifier;

	MTransformationMatrix mtx, inv;
	MFnMatrixData mtxData, invData;

	MPlug matrixPlug = skinNode.findPlug( "matrix" );
	MPlug bindPrePlug = skinNode.findPlug( "bindPreMatrix" );
	MPlug weightListPlug = skinNode.findPlug( "weightList" );

	oJoints.setLength( weightInfo.matrixIndices.length() );

	for( int i=0; i< weightInfo.matrixIndices.length(); i++ )
	{
		mtx.setTranslation( weightInfo.matrixPositions[i], MSpace::kTransform );
		inv.setTranslation( weightInfo.matrixPositions[i]*-1, MSpace::kTransform );
		
		mtxData.create( mtx, &status );
		invData.create( inv, &status );

		int logicalIndex = weightInfo.matrixIndices[i];

		oJoints[i] = dagModifier.createNode( "joint" );
		dagModifier.doIt();
		MFnTransform fnJoint = oJoints[i];
		MPlug jntMatrixPlug = fnJoint.findPlug( "matrix", status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		fnJoint.translateBy( weightInfo.matrixPositions[i], MSpace::kTransform );

		MPlug matrixElement = matrixPlug.elementByLogicalIndex( logicalIndex );
		MPlug bindPreElement = bindPrePlug.elementByLogicalIndex( logicalIndex );
		dagModifier.connect( jntMatrixPlug, matrixElement );

		bindPreElement.setMObject( invData.object() );
		dagModifier.doIt();
	}
	

	for( int i=0; i< weightInfo.weightListIndices.size(); i++ )
	{
		MIntArray& weightIndices = weightInfo.weightListIndices[i];
		MFloatArray& weightValues = weightInfo.weightListValues[i];

		MPlug weightListElement = weightListPlug.elementByLogicalIndex( i );
		MPlug weightPlug = weightListElement.child( 0 );

		for( int j=0; j<weightIndices.length(); j++ )
		{
			MPlug weightElement = weightPlug.elementByLogicalIndex( weightIndices[j] );
			weightElement.setFloat( weightValues[j] );
		}
	}

	return MS::kSuccess;
}


MStatus sgSkinWeightExportImport::getFileInfo( std::ifstream& inFile, fileInfo* pInfo,
	                                         MFnTransform& targetTransform, MMatrix& getMatrix )
{
	MStatus status;

	float transformMatrix[16];
	inFile.read( (char*)transformMatrix, sizeof( float )*16 );

	for( int i=0; i<4; i++ )
	{
		for( int j=0; j<4; j++ )
		{
			getMatrix[i][j] = transformMatrix[i*4+j];
		}
	}

	unsigned int numJoint = 0;
	inFile.read( (char*)&numJoint, sizeof( unsigned int ) );
	
	MIntArray& matrixIndices = pInfo->matrixIndices;
	MPointArray& matrixPositions = pInfo->matrixPositions;
	MPointArray& vtxPoints = pInfo->vtxPoints;
	vector< MIntArray >& weightListIndices = pInfo->weightListIndices;
	vector< MFloatArray >& weightListValues = pInfo->weightListValues;

	matrixIndices.setLength( numJoint );
	matrixPositions.setLength( numJoint );

	unsigned int matrixIndex;
	double matrixPoint[3];
	
	for( unsigned int i=0; i<numJoint; i++ )
	{
		inFile.read( (char*)&matrixIndex, sizeof( unsigned int ) );
		inFile.read( (char*)matrixPoint, sizeof( double )*3 );
		matrixIndices[i] = matrixIndex;
		matrixPositions[i].x = matrixPoint[0];
		matrixPositions[i].y = matrixPoint[1];
		matrixPositions[i].z = matrixPoint[2];
		matrixPositions[i].w = 1.0;
	}

	unsigned int numVertices = 0;
    unsigned int numPolygons = 0;
    inFile.read( (char*)&numVertices, sizeof(unsigned int) );
    inFile.read( (char*)&numPolygons, sizeof(unsigned int) );

    float* pPoints = new float[numVertices * 3];
    inFile.read( (char*)pPoints, sizeof(float) * numVertices * 3 );
    MFloatPointArray points( numVertices );
    for ( unsigned int i = 0; i < numVertices; i++ )
    {
        points[i].x = pPoints[i*3];
        points[i].y = pPoints[i*3 + 1];
        points[i].z = pPoints[i*3 + 2];
    }

    int* pPolyCounts = new int[numPolygons];
    inFile.read( (char*)pPolyCounts, sizeof(int) * numPolygons );
    MIntArray polyCounts( pPolyCounts, numPolygons );

    unsigned int numFaceVertices = 0;
    inFile.read( (char*)&numFaceVertices, sizeof(unsigned int) );
    int* pFaceVertices = new int[numFaceVertices];
    inFile.read( (char*)pFaceVertices, sizeof(int) * numFaceVertices );
    MIntArray faceVertices( pFaceVertices, numFaceVertices );

	MObject targetObj = targetTransform.object();
    MFnMesh fnMesh;
    MObject oResultMesh = fnMesh.create( numVertices, numPolygons, points, polyCounts, faceVertices, targetObj, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	vtxPoints.setLength( numVertices );
	weightListIndices.resize( numVertices );
	weightListValues.resize( numVertices );

	unsigned int numWeights;
	for( unsigned int i=0; i<numVertices; i++ )
	{
		inFile.read( (char*)&numWeights, sizeof( unsigned int ) );

		weightListIndices[i].setLength( numWeights );
		weightListValues[i].setLength( numWeights );

		unsigned int weightIndex;
		float weight;
		for( unsigned int j=0; j<numWeights; j++ )
		{
			inFile.read( (char*)&weightIndex, sizeof( unsigned int ) );
			inFile.read( (char*)&weight, sizeof( float ) );
			weightListIndices[i][j] = weightIndex;
			weightListValues[i][j] = weight;
		}
	}
	return MS::kSuccess;
}


MStatus sgSkinWeightExportImport::getSkinClusterNodeFromPath( 
	        MDagPath& pathDag, MFnDependencyNode& skinNode )
{
	MStatus status;

	if( pathDag.apiType() != MFn::kMesh )
	{
		unsigned int numShapes;
		status = pathDag.numberOfShapesDirectlyBelow( numShapes );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		if( !numShapes )
			return MS::kFailure;
		bool shapeExists = false;
		for( int i=0; i< numShapes; i++ )
		{
			status = pathDag.extendToShapeDirectlyBelow( i );
			if( pathDag.hasFn( MFn::kMesh ) )
			{
				shapeExists = true;
				break;
			}
			pathDag.pop();
		}
		if( !shapeExists ) return MS::kFailure;
	}

	MObject oMesh = pathDag.node();
	MItDependencyGraph itGraph( oMesh, MFn::kInvalid, MItDependencyGraph::kUpstream,
		MItDependencyGraph::kDepthFirst, MItDependencyGraph::kNodeLevel, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	while( !itGraph.isDone() )
	{
		skinNode.setObject( itGraph.currentItem() );
		if( skinNode.typeName() == "skinCluster" )
		{
			return MS::kSuccess;
		}
		itGraph.next();
	}

	return MS::kFailure;
}