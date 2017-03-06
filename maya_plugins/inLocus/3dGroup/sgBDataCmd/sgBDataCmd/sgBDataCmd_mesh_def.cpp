#include "sgBDataCmd.h"
#include "sgBDataCmd_mesh.h"



void writeDataUV( const sgData_uv& dataUv, std::ofstream& outFile )
{
	writeString( dataUv.name_set, outFile );
	writeFloatArray( dataUv.uArray, outFile );
	writeFloatArray( dataUv.vArray, outFile );
	writeUnsignedIntArray( dataUv.uvCounts, outFile );
	writeUnsignedIntArray( dataUv.uvIds, outFile );
}




void readDataUV( sgData_uv& dataUv, std::ifstream& inFile )
{
	readString( dataUv.name_set, inFile );
	readFloatArray( dataUv.uArray, inFile );
	readFloatArray( dataUv.vArray, inFile );
	readUnsignedIntArray( dataUv.uvCounts, inFile );
	readUnsignedIntArray( dataUv.uvIds, inFile );
}




void writeDataUVs( const sgData_uvArray& dataUvs, std::ofstream& outFile )
{
	writeUnsignedInt( dataUvs.length(), outFile );
	for( unsigned int i=0; i< dataUvs.length(); i++ )
	{
		writeDataUV( dataUvs[i], outFile );
	}
}




void readDataUVs( sgData_uvArray& dataUvs, std::ifstream& inFile )
{
	unsigned int length;
	readUnsignedInt( length, inFile );
	dataUvs.setLength( length );
	for( unsigned int i=0; i< length; i++ )
	{
		readDataUV( dataUvs[i], inFile );
	}
}




void writeDataMesh( const sgData_mesh& dataMesh, std::ofstream& outFile )
{
	writeString( dataMesh.nameMesh, outFile );
	writeUnsignedInt( dataMesh.length_trs, outFile );
	writeStringArray( dataMesh.names_tr, outFile );
	writeUnsignedIntArray( dataMesh.rotateOders_tr, outFile );
	writeMatrixArray( dataMesh.matrixs_tr, outFile );
	writeVectorArray( dataMesh.translates_tr, outFile );
	writeVectorArray( dataMesh.rotates_tr, outFile );
	writeVectorArray( dataMesh.scales_tr, outFile );
	writeVectorArray( dataMesh.shears_tr, outFile );
	writeVectorArray( dataMesh.rotatePivs_tr, outFile );
	writeVectorArray( dataMesh.rotatePivTranslates_tr, outFile );
	writeVectorArray( dataMesh.scalePivs_tr, outFile );
	writeVectorArray( dataMesh.scalePivTranslates_tr, outFile );
	writeUnsignedIntArray( dataMesh.visibilitys_tr, outFile );

	writePointArray( dataMesh.points, outFile );
	writeUnsignedIntArray( dataMesh.polyCounts, outFile );
	writeUnsignedIntArray( dataMesh.polyConnects, outFile );

	writeDataUVs( dataMesh.uvs, outFile );
}




void readDataMesh( sgData_mesh& dataMesh, std::ifstream& inFile )
{
	readString( dataMesh.nameMesh, inFile );
	readUnsignedInt( dataMesh.length_trs, inFile );
	readStringArray( dataMesh.names_tr, inFile );
	readUnsignedIntArray( dataMesh.rotateOders_tr, inFile );
	readMatrixArray( dataMesh.matrixs_tr, inFile );
	readVectorArray( dataMesh.translates_tr, inFile );
	readVectorArray( dataMesh.rotates_tr, inFile );
	readVectorArray( dataMesh.scales_tr, inFile );
	readVectorArray( dataMesh.shears_tr, inFile );
	readVectorArray( dataMesh.rotatePivs_tr, inFile );
	readVectorArray( dataMesh.rotatePivTranslates_tr, inFile );
	readVectorArray( dataMesh.scalePivs_tr, inFile );
	readVectorArray( dataMesh.scalePivTranslates_tr, inFile );
	readUnsignedIntArray( dataMesh.visibilitys_tr, inFile );

	readPointArray( dataMesh.points, inFile );
	readUnsignedIntArray( dataMesh.polyCounts, inFile );
	readUnsignedIntArray( dataMesh.polyConnects, inFile );

	readDataUVs( dataMesh.uvs, inFile );
}




