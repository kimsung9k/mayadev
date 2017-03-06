#ifndef _SGManip_h
#define _SGManip_h

#include "SGBase.h"
#include <maya/MIOStream.h>
#include <stdio.h>
#include <stdlib.h>

#include <maya/MFn.h>
#include <maya/MPxNode.h>
#include <maya/MPxManipContainer.h>
#include <maya/MPxSelectionContext.h>
#include <maya/MPxContextCommand.h>
#include <maya/MModelMessage.h>
#include <maya/MGlobal.h>
#include <maya/MItSelectionList.h>
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MDagPath.h>
#include <maya/MManipData.h>
#include <maya/MCursor.h>
#include <maya/MColor.h>

// Manipulators
#include <maya/MFnFreePointTriadManip.h>
#include <maya/MFnDistanceManip.h>

#include <maya/MHardwareRenderer.h>
#include <maya/MGLFunctionTable.h>

#include <maya/MPointArray.h>

#include "SGShape.h"



#define MANIPLENGTH 4



struct SGVec4 {
	float x, y, z, w;
};



struct SGVec4Color {
	float r, g, b, a;
};



struct vtxManipStruct {
	SGVec4 point;
	SGVec4Color color;
	short pointSise;
	bool depthTest;
};



struct edgeManipStruct {
	SGVec4* points;
	int numPoint;
	SGVec4Color color;
	GLushort pattern;
	short lineWidth;
	bool depthTest;
};



struct polyManipStruct {
	SGVec4* points;
	int numPoint;
	SGVec4Color color;
	GLushort pattern;
	short lineWidth;
	bool depthTest;
};



struct shapeManipStruct {
	float* points;
	unsigned int*   elements;
	int numPolygon;
	int interval;
	SGVec4Color color;
	float matrix[16];
	bool depthTest;
};



struct curveManipStruct {
	float* points;
	unsigned int numPoints;
	SGVec4Color color;
	float matrix[16];
	bool depthTest;
};



class SGManip : public MPxManipContainer
{
public:
	enum ManipIndex
	{
		kManipDefault,
		kManipSpplit,
		kManipVtxNormal
	};

	SGManip();
	virtual ~SGManip();

	static  void *  creator();
	static  MStatus initialize();

	void draw(M3dView& view, const MDagPath& dagPath, M3dView::DisplayStyle style, M3dView::DisplayStatus status);

	MGLFunctionTable *gGLFT;
	MHardwareRenderer *rend;


	static vector<vtxManipStruct>   vtxs[MANIPLENGTH];
	static vector<edgeManipStruct>  edges[MANIPLENGTH];
	static vector<polyManipStruct>  polygons[MANIPLENGTH];
	static vector<shapeManipStruct> shapes[MANIPLENGTH];
	static vector<curveManipStruct> curves[MANIPLENGTH];

	void clearManip(int index);
	void clearAll();
	void pushPoint(int index, MPoint point, MColor color = MColor(1, 1, 1, 1), short pointSize = 3 );
	void pushLine(int index, const MPointArray& points, MColor color = MColor(1, 1, 1, 1), short lineWidth = 1, GLushort* stiple = NULL);
	void pushPolygon(int index, const MPointArray& points, MColor color = MColor(1, 1, 1, 1), short lineWidth = 1, GLushort* stiple = NULL);
	void pushShape(int index, const SGShape& shape, MMatrix mtx, MColor color = MColor(1, 1, 1, 1));
	void pushCurve(int index, float* pointList, unsigned int numPoints, MMatrix mtx, MColor color);

	virtual MStatus createChildren();
	MStatus connectToDependNode( const MObject& oNode);

	MDagPath transManip;

	static MTypeId id;
};

#endif