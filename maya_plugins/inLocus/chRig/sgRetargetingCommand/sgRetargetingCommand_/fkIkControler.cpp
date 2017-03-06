#include "fkIkControler.h"
#include <maya/MPlug.h>

#define degToRad( x ) ((x)*3.14159/180.0)
#define radToDeg( x ) ((x)/3.14159*180.0)


void flipValue( bool& vFirst, bool& vSecond )
{
	bool vKeep = vFirst;
	vFirst = vSecond;
	vSecond = vKeep;
}


void flipValue( double& vFirst, double& vSecond )
{
	double vKeep = vFirst;
	vFirst = vSecond;
	vSecond = vKeep;
}


void flipValue( MMatrix& mtxFirst, MMatrix& mtxSecond )
{
	MMatrix mtxKeep = mtxFirst;
	mtxFirst = mtxSecond;
	mtxSecond = mtxKeep;
}


void mirrorDirection( MMatrix& mtx )
{
	MVector vectorX = mtx[0];
	MVector vectorY = mtx[1];
	MVector vectorZ = mtx[2];

	vectorX *= -1; vectorY *= -1; vectorZ *= -1;

	mtx(0,0) = -vectorX.x; mtx(0,1) = vectorX.y; mtx(0,2) = vectorX.z;
	mtx(1,0) = -vectorY.x; mtx(1,1) = vectorY.y; mtx(1,2) = vectorY.z;
	mtx(2,0) = -vectorZ.x; mtx(2,1) = vectorZ.y; mtx(2,2) = vectorZ.z;
}


void mirrorPosition( MMatrix& mtx )
{
	MVector vectorP = mtx[3];

	vectorP *= -1;

	mtx(3,0) = vectorP.x; mtx(3,1) = vectorP.y; mtx(3,2) = vectorP.z;
}


FkIkCtl::FkIkCtl()
{
	m_enable = true;
	m_weight = 1.0;
	m_followEnable = false;

	ud_poleTwist = 0.0;
	ud_length = 0.0;
	ud_bias = 0.0;
	ud_stretchAble = 0.0;
	ud_smoothRate = 0.0;
	ud_positionAttach = 0.0;
	ud_kneeAutoAngle = 0.0;
	ud_tapToe = 0.0;
	ud_toeRot = 0.0;
	ud_heelLift = 0.0;
	ud_walkRoll = 0.0;
	ud_walkRollAngle = 0.0;
	ud_heelRot = 0.0;
	ud_ballRot = 0.0;
	ud_heelTwist = 0.0;
	ud_ballTwist = 0.0;
	ud_toeTwist = 0.0;
	ud_bank = 0.0;

	m_pFlip = NULL;
}


void FkIkCtl::getOrigName( MString nameShd, MString nameElb, MString nameWrt, 
	MString namePoleV, MString namePTrs, MString namePOrt )
{
	m_nameShdOrig = nameShd;
	m_nameElbOrig = nameElb;
	m_nameWrtOrig = nameWrt;
	m_namePoleVOrig = namePoleV;
	m_namePTrsOrig = namePTrs;
	m_namePOrtOrig = namePOrt;
}


void FkIkCtl::getCuName( MString nameShd, MString nameElb, MString nameWrt, MString nameBall, MString nameToe )
{
	m_nameShdCu = nameShd;
	m_nameElbCu = nameElb;
	m_nameWrtCu = nameWrt;
	m_nameBallCu = nameBall;
	m_nameToeCu  = nameToe;
}


void FkIkCtl::getFkName( MString nameShd, MString nameElb, MString nameWrt, MString nameBall )
{
	m_nameShdFk = nameShd;
	m_nameElbFk = nameElb;
	m_nameWrtFk = nameWrt;
	m_nameFootFk  = nameBall;
}


void FkIkCtl::getIkName( MString nameIk, MString nameItp, MString namePoleV, MString nameSwitch, MString namePTrs, MString namePOrt )
{
	m_nameIk = nameIk;
	m_namePoleV  = namePoleV;
	m_nameItp = nameItp;
	m_nameSwitch = nameSwitch;
	m_nameIkPTrs = namePTrs;
	m_nameIkPOrt = namePOrt;
}


void FkIkCtl::getFootName( MString nameFoot )
{
	m_nameFoot = nameFoot;
}


void FkIkCtl::getOrientPName( MString nameOrientP )
{
	m_nameOrientP = nameOrientP;
}


void FkIkCtl::getUdAttr()
{
	MFnTransform trIk = m_pathIk;
	MFnTransform trPoleV = m_pathPoleV;
	MFnTransform trSwitch = m_pathSwitch;

	ud_poleTwist = trIk.findPlug( "poleTwist" ).asDouble();
	ud_length    = trIk.findPlug( "length" ).asDouble();
	ud_bias      = trIk.findPlug( "bias" ).asDouble();
	ud_stretchAble = trIk.findPlug( "stretchAble" ).asDouble();
	ud_smoothRate  = trIk.findPlug( "smoothRate" ).asDouble();
	ud_positionAttach = trIk.findPlug( "positionAttach" ).asDouble();

	ud_handScale   = trSwitch.findPlug( "handScale" ).asDouble();
	ud_twist       = trSwitch.findPlug( "twist" ).asDouble();
	ud_interpoleSwitch = trSwitch.findPlug( "interpoleSwitch" ).asDouble();
	ud_collarFollow = trSwitch.findPlug( "collarFollow" ).asDouble();
	ud_chestFollow  = trSwitch.findPlug( "chestFollow"  ).asDouble();
	ud_hipFollow    = trSwitch.findPlug( "hipFollow"    ).asDouble();
	ud_rootFollow   = trSwitch.findPlug( "rootFollow"   ).asDouble();
	ud_moveFollow   = trSwitch.findPlug( "moveFollow"   ).asDouble();

	if( m_nameFoot.length() )
	{
		ud_tapToe = trIk.findPlug( "tapToe" ).asDouble();
		ud_toeRot = trIk.findPlug( "toeRot" ).asDouble();
		ud_heelLift = trIk.findPlug( "heelLift" ).asDouble();
		ud_walkRoll = trIk.findPlug( "walkRoll" ).asDouble();
		ud_walkRollAngle = trIk.findPlug( "walkRollAngle" ).asDouble();

		MFnTransform trFoot = m_pathFoot;
		MPlug plugHeelRot = trFoot.findPlug( "heelRot" );
		MPlug plugBallRot = trFoot.findPlug( "ballRot" );
		MPlug plugHeelTwist = trFoot.findPlug( "heelTwist" );
		MPlug plugBallTwist = trFoot.findPlug( "ballTwist" );
		MPlug plugToeTwist  = trFoot.findPlug( "toeTwist" );
		MPlug plugBank      = trFoot.findPlug( "bank" );

		ud_heelRot   = plugHeelRot.asDouble();
		ud_ballRot   = plugBallRot.asDouble();
		ud_heelTwist = plugHeelTwist.asDouble();
		ud_ballTwist = plugBallTwist.asDouble();
		ud_toeTwist  = plugToeTwist.asDouble();
		ud_bank      = plugBank.asDouble();
	}
}


