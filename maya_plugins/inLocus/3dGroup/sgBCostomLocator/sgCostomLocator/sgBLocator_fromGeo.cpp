#include "sgBLocator_fromGeo.h"


MTypeId  sgBLocator_fromGeo::id( 0x2015011500 );

MObject  sgBLocator_fromGeo::aOutputValue;
MObject  sgBLocator_fromGeo::aInputCurve;
MObject  sgBLocator_fromGeo::aLineWidth;

sgBLocator_fromGeo::sgBLocator_fromGeo()
{
	m_pointArr.setLength(6);

 	m_pointArr[0] = MFloatPoint(  1,  0, 0 );
	m_pointArr[1] = MFloatPoint( -1,  0, 0 );
	m_pointArr[2] = MFloatPoint(  0, -1, 0 );
	m_pointArr[3] = MFloatPoint(  0,  1, 0 );
	m_pointArr[4] = MFloatPoint(  0,  0, 1 );
	m_pointArr[5] = MFloatPoint(  0,  0, -1 );

	m_boundingBox.clear();
    m_boundingBox.expand( MVector( 1.0, 1.0, 1.0 ) );
    m_boundingBox.expand( MVector( -1.0, -1.0, -1.0 ) );

	m_colorActive =  MColor( 1.0f, 1.0f, 1.0f );
	m_colorLead   =	 MColor( .26f, 1.0f, .64f );
	m_colorDefault = MColor( 1.0f, 1.0f, 0.0f );

	m_lineWidth = 1;

	MFnDependencyNode fnNode( thisMObject() );
	MPlug plugOutput = fnNode.findPlug( aOutputValue );
	MPlug plugVis    =fnNode.findPlug( "v" );

	MDGModifier dgModifier;
	dgModifier.connect( plugOutput, plugVis );
}



sgBLocator_fromGeo::~sgBLocator_fromGeo()
{
}



void sgBLocator_fromGeo::postConstructor()
{
}



bool  sgBLocator_fromGeo::isBounded() const
{
	return true;
}



bool  sgBLocator_fromGeo::isTransparent() const
{
	return false;
}



MBoundingBox  sgBLocator_fromGeo::boundingBox() const
{
	return m_boundingBox;
}



void* sgBLocator_fromGeo::creator()
{
	return new sgBLocator_fromGeo();
}


MStatus sgBLocator_fromGeo::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	m_boundingBox.clear();
    m_boundingBox.expand( MVector( 1.0, 1.0, 1.0 ) );
    m_boundingBox.expand( MVector( -1.0, -1.0, -1.0 ) );

	m_pointArr.setLength(6);
 
 	m_pointArr[0] = MFloatPoint(  1,  0, 0 );
	m_pointArr[1] = MFloatPoint( -1,  0, 0 );
	m_pointArr[2] = MFloatPoint(  0, -1, 0 );
	m_pointArr[3] = MFloatPoint(  0,  1, 0 );
	m_pointArr[4] = MFloatPoint(  0,  0, 1 );
	m_pointArr[5] = MFloatPoint(  0,  0, -1 );

	m_lineWidth = data.inputValue( aLineWidth ).asInt();

	data.setClean( plug );

	return MS::kSuccess;
}



void sgBLocator_fromGeo::draw( M3dView& view, const MDagPath& dagPath, M3dView::DisplayStyle displayStyle, M3dView::DisplayStatus status )
{
	view.beginGL();

	glPushAttrib( GL_CURRENT_BIT );
    glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
    glDepthMask( GL_FALSE );

	glDisable ( GL_LIGHTING );

    if ( status == M3dView::kActive )
    {
        glColor3f( m_colorActive.r, m_colorActive.g, m_colorActive.b );
    }
    else if ( status == M3dView::kLead )
    {
        glColor3f( m_colorLead.r, m_colorLead.g, m_colorLead.b );
    }
    else
    {
		glColor3f( m_colorDefault.r, m_colorDefault.g, m_colorDefault.b );
    }
    
	glLineWidth( m_lineWidth );
	glBegin( GL_LINES );
    glVertex3f( m_pointArr[0].x, m_pointArr[0].y, m_pointArr[0].z );
	glVertex3f( m_pointArr[1].x, m_pointArr[1].y, m_pointArr[1].z );

    glVertex3f( m_pointArr[2].x, m_pointArr[2].y, m_pointArr[2].z );
	glVertex3f( m_pointArr[3].x, m_pointArr[3].y, m_pointArr[3].z );

    glVertex3f( m_pointArr[4].x, m_pointArr[4].y, m_pointArr[4].z );
	glVertex3f( m_pointArr[5].x, m_pointArr[5].y, m_pointArr[5].z );
    glEnd();

	glLineWidth( 1 );
	glDepthMask( GL_TRUE );
	glPopAttrib();
    view.endGL();
}



MStatus  sgBLocator_fromGeo::initialize()
{
	MStatus status;

	MFnNumericAttribute nAttr;
	MFnTypedAttribute   tAttr;

	aOutputValue    = nAttr.create( "outputValue", "outputValue", MFnNumericData::kInt, 1.0 );
	nAttr.setStorable( false );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aOutputValue ) );
	CHECK_MSTATUS_AND_RETURN_IT( status );


	aInputCurve = tAttr.create( "inputCurve", "inputCurve", MFnData::kNurbsCurve );
	tAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aInputCurve ) );


	aLineWidth = nAttr.create( "lineWidth", "lineWidth", MFnNumericData::kInt, 1 );
	nAttr.setMin( 1 );
	nAttr.setKeyable( true );
	nAttr.setStorable( true );
	CHECK_MSTATUS_AND_RETURN_IT( addAttribute( aLineWidth ) );

	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aInputCurve, aOutputValue ) );
	CHECK_MSTATUS_AND_RETURN_IT( attributeAffects( aLineWidth,  aOutputValue ) );


	return MS::kSuccess;
}