#include "retargetLocator.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MFloatPointArray.h>
#include <maya/MPointArray.h>
#include <maya/MDagPath.h>
#include <maya/MAngle.h>

#include <maya/MFnDependencyNode.h>

#include <maya/MVector.h> 
#include <maya/MPoint.h> 
#include <maya/MMatrix.h> 
#include <maya/MFnMatrixData.h>

#include <maya/MGlobal.h>

MTypeId  retargetLocator::id( 0xc8d201 );

MObject  retargetLocator::aDiscMatrix;
MObject  retargetLocator::aDiscAxis;
MObject  retargetLocator::aDiscAngle;
MObject  retargetLocator::aDiscDivision;
MObject  retargetLocator::aDiscOffset;
	MObject  retargetLocator::aDiscOffsetX;
	MObject  retargetLocator::aDiscOffsetY;
	MObject  retargetLocator::aDiscOffsetZ;
MObject  retargetLocator::aDiscSize;
	MObject  retargetLocator::aDiscSizeX;
	MObject  retargetLocator::aDiscSizeY;
	MObject  retargetLocator::aDiscSizeZ;
MObject  retargetLocator::aDiscActiveColor;
MObject  retargetLocator::aDiscLeadColor;
MObject  retargetLocator::aDiscDefaultColor;
MObject  retargetLocator::aDiscFillAlpha;
MObject  retargetLocator::aDiscLineAlpha;


MObject  retargetLocator::aArrow;
	MObject  retargetLocator::aInheritMatrix;
	MObject  retargetLocator::aAimMatrix;
	MObject  retargetLocator::aInputMesh;
	MObject  retargetLocator::aStartSize;
	MObject  retargetLocator::aSize;
	MObject  retargetLocator::aActiveColor;
	MObject  retargetLocator::aLeadColor;
	MObject  retargetLocator::aDefaultColor;
	MObject  retargetLocator::aFillAlpha;
	MObject  retargetLocator::aLineAlpha;
	MObject  retargetLocator::aOffset;
		MObject  retargetLocator::aOffsetX;
		MObject  retargetLocator::aOffsetY;
		MObject  retargetLocator::aOffsetZ;

MObject  retargetLocator::aOutput;
/*
short retargetLocator::viewMode;

int retargetLocator::discAxis;
int retargetLocator::discDivision;
float retargetLocator::discAngle;
MVector retargetLocator::discSize;
MVector retargetLocator::discOffset;
MColor retargetLocator::discActiveColor;
MColor retargetLocator::discLeadColor;
MColor retargetLocator::discDefaultColor;

MMatrix retargetLocator::thisWorldMatrixInverse;

int retargetLocator::arrowNum;
MIntArray retargetLocator::inheritMatrix;
MMatrixArray retargetLocator::aimMatrix;
MObjectArray retargetLocator::inputMeshObj;
MColorArray retargetLocator::activeColor;
MColorArray retargetLocator::leadColor;
MColorArray retargetLocator::defaultColor;
int retargetLocator::polygonNum;
MIntArray retargetLocator::lineOff;
MFloatArray retargetLocator::size;

MBoundingBox retargetLocator::bbox;
*/

MMatrix retargetLocator::getAimMatrix( MMatrix inputAimMatrix )
{
	MVector aimVector( inputAimMatrix(3,0), inputAimMatrix(3,1), inputAimMatrix(3,2) );
	aimVector -= discOffset;

	MVector upVector( -aimVector.y - aimVector.z, aimVector.x, aimVector.x );
	MVector otherVector = aimVector^upVector;
	upVector = otherVector^aimVector;

	MVector normalizeAim = aimVector.normal();
	upVector.normalize();
	otherVector.normalize();

	aimVector += discOffset;
	double buildMatrix[4][4] = { normalizeAim.x, normalizeAim.y, normalizeAim.z, 0,
	                             upVector.x,  upVector.y,  upVector.z,  0,
	                             otherVector.x, otherVector.y, otherVector.z, 0,
								 aimVector.x, aimVector.y, aimVector.z, 1 };
	return MMatrix( buildMatrix );
}