MStatus FkIkCtl::setData( MString namespaceIn )
{
	if( !m_enable ) return MS::kSuccess;

	m_namespace = namespaceIn;

	MStatus			status;
	MSelectionList	selList;
	MDagPath		path;

	selList.add( namespaceIn + m_nameOrientP );
	selList.add( namespaceIn + m_nameShdFk );
	selList.add( namespaceIn + m_nameElbFk );
	selList.add( namespaceIn + m_nameWrtFk );
	selList.add( namespaceIn + m_nameFootFk );
	selList.getDagPath( 0, m_pathOrientP );
	selList.getDagPath( 1, m_pathShdFk );
	selList.getDagPath( 2, m_pathElbFk );
	selList.getDagPath( 3, m_pathWrtFk );
	selList.getDagPath( 4, m_pathToeFk );

	selList.clear();
	selList.add( namespaceIn + m_nameShdCu );
	selList.add( namespaceIn + m_nameElbCu );
	selList.add( namespaceIn + m_nameWrtCu );
	selList.add( namespaceIn + m_nameBallCu );
	selList.add( namespaceIn + m_nameToeCu );

	selList.getDagPath( 0, m_pathShd );
	selList.getDagPath( 1, m_pathElb );
	selList.getDagPath( 2, m_pathWrt );
	selList.getDagPath( 3, m_pathBall );
	selList.getDagPath( 4, m_pathToe );

	m_mtxShdOrientOffset = m_pathShd.inclusiveMatrix() * m_pathOrientP.inclusiveMatrixInverse();

	selList.clear();
	selList.add( namespaceIn + m_nameShdOrig );
	selList.add( namespaceIn + m_nameElbOrig );
	selList.add( namespaceIn + m_nameWrtOrig );
	selList.add( namespaceIn + m_namePoleVOrig );
	selList.add( namespaceIn + m_namePTrsOrig );
	selList.add( namespaceIn + m_namePOrtOrig );

	selList.getDagPath( 0, path );
	m_mtxShdOrig = path.inclusiveMatrix();
	selList.getDagPath( 1, path );
	m_mtxElbOrig = path.inclusiveMatrix();
	selList.getDagPath( 2, path );
	m_mtxWrtOrig = path.inclusiveMatrix();
	selList.getDagPath( 3, path );
	m_mtxPoleVOrig = path.inclusiveMatrix();
	selList.getDagPath( 4, path );
	m_mtxPTrsOrig = path.inclusiveMatrix();

	if( m_namePOrtOrig.length() )
	{
		selList.getDagPath( 5, path );
		m_mtxPOrtOrig = path.inclusiveMatrix();
	}
	else
	{
		m_mtxPOrtOrig = m_mtxPTrsOrig;
	}

	m_mtxElb *= m_mtxShdOrig * m_mtxElbOrig.inverse();
	m_mtxWrt *= m_mtxElbOrig * m_mtxWrtOrig.inverse();

	selList.clear();
	selList.add( namespaceIn + m_nameIk );
	selList.add( namespaceIn + m_namePoleV );
	selList.add( namespaceIn + m_nameItp );
	selList.add( namespaceIn + m_nameSwitch );
	selList.add( namespaceIn + m_nameIkPTrs );
	selList.add( namespaceIn + m_nameIkPOrt );
	selList.add( namespaceIn + m_nameFoot );

	selList.getDagPath( 0, path ); m_pathIk = path;
	selList.getDagPath( 1, path ); m_pathPoleV = path;
	selList.getDagPath( 2, path ); m_pathItp = path;
	selList.getDagPath( 3, path ); m_pathSwitch = path;
	selList.getDagPath( 4, path ); m_pathIkPTrs = path;
	selList.getDagPath( 5, path ); m_pathIkPOrt = path;
	selList.getDagPath( 6, path ); m_pathFoot = path;

	m_mtxIk     = m_pathIk.inclusiveMatrix();
	m_mtxItp    = m_pathItp.inclusiveMatrix() * m_pathItp.exclusiveMatrix();
	m_mtxPoleV  = m_pathPoleV.inclusiveMatrix();
	m_mtxIkPOrt = m_pathIkPOrt.inclusiveMatrix();
	m_mtxIkPTrs = m_pathIkPTrs.inclusiveMatrix();


	if( !m_nameFoot.length() ) return MS::kSuccess;

	MDagPath pathAnkleInit;
	MDagPath pathBallInit;
	MDagPath pathToeInit;
	MDagPath pathHeelInit;
	MDagPath pathBallPivInit;
	MDagPath pathBankInInit;
	MDagPath pathBankOutInit;
	MDagPath pathToePivInit;

	selList.clear();
	selList.add( namespaceIn + m_nameWrtOrig );
	selList.getDagPath( 0, pathAnkleInit );

	pathBallInit.getAPathTo( pathAnkleInit.child( 0 ), pathBallInit );
	pathHeelInit.getAPathTo( pathAnkleInit.child( 1 ), pathHeelInit );
	pathToeInit.getAPathTo( pathBallInit.child( 0 ), pathToeInit );
	pathBallPivInit.getAPathTo( pathHeelInit.child( 0 ), pathBallPivInit );
	pathBankInInit.getAPathTo( pathBallPivInit.child( 0 ), pathBankInInit );
	pathBankOutInit.getAPathTo( pathBankInInit.child( 0 ), pathBankOutInit );
	pathToePivInit.getAPathTo( pathBankOutInit.child( 0 ), pathToePivInit );

	m_trMtxHeelInit    = pathHeelInit.inclusiveMatrix() * pathHeelInit.exclusiveMatrixInverse();
	m_trMtxBallPivInit = pathBallPivInit.inclusiveMatrix() * pathBallPivInit.exclusiveMatrixInverse();
	m_trMtxBankInInit  = pathBankInInit.inclusiveMatrix() * pathBankInInit.exclusiveMatrixInverse();
	m_trMtxBankOutInit = pathBankOutInit.inclusiveMatrix() * pathBankOutInit.exclusiveMatrixInverse();
	m_trMtxToePivInit  = pathToePivInit.inclusiveMatrix() * pathToePivInit.exclusiveMatrixInverse();
	m_trMtxToeInit     = pathToeInit.inclusiveMatrix() * pathToePivInit.inclusiveMatrixInverse();
	m_trMtxBallInit    = pathBallInit.inclusiveMatrix() * pathToeInit.inclusiveMatrixInverse();
	m_trMtxAnkleInit   = pathAnkleInit.inclusiveMatrix() * pathBallInit.inclusiveMatrixInverse();

	MMatrix mtxAnkleInit   = pathAnkleInit.inclusiveMatrix();
	MMatrix mtxBallInit    = pathBallInit.inclusiveMatrix();
	MMatrix mtxToeInit     = pathToeInit.inclusiveMatrix();
	MVector pointAnkle = mtxAnkleInit[3];
	MVector pointBall = mtxBallInit[3];
	MVector pointToe  = mtxToeInit[3];

	MVector aim = pointBall - pointAnkle;
	MVector up  = mtxAnkleInit[1];
	MVector cross = aim^up;
	up = cross^aim;
	aim.normalize(); up.normalize(); cross.normalize();

	if( pathAnkleInit.inclusiveMatrix()[0][1] > 0 )
	{
		aim *=-1; cross *= -1;
	}

	double dMatrix[4][4] = { aim.x, aim.y, aim.z, 0,
		                     up.x,  up.y,  up.z,  0,
							 cross.x, cross.y, cross.z, 0,
							 pointAnkle.x, pointAnkle.y, pointAnkle.z, 1 };

	m_mtxCu3_orig = MMatrix( dMatrix ) * mtxAnkleInit.inverse();

	aim = pointToe - pointBall;
	up  = mtxAnkleInit[1];
	cross = aim^up;
	up = cross^aim;
	aim.normalize(); up.normalize(); cross.normalize();

	if( pathAnkleInit.inclusiveMatrix()[0][1] > 0 )
	{
		aim *=-1; cross *= -1;
	}

	double eMatrix[4][4] = { aim.x, aim.y, aim.z, 0,
		                     up.x,  up.y,  up.z,  0,
							 cross.x, cross.y, cross.z, 0,
							 pointBall.x, pointBall.y, pointBall.z, 1 };

	m_mtxCu4_orig = MMatrix( eMatrix ) * MMatrix( dMatrix ).inverse();

	return MS::kSuccess;
}


