#include "enableSet.h"



void EnableSet::setDefaultRoot()
{
	moveEnable(false);
	keepCurrent(false);
	keepHorizon(true);
}


void EnableSet::allEnable( bool value )
{
	if( value )
		m_pCtlSet->setAllEnable();
	else
		m_pCtlSet->setAllDisable();
}


void EnableSet::getCtlSet( CtlSet* pTarget )
{
	m_pCtlSet = pTarget;
}


void EnableSet::moveEnable( bool value )
{
	m_pCtlSet->m_rootMoveEnable = value;
}


void EnableSet::keepCurrent( bool value )
{
	m_pCtlSet->m_rootKeepCurrent = value;
}


void EnableSet::keepHorizon( bool value )
{
	m_pCtlSet->m_rootKeepHorizon  = value;
}


void EnableSet::bodyEnable( bool value )
{
	m_pCtlSet->m_ctls[ Root ].m_enable = value;
	m_pCtlSet->m_ctls[ Fly ].m_enable = value;
	m_pCtlSet->m_ctls[ Hip ].m_enable = value;
	m_pCtlSet->m_ctls[ Torso ].m_enable = value;
	m_pCtlSet->m_ctls[ Chest ].m_enable = value;
	m_pCtlSet->m_ctls[ Waist ].m_enable = value;
	m_pCtlSet->m_ctls[ ChestMove ].m_enable = value;
	m_pCtlSet->m_ctls[ Collar_L_ ].m_enable = value;
	m_pCtlSet->m_ctls[ Shoulder_L_ ].m_enable = value;
	m_pCtlSet->m_ctls[ Collar_R_ ].m_enable = value;
	m_pCtlSet->m_ctls[ Shoulder_R_ ].m_enable = value;
}


void EnableSet::headEnable( bool value )
{
	m_pCtlSet->m_ctls[ Eye ].m_enable = value;
	m_pCtlSet->m_ctls[ Neck ].m_enable = value;
	m_pCtlSet->m_ctls[ Head ].m_enable = value;
}


void EnableSet::arm_L_Enable( bool value )
{
	m_pCtlSet->m_fkIkCtls[ arm_L_ ].m_enable = value;
}


void EnableSet::arm_R_Enable( bool value )
{
	m_pCtlSet->m_fkIkCtls[ arm_R_ ].m_enable = value;
}


void EnableSet::leg_L_Enable( bool value )
{
	m_pCtlSet->m_fkIkCtls[ leg_L_ ].m_enable = value;
}


void EnableSet::leg_R_Enable( bool value )
{
	m_pCtlSet->m_fkIkCtls[ leg_R_ ].m_enable = value;
}


void EnableSet::hand_L_Enable( bool value )
{
	m_pCtlSet->m_fingerCtls[ thumb_L_ ].m_enable = value;
	m_pCtlSet->m_fingerCtls[ index_L_ ].m_enable = value;
	m_pCtlSet->m_fingerCtls[ middle_L_ ].m_enable = value;
	m_pCtlSet->m_fingerCtls[ ring_L_ ].m_enable = value;
	m_pCtlSet->m_fingerCtls[ pinky_L_ ].m_enable = value;
}


void EnableSet::hand_R_Enable( bool value )
{
	m_pCtlSet->m_fingerCtls[ thumb_R_ ].m_enable = value;
	m_pCtlSet->m_fingerCtls[ index_R_ ].m_enable = value;
	m_pCtlSet->m_fingerCtls[ middle_R_ ].m_enable = value;
	m_pCtlSet->m_fingerCtls[ ring_R_ ].m_enable = value;
	m_pCtlSet->m_fingerCtls[ pinky_R_ ].m_enable = value;
}


void EnableSet::enablePart( MString namePart, bool value )
{
	MString nameLower = namePart.toLowerCase();
	if( nameLower == "all" )
	{
		bodyEnable( value );
		headEnable( value );
		arm_L_Enable( value );
		arm_R_Enable( value );
		leg_L_Enable( value );
		leg_R_Enable( value );
		hand_L_Enable( value );
		hand_R_Enable( value );
	}
	if( nameLower == "body" )
		bodyEnable( value );
	else if( nameLower == "head" )
		headEnable( value );
	else if( nameLower == "arml" )
		arm_L_Enable( value );
	else if( nameLower == "armr" )
		arm_R_Enable( value );
	else if( nameLower == "legl" )
		leg_L_Enable( value );
	else if( nameLower == "legr" )
		leg_R_Enable( value );
	else if( nameLower == "handl" )
		hand_L_Enable( value );
	else if( nameLower == "handr" )
		hand_R_Enable( value );
}


void EnableSet::enableCtl( MString nameCtl, bool value )
{
	for( int i=0; i< m_pCtlSet->m_ctls.length(); i++ )
	{
		if( m_pCtlSet->m_ctls[i].m_name == nameCtl )
		{
			m_pCtlSet->m_ctls[i].m_enable = value;
			if( i==0 )
			{
				m_pCtlSet->m_ctls[i+1].m_enable=value;
			}
			break;
		}
	}
}


void EnableSet::enableFollow( MString followString, bool value )
{
	if( followString.toLowerCase() == "all" )
	{
		m_pCtlSet->m_fkIkCtls[ 0 ].m_followEnable = value;
		m_pCtlSet->m_fkIkCtls[ 1 ].m_followEnable = value;
		m_pCtlSet->m_fkIkCtls[ 2 ].m_followEnable = value;
		m_pCtlSet->m_fkIkCtls[ 3 ].m_followEnable = value;

		m_pCtlSet->m_ctls[ Head ].m_followEnable = value;
		m_pCtlSet->m_ctls[ Collar_L_ ].m_followEnable = value;
		m_pCtlSet->m_ctls[ Collar_R_ ].m_followEnable = value;
	}
	else if( followString.toLowerCase() == "arml" )
		m_pCtlSet->m_fkIkCtls[ 0 ].m_followEnable = value;
	else if( followString.toLowerCase() == "armr" )
		m_pCtlSet->m_fkIkCtls[ 1 ].m_followEnable = value;
	else if( followString.toLowerCase() == "legl" )
		m_pCtlSet->m_fkIkCtls[ 2 ].m_followEnable = value;
	else if( followString.toLowerCase() == "legr" )
		m_pCtlSet->m_fkIkCtls[ 3 ].m_followEnable = value;
	else if( followString.toLowerCase() == "head" )
		m_pCtlSet->m_ctls[ Head ].m_followEnable = value;
	else if( followString.toLowerCase() == "collarl" )
		m_pCtlSet->m_ctls[ Collar_L_ ].m_followEnable = value;
	else if( followString.toLowerCase() == "collarr" )
		m_pCtlSet->m_ctls[ Collar_R_ ].m_followEnable = value;
}