void setPositionByData( MObject& oTarget, const sgData_mesh& dataMesh, unsigned int index, bool b_importByMatrix )
{
	MFnTransform fnTarget = oTarget;
	
	MPlugArray plugArrTrans;
	plugArrTrans.append( fnTarget.findPlug( "t" ) );
	plugArrTrans.append( fnTarget.findPlug( "tx" ) );
	plugArrTrans.append( fnTarget.findPlug( "ty" ) );
	plugArrTrans.append( fnTarget.findPlug( "tz" ) );

	MPlugArray plugArrRotates;
	plugArrRotates.append( fnTarget.findPlug( "r" ) );
	plugArrRotates.append( fnTarget.findPlug( "rx" ) );
	plugArrRotates.append( fnTarget.findPlug( "ry" ) );
	plugArrRotates.append( fnTarget.findPlug( "rz" ) );

	MPlugArray plugArrScales;
	plugArrScales.append( fnTarget.findPlug( "s" ) );
	plugArrScales.append( fnTarget.findPlug( "sx" ) );
	plugArrScales.append( fnTarget.findPlug( "sy" ) );
	plugArrScales.append( fnTarget.findPlug( "sz" ) );

	MPlugArray plugArrShears;
	plugArrShears.append( fnTarget.findPlug( "sh" ) );
	plugArrShears.append( fnTarget.findPlug( "shx" ) );
	plugArrShears.append( fnTarget.findPlug( "shy" ) );
	plugArrShears.append( fnTarget.findPlug( "shz" ) );

	MPlugArray plugArrVis;
	plugArrVis.append( fnTarget.findPlug( "v" ) );

	if( b_importByMatrix )
	{
		if( !plugsHasConnection( plugArrTrans ) && !plugsHasConnection( plugArrRotates ) &&
			!plugsHasConnection( plugArrScales ) && !plugsHasConnection( plugArrShears ) )
		{
			MTransformationMatrix trMtx( dataMesh.matrixs_tr[index] );
			fnTarget.setTranslation( trMtx.translation( MSpace::kTransform ), MSpace::kTransform );
			fnTarget.setRotation( trMtx.rotation(), MSpace::kTransform );
			double scale[3], shear[3];
			trMtx.getScale( scale, MSpace::kTransform );
			trMtx.getShear( shear, MSpace::kTransform );
			fnTarget.setScale( scale );
			fnTarget.setShear( shear );
		}
	}
	else
	{
		if( !plugsHasConnection( plugArrTrans ) )
		fnTarget.setTranslation( dataMesh.translates_tr[ index ], MSpace::kTransform );
		if( !plugsHasConnection( plugArrRotates ) )
		{
			double rot[3];
			rot[0] = dataMesh.rotates_tr[ index ].x;
			rot[1] = dataMesh.rotates_tr[ index ].y;
			rot[2] = dataMesh.rotates_tr[ index ].z;
			fnTarget.setRotation( rot, ( MTransformationMatrix::RotationOrder )dataMesh.rotateOders_tr[ index ] );
		}
		if( !plugsHasConnection( plugArrScales ) )
		{
			double scale[3];
			scale[0] = dataMesh.scales_tr[index].x;
			scale[1] = dataMesh.scales_tr[index].y;
			scale[2] = dataMesh.scales_tr[index].z;
			fnTarget.setScale( scale );
		}
		if( !plugsHasConnection( plugArrShears ) )
		{
			double shear[3];
			shear[0] = dataMesh.shears_tr[index].x;
			shear[1] = dataMesh.shears_tr[index].y;
			shear[2] = dataMesh.shears_tr[index].z;
			fnTarget.setShear( shear );
		}
		fnTarget.setRotatePivot( dataMesh.rotatePivs_tr[index], MSpace::kTransform, false );
		fnTarget.setRotatePivotTranslation( dataMesh.rotatePivTranslates_tr[index], MSpace::kTransform );
		fnTarget.setScalePivot( dataMesh.scalePivs_tr[index], MSpace::kTransform, false );
		fnTarget.setScalePivotTranslation( dataMesh.scalePivTranslates_tr[index], MSpace::kTransform );
	}

	if( !plugsHasConnection( plugArrVis ) )
	{
		plugArrVis[0].setBool( dataMesh.visibilitys_tr[index] );
	}
}




