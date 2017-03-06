#ifndef _sgPolyUnit_h
#define _sgPolyUnit_h


#include <maya/MPxNode.h>
#include <maya/MGlobal.h>
#include <maya/MObject.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MTypeId.h>
#include <maya/MStatus.h>
#include <maya/MSyntax.h>
#include <maya/MPlugArray.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnCompoundAttribute.h>

#include <maya/MFloatArray.h>
#include <maya/MPointArray.h>
#include <maya/MFloatPointArray.h>
#include <maya/MMatrixArray.h>

#include <maya/MFnMesh.h>
#include <maya/MFnMeshData.h>

#include "sgBuildMeshData.h"



class sgPolyUnit: public MPxNode
{
public:
	sgPolyUnit();
	virtual ~sgPolyUnit();

	virtual MStatus compute( const MPlug& plug, MDataBlock& data );
	virtual MStatus setDependentsDirty( const MPlug& plug, MPlugArray& plugArr );

	static  void* creator();
	static  MStatus initialize();

	MStatus check_and_buildMeshData( MDataBlock& data );

	static  MTypeId id;

	static  MObject  aInputMeshs;
	static  MObject  aOutputMesh;

private:

	bool m_isDirty_inputMeshs;
	bool m_rebuildMeshData;

	MObjectArray   m_oArr_inputMesh;
	MMatrixArray   m_mtxArr_inputMesh;
	MIntArray      m_intArr_numVertices;
	MIntArray      m_intArr_numPolygons;

	sgBuildMeshData  m_sgBuildMeshData;
};


#endif