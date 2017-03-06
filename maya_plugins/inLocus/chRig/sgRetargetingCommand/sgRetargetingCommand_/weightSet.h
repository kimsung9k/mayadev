#ifndef _weightSet_h
#define _weightSet_h


#include "controlerSet.h"


class WeightSet
{	
public:
	void getCtlSet( CtlSet* pTarget );
	void setAll(   double value ); 
	void setBody(  double value );
	void setHead(  double value );
	void setArmL(  double value );
	void setArmR(  double value );
	void setLegL(  double value );
	void setLegR(  double value );
	void setHandL( double value );
	void setHandR( double value );
	void setPart(   MString namePart, double value );
	void setCtl(    MString nameCtl , double value ); 

	CtlSet* m_pCtlSet;
};


#endif