MStatus  retargetLocator::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MDataHandle hDiscMatrix = data.inputValue( aDiscMatrix );
	MDataHandle hDiscAxis = data.inputValue( aDiscAxis );
	MDataHandle hDiscAngle = data.inputValue( aDiscAngle );
	MDataHandle hDiscDivision = data.inputValue( aDiscDivision );
	MDataHandle hDiscOffset = data.inputValue( aDiscOffset );
	MDataHandle hDiscSize = data.inputValue( aDiscSize );
	MDataHandle hDiscActiveColor = data.inputValue( aDiscActiveColor );
	MDataHandle hDiscLeadColor = data.inputValue( aDiscLeadColor );
	MDataHandle hDiscDefaultColor = data.inputValue( aDiscDefaultColor );
	MDataHandle hDiscFillAlpha = data.inputValue( aDiscFillAlpha );
	MDataHandle hDiscLineAlpha = data.inputValue( aDiscLineAlpha );

	discAxis = hDiscAxis.asInt();
	discDivision = hDiscDivision.asInt();
	discAngle = hDiscAngle.asDouble();
	discSize = hDiscSize.asVector();
	discOffset = hDiscOffset.asVector();
	discActiveColor = hDiscActiveColor.asFloat3();
	discLeadColor = hDiscLeadColor.asFloat3();
	discDefaultColor = hDiscDefaultColor.asFloat3();
	discFillAlpha = hDiscFillAlpha.asFloat();
	discLineAlpha = hDiscLineAlpha.asFloat();

	MArrayDataHandle hArrArrow = data.inputArrayValue( aArrow );
	arrowNum = hArrArrow.elementCount();

	inheritMatrix.setLength( arrowNum );
	aimMatrix.setLength( arrowNum );
	inputMeshObj.setLength( arrowNum );
	startSize.setLength( arrowNum );
	size.setLength( arrowNum );
	activeColor.setLength( arrowNum );
	leadColor.setLength( arrowNum );
	defaultColor.setLength( arrowNum );
	fillAlpha.setLength( arrowNum );
	lineAlpha.setLength( arrowNum );
	offset.setLength( arrowNum );

	for( int i =0; i < arrowNum; i++ )
	{
		MDataHandle hArrow = hArrArrow.inputValue();

		MDataHandle hInheritMatrix = hArrow.child( aInheritMatrix );
		MDataHandle hAimMatrix = hArrow.child( aAimMatrix );
		MDataHandle hInputMesh = hArrow.child( aInputMesh );
		MDataHandle hStartSize = hArrow.child( aStartSize );
		MDataHandle hSize = hArrow.child( aSize );
		MDataHandle hActiveColor = hArrow.child( aActiveColor );
		MDataHandle hLeadColor = hArrow.child( aLeadColor );
		MDataHandle hDefaultColor = hArrow.child( aDefaultColor );
		MDataHandle hFillAlpha = hArrow.child( aFillAlpha );
		MDataHandle hLineAlpha = hArrow.child( aLineAlpha );
		MDataHandle hOffset = hArrow.child( aOffset );

		inheritMatrix[i] = hInheritMatrix.asBool();
		aimMatrix[i] = hAimMatrix.asMatrix()*hDiscMatrix.asMatrix().inverse();
		inputMeshObj[i] = hInputMesh.asMesh();
		startSize[i] = hStartSize.asFloat();
		size[i] = hSize.asFloat();
		activeColor[i] = hActiveColor.asFloat3();
		leadColor[i] = hLeadColor.asFloat3();
		defaultColor[i] = hDefaultColor.asFloat3();
		fillAlpha[i] = hFillAlpha.asFloat();
		lineAlpha[i] = hLineAlpha.asFloat();
		offset[i] = hOffset.asVector();

		hArrArrow.next();
	}

	MDataHandle hOutput = data.outputValue( aOutput );
	hOutput.set( 1.0 );
	data.setClean( plug );

	return MS::kSuccess;
}

void retargetLocator::getRadPoints( MPointArray& radPoints )
{
	int    div = discDivision;
	double angle = 360.0/div*0.01745327778;

	radPoints.setLength( div );

	double axisList[3];
	for( int i=0; i<div; i++ )
	{
		axisList[0] = 0.0;
		axisList[1] = sin( angle*i + discAngle );
		axisList[2] = cos( angle*i + discAngle );
		radPoints.set( i, axisList[(discAxis+3)%3]*discSize.x, 
			              axisList[(discAxis+2)%3]*discSize.y, 
						  axisList[(discAxis+1)%3]*discSize.z );
	}
}

