#ifndef _sgMeshData_h
#define _sgMeshData_h

#include <maya/MObject.h>
#include <maya/MGlobal.h>
#include <maya/MIntArray.h>
#include <maya/MItDag.h>
#include <maya/MVector.h>
#include <maya/MVector.h>
#include <maya/MPoint.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDagPath.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnMesh.h>
#include <maya/MDagPathArray.h>
#include <maya/MFloatArray.h>
#include <maya/MFloatPointArray.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MFnTransform.h>
#include <maya/MFnSet.h>
#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>

#include <maya/MStringArray.h>

#include <fstream>

#include <maya/MSyntax.h>
#include <maya/MArgList.h>
#include <maya/MArgDatabase.h>
#include <maya/MSelectionList.h>
#include <maya/MPxCommand.h>
#include <maya/MTransformationMatrix.h>



class sgData_uv
{
public:
	sgData_uv();
	~sgData_uv();

	MString  name_set;
	MFloatArray uArray, vArray;
	MIntArray   uvCounts, uvIds;
};


class sgData_uvArray
{
public:
	sgData_uvArray();
	~sgData_uvArray();

	void setLength( unsigned int length );
	unsigned int length() const;
	sgData_uv& operator[]( unsigned int index ) const;

private:
	unsigned int m_length;
	sgData_uv* m_p_data;
};


class sgData_mesh
{
public:
	sgData_mesh();
	~sgData_mesh();

	MString      nameMesh;

	MObjectArray oArr_created;

	unsigned int length_trs;
	MStringArray names_tr;
	MIntArray    rotateOders_tr;
	MMatrixArray matrixs_tr;
	MVectorArray translates_tr;
	MVectorArray rotates_tr;
	MVectorArray scales_tr;
	MVectorArray shears_tr;
	MVectorArray rotatePivs_tr;
	MVectorArray rotatePivTranslates_tr;
	MVectorArray scalePivs_tr;
	MVectorArray scalePivTranslates_tr;
	MIntArray    visibilitys_tr;

	MFloatPointArray  points;
	MIntArray         polyCounts;
	MIntArray         polyConnects;

	sgData_uvArray uvs;
};


class MObjectArrayArray
{
public:
	MObjectArrayArray();
	~MObjectArrayArray();

	void setLength( unsigned int length );
	unsigned int length() const;
	MObjectArray& operator[]( unsigned int index ) const;

private:
	unsigned int m_length;
	MObjectArray* m_p_data;
};


void writeDataMesh( const sgData_mesh& dataMesh, std::ofstream& outFile );
void writeDataUV( const sgData_uv& dataUv, std::ofstream& outFile );
void writeDataUVs( const sgData_uvArray& dataUvs, std::ofstream& outFile );

void readDataMesh( sgData_mesh& dataMesh, std::ifstream& inFile );
void readDataUV( sgData_uv& dataUv, std::ifstream& inFile );
void readDataUVs( sgData_uvArray& dataUvs, std::ifstream& inFile );

void setPositionByData( MObject& oTarget, sgData_mesh& dataMesh, 
	unsigned int indexTarget, bool b_importByMatrix );


MString getLocalName( const MString& fullPathName );


class sgData_meshArray
{
public:
	sgData_meshArray();
	~sgData_meshArray();

	void setLength( unsigned int length );
	unsigned int length() const;
	sgData_mesh& operator[]( unsigned int index ) const;

private:
	unsigned int m_length;
	sgData_mesh* m_p_data;
};



class sgBDataCmd_mesh : public MPxCommand
{
public:
	sgBDataCmd_mesh();
	virtual ~sgBDataCmd_mesh();

	static void* creator();
	static MSyntax newSyntax();

	MStatus doIt( const MArgList& argList );
	MStatus redoIt();
	MStatus undoIt();
	bool    isUndoable() const;

	MStatus readMesh_fromMesh( sgData_mesh& dataMesh, const MDagPath& dagPath_mesh );
	MStatus readUVs_fromMesh( sgData_uvArray& dataUVs, const MDagPath& dagPath_mesh  );

	MStatus readMesh_fromFile( sgData_mesh& dataMesh, MString str_filePath );
	MStatus readUVs_fromFile(  sgData_uvArray& dataUVs, MString str_filePath );

	MStatus exportMesh_toFile( const sgData_mesh& dataMesh,  MString str_filePath );
	MStatus exportUVs_toFile(  const sgData_uvArray& dataUVs, MString str_filePath );

	MStatus importMesh_fromData( const sgData_mesh& dataMesh, bool importByMatrix=false );
	MStatus importUVs_fromData( const sgData_uvArray& dataUVs, MDagPath& dagPath_mesh );

private:
	MString m_filePath;
	MString m_folderPath;
	bool    m_exportMesh;
	bool    m_importMesh;
	bool    m_exportUVs;
	bool    m_importUVs;
	bool    m_importByMatrix;

	sgData_mesh     m_dataMesh_import;
	MObjectArray    m_oArrTransformsImported;
	MObject         m_oMeshImported;

	sgData_uvArray  m_dataUVs_import;
	sgData_uvArray  m_dataUVs_original;
	MDagPath        m_dp_uvImportTarget;
};


#endif