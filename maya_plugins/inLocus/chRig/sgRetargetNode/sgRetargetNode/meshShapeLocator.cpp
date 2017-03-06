#include "meshShapeLocator.h"

#include <maya/MPlug.h>
#include <maya/MDataBlock.h>
#include <maya/MArrayDataHandle.h>
#include <maya/MFloatPointArray.h>
#include <maya/MPointArray.h>
#include <maya/MDagPath.h>

#include <maya/MFnDependencyNode.h>

#include <maya/MVector.h> 
#include <maya/MPoint.h> 
#include <maya/MMatrix.h> 
#include <maya/MFnMatrixData.h>

#include <maya/MGlobal.h>

MTypeId  meshShapeLocator::id( 0xc8d202 );

MObject  meshShapeLocator::aShapes;
	MObject  meshShapeLocator::aOffsetMatrix;
	MObject  meshShapeLocator::aLocalObject;
	MObject  meshShapeLocator::aInputMesh;
	MObject  meshShapeLocator::aMeshSize;
	MObject  meshShapeLocator::aActiveColor;
	MObject  meshShapeLocator::aLeadColor;
	MObject  meshShapeLocator::aDefaultColor;
	MObject  meshShapeLocator::aLineOff;
	MObject  meshShapeLocator::aFillAlpha;
	MObject  meshShapeLocator::aLineAlpha;
	MObject  meshShapeLocator::aOverRate;

MObject  meshShapeLocator::aOutput;

short meshShapeLocator::viewMode;

/*
MMatrix      meshShapeLocator::inverseMatrix;

int           meshShapeLocator::inputNum;
MMatrixArray  meshShapeLocator::offsetMatrix;
MIntArray     meshShapeLocator::localObject;
MObjectArray  meshShapeLocator::inputMeshObj;
MFloatArray  meshShapeLocator::meshSize;
MColorArray   meshShapeLocator::activeColor;
MColorArray   meshShapeLocator::leadColor;
MColorArray   meshShapeLocator::defaultColor;
MFloatArray  meshShapeLocator::fillAlpha;
MFloatArray  meshShapeLocator::lineAlpha;
MIntArray     meshShapeLocator::lineOff;
MFloatArray   meshShapeLocator::overRate;


MPointArray* meshShapeLocator::polygonPoints;

int          meshShapeLocator::polygonNum;

MBoundingBox meshShapeLocator::BBox;
*/

MStatus  meshShapeLocator::compute( const MPlug& plug, MDataBlock& data )
{
	MStatus status;

	MArrayDataHandle hArrShapes = data.inputArrayValue( aShapes );

	inputNum = hArrShapes.elementCount();

	offsetMatrix.setLength( inputNum );
	 localObject.setLength( inputNum );
	inputMeshObj.setLength( inputNum );
	 activeColor.setLength( inputNum );
	   leadColor.setLength( inputNum );
	defaultColor.setLength( inputNum );
	    meshSize.setLength( inputNum );
	     lineOff.setLength( inputNum );
	   fillAlpha.setLength( inputNum );
	   lineAlpha.setLength( inputNum );
	 overRate.setLength( inputNum );

	for( unsigned int i=0; i< inputNum; i++ )
	{
		MDataHandle hShapes = hArrShapes.inputValue();

		offsetMatrix[i] = hShapes.child( aOffsetMatrix ).asMatrix();
		localObject[i]  = hShapes.child( aLocalObject ).asInt();
		inputMeshObj[i] = hShapes.child( aInputMesh ).asMesh();
		meshSize[i]     = hShapes.child( aMeshSize ).asFloat();
		activeColor[i]  = hShapes.child( aActiveColor ).asFloat3();
		leadColor[i]    = hShapes.child( aLeadColor ).asFloat3();
		defaultColor[i] = hShapes.child( aDefaultColor ).asFloat3();
		fillAlpha[i]    = hShapes.child( aFillAlpha ).asFloat();
		lineAlpha[i]    = hShapes.child( aLineAlpha ).asFloat();
		lineOff[i]      = hShapes.child( aLineOff ).asInt();
		overRate[i]     = hShapes.child( aOverRate ).asFloat();

		BBox.expand( MPoint( offsetMatrix[i]( 3,0 ), offsetMatrix[i]( 3,1 ), offsetMatrix[i]( 3,2 ) ) );

		hArrShapes.next();
	}

	MDataHandle hOutput = data.outputValue( aOutput );
	hOutput.set( 1.0f );
	hOutput.setClean();

	data.setClean( plug );

	return MS::kSuccess;
}

void meshShapeLocator::getPolygonPoints( MFnMesh& inputMesh )
{
	polygonNum = inputMesh.numPolygons();

	MPointArray inputMeshPoints;
	inputMesh.getPoints( inputMeshPoints );

	polygonPoints = new MPointArray[ polygonNum ];

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
}

