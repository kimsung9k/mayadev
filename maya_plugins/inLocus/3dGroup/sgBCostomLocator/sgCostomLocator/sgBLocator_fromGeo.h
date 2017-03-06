#ifndef sgBLocator_fromGeo_h
#define sgBLocator_fromGeo_h


#include <maya/MPoint.h>
#include <maya/MFloatPoint.h>
#include <maya/MFloatPointArray.h>
#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/M3dView.h>
#include <maya/MHardwareRenderer.h>
#include <maya/MGLFunctionTable.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include <maya/MPointArray.h>

#include <maya/MDagPath.h>
#include <maya/MPxLocatorNode.h>

#include <maya/MDGModifier.h>

#include <maya/MTypeId.h>


class sgBLocator_fromGeo : public MPxLocatorNode
{
public:
	sgBLocator_fromGeo();
	virtual void postConstructor();
	virtual      ~sgBLocator_fromGeo();

	virtual MStatus  compute( const MPlug& plug, MDataBlock& data );
	virtual void     draw( M3dView& view, const MDagPath& dagPath, M3dView::DisplayStyle, M3dView::DisplayStatus );
	virtual bool     isBounded() const;
	virtual bool     isTransparent() const;
	virtual MBoundingBox boundingBox() const;

	static void* creator();
	static MStatus initialize();

	static  MObject  aOutputValue;
	static  MObject  aInputCurve;
	static  MObject  aLineWidth;

	static  MTypeId  id;


private:
	MBoundingBox m_boundingBox;
	float          m_lineWidth;
	MFloatPointArray  m_pointArr;
	MColor       m_colorActive;
	MColor       m_colorLead;
	MColor       m_colorDefault;

};

#endif