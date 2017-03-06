#ifndef _enableSet_h
#define _enableSet_h


#include "controlerSet.h"


class EnableSet
{	
public:

	void setDefaultRoot();
	void allEnable( bool value = true );
	void getCtlSet( CtlSet* pTarget );
	void moveEnable( bool value=true );
	void keepCurrent( bool value=true );
	void keepHorizon( bool value=true );
	void bodyEnable( bool value=true );
	void headEnable( bool value=true );
	void arm_L_Enable( bool value=true );
	void arm_R_Enable( bool value=true );
	void leg_L_Enable( bool value=true );
	void leg_R_Enable( bool value=true );
	void hand_L_Enable( bool value=true );
	void hand_R_Enable( bool value=true );
	void enablePart( MString namePart, bool value= true );
	void enableCtl( MString nameCtl, bool value=true );
	void enableFollow( MString followString, bool value=true );

	CtlSet* m_pCtlSet;
};


#endif