bool meshShapeLocator::drawPolygon( int index, float alphaMult )
{
	MStatus status;

	MFnMesh inputMesh( inputMeshObj[index], &status );
	if( !status )
		return false;

	MMatrix matrixElement = offsetMatrix[index];

	MColor cuColor;
	if( viewMode == 0 )
		cuColor = activeColor[index];
	else if( viewMode == 1 )
		cuColor = leadColor[index];
	else
		cuColor = defaultColor[index];

	double indexedMeshSize = meshSize[index];

	getPolygonPoints( inputMesh );

	glColor4f( cuColor.r, cuColor.g, cuColor.b, fillAlpha[index]*alphaMult );
	for( int polygonId=0; polygonId< polygonNum ; polygonId++ )
	{
		glBegin( GL_POLYGON );
		MPointArray& cuPolygonPoints = polygonPoints[polygonId];
		for( unsigned int i=0; i< cuPolygonPoints.length(); i++ )
		{
			MPoint cuPoint = cuPolygonPoints[i]*indexedMeshSize*offsetMatrix[index];
			BBox.expand( cuPoint );
			if( !localObject[index] )
				cuPoint *=inverseMatrix;
			glVertex3f( (float)cuPoint.x, (float)cuPoint.y, (float)cuPoint.z );
		}
		glEnd();
	}

	if( !lineOff[index] )
	{
		glColor4f( cuColor.r, cuColor.g, cuColor.b, lineAlpha[index]*alphaMult );
		for( int polygonId=0; polygonId< polygonNum ; polygonId++ )
		{
			glBegin( GL_LINE_LOOP );
			MPointArray& cuPolygonPoints = polygonPoints[polygonId];
			for( unsigned int i=0; i < cuPolygonPoints.length(); i++ )
			{
				MPoint cuPoint = cuPolygonPoints[i]*indexedMeshSize*offsetMatrix[index];
				if( !localObject[index] )
					cuPoint *=inverseMatrix;
				glVertex3f( (float)cuPoint.x, (float)cuPoint.y, (float)cuPoint.z );
			}
			glEnd();
		}
	}

	delete []polygonPoints;

	return true;
}

void meshShapeLocator::draw( M3dView& view, const MDagPath& DAGPath, 
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

	MDagPath dagPath;

	dagPath.getAPathTo( thisMObject(), dagPath );

	inverseMatrix = dagPath.exclusiveMatrixInverse();
	
	glDepthFunc( GL_ALWAYS );

	for( int i=0; i<inputNum; i++ )
	{
		drawPolygon( i, overRate[i] );
	}
	glDepthFunc( GL_LESS );

	for( int i=0; i<inputNum; i++ )
	{
		drawPolygon( i, 1.0f );
	}

	glDepthMask( GL_TRUE );
	glDisable( GL_BLEND );
	glPopAttrib();
    view.endGL();
}

bool meshShapeLocator::isBounded() const
{ 
	return true;
}

bool meshShapeLocator::isTransparent() const
{ 
	return true;
}

MBoundingBox meshShapeLocator::boundingBox() const
{
	return BBox;
}

MStatus meshShapeLocator::initialize()
{
    MFnNumericAttribute nAttr;
	MFnMatrixAttribute mAttr;
	MFnEnumAttribute eAttr;
	MFnUnitAttribute uAttr;
	MFnCompoundAttribute cAttr;
	MFnTypedAttribute tAttr;
	
	aOutput = nAttr.create( "output", "output", MFnNumericData::kFloat );
	nAttr.setStorable( false );
	CHECK_MSTATUS( addAttribute( aOutput ) );


	aShapes = cAttr.create( "shapes", "shapes" );

	aInputMesh = tAttr.create( "inputMesh", "inputMesh", MFnData::kMesh );
	aOffsetMatrix = mAttr.create( "offsetMatrix", "offsetMatrix" );
	aLocalObject  = nAttr.create( "localObject", "localObject", MFnNumericData::kBoolean, true );
	aMeshSize = nAttr.create( "meshSize", "meshSize", MFnNumericData::kFloat, 1.0 );
	aActiveColor = nAttr.createColor( "activeColor", "activeColor" );
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(1.0f, 1.0f, 1.0f);
	aLeadColor = nAttr.createColor( "leadColor", "leadColor" );
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(.263f, 1.0f, .639f);
	aDefaultColor = nAttr.createColor( "defaultColor", "defaultColor" );
	nAttr.setUsedAsColor(true);
	nAttr.setDefault(.0f, .016f, .376f);
	aFillAlpha = nAttr.create( "fillAlpha", "fillAlpha", MFnNumericData::kFloat, 0.1 );
	nAttr.setMin( 0 );
	nAttr.setMax( 1 );
	aLineAlpha = nAttr.create( "lineAlpha", "lineAlpha", MFnNumericData::kFloat, 1.0 );
	nAttr.setMin( 0 );
	nAttr.setMax( 1 );
	aOverRate = nAttr.create( "overRate", "overRate", MFnNumericData::kFloat, 0.4 );
	nAttr.setMin( 0 );
	nAttr.setMax( 1 );

	aLineOff = nAttr.create( "lineOff", "lineOff", MFnNumericData::kBoolean, false );

	cAttr.addChild( aOffsetMatrix );
	cAttr.addChild( aLocalObject );
	cAttr.addChild( aInputMesh );
	cAttr.addChild( aMeshSize );
	cAttr.addChild( aActiveColor );
	cAttr.addChild( aLeadColor );
	cAttr.addChild( aDefaultColor );
	cAttr.addChild( aFillAlpha );
	cAttr.addChild( aLineAlpha );
	cAttr.addChild( aLineAlpha );
	cAttr.addChild( aOverRate );
	cAttr.setArray( true );
	cAttr.setStorable( true );
	CHECK_MSTATUS( addAttribute( aShapes ) );
	CHECK_MSTATUS( attributeAffects( aShapes, aOutput ) );

	return MS::kSuccess;
}

meshShapeLocator::meshShapeLocator()
{
}


void meshShapeLocator::postConstructor()
{
	MObject oThis = thisMObject();
	MFnDependencyNode fnNode( oThis );
	fnNode.setName( "meshShapeLocatorShape#" );
}

meshShapeLocator::~meshShapeLocator()
{
}

void *meshShapeLocator::creator()
{
	return new meshShapeLocator();
}