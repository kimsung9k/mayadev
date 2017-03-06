#include "sgGetMeshElementInfo.h"
#include <Windows.h>

sgBuildMeshData_array   sgGetMeshElementInfo::m_buildMeshDatas;

sgGetMeshElementInfo::sgGetMeshElementInfo()
{
}

sgGetMeshElementInfo::~sgGetMeshElementInfo()
{
}


void* sgGetMeshElementInfo::creator()
{
	return new sgGetMeshElementInfo();
}


MSyntax sgGetMeshElementInfo::newSyntax()
{
	MSyntax syntax;

	syntax.setObjectType( MSyntax::kSelectionList );
	syntax.useSelectionAsDefault( true );

	syntax.addFlag( "-set", "-setTargets", MSyntax::kBoolean );
	syntax.addFlag( "-ne",  "-numElement", MSyntax::kBoolean );
	syntax.addFlag( "-nv",  "-numVertcies", MSyntax::kBoolean );
	syntax.addFlag( "-np",  "-numPolygons", MSyntax::kBoolean );
	syntax.addFlag( "-fi",  "-faceIndices", MSyntax::kBoolean );
	syntax.addFlag( "-bbc", "-boundingBoxCenter", MSyntax::kBoolean );

	syntax.enableEdit( false );
	syntax.enableQuery( false );

	return syntax;
}



MStatus sgGetMeshElementInfo::doIt( const MArgList& argList )
{
	MStatus status;

	MArgDatabase argData( syntax(), argList, &status );
	CHECK_MSTATUS_AND_RETURN_IT( status );

	argData.getObjects( m_selList );

	bool resultSet=0;
	bool resultNumElement=0;
	bool resultNumVertices=0;
	bool resultNumPolygons=0;
	bool resultFaceIndices=0;
	bool resultBoundingBox=0;
	argData.getFlagArgument( "-set", 0, resultSet );
	argData.getFlagArgument( "-ne" , 0, resultNumElement );
	argData.getFlagArgument( "-nv" , 0, resultNumVertices );
	argData.getFlagArgument( "-np" , 0, resultNumPolygons );
	argData.getFlagArgument( "-fi" , 0, resultFaceIndices );
	argData.getFlagArgument( "-bbc", 0, resultBoundingBox );

	MIntArray intArrResult;
	MDoubleArray dArrResult;
	if( resultSet )
	{
		getInfomationFromSelection();
	}
	else if( resultNumElement )
	{
		setResult( m_buildMeshDatas.length() );
	}
	else if( resultNumVertices )
	{
		for( int j=0; j< m_buildMeshDatas.length(); j++ )
		{
			intArrResult.append( m_buildMeshDatas[j].m_numVertices );
		}
		setResult( intArrResult );
	}
	else if( resultNumPolygons )
	{
		for( int j=0; j< m_buildMeshDatas.length(); j++ )
		{
			intArrResult.append( m_buildMeshDatas[j].m_numPolygons );
		}
		setResult( intArrResult );
	}
	else if( resultFaceIndices )
	{
		for( int j=0; j< m_buildMeshDatas.length(); j++ )
		{
			MIntArray faceIndices = m_buildMeshDatas[j].m_originalFaceIndices;
			//cout << "len faces : " << faceIndices.length() << endl;
			for( int k=0; k< faceIndices.length(); k++ )
			{
				intArrResult.append( faceIndices[k] );
			}
		}
		setResult( intArrResult );
	}
	else if( resultBoundingBox )
	{
		for( int j=0; j< m_buildMeshDatas.length(); j++ )
		{
			MBoundingBox bb;
			MPointArray& points = m_buildMeshDatas[j].m_points;
			for( int k=0; k< points.length(); k++ )
			{
				bb.expand( points[k] );
			}
			MVector vBBCenter = bb.center();
			dArrResult.append( vBBCenter.x );
			dArrResult.append( vBBCenter.y );
			dArrResult.append( vBBCenter.z );
		}
		setResult( dArrResult );
	}

	return MS::kSuccess;
}



MStatus sgGetMeshElementInfo::redoIt()
{
	MStatus status;
	return MS::kSuccess;
}



MStatus sgGetMeshElementInfo::undoIt()
{
	MStatus status;
	return MS::kSuccess;
}



bool sgGetMeshElementInfo::isUndoable() const
{
	return false;

}