MString getLocalName( const MString& fullPathName )
{
	MStringArray splits;
	fullPathName.split( '|', splits );
	return splits[splits.length()-1];
}




MStatus sgBDataCmd_mesh::readMesh_fromMesh( sgData_mesh& dataMesh, const MDagPath& dagPath_mesh )
{
	MStatus status;

	if( dagPath_mesh.apiType() != MFn::kMesh ) return MS::kFailure;

	MDagPathArray dagPathArr_parents;
	status = getParents( dagPath_mesh, dagPathArr_parents );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnMesh fnMesh( dagPath_mesh );

	dataMesh.nameMesh = fnMesh.name();
	dataMesh.length_trs = dagPathArr_parents.length();
	dataMesh.rotateOders_tr.setLength( dataMesh.length_trs );
	dataMesh.names_tr.setLength( dataMesh.length_trs );
	dataMesh.matrixs_tr.setLength( dataMesh.length_trs );
	dataMesh.translates_tr.setLength( dataMesh.length_trs );
	dataMesh.rotates_tr.setLength( dataMesh.length_trs );
	dataMesh.scales_tr.setLength( dataMesh.length_trs );
	dataMesh.shears_tr.setLength( dataMesh.length_trs );
	dataMesh.rotatePivs_tr.setLength( dataMesh.length_trs );
	dataMesh.rotatePivTranslates_tr.setLength( dataMesh.length_trs );
	dataMesh.scalePivs_tr.setLength( dataMesh.length_trs );
	dataMesh.scalePivTranslates_tr.setLength( dataMesh.length_trs );
	dataMesh.visibilitys_tr.setLength( dataMesh.length_trs );

	for( unsigned int i=0; i< dagPathArr_parents.length(); i++ )
	{
		MFnTransform fnTransform = dagPathArr_parents[i];
		dataMesh.names_tr[i]      = fnTransform.fullPathName();
		dataMesh.rotateOders_tr[i]= fnTransform.rotationOrder();
		dataMesh.matrixs_tr[i]    = fnTransform.transformation().asMatrix();
		dataMesh.translates_tr[i] = fnTransform.translation( MSpace::kTransform );
		MEulerRotation euler; fnTransform.getRotation( euler );
		double scale[3]; fnTransform.getScale( scale );
		double shear[3]; fnTransform.getShear( shear );
		dataMesh.rotates_tr[i] = euler.asVector();
		dataMesh.scales_tr[i]  = MVector( scale );
		dataMesh.shears_tr[i]  = MVector( shear );
		dataMesh.rotatePivs_tr[i] = fnTransform.rotatePivot( MSpace::kTransform );
		dataMesh.rotatePivTranslates_tr[i] = fnTransform.rotatePivotTranslation( MSpace::kTransform );
		dataMesh.scalePivs_tr[i] = fnTransform.scalePivot( MSpace::kTransform );
		dataMesh.scalePivTranslates_tr[i] = fnTransform.scalePivotTranslation( MSpace::kTransform );
		dataMesh.visibilitys_tr[i] = fnTransform.findPlug( "v" ).asBool();
	}

	fnMesh.getPoints( dataMesh.points );
	dataMesh.polyCounts.setLength( fnMesh.numPolygons() );
	dataMesh.polyConnects.setLength( fnMesh.numFaceVertices() );

    MIntArray vertexList;
    int index = 0;
    for ( int i = 0; i < fnMesh.numPolygons(); i++ )
    {
        status = fnMesh.getPolygonVertices( i, vertexList ); CHECK_MSTATUS_AND_RETURN_IT( status );
        dataMesh.polyCounts[i] = vertexList.length();
        for ( unsigned int j = 0; j < vertexList.length(); j++ )
            dataMesh.polyConnects[index++] = vertexList[j];
    }

	status = readUVs_fromMesh( dataMesh.uvs, dagPath_mesh );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	return MS::kSuccess;
}




