#ifndef _coontrolerInfo_h
#define _coontrolerInfo_h



#include <maya/MString.h>
#include <vector>
#include "controler.h"
#include "fkikControler.h"
#include "fingerControler.h"


enum 
{
	Root, Fly, Hip, Torso, Chest, Waist, ChestMove,
	Neck, Head, Eye,
	Collar_L_, Shoulder_L_, Collar_R_, Shoulder_R_
};


enum 
{
	arm_L_, arm_R_, leg_L_, leg_R_
};


enum
{
	thumb_L_, index_L_, middle_L_, ring_L_, pinky_L_,
	thumb_R_, index_R_, middle_R_, ring_R_, pinky_R_
};


class CtlSet
{
public:
	CtlSet();
	void reset();
	void appendData( const Ctl& data );
	void appendData( const FkIkCtl& data );
	void appendData( const FingerCtl& data );
	void connectBase( CtlSet* pCtlSetBase );
	void connectSource( CtlSet* pCtlSetSrc );
	MStatus setBaseData( MString namespaceIn, bool isSrc= false );
	void updateRootMatrix();
	void updateCtlMatrix();
	MMatrix getDirectionMatrix( MMatrix mtx );
	void flip();
	void setRetargetValues();
	void retarget( double weight );
	void undoRetarget();
	void setAllEnable();
	void setAllDisable();
	CtlSet& operator=( const CtlSet& other );
	void getBlend( const CtlSet& first, const CtlSet& second, float wFirst, float wSecond );


public:
	MString m_namespace;

	static bool m_rootMoveEnable;
	static bool m_rootKeepHorizon;
	static bool m_rootKeepCurrent;

	MDagPath m_pathRootGrp;

	MMatrix m_mtxRoot;
	MMatrix m_mtxDirection;

	CtlArray       m_ctls;
	FkIkCtlArray   m_fkIkCtls;
	FingerCtlArray m_fingerCtls;

	CtlSet* m_pSrc;

	float   m_frameOffset;
};


class CtlSetArray
{
public:
	CtlSetArray()
	{
		m_pCtlSet = new CtlSet[0];
		m_length = 0;
	}

	~CtlSetArray()
	{
		delete []m_pCtlSet;
	}

	void setLength( unsigned int length )
	{
		delete []m_pCtlSet;
		m_pCtlSet = new CtlSet[length];
		m_length = length;
	}

	unsigned int length() const
	{
		return m_length;
	}

	CtlSet& operator[]( unsigned int index ) const
	{
		return m_pCtlSet[index];
	}

	void append( const CtlSet& target )
	{
		CtlSet* pNew = new CtlSet[ m_length+1 ];

		for( int i=0; i< m_length; i++ )
		{
			pNew[i] = m_pCtlSet[i];
		}

		pNew[ m_length ] = target;
		delete []m_pCtlSet;
		m_pCtlSet = pNew;

		m_length += 1;
	}

	int  m_length;
	CtlSet* m_pCtlSet;
};



#endif