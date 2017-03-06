#ifndef _matrixFromPolygon_h
#define _matrixFromPolygon_h

#include <maya/MPxNode.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MTypeId.h>

#include <maya/MDagPath.h>
#include <maya/MItMeshPolygon.h>

#include <maya/MPointArray.h>

#include <maya/MMatrix.h>

#include <maya/MGlobal.h>

class matrixFromPolygon : public MPxNode
{
public:
						matrixFromPolygon();
	virtual				~matrixFromPolygon(); 

	virtual MStatus		compute( const MPlug& plug, MDataBlock& data );

	static  void*		creator();
	static  MStatus		initialize();

public:

	static  MObject     aInputMesh;
	static  MObject     aInputMeshMatrix;

	static  MObject     aPolygonIndex;
	static  MObject     aU;
	static  MObject     aV;

	static  MObject		aOutputMatrix;

	static	MTypeId		id;
};

#endif
