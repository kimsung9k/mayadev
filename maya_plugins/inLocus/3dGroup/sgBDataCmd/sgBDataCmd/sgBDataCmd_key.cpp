#include  "sgBDataCmd.h"
#include  "sgBDataCmd_key.h"


MDagPathArray         sgBDataCmd_key::m_pathArrExport;
MStringArray          sgBDataCmd_key::m_filePaths;
sgObject_keyDataArray sgBDataCmd_key::m_objectKeyDatasExport;
bool                  sgBDataCmd_key::m_exportByMatrix;


sgObject_keyDataArray::sgObject_keyDataArray()
{
	m_p_data = new sgObject_keyData[ 0 ];
}
sgObject_keyDataArray::~sgObject_keyDataArray()
{
	delete[] m_p_data;
}
unsigned int sgObject_keyDataArray::length() const
{
	return m_length;
}
void sgObject_keyDataArray::setLength( unsigned int length )
{
	delete[] m_p_data;
	m_p_data = new sgObject_keyData[ length ];
	m_length = length;
}
sgObject_keyData& sgObject_keyDataArray::operator[]( unsigned int index ) const
{
	return m_p_data[index];
}



sgBDataCmd_key::sgBDataCmd_key()
{
	m_startExport = false;
	m_write = false;
	m_endExport = false;
	m_import = false;
}


sgBDataCmd_key::~sgBDataCmd_key()
{
}



void* sgBDataCmd_key::creator()
{
	return new sgBDataCmd_key();
}



MSyntax sgBDataCmd_key::newSyntax()
{
	MSyntax syntax;

	syntax.setObjectType( MSyntax::kSelectionList );
	syntax.useSelectionAsDefault( true );

	syntax.addFlag( "-se", "-startExport",  MSyntax::kBoolean );
	syntax.addFlag( "-w" , "-write",        MSyntax::kBoolean );
	syntax.addFlag( "-ee", "-endExport",    MSyntax::kBoolean );
	syntax.addFlag( "-im", "-import",       MSyntax::kBoolean );
	syntax.addFlag( "-fp", "-filePath",   MSyntax::kString  );
	syntax.addFlag( "-fdp", "-folderPath",   MSyntax::kString  );
	syntax.addFlag( "-ebm", "-exportByMatrix", MSyntax::kBoolean );
	syntax.addFlag( "-st", "-step", MSyntax::kBoolean );

	return syntax;
}



MStatus sgBDataCmd_key::doIt( const MArgList& argList )
{
	MStatus status;

	MArgDatabase argData( syntax(), argList, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	argData.getObjects( m_selList );
	
	argData.getFlagArgument( "se", 0, m_startExport );
	argData.getFlagArgument( "w" , 0, m_write );
	argData.getFlagArgument( "ee", 0, m_endExport );
	argData.getFlagArgument( "im", 0, m_import );
	argData.getFlagArgument( "fdp", 0, m_folderPath );
	argData.getFlagArgument( "fp", 0, m_filePath );
	argData.getFlagArgument( "st", 0, m_step );
	
	if( !m_selList.length() && m_startExport ){
		MGlobal::displayError( "Export 할 Target을 지정해야 합니다." );
	}

	if( !m_filePath.length() && m_import )
	{
		MGlobal::displayError( "Import 할 Path를 지정해야 합니다." );
	}
	else if( m_import )
	{
		readData( m_filePath );
	}

	if( m_startExport )
	{
		m_exportByMatrix = false;
		argData.getFlagArgument( "ebm", 0, m_exportByMatrix );
	}

	return redoIt();
}



MStatus sgBDataCmd_key::redoIt()
{
	MStatus status;

	if( m_startExport )
	{
		m_pathArrExport.clear();
		m_filePaths.clear();

		for( unsigned int i=0; i< m_selList.length(); i++ )
		{
			MDagPath dagPath;
			m_selList.getDagPath( i, dagPath );
			m_pathArrExport.append( dagPath );
		}

		if( m_folderPath == "" ){
			MGlobal::displayError( "Start export 시에는 Folder Path를 입력해야 합니다." );
			return MS::kFailure;
		}
		status = startExport( m_folderPath );
	}
	else if( m_endExport )
	{
		endExport();
	}
	else if( m_write )
	{
		writeData( m_exportByMatrix );
	}
	else if( m_import )
	{
		importData();
	}

	return MS::kSuccess;
}



MStatus sgBDataCmd_key::undoIt()
{
	MStatus status;

	if( m_import )
	{
		for( unsigned int i=0; i < m_oArrKeyAfter.length(); i++ )
			MGlobal::deleteNode( m_oArrKeyAfter[i] );
		m_dgMod_delete.undoIt();
		m_dgMod_connection.doIt();
	}

	return MS::kSuccess;
}



bool sgBDataCmd_key::isUndoable() const
{
	if( m_import ) return true;
	else return false;
}