MStatus sgBDataCmd_mesh::readUVs_fromMesh( sgData_uvArray& dataUVs, const MDagPath& dagPath_mesh )
{
	MStatus status;

	if( dagPath_mesh.apiType() != MFn::kMesh ) return MS::kFailure;

	MDagPathArray dagPathArr_parents;
	status = getParents( dagPath_mesh, dagPathArr_parents );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnMesh fnMesh( dagPath_mesh );

	MStringArray namesUV;
	fnMesh.getUVSetNames( namesUV );

	dataUVs.setLength( namesUV.length() );

	MFloatArray uArray, vArray;
	MIntArray   countsUV, idsUV;
	for( unsigned int i=0; i< dataUVs.length(); i++ )
	{
		fnMesh.getUVs( uArray, vArray, &namesUV[i] );
		fnMesh.getAssignedUVs( countsUV, idsUV, &namesUV[i] );

		dataUVs[i].name_set = namesUV[i];
		dataUVs[i].uArray   = uArray;
		dataUVs[i].vArray   = vArray;
		dataUVs[i].uvCounts = countsUV;
		dataUVs[i].uvIds    = idsUV;
	}
	return MS::kSuccess;
}




MStatus sgBDataCmd_mesh::exportMesh_toFile( const sgData_mesh& dataMesh, MString str_filePath )
{
	MStatus status;

	std::ofstream outFile( str_filePath.asChar(), ios::binary );

	writeString( "sgBData_mesh", outFile );
	writeDataMesh( dataMesh, outFile );

	outFile.close();

	return MS::kSuccess;
}




MStatus sgBDataCmd_mesh::exportUVs_toFile( const sgData_uvArray& dataUVs, MString str_filePath )
{
	MStatus stauts;

	std::ofstream outFile( str_filePath.asChar(), ios::binary );

	writeString( "sgBData_uvs", outFile );
	writeDataUVs( dataUVs, outFile );

	outFile.close();

	return MS::kSuccess;
}




MStatus sgBDataCmd_mesh::readMesh_fromFile( sgData_mesh& dataMesh, MString str_filePath )
{
	MStatus status;

	std::ifstream inFile( str_filePath.asChar(), ios::binary );

	MString str_dataType;
	readString( str_dataType, inFile );
	if( str_dataType != "sgBData_mesh" )
	{
		char buffer[512];
		str_filePath.substitute( "\\", "/" );
		MStringArray names_split;
		str_filePath.split( '/', names_split );
		sprintf( buffer, "%s는 sgBData_mesh 파일 타입이 아닙니다.", names_split[ names_split.length()-1 ].asChar() );
	}
	readDataMesh( dataMesh, inFile );

	inFile.close();

	return MS::kSuccess;
}




