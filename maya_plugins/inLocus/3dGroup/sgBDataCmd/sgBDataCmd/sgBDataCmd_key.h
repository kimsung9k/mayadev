#ifndef _sgDataCmd_key_h
#define _sgDataCmd_key_h


#include <maya/MObject.h>
#include <maya/MGlobal.h>
#include <maya/MIntArray.h>
#include <maya/MItDag.h>
#include <maya/MVector.h>
#include <maya/MPoint.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MFnDagNode.h>
#include <maya/MFloatArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MFnTransform.h>
#include <maya/MFnSet.h>
#include <maya/MFnAttribute.h>

#include <maya/MStringArray.h>
#include <maya/MTimeArray.h>
#include <maya/MObjectArray.h>
#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>

#include <fstream>

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>

#include <maya/MSyntax.h>
#include <maya/MArgDatabase.h>
#include <maya/MSelectionList.h>
#include <maya/MPxCommand.h>

#include <maya/MAnimControl.h>

#include <maya/MDGModifier.h>


struct sgObject_keyData
{
	unsigned int unit;

	MObject      oTargetNode;
	unsigned int numAttr;
	MStringArray namesAttribute;
	unsigned int lengthTime;
	MDoubleArray dArrTime;
	MDoubleArray dArrValuesArray;
};


class sgObject_keyDataArray
{
public:
	sgObject_keyDataArray();
	~sgObject_keyDataArray();

	void setLength( unsigned int length );
	unsigned int length() const;
	sgObject_keyData& operator[]( unsigned int index ) const;

private:
	unsigned int m_length;
	sgObject_keyData* m_p_data;
};


class sgBDataCmd_key : public MPxCommand
{
public:
	sgBDataCmd_key();
	virtual ~sgBDataCmd_key();

	static void*   creator();
	static MSyntax newSyntax();

	MStatus doIt( const MArgList& argList );
	MStatus redoIt();
	MStatus undoIt();
	bool    isUndoable() const;

	MStatus startExport( MString pathFolder );
	MStatus writeData( bool exportByMatrix );
	void endExport();

	MStatus setObjectKeyDataDefault( sgObject_keyData& objectKeyData, const MDagPath& dagPathTarget, bool bMatrixType );

	MStatus readData( MString nameFilePath );
	MStatus importData();

	
	void getKeyableAttribute( const MDagPath& pathTransform, sgObject_keyData& attrList );

private:
	MSelectionList  m_selList;

	bool m_startExport;
	bool m_write;
	bool m_endExport;
	bool m_import;
	bool m_step;

	MString  m_folderPath;
	MString  m_filePath;

	sgObject_keyData  m_objectKeyDataImport;

	MObjectArray m_oArrKeyAfter;

	MDGModifier  m_dgMod_connection, m_dgMod_delete;

public:
	static  bool             m_exportByMatrix;
	static  MDagPathArray    m_pathArrExport;
	static  MStringArray     m_filePaths;
	static  sgObject_keyDataArray   m_objectKeyDatasExport;
};


#endif