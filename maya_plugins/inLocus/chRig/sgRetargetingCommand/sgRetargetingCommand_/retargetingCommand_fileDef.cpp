#include "retargetingCommand.h"


MStatus RetargetingCommand::argChk_exportImport( MArgDatabase& argData )
{
	MStatus statusImport;
	MStatus statusExport;
	MStatus statusImportCAnim;
	MStatus statusFileName;
	MStatus status;

	bool im = false;
	MString ex = "";
	bool ima = false;
	MString exa = "";
	MString nameFile;

	statusImport = argData.getFlagArgument( flagImport[0], 0, im );
	statusExport = argData.getFlagArgument( flagExport[0], 0, ex );
	statusImportCAnim = argData.getFlagArgument( flagImportCAnim[0], 0, ima );
	statusFileName = argData.getFlagArgument( flagFileName[0], 0, nameFile );

	if( !statusImport && !statusExport && !statusImportCAnim )
	return MS::kInvalidParameter;
	if( !statusFileName )
	return MS::kFailure;

	if( ex.length() )
	{
		status = exportFile( nameFile, argData );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}
	else if( im )
	{
		status = importFile( nameFile, m_ctlSetSrc, m_ctlSetSrcFlip );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}
	else if( ima )
	{
		status = importCAnimFile( nameFile );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	return MS::kSuccess;
}


void  writeLength( const int& length, std::ofstream& outFile )
{
	outFile.write( (char*)&length, sizeof( int ) );
}


void writeDouble( const double& value, std::ofstream& outFile )
{
	outFile.write( (char*)&value, sizeof( double ) );
}


void  writeBool( const bool& bValue, std::ofstream& outFile )
{
	outFile.write( (char*)&bValue, sizeof( bool ) );
}


void  writeMatrix( const MMatrix& mtx, std::ofstream& outFile )
{
	double dArr[16];

	for( int i=0; i< 4; i++ )
	{
		for( int j=0; j<4; j++ )
		{
			dArr[i*4+j] = mtx( i, j );
		}
	}
	outFile.write( (char*)dArr, sizeof( double )*16 );
}


void  readLength( int& length, std::ifstream& inFile )
{
	inFile.read( (char*)&length, sizeof( int ) );
}


void  readDouble( double& value, std::ifstream& inFile )
{
	inFile.read( (char*)&value, sizeof( double ) );
}


void  readBool( bool& bValue, std::ifstream& inFile )
{
	inFile.read( (char*)&bValue, sizeof( bool ) );
}


void  readMatrix( MMatrix& mtx, std::ifstream& inFile )
{
	double dArr[16];

	inFile.read( (char*)dArr, sizeof( double ) * 16 );

	for( int i=0; i< 4; i++ )
	{
		for( int j=0; j<4; j++ )
		{
			mtx( i, j ) = dArr[i*4+j];
		}
	}
}


MStatus RetargetingCommand::exportFile( const MString& nameFile, MArgDatabase& argData )
{
	MStatus status;

	if( !nameFile.length() ) return MS::kFailure;

	MSelectionList selList;
	MString nameWorldCtl;
	status = argData.getFlagArgument( flagExport[0], 0, nameWorldCtl );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	selList.add( nameWorldCtl );

	MDagPath path;
	status = selList.getDagPath( 0, path );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	nameWorldCtl = MFnDependencyNode( path.node() ).name();
	int lengthStr = nameWorldCtl.length();
	MString strWorldCtl = nameWorldCtl.substring( lengthStr-9, lengthStr );

	MString strNamespace;

	if( strWorldCtl == "World_CTL" )
	{
		strNamespace = nameWorldCtl.substring( 0, lengthStr-10 );
	}
	else
	{
		MGlobal::displayError( "Select World_CTL" );
		return MS::kFailure;
	}

	CtlSet& ctlSet = m_ctlSetSrc;

	ctlSet.setBaseData( strNamespace, true );
	ctlSet.updateRootMatrix();
	ctlSet.updateCtlMatrix();

	std::ofstream outFile( nameFile.asChar(), ios::binary );
	if( !outFile.is_open() ) return MS::kFailure;

	CtlArray& ctls = ctlSet.m_ctls;
	FkIkCtlArray& fkIkCtls = ctlSet.m_fkIkCtls;
	FingerCtlArray& fingerCtls = ctlSet.m_fingerCtls;

	writeMatrix( ctlSet.m_mtxRoot,      outFile );
	writeMatrix( ctlSet.m_mtxDirection, outFile );

	for( int i=0; i< ctls.length(); i++ )
	{
		writeBool( ctls[i].m_enable, outFile );
		if( !ctls[i].m_enable ) continue;

		writeMatrix( ctls[i].m_mtx,             outFile );
		writeMatrix( ctls[i].m_mtxOrt,          outFile );
		writeMatrix( ctls[i].m_mtxOrig,         outFile );
		writeMatrix( ctls[i].m_mtxOrigPTrs,     outFile );
		writeMatrix( ctls[i].m_mtxOrigPOrt,     outFile );
		
		writeLength( ctls[i].m_valueArrUdAttr.length(), outFile );
		for( int j=0; j< ctls[i].m_valueArrUdAttr.length(); j++ )
			writeDouble( ctls[i].m_valueArrUdAttr[j], outFile );
	}

	for( int i=0; i< fkIkCtls.length(); i++ )
	{
		writeBool( fkIkCtls[i].m_enable, outFile );
		if( !fkIkCtls[i].m_enable ) continue;

		writeMatrix( fkIkCtls[i].m_mtxShd, outFile );
		writeMatrix( fkIkCtls[i].m_mtxElb, outFile );
		writeMatrix( fkIkCtls[i].m_mtxWrt, outFile );
		writeMatrix( fkIkCtls[i].m_mtxShdOrig, outFile );
		writeMatrix( fkIkCtls[i].m_mtxElbOrig, outFile );
		writeMatrix( fkIkCtls[i].m_mtxWrtOrig, outFile );
		writeMatrix( fkIkCtls[i].m_mtxPTrsOrig, outFile );
		writeMatrix( fkIkCtls[i].m_mtxPOrtOrig, outFile );
		writeMatrix( fkIkCtls[i].m_mtxFk4, outFile );
		writeMatrix( fkIkCtls[i].m_mtxShdOrientOffset, outFile );
		writeMatrix( fkIkCtls[i].m_mtxItp, outFile );

		writeDouble( fkIkCtls[i].ud_poleTwist, outFile );
		writeDouble( fkIkCtls[i].ud_length, outFile );
		writeDouble( fkIkCtls[i].ud_bias, outFile );
		writeDouble( fkIkCtls[i].ud_stretchAble, outFile );
		writeDouble( fkIkCtls[i].ud_smoothRate, outFile );
		writeDouble( fkIkCtls[i].ud_positionAttach, outFile );

		writeDouble( fkIkCtls[i].ud_twist, outFile );
		writeDouble( fkIkCtls[i].ud_interpoleSwitch, outFile );

		writeDouble( fkIkCtls[i].ud_collarFollow, outFile );
		writeDouble( fkIkCtls[i].ud_chestFollow, outFile );
		writeDouble( fkIkCtls[i].ud_hipFollow, outFile );
		writeDouble( fkIkCtls[i].ud_rootFollow, outFile );
		writeDouble( fkIkCtls[i].ud_moveFollow, outFile );

		if( !fkIkCtls[i].m_nameFoot.length() ) continue;

		writeDouble( fkIkCtls[i].ud_heelRot, outFile );
		writeDouble( fkIkCtls[i].ud_heelLift, outFile );
		writeDouble( fkIkCtls[i].ud_toeRot, outFile );
		writeDouble( fkIkCtls[i].ud_tapToe, outFile );
		writeDouble( fkIkCtls[i].ud_walkRollAngle, outFile );
		writeDouble( fkIkCtls[i].ud_walkRoll, outFile );
		writeDouble( fkIkCtls[i].ud_bank, outFile );
		writeDouble( fkIkCtls[i].ud_heelTwist, outFile );
		writeDouble( fkIkCtls[i].ud_ballTwist, outFile );
		writeDouble( fkIkCtls[i].ud_ballRot, outFile );
		writeDouble( fkIkCtls[i].ud_toeTwist, outFile );
	}

	for( int i=0; i< fingerCtls.length(); i++ )
	{
		writeBool( fingerCtls[i].m_enable, outFile );
		if( !fingerCtls[i].m_enable ) continue;

		writeLength( fingerCtls[i].m_length, outFile );
		for( int j=0; j< fingerCtls[i].m_length; j++ )
		{
			writeMatrix( fingerCtls[i].m_mtxArr[j], outFile );
			writeMatrix( fingerCtls[i].m_mtxArrOrig[j], outFile );
			writeMatrix( fingerCtls[i].m_mtxArrOrigP[j], outFile );
		}
	}

	outFile.close();


	return MS::kSuccess;
}


MStatus RetargetingCommand::importFile( const MString& nameFile, CtlSet& ctlSetDefault, CtlSet& ctlSetFlip )
{
	MStatus status;

	if( !nameFile.length() ) return MS::kFailure;

	MSelectionList selList;
	MGlobal::getActiveSelectionList( selList );

	CtlSet& ctlSet = ctlSetFlip;
	ctlSet.setAllDisable();

	std::ifstream inFile( nameFile.asChar(), ios::binary );
	if( !inFile.is_open() ) return MS::kFailure;

	CtlArray& ctls = ctlSet.m_ctls;
	FkIkCtlArray& fkIkCtls = ctlSet.m_fkIkCtls;
	FingerCtlArray& fingerCtls = ctlSet.m_fingerCtls;

	readMatrix( ctlSet.m_mtxRoot,      inFile );
	readMatrix( ctlSet.m_mtxDirection, inFile );

	for( int i=0; i< ctls.length(); i++ )
	{
		readBool( ctls[i].m_enable, inFile );
		if( !ctls[i].m_enable ) continue;

		readMatrix( ctls[i].m_mtx,             inFile );
		readMatrix( ctls[i].m_mtxOrt,          inFile );
		readMatrix( ctls[i].m_mtxOrig,         inFile );
		readMatrix( ctls[i].m_mtxOrigPTrs,     inFile );
		readMatrix( ctls[i].m_mtxOrigPOrt,     inFile );

		int udAttrLength; readLength( udAttrLength, inFile );
		ctls[i].m_valueArrUdAttr.setLength( udAttrLength );

		for( int j=0; j< udAttrLength; j++ )
			readDouble( ctls[i].m_valueArrUdAttr[j], inFile );
	}

	for( int i=0; i< fkIkCtls.length(); i++ )
	{
		readBool( fkIkCtls[i].m_enable, inFile );
		if( !fkIkCtls[i].m_enable ) continue;

		readMatrix( fkIkCtls[i].m_mtxShd, inFile );
		readMatrix( fkIkCtls[i].m_mtxElb, inFile );
		readMatrix( fkIkCtls[i].m_mtxWrt, inFile );
		readMatrix( fkIkCtls[i].m_mtxShdOrig, inFile );
		readMatrix( fkIkCtls[i].m_mtxElbOrig, inFile );
		readMatrix( fkIkCtls[i].m_mtxWrtOrig, inFile );
		readMatrix( fkIkCtls[i].m_mtxPTrsOrig, inFile );
		readMatrix( fkIkCtls[i].m_mtxPOrtOrig, inFile );
		readMatrix( fkIkCtls[i].m_mtxFk4, inFile );
		readMatrix( fkIkCtls[i].m_mtxShdOrientOffset, inFile );
		readMatrix( fkIkCtls[i].m_mtxItp, inFile );

		readDouble( fkIkCtls[i].ud_poleTwist, inFile );
		readDouble( fkIkCtls[i].ud_length, inFile );
		readDouble( fkIkCtls[i].ud_bias, inFile );
		readDouble( fkIkCtls[i].ud_stretchAble, inFile );
		readDouble( fkIkCtls[i].ud_smoothRate, inFile );
		readDouble( fkIkCtls[i].ud_positionAttach, inFile );

		readDouble( fkIkCtls[i].ud_twist, inFile );
		readDouble( fkIkCtls[i].ud_interpoleSwitch, inFile );

		readDouble( fkIkCtls[i].ud_collarFollow, inFile );
		readDouble( fkIkCtls[i].ud_chestFollow, inFile );
		readDouble( fkIkCtls[i].ud_hipFollow, inFile );
		readDouble( fkIkCtls[i].ud_rootFollow, inFile );
		readDouble( fkIkCtls[i].ud_moveFollow, inFile );

		if( !fkIkCtls[i].m_nameFoot.length() ) continue;

		readDouble( fkIkCtls[i].ud_heelRot, inFile );
		readDouble( fkIkCtls[i].ud_heelLift, inFile );
		readDouble( fkIkCtls[i].ud_toeRot, inFile );
		readDouble( fkIkCtls[i].ud_tapToe, inFile );
		readDouble( fkIkCtls[i].ud_walkRollAngle, inFile );
		readDouble( fkIkCtls[i].ud_walkRoll, inFile );
		readDouble( fkIkCtls[i].ud_bank, inFile );
		readDouble( fkIkCtls[i].ud_heelTwist, inFile );
		readDouble( fkIkCtls[i].ud_ballTwist, inFile );
		readDouble( fkIkCtls[i].ud_ballRot, inFile );
		readDouble( fkIkCtls[i].ud_toeTwist, inFile );
	}

	for( int i=0; i< fingerCtls.length(); i++ )
	{
		readBool( fingerCtls[i].m_enable, inFile );
		if( !fingerCtls[i].m_enable ) continue;

		readLength( fingerCtls[i].m_length, inFile );
		fingerCtls[i].m_mtxArr.setLength( fingerCtls[i].m_length );
		fingerCtls[i].m_mtxArrOrig.setLength( fingerCtls[i].m_length );
		fingerCtls[i].m_mtxArrOrigP.setLength( fingerCtls[i].m_length );
		for( int j=0; j< fingerCtls[i].m_length; j++ )
		{
			readMatrix( fingerCtls[i].m_mtxArr[j], inFile );
			readMatrix( fingerCtls[i].m_mtxArrOrig[j], inFile );
			readMatrix( fingerCtls[i].m_mtxArrOrigP[j], inFile );
		}
	}

	
	inFile.close();

	ctlSetDefault = ctlSetFlip;

	ctlSetFlip.flip();

	m_srcNsUpdated   = false;
	m_srcMtxRequired = false;

	return MS::kSuccess;
}


MStatus RetargetingCommand::importCAnimFile( const MString& nameFile )
{
	MStatus status;

	struct _finddata_t fd;
    long handle;
    int result = 1;
 
	MString editName = nameFile  + "/*.cpose";

	handle = _findfirst( editName.asChar(), &fd);
	if(handle == -1)return MS::kFailure;

	m_fArrFrame.clear();

	MStringArray nameArrFile;

    while (result != -1)
    {
		nameArrFile.append( nameFile + "/" + fd.name );

		MString subString = MString( fd.name ).substring( 5, 11 );
		MString intArea = subString.substring( 0, 3 );
		MString floatArea = subString.substring( 5,6 );

		float frameRate = intArea.asFloat() + floatArea.asFloat() / 100.0;
		m_fArrFrame.append( frameRate );

        result = _findnext(handle, &fd);
    }
    _findclose(handle);

	m_ctlSetAnim.setLength( nameArrFile.length() );
	m_ctlSetAnimFlip.setLength( nameArrFile.length() );

	for( int i=0; i< nameArrFile.length(); i++ )
	{
		importFile( nameArrFile[i], m_ctlSetAnim[i], m_ctlSetAnimFlip[i] );
	}

	return MS::kSuccess;
}