MPointArray* retargetLocator::getPolygonPoints( MFnMesh& inputMesh )
{
	polygonNum = inputMesh.numPolygons();

	MPointArray inputMeshPoints;
	inputMesh.getPoints( inputMeshPoints );

	MPointArray* polygonPoints = new MPointArray[ polygonNum ];

	MIntArray polyVertexIndies;

	for( int polygonId =0; polygonId < polygonNum; polygonId++ )
	{
		inputMesh.getPolygonVertices( polygonId, polyVertexIndies );

		int length = polyVertexIndies.length();

		polygonPoints[polygonId].setLength( length );
		for( int i=0; i < length; i++ )
		{
			polygonPoints[polygonId].set( inputMeshPoints[ polyVertexIndies[i] ], i );
		}
	}
	return polygonPoints;
}

void retargetLocator::drawDisc( const MPointArray& radPoints )
{
	MPoint point1;
	for ( int i = 0; i < discDivision; i++ )
    {
		point1 = radPoints[i];
        glVertex3f( (float)point1.x, (float)point1.y, (float)point1.z );
    }
}

void retargetLocator::drawDiscAll( float lineAlpha, float fillAlpha )
{
	MPointArray radPoints;
    getRadPoints( radPoints );

	MColor cuColor;
	if( viewMode == 0 )
		cuColor = discActiveColor;
	else if( viewMode == 1 )
		cuColor = discLeadColor;
	else
		cuColor = discDefaultColor;

	glColor4f( cuColor.r, cuColor.g, cuColor.b, lineAlpha );
	glBegin( GL_LINE_LOOP );
	drawDisc( radPoints );
	glEnd();
	if( fillAlpha > 0.0f )
	{
		glColor4f( cuColor.r, cuColor.g, cuColor.b, fillAlpha );
		glBegin( GL_POLYGON );
		drawDisc( radPoints );
		glEnd();
	}
}

bool retargetLocator::drawArrowPolygon( MMatrix aimMatrix, MColor cuColor,float fillAlpha, float lineAlpha, int index )
{
	MStatus status;
	MFnMesh inputMesh( inputMeshObj[index], &status );
	if( !status )
		return false;

	float indexedSize = size[index];
	float startIndexedSize = startSize[ index ];

	MPointArray* polygonPoints = getPolygonPoints( inputMesh );

	if( indexedSize > 0 )
	{
		glColor4f( cuColor.r, cuColor.g, cuColor.b, lineAlpha );
		for( int polygonId=0; polygonId< polygonNum ; polygonId++ )
		{
			glBegin( GL_LINE_LOOP );
			MPointArray& cuPolygonPoints = polygonPoints[polygonId];
			for( unsigned int i=0; i < cuPolygonPoints.length(); i++ )
			{
				MPoint cuPoint = cuPolygonPoints[i]*indexedSize*aimMatrix;
				bbox.expand( cuPoint );
				glVertex3f( (float)cuPoint.x, (float)cuPoint.y, (float)cuPoint.z );
			}
			glEnd();
		}

		glColor4f( cuColor.r, cuColor.g, cuColor.b, fillAlpha );
		for( int polygonId=0; polygonId< polygonNum ; polygonId++ )
		{
			glBegin( GL_POLYGON );
			MPointArray& cuPolygonPoints = polygonPoints[polygonId];
			for( unsigned int i=0; i< cuPolygonPoints.length(); i++ )
			{
				MPoint cuPoint = cuPolygonPoints[i]*indexedSize*aimMatrix;
				glVertex3f( (float)cuPoint.x, (float)cuPoint.y, (float)cuPoint.z );
			}
			glEnd();
		}
	}

	MVector offsetPosition( offset[index].x, offset[index].y, offset[index].z );

	if( startIndexedSize > 0 )
	{
		glColor4f( cuColor.r, cuColor.g, cuColor.b, lineAlpha );
		for( int polygonId=0; polygonId< polygonNum ; polygonId++ )
		{
			glBegin( GL_LINE_LOOP );
			MPointArray& cuPolygonPoints = polygonPoints[polygonId];
			for( unsigned int i=0; i < cuPolygonPoints.length(); i++ )
			{
				MPoint cuPoint = cuPolygonPoints[i]*startIndexedSize+offsetPosition;
				bbox.expand( cuPoint );

				glVertex3f( (float)cuPoint.x, (float)cuPoint.y, (float)cuPoint.z );
			}
			glEnd();
		}

		glColor4f( cuColor.r, cuColor.g, cuColor.b, fillAlpha );
		for( int polygonId=0; polygonId< polygonNum ; polygonId++ )
		{
			glBegin( GL_POLYGON );
			MPointArray& cuPolygonPoints = polygonPoints[polygonId];
			for( unsigned int i=0; i< cuPolygonPoints.length(); i++ )
			{
				MPoint cuPoint = cuPolygonPoints[i]*startIndexedSize+offsetPosition;
				glVertex3f( (float)cuPoint.x, (float)cuPoint.y, (float)cuPoint.z );
			}
			glEnd();
		}
	}

	delete []polygonPoints;

	return true;
}