void FkIkCtl::updateCtlMatrix()
{
	if( !m_enable ) return;

	m_mtxShdOrientOffset = m_pathShd.inclusiveMatrix() * m_pathOrientP.inclusiveMatrixInverse();

	m_mtxShd = m_pathShd.inclusiveMatrix() * m_pathShd.exclusiveMatrixInverse();
	m_mtxElb = m_pathElb.inclusiveMatrix() * m_pathElb.exclusiveMatrixInverse();
	m_mtxWrt = m_pathWrt.inclusiveMatrix() * m_pathWrt.exclusiveMatrixInverse();
	m_mtxBall = m_pathBall.inclusiveMatrix() * m_pathWrt.inclusiveMatrixInverse();
	m_mtxToe  = m_pathToe.inclusiveMatrix() * m_pathBall.inclusiveMatrixInverse();
	
	m_mtxElb *= m_mtxShdOrig * m_mtxElbOrig.inverse();
	m_mtxWrt *= m_mtxElbOrig * m_mtxWrtOrig.inverse();

	m_mtxFk3 = m_mtxBall * m_mtxCu3_orig.inverse();
	m_mtxFk4 = m_mtxToe  * m_mtxCu4_orig.inverse();

	m_mtxIk     = m_pathIk.inclusiveMatrix();
	m_mtxPoleV  = m_pathPoleV.inclusiveMatrix();

	getUdAttr();
}


