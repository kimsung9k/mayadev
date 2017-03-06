#ifndef _meshShapeLocator_h
#define _meshShapeLocator_h

#include <maya/MPxLocatorNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnMatrixAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnCompoundAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MMatrixArray.h>
#include <maya/MVectorArray.h>
#include <maya/MPointArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MColorArray.h>
#include <maya/MFnMesh.h>
#include <maya/MObjectArray.h>

class meshShapeLocator : public MPxLocatorNode
{
public:
			       meshShapeLocator();
	virtual void   postConstructor();
	virtual        ~meshShapeLocator();

	virtual MStatus  compute( const MPlug& plug, MDataBlock& data );

	virtual void     draw( M3dView&, const MDagPath&, M3dView::DisplayStyle, M3dView::DisplayStatus );
	virtual bool     isBounded() const;
	virtual bool     isTransparent() const;
	virtual MBoundingBox  boundingBox() const;

	bool drawPolygon( int index, float alphaMult );
	void getPolygonPoints( MFnMesh& indexMesh );

	static  void*    creator();
	static  MStatus  initialize();

public:

	static  MObject  aShapes;
		static  MObject  aOffsetMatrix;
		static  MObject  aLocalObject;
		static  MObject  aInputMesh;
		static  MObject  aMeshSize;
		static  MObject  aActiveColor;
		static  MObject  aLeadColor;
		static  MObject  aDefaultColor;
		static  MObject  aLineOff;
		static  MObject  aFillAlpha;
		static  MObject  aLineAlpha;
		static  MObject  aOverRate;

	static  MObject aOutput;

	static  MTypeId  id;

public:
	static  short  viewMode;

	MMatrix  inverseMatrix;

	int inputNum;
	MMatrixArray offsetMatrix;
	MIntArray    localObject;
	MObjectArray inputMeshObj;
	MFloatArray meshSize;
	MColorArray activeColor;
	MColorArray leadColor;
	MColorArray defaultColor;
	MFloatArray fillAlpha;
	MFloatArray lineAlpha;
	MFloatArray overRate;
	MIntArray   lineOff;

	MPointArray* polygonPoints;

	int polygonNum;

	MBoundingBox  BBox;
};

#endif