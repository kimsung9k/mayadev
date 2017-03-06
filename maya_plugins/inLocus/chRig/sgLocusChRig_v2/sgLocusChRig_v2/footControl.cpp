#include "footControl.h"

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MDagPath.h>
#include <maya/MObjectArray.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnTransform.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <cmath>

#include <maya/MVector.h>

#define toRadian( degree ) ( (degree)*(3.14159265359/180.f) )

MTypeId  footControl::id( 0xc8c914 );

MObject  footControl::aFootStart;
MObject  footControl::aFootEnd;

MObject  footControl::aWalkRollAngle;

MObject  footControl::aHeelRot;
MObject  footControl::aBallRot;
MObject  footControl::aToeRot;
MObject  footControl::aHeelTwist;
MObject  footControl::aBallTwist;
MObject  footControl::aToeTwist;
MObject  footControl::aBank;
MObject  footControl::aTapToe;
MObject  footControl::aHeelLift;
MObject  footControl::aWalkRoll;

MObject  footControl::aOutput;

footControl::footControl() {};
footControl::~footControl() {};

MStatus footControl::initialize()
{
	MStatus stat;

	MFnNumericAttribute nAttr;
	MFnMessageAttribute msAttr;
	
	aFootStart = msAttr.create( "footStart", "fs" );
	aFootEnd   = msAttr.create( "footEnd", "fe" );
	 
	aHeelRot = nAttr.create( "heelRot", "hr", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aBallRot = nAttr.create( "ballRot", "br", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aToeRot = nAttr.create( "toeRot", "tr", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aHeelTwist = nAttr.create( "heelTwist", "ht", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aBallTwist = nAttr.create( "ballTwist", "bt", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aToeTwist = nAttr.create( "toeTwist", "tt", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aBank = nAttr.create( "bank", "b", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aTapToe = nAttr.create( "tapToe", "tapt", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aHeelLift = nAttr.create( "heelLift", "hl", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aWalkRoll = nAttr.create( "walkRoll", "wr", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );
	aWalkRollAngle = nAttr.create( "walkRollAngle", "wra", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( true );

	aOutput = nAttr.create( "output", "o", MFnNumericData::kDouble, 0.0 );
	nAttr.setStorable( false );
	nAttr.setWritable( false );

	stat = addAttribute( aFootStart );
	if( !stat ){ stat.perror( "addAttribute : baseVector" ); return stat; }
	stat = addAttribute( aFootEnd );
	if( !stat ){ stat.perror( "addAttribute : inputVector" ); return stat; }

	stat = addAttribute( aHeelRot );
	if( !stat ){ stat.perror( "addAttribute : HeelRot" ); return stat; }
	stat = addAttribute( aBallRot );
	if( !stat ){ stat.perror( "addAttribute : BallRot" ); return stat; }
	stat = addAttribute( aToeRot );
	if( !stat ){ stat.perror( "addAttribute : ToeRot" ); return stat; }
	stat = addAttribute( aHeelTwist );
	if( !stat ){ stat.perror( "addAttribute : HeelTwist" ); return stat; }
	stat = addAttribute( aBallTwist );
	if( !stat ){ stat.perror( "addAttribute : BallTwist" ); return stat; }
	stat = addAttribute( aToeTwist );
	if( !stat ){ stat.perror( "addAttribute : ToeTwist" ); return stat; }
	stat = addAttribute( aBank );
	if( !stat ){ stat.perror( "addAttribute : Bank" ); return stat; }
	stat = addAttribute( aTapToe );
	if( !stat ){ stat.perror( "addAttribute : aTapToe" ); return stat; }
	stat = addAttribute( aHeelLift );
	if( !stat ){ stat.perror( "addAttribute : HeelLift" ); return stat; }
	stat = addAttribute( aWalkRoll );
	if( !stat ){ stat.perror( "addAttribute : WalkRoll" ); return stat; }
	stat = addAttribute( aWalkRollAngle );
	if( !stat ){ stat.perror( "addAttribute : WalkRoll" ); return stat; }

	stat = addAttribute( aOutput );
	if( !stat ){ stat.perror( "addAttribute : WalkRoll" ); return stat; }

	stat = attributeAffects( aHeelRot, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : HeelRot" ); return stat; }
	stat = attributeAffects( aBallRot, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : BallRot" ); return stat; }
	stat = attributeAffects( aToeRot, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : ToeRot" ); return stat; }
	stat = attributeAffects( aHeelTwist, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : HeelTwist" ); return stat; }
	stat = attributeAffects( aBallTwist, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : BallTwist" ); return stat; }
	stat = attributeAffects( aToeTwist, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : ToeTwist" ); return stat; }
	stat = attributeAffects( aBank, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : Bank" ); return stat; }
	stat = attributeAffects( aHeelLift, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : HeelLift" ); return stat; }
	stat = attributeAffects( aTapToe, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : WalkRoll" ); return stat; }
	stat = attributeAffects( aWalkRoll, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : WalkRoll" ); return stat; }
	stat = attributeAffects( aWalkRollAngle, aOutput );
	if( !stat ){ stat.perror( "attributeAffects : WalkRoll" ); return stat; }

	return MS::kSuccess;

}

MStatus footControl::compute( const MPlug& plug, MDataBlock& block )
{
	MStatus stat;

	MDataHandle hOutput   = block.outputValue( aOutput );

	MDataHandle hHeelRot = block.inputValue( aHeelRot );
	MDataHandle hBallRot = block.inputValue( aBallRot );
	MDataHandle hToeRot = block.inputValue( aToeRot );
	MDataHandle hHeelTwist = block.inputValue( aHeelTwist );
	MDataHandle hBallTwist = block.inputValue( aBallTwist );
	MDataHandle hToeTwist = block.inputValue( aToeTwist );
	MDataHandle hBank = block.inputValue( aBank );
	MDataHandle hTapToe = block.inputValue( aTapToe );
	MDataHandle hHeelLift = block.inputValue( aHeelLift );
	MDataHandle hWalkRoll = block.inputValue( aWalkRoll );
	MDataHandle hWalkRollAngle = block.inputValue( aWalkRollAngle );

	double heelValueY = toRadian( hHeelRot.asDouble() );
	double ballValueY = toRadian( hHeelLift.asDouble() );
	double toeValueY  = toRadian( hToeRot.asDouble()  );
	double tapToeValueY = toRadian( hTapToe.asDouble() );
	double walkRollAngle = toRadian( hWalkRollAngle.asDouble() );

	double walkRollValue = toRadian( hWalkRoll.asDouble() );
	if( walkRollValue < 0 )
		heelValueY += walkRollValue;
	else if( walkRollValue < walkRollAngle )
		ballValueY += walkRollValue;
	else{
		ballValueY += walkRollAngle*2-walkRollValue;
		toeValueY += (walkRollValue-walkRollAngle );
	}
	
	double heelPivValue[3] = { toRadian( hHeelTwist.asDouble() ) ,heelValueY, 0 };
	double ballPivValue[3] = { toRadian( hBallTwist.asDouble() ) ,toRadian( hBallRot.asDouble() ), 0 };
	double toePivValue[3]  = { toRadian( hToeTwist.asDouble()  ) ,toeValueY , 0 };
	double tapToeValue[3]  = { 0, tapToeValueY, 0 };
	double ballValue[3]    = { 0, ballValueY, 0 };

	double bankValue = hBank.asDouble();
	double bankInValueZ;
	double bankOutValueZ;

	if( bankValue > 0 ){
		bankInValueZ = bankValue;
		bankOutValueZ = 0;
	}
	else{
		bankInValueZ = 0;
		bankOutValueZ = bankValue;
	}

	MObject thisNode = thisMObject();
	MPlug footStartPlug( thisNode, aFootStart );
	MPlug footEndPlug( thisNode, aFootEnd );
	
	MPlugArray footStartCon;
	MPlugArray footEndCon;
	footStartPlug.connectedTo( footStartCon, true, false );

	MDagPath footPath;
	footPath.getAPathTo( footStartCon[0].node(), footPath );
	int childCount = footPath.childCount();

	double bankInValue[3]  = {0,0,toRadian( bankInValueZ  )};
	double bankOutValue[3] = {0,0,toRadian( bankOutValueZ )};

	int roofCount = 0;
	MObject currentObj = footPath.node();
	while( childCount )
	{
		if( roofCount > 6 ) break;
		
		if( roofCount == 0 ){
			MFnTransform trNode( currentObj );
			trNode.setRotation( heelPivValue, MTransformationMatrix::kXYZ  );
		}
		else if( roofCount == 1 ){
			MFnTransform trNode( currentObj );
			trNode.setRotation( ballPivValue, MTransformationMatrix::kXYZ  );
		}
		else if( roofCount == 2 ){
			MFnTransform trNode( currentObj );
			trNode.setRotation( bankInValue, MTransformationMatrix::kXYZ  );
		}
		else if( roofCount == 3 ){
			MFnTransform trNode( currentObj );
			trNode.setRotation( bankOutValue, MTransformationMatrix::kXYZ  );
		}
		else if( roofCount == 4 ){
			MFnTransform trNode( currentObj );
			trNode.setRotation( toePivValue, MTransformationMatrix::kXYZ  );
		}
		else if( roofCount == 5 ){
			footPath.getAPathTo( currentObj, footPath );
			if( footPath.childCount() > 1 ){
				MObject tapToeObj = footPath.child(1);
				MFnTransform trNode( tapToeObj );
				trNode.setRotation( tapToeValue, MTransformationMatrix::kXYZ );
			}
		}
		else if( roofCount == 6 ){
			MFnTransform trNode( currentObj );
			trNode.setRotation( ballValue, MTransformationMatrix::kXYZ  );
		}
		footPath.getAPathTo( currentObj, footPath );
		currentObj = footPath.child(0);
		roofCount ++;
	}

	block.setClean( plug );

	return MS::kSuccess;
}

void* footControl::creator()
{
	return new footControl();
}