void FkIkCtl::flip()
{
	if( m_pFlip == NULL ) return;

	flipValue( m_enable, m_pFlip->m_enable );
	
	flipValue( m_mtxShdOrientOffset, m_pFlip->m_mtxShdOrientOffset );

	mirrorDirection( m_mtxShdOrientOffset );
	mirrorDirection( m_pFlip->m_mtxShdOrientOffset );
	mirrorPosition( m_mtxElb );
	mirrorPosition( m_mtxWrt );
	mirrorPosition( m_mtxFk3 );
	mirrorPosition( m_mtxFk4 );

	flipValue( m_mtxShd, m_pFlip->m_mtxShd );
	flipValue( m_mtxElb, m_pFlip->m_mtxElb );
	flipValue( m_mtxWrt, m_pFlip->m_mtxWrt );
	flipValue( m_mtxFk3, m_pFlip->m_mtxFk3 );
	flipValue( m_mtxFk4, m_pFlip->m_mtxFk4 );
	flipValue( m_mtxIk, m_pFlip->m_mtxIk );
	flipValue( m_mtxPoleV, m_pFlip->m_mtxPoleV );

	flipValue( ud_handScale, m_pFlip->ud_handScale );
	flipValue( ud_twist, m_pFlip->ud_twist );
	flipValue( ud_interpoleSwitch, m_pFlip->ud_interpoleSwitch );
	flipValue( ud_collarFollow, m_pFlip->ud_collarFollow );
	flipValue( ud_chestFollow,  m_pFlip->ud_chestFollow );
	flipValue( ud_hipFollow,    m_pFlip->ud_hipFollow );
	flipValue( ud_rootFollow,   m_pFlip->ud_rootFollow );
	flipValue( ud_moveFollow,   m_pFlip->ud_moveFollow );

	flipValue( ud_poleTwist, m_pFlip->ud_poleTwist );
	flipValue( ud_length, m_pFlip->ud_length );
	flipValue( ud_bias, m_pFlip->ud_bias );
	flipValue( ud_stretchAble, m_pFlip->ud_stretchAble );
	flipValue( ud_smoothRate, m_pFlip->ud_smoothRate );
	flipValue( ud_positionAttach, m_pFlip->ud_positionAttach );
	flipValue( ud_kneeAutoAngle, m_pFlip->ud_kneeAutoAngle );
	flipValue( ud_tapToe, m_pFlip->ud_tapToe );
	flipValue( ud_toeRot, m_pFlip->ud_toeRot );
	flipValue( ud_heelLift, m_pFlip->ud_heelLift );
	flipValue( ud_walkRoll, m_pFlip->ud_walkRoll );
	flipValue( ud_walkRollAngle, m_pFlip->ud_walkRollAngle );
	flipValue( ud_heelRot, m_pFlip->ud_heelRot );
	flipValue( ud_ballRot, m_pFlip->ud_ballRot );
	flipValue( ud_heelTwist, m_pFlip->ud_heelTwist );
	flipValue( ud_ballTwist, m_pFlip->ud_ballTwist );
	flipValue( ud_toeTwist, m_pFlip->ud_toeTwist );
	flipValue( ud_bank, m_pFlip->ud_bank );
}


MMatrix FkIkCtl::getEachRetargetMatrix( const MMatrix& mtxOrigTrg, const MMatrix& mtxPTrsOrigTrg, const MMatrix& mtxPOrtOrigTrg,
		                        const MMatrix& mtxOrigSrc, const MMatrix& mtxPTrsOrigSrc, const MMatrix& mtxPOrtOrigSrc,
								const MMatrix& mtxSrc )
{
	MMatrix mtxResult;
	MMatrix mtxOrigLocTrsTrg = mtxOrigTrg*mtxPTrsOrigTrg.inverse();
	MMatrix mtxOrigLocTrsSrc = mtxOrigSrc*mtxPTrsOrigSrc.inverse();

	MVector trsTrg = mtxOrigLocTrsTrg[3];
	MVector trsSrc = mtxOrigLocTrsSrc[3];

	double distRate;
	if( trsSrc.length() == 0 )
	{
		distRate = 1;
	}
	else
	{
		distRate = trsTrg.length() / trsSrc.length();
	}

	trsSrc *= distRate;
	MVector offset = trsSrc - trsTrg;

	MMatrix mtxOrigLocOrtTrg	= removePoint( mtxOrigTrg*mtxPOrtOrigTrg.inverse() );
	MMatrix mtxOrigLocOrtSrc	= removePoint( mtxOrigSrc*mtxPOrtOrigSrc.inverse() );

	mtxResult = mtxSrc * mtxOrigLocOrtSrc * mtxOrigLocOrtTrg.inverse();
	mtxResult( 3, 0 ) *= distRate;
	mtxResult( 3, 1 ) *= distRate;
	mtxResult( 3, 2 ) *= distRate;
	mtxResult( 3, 0 ) += offset.x;
	mtxResult( 3, 1 ) += offset.y;
	mtxResult( 3, 2 ) += offset.z;

	return mtxResult;
}


