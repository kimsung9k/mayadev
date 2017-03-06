#include "sgBDataCmd.h"
#include "sgBDataCmd_mesh.h"


sgData_uv::sgData_uv(){}
sgData_uv::~sgData_uv(){}

sgData_uvArray::sgData_uvArray()
{
	m_p_data = new sgData_uv[ 0 ];
}
sgData_uvArray::~sgData_uvArray()
{
	delete[] m_p_data;
}
unsigned int sgData_uvArray::length() const
{
	return m_length;
}
void sgData_uvArray::setLength( unsigned int length )
{
	delete[] m_p_data;
	m_p_data = new sgData_uv[ length ];
	m_length = length;
}
sgData_uv& sgData_uvArray::operator[]( unsigned int index ) const
{
	return m_p_data[index];
}

sgData_mesh::sgData_mesh()
{
}
sgData_mesh::~sgData_mesh()
{
}


sgData_meshArray::sgData_meshArray()
{
	m_p_data = new sgData_mesh[ 0 ];
}
sgData_meshArray::~sgData_meshArray()
{
	delete[] m_p_data;
}
unsigned int sgData_meshArray::length() const
{
	return m_length;
}
void sgData_meshArray::setLength( unsigned int length )
{
	delete[] m_p_data;
	m_p_data = new sgData_mesh[ length ];
	m_length = length;
}
sgData_mesh& sgData_meshArray::operator[]( unsigned int index ) const
{
	return m_p_data[index];
}


MObjectArrayArray::MObjectArrayArray()
{
	m_p_data = new MObjectArray[ 0 ];
}
MObjectArrayArray::~MObjectArrayArray()
{
	delete[] m_p_data;
}
unsigned int MObjectArrayArray::length() const
{
	return m_length;
}
void MObjectArrayArray::setLength( unsigned int length )
{
	delete[] m_p_data;
	m_p_data = new MObjectArray[ length ];
	m_length = length;
}
MObjectArray& MObjectArrayArray::operator[]( unsigned int index ) const
{
	return m_p_data[index];
}


MSyntax sgBDataCmd_mesh::newSyntax()
{
	MSyntax syntax;

	syntax.setObjectType( MSyntax::kSelectionList );
	syntax.useSelectionAsDefault( true );

	syntax.addFlag( "-em",  "-exportMesh",  MSyntax::kBoolean );
	syntax.addFlag( "-im",  "-importMesh",  MSyntax::kBoolean );
	syntax.addFlag( "-ibm", "-importByMatrix",  MSyntax::kBoolean );

	syntax.addFlag( "-euv", "-exportUVs",   MSyntax::kBoolean );
	syntax.addFlag( "-iuv", "-importUVs",   MSyntax::kBoolean );
	
	syntax.addFlag( "-skp", "-skipByName",  MSyntax::kBoolean );
	syntax.addFlag( "-fp" , "-filePath",    MSyntax::kString  );

	return syntax;
}


sgBDataCmd_mesh::sgBDataCmd_mesh()
{
	m_filePath.clear();
	m_folderPath.clear();
	m_exportUVs = false;
	m_exportMesh = false;
	m_importUVs = false;
	m_importMesh = false;
	m_importByMatrix = false;
}


sgBDataCmd_mesh::~sgBDataCmd_mesh()
{
}


void* sgBDataCmd_mesh::creator()
{
	return new sgBDataCmd_mesh();
}



MStatus sgBDataCmd_mesh::doIt( const MArgList& argList )
{
	MStatus status;

	MArgDatabase argData( syntax(), argList, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	MSelectionList selList_targets;
	argData.getObjects( selList_targets );
	argData.getFlagArgument( "-fp" , 0, m_filePath );
	argData.getFlagArgument( "-im" , 0, m_importMesh );
	argData.getFlagArgument( "-iuv", 0, m_importUVs );
	argData.getFlagArgument( "-em" , 0, m_exportMesh );
	argData.getFlagArgument( "-euv", 0, m_exportUVs );
	argData.getFlagArgument( "-ibm", 0, m_importByMatrix );

	if( !m_filePath.length() ){
		MGlobal::displayError( "'-filePath' 를 입력해야 합니다." );
		return MS::kFailure;
	}
	
	unsigned int flag_targets = 0;
	if( m_exportMesh ) flag_targets++;
	if( m_importMesh ) flag_targets++;
	if( m_exportUVs )  flag_targets++;
	if( m_importUVs )  flag_targets++;

	if( flag_targets == 0 )
	{
		MGlobal::displayError( "Export, import 혹은 data 타입 하나를 지정해야 합니다." );
		return MS::kFailure;
	}
	else if( flag_targets > 1 )
	{
		MGlobal::displayError( "Export, import 혹은 data 타입을 하나만 지정해야 합니다." );
		return MS::kFailure;
	}

	if( m_exportMesh && m_filePath.length() )
	{
		MDagPath dagPath;
		selList_targets.getDagPath( 0, dagPath );
		status = getShapeNode( dagPath );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		
		sgData_mesh dataMesh;

		status = readMesh_fromMesh( dataMesh, dagPath );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		status = exportMesh_toFile( dataMesh, m_filePath );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}
	else if( m_exportUVs && m_filePath.length() )
	{
		MDagPath dagPath;
		selList_targets.getDagPath( 0, dagPath );
		status = getShapeNode( dagPath );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		sgData_uvArray dataUVs;

		status = readUVs_fromMesh( dataUVs, dagPath );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		status = exportUVs_toFile( dataUVs, m_filePath );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}
	else if( m_importMesh && m_filePath.length() )
	{
		status = readMesh_fromFile( m_dataMesh_import, m_filePath );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		return redoIt();
	}
	else if( m_importUVs && m_filePath.length() )
	{
		selList_targets.getDagPath( 0, m_dp_uvImportTarget );
		status = getShapeNode( m_dp_uvImportTarget );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		status = readUVs_fromFile( m_dataUVs_import, m_filePath );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		return redoIt();
	}

	return MS::kSuccess;
}



MStatus sgBDataCmd_mesh::redoIt()
{
	MStatus status;

	if( m_importMesh )
	{
		m_oArrTransformsImported.clear();
		status = importMesh_fromData( m_dataMesh_import, m_importByMatrix );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}
	else if( m_importUVs )
	{
		readUVs_fromMesh( m_dataUVs_original, m_dp_uvImportTarget );
		status = importUVs_fromData( m_dataUVs_import, m_dp_uvImportTarget );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}
	return MS::kSuccess;
}



MStatus sgBDataCmd_mesh::undoIt()
{
	MStatus status;

	if( m_importMesh )
	{
		if( !m_oMeshImported.isNull() )
		MGlobal::deleteNode( m_oMeshImported );

		if( m_oArrTransformsImported.length() )
		MGlobal::deleteNode( m_oArrTransformsImported[0] );
	}
	else if( m_importUVs )
	{
		status = importUVs_fromData( m_dataUVs_original, m_dp_uvImportTarget );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}
	return MS::kSuccess;
}



bool sgBDataCmd_mesh::isUndoable() const
{
	if( m_importMesh || m_importUVs )
		return true;
	else
		return false;
}