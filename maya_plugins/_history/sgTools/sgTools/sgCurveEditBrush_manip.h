#ifndef _sgCurveEditBrush_manip_h
#define _sgCurveEditBrush_manip_h

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

// Manipulators
#include <maya/MFnFreePointTriadManip.h>
#include <maya/MFnDistanceManip.h>


class sgCurveEditBrush_manip : public MPxManipContainer
{
public:
        sgCurveEditBrush_manip();
        virtual ~sgCurveEditBrush_manip();
        
        static void * creator();
        static MStatus initialize();
        virtual MStatus createChildren();
        virtual MStatus connectToDependNode(const MObject &node);

        virtual void draw(M3dView &view, 
                                          const MDagPath &path, 
                                          M3dView::DisplayStyle style,
                                          M3dView::DisplayStatus status);
		
        MDagPath m_distManip;

		void setCirclePoint( const MPoint& inputPoint );

public:
        static MTypeId id;
		float  m_radiusCircle;
		MPoint m_circlePos;
		MVector m_vMouseRay;
		bool   m_drawOn;
		int m_mouseX, m_mouseY;
};

#endif