MStatus sgBDataCmd_mesh::readUVs_fromFile(  sgData_uvArray& dataUVs, MString str_filePath )
{
	MStatus status;

	std::ifstream inFile( str_filePath.asChar(), ios::binary );

	MString str_dataType;
	readString( str_dataType, inFile );
	if( str_dataType != "sgBData_uvs" )
	{
		char buffer[512];
		str_filePath.substitute( "\\", "/" );
		MStringArray names_split;
		str_filePath.split( '/', names_split );
		sprintf( buffer, "%s는 sgBData_uvs 파일 타입이 아닙니다.", names_split[ names_split.length()-1 ].asChar() );
	}
	readDataUVs( dataUVs, inFile );

	inFile.close();

	return MS::kSuccess;
}




MStatus sgBDataCmd_mesh::importMesh_fromData( const sgData_mesh& dataMesh, bool b_importByMatrix )
{
	MStatus status;

	MFnTransform fnTrForCreate;
	MFnMesh      fnMeshForCreate;
	
	MObject oLast;

	bool bNotExists = true;
	bool firstCreateExists = false;

	for( unsigned int i=0; i< dataMesh.length_trs; i++ )
	{
		MObject oTarget = getExistObjectByName( dataMesh.names_tr[i] );
		bNotExists = oTarget.isNull();

		if( bNotExists && i==0 )
		oTarget = fnTrForCreate.create();
		else if( bNotExists )
		oTarget = fnTrForCreate.create( oLast );

		if( bNotExists )
		{
			MString localName = getLocalName( dataMesh.names_tr[i] );
			localName.substitute( ":", "_" );
			fnTrForCreate.setName( localName );
			if( !firstCreateExists )m_oArrTransformsImported.append( oTarget );
			firstCreateExists = true;
		}

		setPositionByData( oTarget, dataMesh, i, b_importByMatrix );
		oLast = oTarget;
	}
	MString nameMesh = dataMesh.nameMesh;
	nameMesh.substitute( ":", "_" );

	MFnDagNode dagLast = oLast;
	MString nameFullPathMesh = dagLast.fullPathName() + "|" + nameMesh;

	MObject oMesh = getExistObjectByName( nameFullPathMesh );

	if( oMesh.isNull() )
	{
		int numVertices = dataMesh.points.length();
		int numPolygons  = dataMesh.polyCounts.length();
		MObject oMesh = fnMeshForCreate.create( numVertices, numPolygons, dataMesh.points, 
			dataMesh.polyCounts, dataMesh.polyConnects, oLast, &status );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		m_oMeshImported = oMesh;

		fnMeshForCreate.setObject( oMesh );
		fnMeshForCreate.setName( nameMesh );

		MDagPath dagPathMesh;
		dagPathMesh.getAPathTo( oMesh, dagPathMesh );
		importUVs_fromData( dataMesh.uvs, dagPathMesh );

		assignInitialShadingGroup( oMesh );
	}

	return MS::kSuccess;
}




MStatus sgBDataCmd_mesh::importUVs_fromData( const sgData_uvArray& dataUVs, MDagPath& dagPath_mesh )
{
	MStatus status;

	MFnMesh fnMesh = dagPath_mesh;
	MStringArray namesUVSetOrig;
	status = fnMesh.getUVSetNames( namesUVSetOrig ); CHECK_MSTATUS_AND_RETURN_IT( status );
	fnMesh.clearUVs( &namesUVSetOrig[0] );
	for( unsigned int i=1; i< namesUVSetOrig.length(); i++ ) fnMesh.deleteUVSet( namesUVSetOrig[i] );

	MString nameUVSet;
	for( unsigned int i=0; i< dataUVs.length(); i++ )
	{
		if( i == 0 ) nameUVSet = namesUVSetOrig[i]; 
		else fnMesh.createUVSet( nameUVSet );

		fnMesh.setUVs( dataUVs[i].uArray, dataUVs[i].vArray, &nameUVSet );
		fnMesh.assignUVs( dataUVs[i].uvCounts, dataUVs[i].uvIds, &nameUVSet );
	}
	return MS::kSuccess;
}