void retargetLocator::drawArrowAimLine( MVector aimVector, int index )
{
	glBegin( GL_LINES );
	glVertex3f( 0.0f, 0.0f, 0.0f);
	glVertex3f( (float)offset[index].x, (float)offset[index].y, (float)offset[index].z );
	glVertex3f( (float)offset[index].x, (float)offset[index].y, (float)offset[index].z );
	glVertex3f( (float)aimVector.x, (float)aimVector.y, (float)aimVector.z );
	glEnd();
}

void retargetLocator::drawArrowAll( float lineAlpha, float fillAlpha, int index )
{
	MMatrix matrixElement;
	if( inheritMatrix[index]==1 )
		matrixElement = aimMatrix[index];
	else
		matrixElement = getAimMatrix( aimMatrix[index] );

	MVector aimVector( matrixElement( 3,0 ), matrixElement( 3,1 ), matrixElement( 3,2 ) );

	bbox.expand(aimVector);

	MColor cuColor;
	if( viewMode == 0 )
		cuColor = activeColor[index];
	else if( viewMode == 1 )
		cuColor = leadColor[index];
	else
		cuColor = defaultColor[index];

	drawArrowPolygon( matrixElement, cuColor, fillAlpha*0.5f, lineAlpha*0.5f, index );
	glColor4f( cuColor.r, cuColor.g, cuColor.b, 1.0f );
	drawArrowAimLine( aimVector, index );
}

void retargetLocator::draw( M3dView& view, const MDagPath& DAGPath, 
							M3dView::DisplayStyle style, M3dView::DisplayStatus status )
{
	view.beginGL();
	glPushAttrib( GL_CURRENT_BIT );
	glEnable( GL_BLEND );
	glBlendFunc( GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA );
	glDepthMask( GL_FALSE );
	if ( status == M3dView::kActive ) viewMode = 0;
	else if ( status == M3dView::kLead ) viewMode = 1;
    else  viewMode = 2;
	glDepthFunc( GL_ALWAYS );
	drawDiscAll( discLineAlpha*0.5f, discFillAlpha*0.5f );
	for( int i =0; i<lineAlpha.length(); i++ )
	{
		drawArrowAll( lineAlpha[i]*0.5f, fillAlpha[i]*0.5f, i );
	}
	glDepthFunc( GL_LESS );
	drawDiscAll( discLineAlpha, discFillAlpha );
	for( int i =0; i<lineAlpha.length(); i++ )
	{
		drawArrowAll( lineAlpha[i], fillAlpha[i], i );
	}
	glDepthMask( GL_TRUE );
	glDisable( GL_BLEND );
	glPopAttrib();
    view.endGL();
}

bool retargetLocator::isBounded() const
{ 
	return true;
}

bool retargetLocator::isTransparent() const
{ 
	return true;
}

MBoundingBox retargetLocator::boundingBox() const
{	
	MBoundingBox bbox( this->bbox );
	bbox.expand( MPoint( discOffset ) );
	bbox.expand( MPoint( -discSize ) );
	bbox.expand( MPoint( discSize ) );
	return bbox;
}

