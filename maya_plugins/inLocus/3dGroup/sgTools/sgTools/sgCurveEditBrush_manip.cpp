#include "sgCurveEditBrush_manip.h"
#include <gl/GL.h>
#include <gl/GLU.h>
#include "sgPrintf.h"
#include "sgCurveEditBrush_functions.h"

MTypeId sgCurveEditBrush_manip::id( (unsigned int)0x2015052900 );

sgCurveEditBrush_manip::sgCurveEditBrush_manip() 
{
	m_radiusCircle = 1.0;
	m_circlePos = MPoint( 0,0,0 );
}


sgCurveEditBrush_manip::~sgCurveEditBrush_manip() 
{
}


void *sgCurveEditBrush_manip::creator()
{
	return new sgCurveEditBrush_manip();
}


MStatus sgCurveEditBrush_manip::initialize()
{ 
    MStatus stat;
    stat = MPxManipContainer::initialize();
    return stat;
}


MStatus sgCurveEditBrush_manip::createChildren()
{
    MStatus stat = MStatus::kSuccess;
	finishAddingManips();

    return stat;
}


MStatus sgCurveEditBrush_manip::connectToDependNode(const MObject &node)
{
    MStatus stat;
    return stat;
}


void sgCurveEditBrush_manip::draw( M3dView & view, 
                                         const MDagPath & path, 
                                         M3dView::DisplayStyle style,
                                         M3dView::DisplayStatus status )
{
	if( !m_drawOn ) return;

	double rad = 3.14159/180;
	double r   = m_radiusCircle;
	if( r < 0 ) r = 0;

	view.beginGL();

	glPushAttrib( GL_CURRENT_BIT );

	MPoint currentPoint;
	glColor3f( 1,0,0 );
	//glLineWidth( 3 );
	//glEnable( GL_LINE_SMOOTH );
	glBegin(GL_LINE_LOOP);
	for (int i=0; i<360; i++){
		double currentRad=i*rad;
		currentPoint.x = sin(currentRad)*m_radiusCircle + m_mouseX;
		currentPoint.y = cos(currentRad)*m_radiusCircle + m_mouseY;
		currentPoint.z = -0.999;
		currentPoint.w = 1.0;
		currentPoint = getViewToWorldPoint(currentPoint);
		glVertex3f( (float)currentPoint.x, (float)currentPoint.y, (float)currentPoint.z );
	}
	//glLineWidth( 1 );
	//glEnable( GL_LINE_STIPPLE );
	glEnd();

	glPopAttrib();

	view.endGL();
}


MStatus sgCurveEditBrush_manip::dependsOn(MPlug const & plug1, MPlug const &plug2, bool &result) const
{
	return MS::kSuccess;
}