void FkIkCtl::setRetargetValues()
{
	if( !m_enable || !m_pSrc->m_enable ) return;

	MMatrix& mtxShd = m_pSrc->m_mtxShd;
	MMatrix& mtxElb = m_pSrc->m_mtxElb;
	MMatrix& mtxWrt = m_pSrc->m_mtxWrt;
	MMatrix& mtxShdOrig = m_pSrc->m_mtxShdOrig;
	MMatrix& mtxElbOrig = m_pSrc->m_mtxElbOrig;
	MMatrix& mtxWrtOrig = m_pSrc->m_mtxWrtOrig;
	MMatrix& mtxPTrsOrig  = m_pSrc->m_mtxPTrsOrig;
	MMatrix& mtxPOrtOrig  = m_pSrc->m_mtxPOrtOrig;

	m_mtxShdResult = getEachRetargetMatrix( m_mtxShdOrig, m_mtxPTrsOrig, m_mtxPOrtOrig,
			                                        mtxShdOrig,   mtxPTrsOrig,   mtxPOrtOrig,
							                        mtxShd );
	m_mtxElbResult = getEachRetargetMatrix( m_mtxElbOrig, m_mtxShdOrig, m_mtxShdOrig,
			                                        mtxElbOrig,   mtxShdOrig,   mtxShdOrig,
							                        mtxElb );
	m_mtxWrtResult = getEachRetargetMatrix( m_mtxWrtOrig, m_mtxElbOrig, m_mtxElbOrig,
			                                        mtxWrtOrig,   mtxElbOrig,   mtxElbOrig,
							                        mtxWrt );

	if( !m_nameFoot.length() ) return;

	double heelValueY = m_pSrc->ud_heelRot;
	double ballValueY = m_pSrc->ud_heelLift;
	double toeValueY  = m_pSrc->ud_toeRot;
	double tapToeValueY = m_pSrc->ud_tapToe;
	double walkRollAngle = m_pSrc->ud_walkRollAngle;

	double walkRollValue = m_pSrc->ud_walkRoll;
	if( walkRollValue < 0 )
		heelValueY += walkRollValue;
	else if( walkRollValue < walkRollAngle )
		ballValueY += walkRollValue;
	else{
		ballValueY += walkRollAngle*2-walkRollValue;
		toeValueY += (walkRollValue-walkRollAngle );
	}

	double bankValue = m_pSrc->ud_bank;
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
	
	double heelPivValue[3] = { degToRad( m_pSrc->ud_heelTwist ) ,degToRad( heelValueY ), 0 };
	double ballPivValue[3] = { degToRad( m_pSrc->ud_ballTwist ) ,degToRad( m_pSrc->ud_ballRot ), 0 };
	double toePivValue[3]  = { degToRad( m_pSrc->ud_toeTwist  ) ,degToRad( toeValueY ), 0 };
	double tapToeValue[3]  = { 0, degToRad( tapToeValueY ), 0 };
	double ballValue[3]    = { 0, degToRad( ballValueY ), 0 };
	double bankInValue[3]  = { 0, 0, degToRad( bankInValueZ  ) };
	double bankOutValue[3] = { 0, 0, degToRad( bankOutValueZ ) };

	m_trMtxHeelInit.rotateTo( MEulerRotation( heelPivValue ) );
	m_trMtxBallPivInit.rotateTo( MEulerRotation( ballPivValue ) );
	m_trMtxBankInInit.rotateTo( MEulerRotation( bankInValue ) );
	m_trMtxBankOutInit.rotateTo( MEulerRotation( bankOutValue ) );
	m_trMtxToePivInit.rotateTo( MEulerRotation( toePivValue ) );
	m_trMtxBallInit.rotateTo( MEulerRotation( ballValue ) );

	m_mtxAnkleLocalIk_af  = m_trMtxAnkleInit.asMatrix();
	m_mtxAnkleLocalIk_af *= m_trMtxBallInit.asMatrix();
	m_mtxAnkleLocalIk_af *= m_trMtxToeInit.asMatrix();
	m_mtxAnkleLocalIk_af *= m_trMtxToePivInit.asMatrix();
	m_mtxAnkleLocalIk_af *= m_trMtxBankOutInit.asMatrix();
	m_mtxAnkleLocalIk_af *= m_trMtxBankInInit.asMatrix();
	m_mtxAnkleLocalIk_af *= m_trMtxBallPivInit.asMatrix();
	m_mtxAnkleLocalIk_af *= m_trMtxHeelInit.asMatrix();

	heelValueY = m_pBase->ud_heelRot;
	ballValueY = m_pBase->ud_heelLift;
	toeValueY  = m_pBase->ud_toeRot;
	tapToeValueY = m_pBase->ud_tapToe;
	walkRollAngle = m_pBase->ud_walkRollAngle;

	walkRollValue = m_pBase->ud_walkRoll;
	if( walkRollValue < 0 )
		heelValueY += walkRollValue;
	else if( walkRollValue < walkRollAngle )
		ballValueY += walkRollValue;
	else{
		ballValueY += walkRollAngle*2-walkRollValue;
		toeValueY += (walkRollValue-walkRollAngle );
	}

	bankValue = m_pBase->ud_bank;
	
	if( bankValue > 0 ){
		bankInValueZ = bankValue;
		bankOutValueZ = 0;
	}
	else{
		bankInValueZ = 0;
		bankOutValueZ = bankValue;
	}
	
	double heelPivValue_[3] = { degToRad( m_pBase->ud_heelTwist ) ,degToRad( heelValueY ), 0 };
	double ballPivValue_[3] = { degToRad( m_pBase->ud_ballTwist ) ,degToRad( m_pBase->ud_ballRot ), 0 };
	double toePivValue_[3]  = { degToRad( m_pBase->ud_toeTwist  ) ,degToRad( toeValueY ), 0 };
	double tapToeValue_[3]  = { 0, degToRad( tapToeValueY ), 0 };
	double ballValue_[3]    = { 0, degToRad( ballValueY ), 0 };
	double bankInValue_[3]  = { 0, 0, degToRad( bankInValueZ  ) };
	double bankOutValue_[3] = { 0, 0, degToRad( bankOutValueZ ) };

	m_trMtxHeelInit.rotateTo( MEulerRotation( heelPivValue_ ) );
	m_trMtxBallPivInit.rotateTo( MEulerRotation( ballPivValue_ ) );
	m_trMtxBankInInit.rotateTo( MEulerRotation( bankInValue_ ) );
	m_trMtxBankOutInit.rotateTo( MEulerRotation( bankOutValue_ ) );
	m_trMtxToePivInit.rotateTo( MEulerRotation( toePivValue_ ) );
	m_trMtxBallInit.rotateTo( MEulerRotation( ballValue_ ) );

	m_mtxAnkleLocalIk_bf  = m_trMtxAnkleInit.asMatrix();
	m_mtxAnkleLocalIk_bf *= m_trMtxBallInit.asMatrix();
	m_mtxAnkleLocalIk_bf *= m_trMtxToeInit.asMatrix();
	m_mtxAnkleLocalIk_bf *= m_trMtxToePivInit.asMatrix();
	m_mtxAnkleLocalIk_bf *= m_trMtxBankOutInit.asMatrix();
	m_mtxAnkleLocalIk_bf *= m_trMtxBankInInit.asMatrix();
	m_mtxAnkleLocalIk_bf *= m_trMtxBallPivInit.asMatrix();
	m_mtxAnkleLocalIk_bf *= m_trMtxHeelInit.asMatrix();

	//m_mtxWrtResult = m_pSrc->m_mtxFk3 * m_mtxWrtResult;
}


