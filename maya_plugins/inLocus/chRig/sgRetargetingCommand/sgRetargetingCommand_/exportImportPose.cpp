#include "exportImportPose.h"
#include "retargetingCommand.h"


ExportImportPose::ExportImportPose()
{
	m_enOptions.setLength( 8 );
}


ExportImportPose::~ExportImportPose()
{
}


void* ExportImportPose::creator()
{
	return new ExportImportPose();
}


bool ExportImportPose::canBeOpened() const
{
	return false;
}


bool ExportImportPose::haveReadMethod() const
{
	return true;
}


bool ExportImportPose::haveWriteMethod() const
{
	return true;
}


MString ExportImportPose::defaultExtension() const
{
	return "cpose";
}


MPxFileTranslator::MFileKind ExportImportPose::identifyFile(
	const MFileObject& fileName,
	const char* buffer,
	short size ) const
{
	MStatus status;
	MString name = fileName.name();

	unsigned int nameLength = name.numChars();
	name.toLowerCase();
	MStringArray tokens;
	status = name.split( '.', tokens );
	
	if( !status ) return MPxFileTranslator::kNotMyFileType;

	MString lastToken = tokens[ tokens.length()-1 ];

	if( nameLength > 4 && lastToken == defaultExtension() )
	{
		return MPxFileTranslator::kIsMyFileType;
	}
	else
	{
		return MPxFileTranslator::kNotMyFileType;
	}
}


MStatus ExportImportPose::writer(
	const MFileObject& file,
	const MString& optionsString,
	FileAccessMode mode )
{
	MStatus status;

	const char* fileName = file.fullName().asChar();
	std::ofstream outFile( fileName, ios::binary );
	if( !outFile.is_open() )
	{
		return MS::kFailure;
	}

	if ( mode == MPxFileTranslator::kExportAccessMode )
    {
        //status = exportAll( outFile );
        //CHECK_MSTATUS_AND_RETURN_IT( status );
    }
    else if( mode == MPxFileTranslator::kExportActiveAccessMode )
	{
		parseOptionString( optionsString );
		status = exportData( outFile );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	outFile.close();

	return MS::kSuccess;
}



MStatus  ExportImportPose::parseOptionString( const MString& optionString )
{
	MStatus status;

	if( optionString.numChars() == 0 ) return MS::kFailure;

	cout << "optionString : " << optionString << endl;

	MStringArray optionList;
	MStringArray currentOption;
	optionString.split( ';', optionList );

	cout << "optionList length : " << optionList.length() << endl;

	for( unsigned int i=0; i< optionList.length(); i++ )
	{
		currentOption.clear();
		optionList[i].split( '=', currentOption );

		m_enOptions[i] = currentOption[1].asInt();
	}

	return MS::kSuccess;
}



MStatus  ExportImportPose::reader( const MFileObject& file,
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

	status = importData( inFile );
	CHECK_MSTATUS_AND_RETURN_IT( status );
	inFile.close();

	return MS::kSuccess;
}


MStatus ExportImportPose::getNamespaceFromWorldCtl( MString& namespaceGet )
{
	MStatus status;

	MSelectionList selList;
	status = MGlobal::getActiveSelectionList( selList );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MDagPath path;
	status = selList.getDagPath( 0, path );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MFnTransform tr( path, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MString nameWorldCtl = tr.name( &status );
	int lengthStr = nameWorldCtl.length();
	MString strWorldCtl = nameWorldCtl.substring( lengthStr-9, lengthStr );

	if( strWorldCtl != "World_CTL" )
	CHECK_MSTATUS_AND_RETURN_IT( MS::kFailure );

	namespaceGet = strWorldCtl.substring( 0, lengthStr-10 );

	return MS::kSuccess;
}


MStatus ExportImportPose::exportData( std::ofstream& outFile )
{
	MStatus status;

	MString namespaceGet;
	status = getNamespaceFromWorldCtl( namespaceGet );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	//CtlSet ctlSet;

	for( int i=0; i< m_enOptions.length(); i++ )
	{
	}

	return MS::kSuccess;
}


MStatus ExportImportPose::importData( std::ifstream& outFile )
{
	MStatus status;

	cout << "import excuted!" << endl;

	return MS::kSuccess;
}