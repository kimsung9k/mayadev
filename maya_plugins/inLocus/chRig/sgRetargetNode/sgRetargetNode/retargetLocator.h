#ifndef _retargetLocator_h
#define _retargetLocator_h

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
#include <maya/MAngle.h>

class retargetLocator : public MPxLocatorNode
{
public:
			       retargetLocator();
	virtual void   postConstructor();
	virtual        ~retargetLocator();

	virtual MStatus  compute( const MPlug& plug, MDataBlock& data );

	virtual void     draw( M3dView&, const MDagPath&, M3dView::DisplayStyle, M3dView::DisplayStatus );
	virtual bool     isBounded() const;
	virtual bool     isTransparent() const;
	virtual MBoundingBox  boundingBox() const;

	void drawDisc( const MPointArray& radPoints );
	void drawDiscAll(float lineAlpha, float fillAlpha );
	bool drawArrowPolygon( MMatrix aimMatrix, MColor cuColor, float fillAlpha, float lineAlpha, int index );
	void drawArrowAimLine( MVector aimVector, int index );
	void drawArrowAll( float lineAlpha, float fillAlpha, int index );
	void getValueFromAttribute( void );
	void getRadPoints( MPointArray& radPoints );
	MPointArray* getPolygonPoints( MFnMesh& indexMesh );
	MMatrix getAimMatrix( MMatrix inputAimMatrix );

	static  void*    creator();
	static  MStatus  initialize();

public:

	static  MObject  aDiscMatrix;
	static  MObject  aDiscAxis;
	static  MObject  aDiscAngle;
	static  MObject  aDiscDivision;
	static  MObject  aDiscOffset;
		static  MObject  aDiscOffsetX;
		static  MObject  aDiscOffsetY;
		static  MObject  aDiscOffsetZ;
	static  MObject  aDiscSize;
		static  MObject  aDiscSizeX;
		static  MObject  aDiscSizeY;
		static  MObject  aDiscSizeZ;
	static  MObject  aDiscActiveColor;
	static  MObject  aDiscLeadColor;
	static  MObject  aDiscDefaultColor;
	static  MObject  aDiscFillAlpha;
	static  MObject  aDiscLineAlpha;

	static  MObject  aArrow;
		static  MObject  aInheritMatrix;
		static  MObject  aAimMatrix;
		static  MObject  aInputMesh;
		static  MObject  aStartSize;
		static  MObject  aSize;
		static  MObject  aActiveColor;
		static  MObject  aLeadColor;
		static  MObject  aDefaultColor;
		static  MObject  aFillAlpha;
		static  MObject  aLineAlpha;
		static  MObject  aOffset;
			static  MObject  aOffsetX;
			static  MObject  aOffsetY;
			static  MObject  aOffsetZ;

	static  MObject aOutput;

	static  MTypeId  id;

public:

	short viewMode;

	int discAxis;
	int discDivision;
	double discAngle;
	MVector discSize;
	MVector discOffset;
	MColor discActiveColor;
	MColor discLeadColor;
	MColor discDefaultColor;
	float  discFillAlpha;
	float  discLineAlpha;

	int arrowNum;
	MIntArray inheritMatrix;
	MMatrixArray aimMatrix;
	MObjectArray inputMeshObj;
	MColorArray activeColor;
	MColorArray leadColor;
	MColorArray defaultColor;
	int polygonNum;
	MFloatArray startSize;
	MFloatArray size;
	MFloatArray fillAlpha;
	MFloatArray lineAlpha;
	MVectorArray offset;

	MBoundingBox bbox;
};

#endif