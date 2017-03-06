#include "controlerSet.h"

bool     CtlSet::m_rootMoveEnable = true;
bool     CtlSet::m_rootKeepHorizon = false;
bool     CtlSet::m_rootKeepCurrent = false;


CtlSet::CtlSet()
{
	Ctl Root( "Root_CTL", "Root_Init", "All_Init", "" );
	Ctl Fly( "Fly_CTL", "Root_Init", "All_Init", "" );
	Ctl Hip( "Hip_CTL", "Root_Init", "", "" );
	Ctl Torso( "TorsoRotate_CTL", "Root_Init", "", "" );
	Ctl Chest( "Chest_CTL", "Chest_Init", "Root_Init", "" );
	Ctl Waist( "Waist_CTL", "Waist_Init", "", "" );
	Ctl ChestMove( "ChestMove_CTL", "Chest_Init", "", "" );

	Fly.appendUdAttr( "pivTx" ); Fly.appendUdAttr( "pivTy" ); Fly.appendUdAttr( "pivTz" );
	Fly.appendUdAttr( "pivRx" ); Fly.appendUdAttr( "pivRy" ); Fly.appendUdAttr( "pivRz" );
	Fly.appendUdAttr( "blend" );
	Chest.appendUdAttr( "squash" ); Chest.appendUdAttr( "forceScale" );
	Hip.appendUdAttr( "legFollowL" ); Hip.appendUdAttr( "legFollowR" );

	Ctl Collar_L_( "Collar_L_CTL", "Collar_L_Init", "","" );
	Ctl Shoulder_L_( "Shoulder_L_CTL", "Shoulder_L_Init", "Collar_L_Init","" );
	Collar_L_.appendUdAttr( "chestFollow" ); Collar_L_.appendUdAttr( "rootFollow" );
	Collar_L_.appendUdAttr( "flyFollow" ); Collar_L_.appendUdAttr( "moveFollow" );
	Shoulder_L_.appendUdAttr( "twistCollar" ); Shoulder_L_.appendUdAttr( "twistShoulder" );

	Ctl Collar_R_( "Collar_R_CTL", "Collar_R_Init", "","" );
	Ctl Shoulder_R_( "Shoulder_R_CTL", "Shoulder_R_Init", "Collar_R_Init","" );
	Collar_R_.appendUdAttr( "chestFollow" ); Collar_R_.appendUdAttr( "rootFollow" );
	Collar_R_.appendUdAttr( "flyFollow" ); Collar_R_.appendUdAttr( "moveFollow" );
	Shoulder_R_.appendUdAttr( "twistCollar" ); Shoulder_R_.appendUdAttr( "twistShoulder" );

	Ctl Neck( "Neck_CTL", "Neck_Init", "", "" );
	Ctl Head( "Head_CTL", "Head_Init", "Neck_Init", "" );
	Ctl Eye( "Eye_CTL", "EyeAimPiv_Init", "", "" );
	Head.appendUdAttr( "neckFollow" ); Head.appendUdAttr( "chestFollow" );
	Head.appendUdAttr( "rootFollow" ); Head.appendUdAttr( "flyFollow" ); Head.appendUdAttr( "moveFollow" );
	Eye.appendUdAttr( "chestFollow" ); Eye.appendUdAttr( "rootFollow" );
	Eye.appendUdAttr( "flyFollow" );   Eye.appendUdAttr( "moveFollow" );

	/*
	MStringArray namesRootDistTarget;
	namesRootDistTarget.append( "Knee_L_Init" );
	namesRootDistTarget.append( "Ankle_L_Init" );
	namesRootDistTarget.append( "Ankle_R_Init" );
	namesRootDistTarget.append( "Ankle_R_Init" );
	Fly.specifyRootDistObjects( namesRootDistTarget );
	Root.specifyRootDistObjects( namesRootDistTarget );
	
	MStringArray namesTorsoDistTarget;
	namesTorsoDistTarget.append( "Waist_Init" );
	namesTorsoDistTarget.append( "Chest_Init" );
	Hip.specifyDistObjects( namesTorsoDistTarget );
	Torso.specifyDistObjects( namesTorsoDistTarget );
	Chest.specifyDistObjects( namesTorsoDistTarget );
	Waist.specifyDistObjects( namesTorsoDistTarget );
	ChestMove.specifyDistObjects( namesTorsoDistTarget );

	MStringArray namesCollar_L_DistTarget;
	namesCollar_L_DistTarget.append( "Shoulder_L_Init" );
	Collar_L_.specifyDistObjects( namesCollar_L_DistTarget );

	MStringArray namesCollar_R_DistTarget;
	namesCollar_R_DistTarget.append( "Shoulder_R_Init" );
	Collar_R_.specifyDistObjects( namesCollar_R_DistTarget );

	MStringArray namesHeadDistTarget;
	namesHeadDistTarget.append( "NeckMiddle_Init" );
	namesHeadDistTarget.append( "Neck_Init" );
	Neck.specifyDistObjects( namesHeadDistTarget );
	Head.specifyDistObjects( namesHeadDistTarget );

	MStringArray namesEyeDistTarget;
	namesEyeDistTarget.append( "Eye_L_Init" );
	namesEyeDistTarget.append( "Eye_R_Init" );
	namesEyeDistTarget.append( "EyeAimPiv_Init" );
	Eye.specifyEyeDistObjects( namesEyeDistTarget );
	*/

	appendData( Root );appendData( Fly );appendData( Hip );
	appendData( Torso );appendData( Chest );appendData( Waist );appendData( ChestMove );
	appendData( Neck );appendData( Head );appendData( Eye );
	appendData( Collar_L_ );appendData( Shoulder_L_ );appendData( Collar_R_ );appendData( Shoulder_R_ );
	m_ctls[10].m_pFlip = &m_ctls[12]; m_ctls[11].m_pFlip = &m_ctls[13];
	
	FkIkCtl arm_L_fkIk;
	FkIkCtl arm_R_fkIk;
	FkIkCtl leg_L_fkIk;
	FkIkCtl leg_R_fkIk;

	arm_L_fkIk.getOrigName( "Shoulder_L_Init", "Elbow_L_Init", "Wrist_L_Init",
		                    "ArmPoleV_L_Init", "Collar_L_Init", "Chest_Init" );
	arm_L_fkIk.getCuName( "Arm_L_CU0", "Arm_L_CU1", "Arm_L_CU2" );
	arm_L_fkIk.getFkName( "Arm_L_FK0_CTL", "Arm_L_FK1_CTL", "Arm_L_FK2_CTL" );
	arm_L_fkIk.getIkName( "Arm_L_IK_CTL", "Arm_L_IkItp_CTL", "Arm_L_PoleV_CTL", "Arm_L_Switch_CTL", "Arm_L_Set", "ChestMove_CTL" );
	arm_L_fkIk.getOrientPName( "ChestMove_CTL" );

	arm_R_fkIk.getOrigName( "Shoulder_R_Init", "Elbow_R_Init", "Wrist_R_Init",
		                    "ArmPoleV_R_Init", "Collar_R_Init", "Chest_Init" );
	arm_R_fkIk.getCuName( "Arm_R_CU0", "Arm_R_CU1", "Arm_R_CU2" );
	arm_R_fkIk.getFkName( "Arm_R_FK0_CTL", "Arm_R_FK1_CTL", "Arm_R_FK2_CTL" );
	arm_R_fkIk.getIkName( "Arm_R_IK_CTL", "Arm_R_IkItp_CTL", "Arm_R_PoleV_CTL", "Arm_R_Switch_CTL", "Arm_R_Set", "ChestMove_CTL" );
	arm_R_fkIk.getOrientPName( "ChestMove_CTL" );

	leg_L_fkIk.getOrigName( "Hip_L_Init", "Knee_L_Init", "Ankle_L_Init",
		                    "LegPoleV_L_Init", "Root_Init" );
	leg_L_fkIk.getCuName( "Leg_L_CU0", "Leg_L_CU1", "Leg_L_CU2", "Leg_L_CU3", "Leg_L_CU4" );
	leg_L_fkIk.getFkName( "Leg_L_FK0_CTL", "Leg_L_FK1_CTL", "Leg_L_FK2_CTL", "Leg_L_FK3_CTL" );
	leg_L_fkIk.getIkName( "Leg_L_IK_CTL", "Leg_L_IkItp_CTL", "Leg_L_PoleV_CTL", "Leg_L_Switch_CTL", "Leg_L_Set", "Root_CTL" );
	leg_L_fkIk.getFootName( "Leg_L_Foot_IK_CTL" );
	leg_L_fkIk.getOrientPName( "Root_CTL" );

	leg_R_fkIk.getOrigName( "Hip_R_Init", "Knee_R_Init", "Ankle_R_Init",
		                    "LegPoleV_R_Init", "Root_Init" );
	leg_R_fkIk.getCuName( "Leg_R_CU0", "Leg_R_CU1", "Leg_R_CU2", "Leg_R_CU3", "Leg_R_CU4" );
	leg_R_fkIk.getFkName( "Leg_R_FK0_CTL", "Leg_R_FK1_CTL", "Leg_R_FK2_CTL", "Leg_R_FK3_CTL" );
	leg_R_fkIk.getIkName( "Leg_R_IK_CTL", "Leg_R_IkItp_CTL", "Leg_R_PoleV_CTL", "Leg_R_Switch_CTL", "Leg_R_Set", "Root_CTL" );
	leg_R_fkIk.getFootName( "Leg_R_Foot_IK_CTL" );
	leg_R_fkIk.getOrientPName( "Root_CTL" );

	appendData( arm_L_fkIk );appendData( arm_R_fkIk );appendData( leg_L_fkIk );appendData( leg_R_fkIk );
	m_fkIkCtls[0].m_pFlip = &m_fkIkCtls[1];
	m_fkIkCtls[2].m_pFlip = &m_fkIkCtls[3];

	FingerCtl thumb_L_Ctl( "Thumb*_L_CTL", "Thumb*_L_Init" );
	FingerCtl index_L_Ctl( "Index*_L_CTL", "Index*_L_Init" );
	FingerCtl middle_L_Ctl( "Middle*_L_CTL", "Middle*_L_Init" );
	FingerCtl ring_L_Ctl( "Ring*_L_CTL", "Ring*_L_Init" );
	FingerCtl pinky_L_Ctl( "Pinky*_L_CTL", "Pinky*_L_Init" );

	FingerCtl thumb_R_Ctl( "Thumb*_R_CTL", "Thumb*_R_Init" );
	FingerCtl index_R_Ctl( "Index*_R_CTL", "Index*_R_Init" );
	FingerCtl middle_R_Ctl( "Middle*_R_CTL", "Middle*_R_Init" );
	FingerCtl ring_R_Ctl( "Ring*_R_CTL", "Ring*_R_Init" );
	FingerCtl pinky_R_Ctl( "Pinky*_R_CTL", "Pinky*_R_Init" );

	appendData( thumb_L_Ctl ); appendData( index_L_Ctl ); appendData( middle_L_Ctl ); appendData( ring_L_Ctl ); appendData( pinky_L_Ctl );
	appendData( thumb_R_Ctl ); appendData( index_R_Ctl ); appendData( middle_R_Ctl ); appendData( ring_R_Ctl ); appendData( pinky_R_Ctl );
	m_fingerCtls[0].m_pFlip = &m_fingerCtls[5];
	m_fingerCtls[1].m_pFlip = &m_fingerCtls[6];
	m_fingerCtls[2].m_pFlip = &m_fingerCtls[7];
	m_fingerCtls[3].m_pFlip = &m_fingerCtls[8];
	m_fingerCtls[4].m_pFlip = &m_fingerCtls[9];

	for( int i=0; i< m_fingerCtls.length(); i++ )
	{
		m_fingerCtls[i].setLength( 4 );
	}
	m_fingerCtls[0].setLength( 3 ); m_fingerCtls[5].setLength( 3 );

	m_frameOffset = 0.0f;
}