void FkIkCtl::retarget( double weight )
{
	MStatus status;

	if( !m_enable || !m_pSrc->m_enable ) return;

	MFnTransform trIk( m_pathIk );
	MFnTransform trPoleV( m_pathPoleV );
	MFnTransform trSwitch( m_pathSwitch );

	weight *= m_pBase->m_weight;

	double invWeight = 1.0-weight;

	trIk.findPlug( "poleTwist" ).setDouble( m_pSrc->ud_poleTwist*weight + m_pBase->ud_poleTwist*invWeight );
	trIk.findPlug( "length" ).setDouble( m_pSrc->ud_length*weight + m_pBase->ud_length*invWeight );
	trIk.findPlug( "bias" ).setDouble( m_pSrc->ud_bias*weight + m_pBase->ud_bias*invWeight );
	trIk.findPlug( "stretchAble" ).setDouble( m_pSrc->ud_stretchAble );
	trIk.findPlug( "smoothRate" ).setDouble( m_pSrc->ud_smoothRate );
	trPoleV.findPlug( "positionAttach" ).setDouble( m_pSrc->ud_positionAttach*weight + m_pBase->ud_positionAttach*invWeight );

	trSwitch.findPlug( "twist" ).setDouble( m_pSrc->ud_twist*weight + m_pBase->ud_twist*invWeight );
	trSwitch.findPlug( "interpoleSwitch" ).setDouble( m_pSrc->ud_interpoleSwitch );

	if( m_nameFoot.length() )
	{
		trIk.findPlug( "tapToe" ).setDouble( m_pSrc->ud_tapToe*weight + m_pBase->ud_tapToe*invWeight );
		trIk.findPlug( "toeRot" ).setDouble( m_pSrc->ud_toeRot*weight + m_pBase->ud_toeRot*invWeight );
		trIk.findPlug( "heelLift" ).setDouble( m_pSrc->ud_heelLift*weight + m_pBase->ud_heelLift*invWeight );
		trIk.findPlug( "walkRoll" ).setDouble( m_pSrc->ud_walkRoll*weight + m_pBase->ud_walkRoll*invWeight );
		trIk.findPlug( "walkRollAngle" ).setDouble( m_pSrc->ud_walkRollAngle*weight + m_pBase->ud_walkRollAngle*invWeight );

		MFnTransform trFoot( m_pathFoot );

		trFoot.findPlug( "heelRot" ).setDouble( m_pSrc->ud_heelRot*weight + m_pBase->ud_heelRot*invWeight );
		trFoot.findPlug( "ballRot" ).setDouble( m_pSrc->ud_ballRot*weight + m_pBase->ud_ballRot*invWeight );
		trFoot.findPlug( "heelTwist" ).setDouble( m_pSrc->ud_heelTwist*weight + m_pBase->ud_heelTwist*invWeight );
		trFoot.findPlug( "ballTwist" ).setDouble( m_pSrc->ud_ballTwist*weight + m_pBase->ud_ballTwist*invWeight );
		trFoot.findPlug( "toeTwist" ).setDouble( m_pSrc->ud_toeTwist*weight + m_pBase->ud_toeTwist*invWeight );
		trFoot.findPlug( "bank" ).setDouble( m_pSrc->ud_bank*weight + m_pBase->ud_bank*invWeight );

		MTransformationMatrix trMtxFk4 = m_pSrc->m_mtxFk4 *weight + m_pBase->m_mtxFk4 * invWeight;

		MFnTransform trBall;
		trBall.setObject( m_pathBall );
		trBall.setTranslation( trMtxFk4.translation( MSpace::kTransform ), MSpace::kTransform );
		trBall.setRotation( trMtxFk4.rotation(), MSpace::kTransform );
	}
	
	if( m_followEnable )
	{
		if( !m_nameFoot.length() )
		{
			trSwitch.findPlug( "collarFollow" ).setDouble( m_pSrc->ud_collarFollow*weight + m_pBase->ud_collarFollow*invWeight );
			trSwitch.findPlug( "chestFollow"  ).setDouble( m_pSrc->ud_chestFollow*weight  + m_pBase->ud_chestFollow*invWeight );
		}
		trSwitch.findPlug( "hipFollow"    ).setDouble( m_pSrc->ud_hipFollow*weight    + m_pBase->ud_hipFollow*invWeight );
		trSwitch.findPlug( "rootFollow"   ).setDouble( m_pSrc->ud_rootFollow*weight   + m_pBase->ud_rootFollow*invWeight );
		trSwitch.findPlug( "moveFollow"   ).setDouble( m_pSrc->ud_moveFollow          + m_pBase->ud_moveFollow*invWeight );
	}

	MFnTransform tr;
	MMatrix mtxSrcOrientOffset = m_pSrc->m_mtxShdOrientOffset;
	MMatrix mtxShdPOffset = m_pathShd.exclusiveMatrix() * m_pathOrientP.inclusiveMatrixInverse();
	m_mtxShdResult = mtxSrcOrientOffset * mtxShdPOffset.inverse();

	MTransformationMatrix trMtxShd( m_mtxShdResult * weight + m_pBase->m_mtxShd * invWeight );
	MTransformationMatrix trMtxElb( m_mtxElbResult * weight + m_pBase->m_mtxElb * invWeight );
	MTransformationMatrix trMtxWrt( m_mtxWrtResult * weight + m_pBase->m_mtxWrt * invWeight );
	MTransformationMatrix trMtxToe( m_pSrc->m_mtxFk4 * weight + m_pBase->m_mtxFk4 * invWeight );

	tr.setObject( m_pathShdFk );
	tr.setRotation( trMtxShd.rotation(), MSpace::kTransform );
	tr.setObject( m_pathElbFk );
	tr.setTranslation( trMtxElb.translation( MSpace::kTransform ), MSpace::kTransform );
	tr.setRotation( trMtxElb.rotation(), MSpace::kTransform );
	tr.setObject( m_pathWrtFk );
	tr.setTranslation( trMtxWrt.translation( MSpace::kTransform ), MSpace::kTransform );
	tr.setRotation( trMtxWrt.rotation(), MSpace::kTransform );
	status = tr.setObject( m_pathToeFk );
	
	if( status )
	{
		tr.setTranslation( trMtxToe.translation( MSpace::kTransform ), MSpace::kTransform );
		tr.setRotation( trMtxToe.rotation(), MSpace::kTransform );
	}

	MMatrix mtxIkTrs = m_pathWrtFk.inclusiveMatrix();
	MTransformationMatrix trMtxIk( ( m_mtxAnkleLocalIk_bf * invWeight + m_mtxAnkleLocalIk_af * weight ).inverse() * mtxIkTrs );
	MTransformationMatrix trMtxItp( m_pSrc->m_mtxItp * weight + m_pBase->m_mtxItp * invWeight );

	tr.setObject( m_pathIk );
	tr.setTranslation( trMtxIk.translation( MSpace::kTransform ), MSpace::kWorld );
	tr.setRotation( trMtxIk.rotation(), MSpace::kWorld );

	tr.setObject( m_pathItp );
	tr.setRotation( trMtxItp.rotation(), MSpace::kTransform );

	MMatrix mtxShd = m_pathShdFk.inclusiveMatrix();
	MMatrix mtxElb = m_pathElbFk.inclusiveMatrix();
	MMatrix mtxWrt = m_pathWrtFk.inclusiveMatrix();

	MVector poleVWorld = getPoleVectorPosition( mtxShd, mtxElb, mtxWrt, weight );
	tr.setObject( m_pathPoleV );
	tr.setTranslation( poleVWorld, MSpace::kWorld );
}


