#include "weightSet.h"



void WeightSet::getCtlSet( CtlSet* pTarget )
{
	m_pCtlSet = pTarget;
}


void WeightSet::setAll( double value )
{
	for( int i=0; i< m_pCtlSet->m_ctls.length(); i++ )
		m_pCtlSet->m_ctls[i].m_weight = value;
	for( int i=0; i< m_pCtlSet->m_fkIkCtls.length(); i++ )
		m_pCtlSet->m_fkIkCtls[i].m_weight = value;
	for( int i=0; i< m_pCtlSet->m_fingerCtls.length(); i++ )
		m_pCtlSet->m_fingerCtls[i].m_weight = value;
}


void WeightSet::setBody( double value )
{
	m_pCtlSet->m_ctls[ Root  ].m_weight = value;
	m_pCtlSet->m_ctls[ Fly   ].m_weight = value;
	m_pCtlSet->m_ctls[ Hip   ].m_weight = value;
	m_pCtlSet->m_ctls[ Torso ].m_weight = value;
	m_pCtlSet->m_ctls[ Chest       ].m_weight = value;
	m_pCtlSet->m_ctls[ Waist       ].m_weight = value;
	m_pCtlSet->m_ctls[ ChestMove   ].m_weight = value;
	m_pCtlSet->m_ctls[ Collar_L_   ].m_weight = value;
	m_pCtlSet->m_ctls[ Collar_R_   ].m_weight = value;
	m_pCtlSet->m_ctls[ Shoulder_L_ ].m_weight = value;
	m_pCtlSet->m_ctls[ Shoulder_R_ ].m_weight = value;
}


void WeightSet::setHead( double value )
{
	m_pCtlSet->m_ctls[ Neck  ].m_weight = value;
	m_pCtlSet->m_ctls[ Head  ].m_weight = value;
	m_pCtlSet->m_ctls[ Eye   ].m_weight = value;
}


void WeightSet::setArmL( double value )
{
	m_pCtlSet->m_fkIkCtls[ arm_L_ ].m_weight = value;
}


void WeightSet::setArmR( double value )
{
	m_pCtlSet->m_fkIkCtls[ arm_R_ ].m_weight = value;
}


void WeightSet::setLegL( double value )
{
	m_pCtlSet->m_fkIkCtls[ leg_L_ ].m_weight = value;
}


void WeightSet::setLegR( double value )
{
	m_pCtlSet->m_fkIkCtls[ leg_R_ ].m_weight = value;
}


void WeightSet::setHandL( double value )
{
	m_pCtlSet->m_fingerCtls[ thumb_L_ ].m_weight = value;
	m_pCtlSet->m_fingerCtls[ index_L_ ].m_weight = value;
	m_pCtlSet->m_fingerCtls[ middle_L_ ].m_weight = value;
	m_pCtlSet->m_fingerCtls[ ring_L_ ].m_weight = value;
	m_pCtlSet->m_fingerCtls[ pinky_L_ ].m_weight = value;
}


void WeightSet::setHandR( double value )
{
	m_pCtlSet->m_fingerCtls[ thumb_R_ ].m_weight = value;
	m_pCtlSet->m_fingerCtls[ index_R_ ].m_weight = value;
	m_pCtlSet->m_fingerCtls[ middle_R_ ].m_weight = value;
	m_pCtlSet->m_fingerCtls[ ring_R_ ].m_weight = value;
	m_pCtlSet->m_fingerCtls[ pinky_R_ ].m_weight = value;
}


void WeightSet::setPart( MString namePart, double value )
{
	MString nameLower = namePart.toLowerCase();

	if(      nameLower == "all" )
	{
		setBody( value );
		setHead( value );
		setArmL( value );
		setArmR( value );
		setLegL( value );
		setLegR( value );
		setHandL( value );
		setHandR( value );
	}
	else if( nameLower == "body" )
		setBody( value );
	else if( nameLower == "head" )
		setHead( value );
	else if( nameLower == "arml" )
		setArmL( value );
	else if( nameLower == "armr" )
		setArmR( value );
	else if( nameLower == "legl" )
		setLegL( value );
	else if( nameLower == "legr" )
		setLegR( value );
	else if( nameLower == "handl" )
		setHandL( value );
	else if( nameLower == "handr" )
		setHandR( value );
}


void WeightSet::setCtl( MString nameCtl, double value )
{
	for( int i=0; i< m_pCtlSet->m_ctls.length(); i++ )
	{
		if( m_pCtlSet->m_ctls[i].m_name == nameCtl )
		{
			m_pCtlSet->m_ctls[i].m_weight = value;
			if( i==0 )
			{
				m_pCtlSet->m_ctls[i+1].m_weight = value;
			}
			break;
		}
	}
}