void CtlSet::reset()
{
	m_ctls.setLength( 0 );
	m_fkIkCtls.setLength( 0 );
	m_fingerCtls.setLength( 0 );
}

void CtlSet::appendData( const Ctl& data )
{
	m_ctls.append( data );
}

void CtlSet::appendData( const FkIkCtl& data )
{
	m_fkIkCtls.append( data );
}

void CtlSet::appendData( const FingerCtl& data )
{
	m_fingerCtls.append( data );
}

void CtlSet::connectBase( CtlSet* pCtlSetBase )
{
	for( int i=0; i< m_ctls.length(); i++ )
	{
		m_ctls[i].m_pBase = &pCtlSetBase->m_ctls[i];
	}

	for( int i=0; i< m_fkIkCtls.length(); i++ )
	{
		m_fkIkCtls[i].m_pBase = &pCtlSetBase->m_fkIkCtls[i];
	}

	for( int i=0; i< m_fingerCtls.length(); i++ )
	{
		m_fingerCtls[i].m_pBase = &pCtlSetBase->m_fingerCtls[i];
	}
}

void CtlSet::connectSource( CtlSet* pCtlSetSrc )
{
	for( int i=0; i< m_ctls.length(); i++ )
		m_ctls[i].m_pSrc = &(pCtlSetSrc->m_ctls[i]);

	for( int i=0; i< m_fkIkCtls.length(); i++ )
		m_fkIkCtls[i].m_pSrc = &(pCtlSetSrc->m_fkIkCtls[i]);

	for( int i=0; i< m_fingerCtls.length(); i++ )
		m_fingerCtls[i].m_pSrc = &(pCtlSetSrc->m_fingerCtls[i]);

	m_pSrc = pCtlSetSrc;
}