void FkIkCtl::undoRetarget()
{
	if( !m_enable || !m_pSrc->m_enable ) return;

	MFnTransform trIk( m_pathIk );
	MFnTransform trPoleV( m_pathPoleV );
	MFnTransform trSwitch( m_pathSwitch );

	trIk.findPlug( "poleTwist" ).setDouble( ud_poleTwist );
	trIk.findPlug( "length" ).setDouble( ud_length );
	trIk.findPlug( "bias" ).setDouble( ud_bias );
	trIk.findPlug( "stretchAble" ).setDouble( ud_stretchAble );
	trIk.findPlug( "smoothRate" ).setDouble( ud_smoothRate );
	trPoleV.findPlug( "positionAttach" ).setDouble( ud_positionAttach );
;
	trSwitch.findPlug( "twist" ).setDouble( ud_twist );
	trSwitch.findPlug( "interpoleSwitch" ).setDouble( ud_interpoleSwitch );

	if( m_nameFoot.length() )
	{
		trIk.findPlug( "tapToe" ).setDouble( ud_tapToe );
		trIk.findPlug( "toeRot" ).setDouble( ud_toeRot );
		trIk.findPlug( "heelLift" ).setDouble( ud_heelLift );
		trIk.findPlug( "walkRoll" ).setDouble( ud_walkRoll );
		trIk.findPlug( "walkRollAngle" ).setDouble( ud_walkRollAngle );

		MFnTransform trFoot( m_pathFoot );

		trFoot.findPlug( "heelRot" ).setDouble( ud_heelRot );
		trFoot.findPlug( "ballRot" ).setDouble( ud_ballRot );
		trFoot.findPlug( "heelTwist" ).setDouble( ud_heelTwist );
		trFoot.findPlug( "ballTwist" ).setDouble( ud_ballTwist );
		trFoot.findPlug( "toeTwist" ).setDouble( ud_toeTwist );
		trFoot.findPlug( "bank" ).setDouble( ud_bank );

		MTransformationMatrix trMtxFk4 = m_mtxFk4;

		MFnTransform trBall;
		trBall.setObject( m_pathBall );
		trBall.setTranslation( trMtxFk4.translation( MSpace::kTransform ), MSpace::kTransform );
		trBall.setRotation( trMtxFk4.rotation(), MSpace::kTransform );
	}

	if( m_followEnable )
	{
		if( !m_nameFoot.length() )
		{
			trSwitch.findPlug( "collarFollow" ).setDouble( ud_collarFollow );
			trSwitch.findPlug( "chestFollow"  ).setDouble( ud_chestFollow );
		}
		trSwitch.findPlug( "hipFollow"    ).setDouble( ud_hipFollow );
		trSwitch.findPlug( "rootFollow"   ).setDouble( ud_rootFollow );
		trSwitch.findPlug( "moveFollow"   ).setDouble( ud_moveFollow );
	}

	MTransformationMatrix trMtxShd( m_mtxShd );
	MTransformationMatrix trMtxElb( m_mtxElb );
	MTransformationMatrix trMtxWrt( m_mtxWrt );
	MTransformationMatrix trMtxIk(  m_mtxIk );
	MTransformationMatrix trMtxPoleV( m_mtxPoleV );
	
	MFnTransform tr;
	tr.setObject( m_pathShdFk );
	tr.setRotation( trMtxShd.rotation() );
	tr.setObject( m_pathElbFk );
	tr.setTranslation( trMtxElb.translation( MSpace::kTransform ), MSpace::kTransform );
	tr.setRotation( trMtxElb.rotation() );
	tr.setObject( m_pathWrtFk );
	tr.setTranslation( trMtxWrt.translation( MSpace::kTransform ), MSpace::kTransform );
	tr.setRotation( trMtxWrt.rotation() );

	tr.setObject( m_pathIk );
	tr.setTranslation( trMtxIk.translation( MSpace::kTransform ), MSpace::kWorld );
	tr.setRotation( trMtxIk.rotation(), MSpace::kWorld );
	tr.setObject( m_pathPoleV );
	tr.setTranslation( trMtxPoleV.translation( MSpace::kTransform ), MSpace::kWorld );
}


MVector FkIkCtl::getPoleVectorPosition( const MMatrix& mtxShd, const MMatrix& mtxElb, const MMatrix& mtxWrt, double weight )
{
	double value = ud_positionAttach;
	double invValue = 1.0 - value;

	MVector vectorShd = mtxShd[3];
	MVector vectorElb = mtxElb[3];
	MVector vectorWrt = mtxWrt[3];

	MVector vectorAim   = vectorWrt - vectorShd;
	MVector vectorPoleV = vectorElb - vectorShd;
	MVector vectorProj  = vectorAim * vectorPoleV * vectorAim /pow( vectorAim.length(), 2 );
	MVector vectorVert  = vectorPoleV - vectorProj;
	MVector vectorCross = vectorAim ^ vectorVert;

	double angle = degToRad( m_pSrc->ud_poleTwist * weight );
	if( MVector( mtxElb[0] ) * ( vectorWrt-vectorElb ) > 0 )
		angle *= -1;
	if( m_nameFoot.length() )
	{
		angle *= -1;
	}

	double upperDist = vectorPoleV.length();
	double lowerDist = (vectorElb - vectorWrt).length();
	double allDist = upperDist + lowerDist * 0.75;

	MVector originPoleV = vectorVert.normal()*allDist;
	MVector attachPoleV = vectorVert;

	double setaSin = sin( angle );
	double setaCos = cos( angle );

	originPoleV = vectorCross*( originPoleV.length() / vectorCross.length() * setaSin ) + originPoleV * setaCos;

	MVector resultPoleV = originPoleV * invValue + attachPoleV * value;

	return vectorShd + vectorProj + resultPoleV;
}


