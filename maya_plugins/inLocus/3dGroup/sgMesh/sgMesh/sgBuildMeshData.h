#ifndef _sgBuildMeshData_h
#define _sgBuildMeshData_h

#include <maya/MObject.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MStatus.h>

#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MPointArray.h>
#include <maya/MFloatPointArray.h>
#include <maya/MMatrixArray.h>

#include <maya/MFnMesh.h>
#include <maya/MFnMeshData.h>

#include <vector>

using namespace std;


class sgBuildMeshData
{
public:
	sgBuildMeshData();
	~sgBuildMeshData();

	void clear();

	void appendMeshData( const MObject& oMesh, MMatrix mtxMesh );
	void appendMeshData( const sgBuildMeshData& meshData );
	void getPositon( MObject oMesh, MMatrix mtxMesh, int startIndex );
	void setPosition();
	void operator=( const sgBuildMeshData& meshData );

	MStatus build();

	int m_inputMeshIndex;

	MObject m_oMesh;

	unsigned int m_numVertices;
	unsigned int m_numPolygons;
	MPointArray  m_points;
	MIntArray    m_vertexCount;
	MIntArray    m_vertexList;
	MPointArray* m_pOriginalPoints;
	MIntArray    m_originalVerticesIndices;
	MIntArray    m_originalFaceIndices;

	MIntArray    m_appendedIndices;

	MString      m_mapName;
	MFloatArray  m_uArray;
	MFloatArray  m_vArray;
	MIntArray    m_uvCount;
	MIntArray    m_uvIds;
};



class sgBuildMeshData_array
{
public:
	sgBuildMeshData_array();
	~sgBuildMeshData_array();

	unsigned int length();
	void clear();
	void setLength( unsigned int length );
	void append( const sgBuildMeshData& meshData );
	sgBuildMeshData& operator[]( unsigned int index ) const;
	void operator=( const sgBuildMeshData_array& meshData_array );

	unsigned int m_length;
	sgBuildMeshData* m_pSgBuildMeshData;
};



class sgPolygonPerVertex
{
public:
	sgPolygonPerVertex();
	~sgPolygonPerVertex();

	MIntArray m_IndicesPolygon;
};



class sgPolygonPerVertex_array
{
public:
	sgPolygonPerVertex_array();
	~sgPolygonPerVertex_array();

	void clear();
	
	void setLength( unsigned int length );

	unsigned int length();

	sgPolygonPerVertex& operator[]( unsigned int index ) const;

private:
	unsigned int m_length;
	sgPolygonPerVertex* m_pPolygonPerVertex;
};


#endif