MStatus CtlSet::setBaseData( MString namespaceIn, bool isSrc )
{
	MStatus status;

	m_namespace = namespaceIn;

	MSelectionList selList;
	selList.add( namespaceIn + "Root_GRP" );

	selList.getDagPath( 0, m_pathRootGrp );

	for( int i=0; i< m_ctls.length(); i++ )
	{
		status = m_ctls[i].setData( namespaceIn );

		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	for( int i=0; i< m_fkIkCtls.length(); i++ )
	{
		status = m_fkIkCtls[i].setData( namespaceIn );
		CHECK_MSTATUS_AND_RETURN_IT( status );
		m_fkIkCtls[i].getUdAttr();
	}

	for( int i=0; i< m_fingerCtls.length(); i++ )
	{
		status = m_fingerCtls[i].setData( namespaceIn );
		CHECK_MSTATUS_AND_RETURN_IT( status );
	}

	return MS::kSuccess;
}

void CtlSet::updateRootMatrix()
{
	m_mtxRoot = m_pathRootGrp.inclusiveMatrix()*m_pathRootGrp.exclusiveMatrixInverse();
	m_mtxRoot( 3,0 ) = 0;
	m_mtxRoot( 3,1 ) = 0;
	m_mtxRoot( 3,2 ) = 0;
	m_mtxDirection = getDirectionMatrix( m_mtxRoot );
}

void CtlSet::updateCtlMatrix()
{
	for( int i=0; i< m_ctls.length(); i++ )
		m_ctls[i].updateCtlMatrix();

	for( int i=0; i< m_fkIkCtls.length(); i++ )
		m_fkIkCtls[i].updateCtlMatrix();

	for( int i=0; i< m_fingerCtls.length(); i++ )
		m_fingerCtls[i].updateCtlMatrix();
}

MMatrix CtlSet::getDirectionMatrix( MMatrix mtx )
{
	MVector vectorZ = mtx[2];
	vectorZ.y = 0.0;
	vectorZ.normalize();

	MVector vectorY( 0, 1, 0 );
	MVector vectorX = vectorY ^ vectorZ;

	mtx( 0, 0 ) = vectorX.x;mtx( 0, 1 ) = vectorX.y;mtx( 0, 2 ) = vectorX.z;
	mtx( 1, 0 ) = vectorY.x;mtx( 1, 1 ) = vectorY.y;mtx( 1, 2 ) = vectorY.z;
	mtx( 2, 0 ) = vectorZ.x;mtx( 2, 1 ) = vectorZ.y;mtx( 2, 2 ) = vectorZ.z;

	return mtx;
}

void CtlSet::flip()
{
	for( int i=0; i< m_ctls.length()-2; i++ )
		m_ctls[i].flip();
	for( int i=0; i< m_fkIkCtls.length(); i++ )
		m_fkIkCtls[i].flip();
	for( int i=0; i< m_fingerCtls.length(); i++ )
		m_fingerCtls[i].flip();
}

void CtlSet::setRetargetValues()
{
	for( int i=0; i< m_ctls.length(); i++ )
	{
		m_ctls[i].setRetargetValues();

		if( i == 0 || i==1 )
		{
			if( m_rootKeepCurrent )
			{
				m_ctls[i].m_mtxResult *= m_pSrc->m_mtxRoot.inverse()*m_mtxRoot;
			}
			else if( m_rootKeepHorizon )
			{
				double height = m_ctls[i].m_mtxResult( 3, 1 );
				m_ctls[i].m_mtxResult *= m_pSrc->m_mtxDirection.inverse()*m_mtxDirection;
				m_ctls[i].m_mtxResult( 3, 1 ) = height;
			}

			if( !m_rootMoveEnable )
			{
				m_ctls[i].m_mtxResult( 3, 0 ) = m_ctls[i].m_mtx( 3, 0 );
				m_ctls[i].m_mtxResult( 3, 1 ) = m_ctls[i].m_mtx( 3, 1 );
				m_ctls[i].m_mtxResult( 3, 2 ) = m_ctls[i].m_mtx( 3, 2 );
			}
		}
	}
	for( int i=0; i< m_fkIkCtls.length(); i++ )
		m_fkIkCtls[i].setRetargetValues();

	for( int i=0; i< m_fingerCtls.length(); i++ )
		m_fingerCtls[i].setRetargetValues();
}

void CtlSet::retarget( double weight )
{
	for( int i=0; i< m_ctls.length(); i++ )
		m_ctls[i].retarget( weight );
		
	for( int i=0; i< m_fkIkCtls.length(); i++ )
		m_fkIkCtls[i].retarget( weight );

	for( int i=0; i< m_fingerCtls.length(); i++ )
		m_fingerCtls[i].retarget( weight );
}

void CtlSet::undoRetarget()
{
	for( int i=0; i< m_ctls.length(); i++ )
		m_ctls[i].undoRetarget();
		
	for( int i=0; i< m_fkIkCtls.length(); i++ )
		m_fkIkCtls[i].undoRetarget();

	for( int i=0; i< m_fingerCtls.length(); i++ )
		m_fingerCtls[i].undoRetarget();
}

void CtlSet::setAllEnable()
{
	for( int i=0; i< m_ctls.length(); i++ )
		m_ctls[i].m_enable = true;
		
	for( int i=0; i< m_fkIkCtls.length(); i++ )
		m_fkIkCtls[i].m_enable = true;

	for( int i=0; i< m_fingerCtls.length(); i++ )
		m_fingerCtls[i].m_enable = true;
}

void CtlSet::setAllDisable()
{
	for( int i=0; i< m_ctls.length(); i++ )
		m_ctls[i].m_enable = false;
		
	for( int i=0; i< m_fkIkCtls.length(); i++ )
		m_fkIkCtls[i].m_enable = false;

	for( int i=0; i< m_fingerCtls.length(); i++ )
		m_fingerCtls[i].m_enable = false;
}

CtlSet& CtlSet::operator=( const CtlSet& other )
{
	m_ctls.setLength( other.m_ctls.length() );
	for( int i=0; i<other.m_ctls.length(); i++ )
		m_ctls[i] = other.m_ctls[i];
	m_fkIkCtls.setLength( other.m_fkIkCtls.length() );
	for( int i=0; i<other.m_fkIkCtls.length(); i++ )
		m_fkIkCtls[i] = other.m_fkIkCtls[i];
	m_fingerCtls.setLength( other.m_fingerCtls.length() );
	for( int i=0; i<other.m_fingerCtls.length(); i++ )
		m_fingerCtls[i] = other.m_fingerCtls[i];

	m_pathRootGrp= other.m_pathRootGrp;

	m_mtxRoot = other.m_mtxRoot;
	m_mtxDirection = other.m_mtxDirection;

	m_namespace = other.m_namespace;

	return *this;
}

void CtlSet::getBlend( const CtlSet& first, const CtlSet& second, float wFirst, float wSecond )
{
	for( int i=0; i< m_ctls.length(); i++ )
	{
		m_ctls[i].getBlend( first.m_ctls[i], second.m_ctls[i], wFirst, wSecond );
	}
	for( int i=0; i< m_fkIkCtls.length(); i++ )
	{
		m_fkIkCtls[i].getBlend( first.m_fkIkCtls[i], second.m_fkIkCtls[i], wFirst, wSecond );
	}
	for( int i=0; i< m_fingerCtls.length(); i++ )
	{
		m_fingerCtls[i].getBlend( first.m_fingerCtls[i], second.m_fingerCtls[i], wFirst, wSecond );
	}
}