MMatrix& FkIkCtl::removePoint( MMatrix mtx )
{
	mtx( 3,0 ) = 0.0;
	mtx( 3,1 ) = 0.0;
	mtx( 3,2 ) = 0.0;
	return mtx;
}


void FkIkCtl::getBlend( const FkIkCtl& first, const FkIkCtl& second, float wFirst, float wSecond )
{
	m_enable = first.m_enable;

	m_mtxShd = first.m_mtxShd * wFirst + second.m_mtxShd * wSecond;
	m_mtxElb = first.m_mtxElb * wFirst + second.m_mtxElb * wSecond;
	m_mtxWrt = first.m_mtxWrt * wFirst + second.m_mtxWrt * wSecond;

	m_mtxIk  = first.m_mtxIk * wFirst  + second.m_mtxIk * wSecond;
	m_mtxItp = first.m_mtxItp * wFirst + second.m_mtxItp * wSecond;
	m_mtxPoleV = first.m_mtxPoleV * wFirst + second.m_mtxPoleV * wSecond;
	m_mtxIkPOrt = first.m_mtxIkPOrt * wFirst + second.m_mtxIkPOrt * wSecond;
	m_mtxIkPTrs = first.m_mtxIkPTrs * wFirst + second.m_mtxIkPTrs * wSecond;

	m_mtxShdOrig = first.m_mtxShdOrig * wFirst + second.m_mtxShdOrig * wSecond;
	m_mtxElbOrig = first.m_mtxElbOrig * wFirst + second.m_mtxElbOrig * wSecond;
	m_mtxWrtOrig = first.m_mtxWrtOrig * wFirst + second.m_mtxWrtOrig * wSecond;

	m_mtxPoleVOrig = first.m_mtxPoleVOrig * wFirst + second.m_mtxPoleVOrig * wSecond;
	m_mtxPTrsOrig  = first.m_mtxPTrsOrig  * wFirst + second.m_mtxPTrsOrig  * wSecond;
	m_mtxPOrtOrig  = first.m_mtxPOrtOrig  * wFirst + second.m_mtxPOrtOrig  * wSecond;

	ud_handScale = first.ud_handScale * wFirst + second.ud_handScale * wSecond;
	ud_twist  = first.ud_twist  * wFirst + second.ud_twist  * wSecond;
	ud_interpoleSwitch  = first.ud_interpoleSwitch  * wFirst + second.ud_interpoleSwitch  * wSecond;
	ud_collarFollow = first.ud_collarFollow * wFirst + second.ud_collarFollow * wSecond;
	ud_chestFollow  = first.ud_chestFollow * wFirst  + second.ud_chestFollow * wSecond;
	ud_hipFollow    = first.ud_hipFollow * wFirst    + second.ud_hipFollow  * wSecond;
	ud_rootFollow   = first.ud_rootFollow * wFirst   + second.ud_rootFollow * wSecond;
	ud_moveFollow   = first.ud_moveFollow * wFirst   + second.ud_moveFollow * wSecond;

	ud_poleTwist = first.ud_poleTwist * wFirst + second.ud_poleTwist * wSecond;
	ud_length  = first.ud_length  * wFirst + second.ud_length  * wSecond;
	ud_bias  = first.ud_bias  * wFirst + second.ud_bias  * wSecond;
	ud_stretchAble  = first.ud_stretchAble  * wFirst + second.ud_stretchAble  * wSecond;
	ud_smoothRate   = first.ud_smoothRate  * wFirst + second.ud_smoothRate  * wSecond;
	ud_positionAttach  = first.ud_positionAttach  * wFirst + second.ud_positionAttach * wSecond;
	
	m_mtxShdOrientOffset = first.m_mtxShdOrientOffset * wFirst + second.m_mtxShdOrientOffset * wSecond;

	if( !first.m_nameFoot.length() ) return;
	m_mtxAnkleLocalIk_bf = first.m_mtxAnkleLocalIk_bf * wFirst + second.m_mtxAnkleLocalIk_bf * wSecond;
	m_mtxAnkleLocalIk_af = first.m_mtxAnkleLocalIk_af * wFirst + second.m_mtxAnkleLocalIk_af * wSecond;

	m_mtxBall = first.m_mtxBall * wFirst + second.m_mtxBall * wSecond;
	m_mtxToe  = first.m_mtxToe * wFirst  + second.m_mtxToe * wSecond;

	m_mtxCu3_orig = first.m_mtxCu3_orig * wFirst + second.m_mtxCu3_orig * wSecond;
	m_mtxCu4_orig = first.m_mtxCu4_orig * wFirst  + second.m_mtxCu4_orig * wSecond;
	m_mtxFk3 = first.m_mtxFk3 * wFirst + second.m_mtxFk3 * wSecond;
	m_mtxFk4 = first.m_mtxFk4 * wFirst + second.m_mtxFk4 * wSecond;

	ud_kneeAutoAngle = first.ud_kneeAutoAngle * wFirst + second.ud_kneeAutoAngle * wSecond;
	ud_tapToe  = first.ud_tapToe  * wFirst + second.ud_tapToe  * wSecond;
	ud_toeRot  = first.ud_toeRot  * wFirst + second.ud_toeRot  * wSecond;
	ud_heelLift  = first.ud_heelLift  * wFirst + second.ud_heelLift  * wSecond;
	ud_walkRoll   = first.ud_walkRoll  * wFirst + second.ud_walkRoll  * wSecond;
	ud_walkRollAngle  = first.ud_walkRollAngle  * wFirst + second.ud_walkRollAngle  * wSecond;

	ud_heelRot = first.ud_heelRot * wFirst + second.ud_heelRot * wSecond;
	ud_ballRot  = first.ud_ballRot  * wFirst + second.ud_ballRot  * wSecond;
	ud_heelTwist  = first.ud_heelTwist  * wFirst + second.ud_heelTwist  * wSecond;
	ud_ballTwist  = first.ud_ballTwist  * wFirst + second.ud_ballTwist  * wSecond;
	ud_toeTwist   = first.ud_toeTwist  * wFirst + second.ud_toeTwist  * wSecond;
	ud_bank  = first.ud_bank  * wFirst + second.ud_bank  * wSecond;
}
/*
void FkIkCtl::connectSelf()
{
	m_pBase = this;
}*/