MStatus retargetLocator::initialize()
{
    MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnEnumAttribute eAttr;
	MFnUnitAttribute uAttr;
	MFnCompoundAttribute cAttr;
	MFnTypedAttribute tAttr;
	
	aOutput = nAttr.create( "output", "output", MFnNumericData::kDouble );
	nAttr.setStorable( false );
	CHECK_MSTATUS( addAttribute( aOutput ) );

	aDiscMatrix = mAttr.create( "discMatrix", "discMatrix" );
	mAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aDiscMatrix ) );
	CHECK_MSTATUS( attributeAffects( aDiscMatrix, aOutput ) );

	aDiscAxis = eAttr.create( "discAxis", "discAxis", 0 );
	eAttr.addField( "X", 0 );
	eAttr.addField( "Y", 1 );
	eAttr.addField( "Z", 2 );
	eAttr.setStorable( true );
	eAttr.setChannelBox( true );
	eAttr.setReadable( true );
	CHECK_MSTATUS( addAttribute( aDiscAxis ) );
	CHECK_MSTATUS( attributeAffects( aDiscAxis, aOutput ) );


	aDiscDivision = nAttr.create( "discDivision", "discDivision", MFnNumericData::kInt, 32 );
	nAttr.setMin( 1 );
	nAttr.setMax( 32 );
	nAttr.setStorable( true );
	nAttr.setChannelBox( true );
	CHECK_MSTATUS( addAttribute( aDiscDivision ) );
	CHECK_MSTATUS( attributeAffects( aDiscDivision, aOutput ) );


	aDiscAngle = uAttr.create( "discAngle", "discAngle", MFnUnitAttribute::kAngle, 0.0 );
	uAttr.setStorable( true );
	uAttr.setChannelBox( true );
	CHECK_MSTATUS( addAttribute( aDiscAngle ) );
	CHECK_MSTATUS( attributeAffects( aDiscAngle, aOutput ) );


	aDiscOffsetX = nAttr.create( "discOffsetX", "discOffsetX", MFnNumericData::kDouble, 0.0 );
	aDiscOffsetY = nAttr.create( "discOffsetY", "discOffsetY", MFnNumericData::kDouble, 0.0 );
	aDiscOffsetZ = nAttr.create( "discOffsetZ", "discOffsetZ", MFnNumericData::kDouble, 0.0 );
	aDiscOffset  = nAttr.create( "discOffset", "discOffset", aDiscOffsetX, aDiscOffsetY, aDiscOffsetZ );
	uAttr.setStorable( true );
	uAttr.setChannelBox( true );
	CHECK_MSTATUS( addAttribute( aDiscOffset ) );
	CHECK_MSTATUS( attributeAffects( aDiscOffset, aOutput ) );

	aDiscSizeX = nAttr.create( "discSizeX", "discSizeX", MFnNumericData::kDouble, 1.0 );
	aDiscSizeY = nAttr.create( "discSizeY", "discSizeY", MFnNumericData::kDouble, 1.0 );
	aDiscSizeZ = nAttr.create( "discSizeZ", "discSizeZ", MFnNumericData::kDouble, 1.0 );
	aDiscSize  = nAttr.create( "discSize", "discSize", aDiscSizeX, aDiscSizeY, aDiscSizeZ );
	uAttr.setStorable( true );
	uAttr.setChannelBox( true );
	CHECK_MSTATUS( addAttribute( aDiscSize ) );
	CHECK_MSTATUS( attributeAffects( aDiscSize, aOutput ) );


	aDiscActiveColor = nAttr.createColor( "discActiveColor", "discActiveColor" );
	nAttr.setStorable( true );
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(1.0f, 1.0f, 1.0f);
	CHECK_MSTATUS( addAttribute( aDiscActiveColor ) );
	CHECK_MSTATUS( attributeAffects( aDiscActiveColor, aOutput ) );


	aDiscLeadColor = nAttr.createColor( "discLeadColor", "discLeadColor" );
	nAttr.setStorable( true );
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(.263f, 1.0f, .639f);
	CHECK_MSTATUS( addAttribute( aDiscLeadColor ) );
	CHECK_MSTATUS( attributeAffects( aDiscLeadColor, aOutput ) );


	aDiscDefaultColor = nAttr.createColor( "discDefaultColor", "discDefaultColor" );
	nAttr.setStorable( true );
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(.0f, .016f, .376f);
	CHECK_MSTATUS( addAttribute( aDiscDefaultColor ) );
	CHECK_MSTATUS( attributeAffects( aDiscDefaultColor, aOutput ) );

	aDiscFillAlpha = nAttr.create( "discFillAlpha", "discFillAlpha", MFnNumericData::kFloat, 0.1f );
	nAttr.setStorable( true );
	nAttr.setMin( 0.0f );
	nAttr.setMax( 1.0f );
	CHECK_MSTATUS( addAttribute( aDiscFillAlpha ) );
	CHECK_MSTATUS( attributeAffects( aDiscFillAlpha, aOutput ) );

	aDiscLineAlpha = nAttr.create( "discLineAlpha", "discLineAlpha", MFnNumericData::kFloat, 1.0f );
	nAttr.setStorable( true );
	nAttr.setMin( 0.0f );
	nAttr.setMax( 1.0f );
	CHECK_MSTATUS( addAttribute( aDiscLineAlpha ) );
	CHECK_MSTATUS( attributeAffects( aDiscLineAlpha, aOutput ) );

	aArrow = cAttr.create( "arrow", "arrow" );

	aInheritMatrix = nAttr.create( "inheritMatrix", "inheritMatrix", MFnNumericData::kBoolean, false );

	aInputMesh = tAttr.create( "inputMesh", "inputMesh", MFnData::kMesh );

	aAimMatrix = mAttr.create( "aimMatrix", "aimMatrix" );

	aStartSize = nAttr.create( "startSize", "startSize", MFnNumericData::kFloat, 0.5f );

	aSize = nAttr.create( "size", "size", MFnNumericData::kFloat, 1.0f );

	aActiveColor = nAttr.createColor( "activeColor", "activeColor" );
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(1.0f, 1.0f, 1.0f);
	aLeadColor = nAttr.createColor( "leadColor", "leadColor" );
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(.263f, 1.0f, .639f);
	aDefaultColor = nAttr.createColor( "defaultColor", "defaultColor" );
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(.0f, .016f, .376f);

	aFillAlpha = nAttr.create( "fillAlpha", "fillAlpha", MFnNumericData::kFloat, 0.1f );
	aLineAlpha = nAttr.create( "lineAlpha", "lineAlpha", MFnNumericData::kFloat, 1.0f );

	aOffsetX = nAttr.create( "offsetX", "offsetX", MFnNumericData::kDouble, 0.0 );
	aOffsetY = nAttr.create( "offsetY", "offsetY", MFnNumericData::kDouble, 0.0 );
	aOffsetZ = nAttr.create( "offsetZ", "offsetZ", MFnNumericData::kDouble, 0.0 );
	aOffset = nAttr.create( "offset", "offset", aOffsetX, aOffsetY, aOffsetZ );

	cAttr.addChild( aInheritMatrix );
	cAttr.addChild( aAimMatrix );
	cAttr.addChild( aInputMesh );
	cAttr.addChild( aStartSize );
	cAttr.addChild( aSize );
	cAttr.addChild( aActiveColor );
	cAttr.addChild( aLeadColor );
	cAttr.addChild( aDefaultColor );
	cAttr.addChild( aFillAlpha );
	cAttr.addChild( aLineAlpha );
	cAttr.addChild( aOffset );
	cAttr.setArray( true );
	cAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aArrow ) );
	CHECK_MSTATUS( attributeAffects( aArrow, aOutput ) );

	return MS::kSuccess;
}

retargetLocator::retargetLocator()
{
	discAxis = 0;
	discDivision = 32;
	discSize = MVector( 1,1,1 );
	discOffset = MVector( 0,0,0 );
	float discFillAlpha = 0.1f;
	float discLineAlpha = 1.0f;
	int arrowNum = 0;
}


void retargetLocator::postConstructor()
{
	MObject oThis = thisMObject();
	MFnDependencyNode fnNode( oThis );
	fnNode.setName( "retargetLocatorShape#" );
}

retargetLocator::~retargetLocator()
{
}

void *retargetLocator::creator()
{
	return new retargetLocator();
}