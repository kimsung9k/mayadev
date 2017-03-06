#include "sgCurveEditBrush_manip.h"
#include <gl/GL.h>
#include <gl/GLU.h>

MTypeId sgCurveEditBrush_manip::id( 0x2015052900 );

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

		MDagPath dagPathCam;
		view.getCamera( dagPathCam );

		MPoint  camPos = dagPathCam.inclusiveMatrix()[3];
		MPoint nearClip;
		MPoint farClip;
		view.viewToWorld( m_mouseX, m_mouseY, nearClip, farClip );

		m_vMouseRay = nearClip - camPos;
		m_vMouseRay.normalize();
		m_vMouseRay *= 20;
		m_circlePos = m_vMouseRay + camPos;

		MVector vCamUp  = dagPathCam.inclusiveMatrix()[1];
		MVector vCross = m_vMouseRay ^ vCamUp;

		m_vMouseRay.normalize();
		vCamUp.normalize();
		vCross.normalize();
		
		float rad = 3.14159/180;
		float r = m_radiusCircle;
		if( r < 0 ) r = 0;

		view.beginGL();

		glPushAttrib( GL_CURRENT_BIT );

		MVector currentPoint;
		glColor3f( 1,0,0 );
		//glLineWidth( 3 );
		//glEnable( GL_LINE_SMOOTH );
		glBegin(GL_LINE_LOOP);
		for (int i=0; i<360; i++){
			float currentRad=i*rad;
			currentPoint = vCamUp * sin( currentRad )*r + vCross * cos( currentRad )*r + m_circlePos;
			glVertex3f( currentPoint.x, currentPoint.y, currentPoint.z );
		}
		//glLineWidth( 1 );
		//glEnable( GL_LINE_STIPPLE );
		glEnd();

		glPopAttrib();

		view.endGL();
}