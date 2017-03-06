#ifndef _fkIkControler_h
#define _fkIkControler_h



#include <maya/MStatus.h>

#include <maya/MPlugArray.h>
#include <maya/MStringArray.h>
#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MTransformationMatrix.h>

#include <maya/MDagPath.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnTransform.h>
#include <maya/MSelectionList.h>



class FkIkCtl
{
public:
	enum
	{
		poleTwist, length, bias, stretchAble, smoothRate, positionAttach,
		kneeAutoAngle, tapToe, toeRot, heelLift,walkRoll, walkRollAngle,
		heelRot, ballRot, heelTwist, ballTwist, toeTwist, bank
	};

	FkIkCtl();

	void getOrigName( MString nameShd, MString nameElb, MString nameWrt, 
		MString namePoleV, MString namePTrs, MString namePOrt ="" );

	void getCuName( MString nameShd, MString nameElb, MString nameWrt, MString nameBall="", MString nameToe="" );

	void getFkName( MString nameShd, MString nameElb, MString nameWrt, MString nameBall ="" );

	void getIkName( MString nameIk, MString nameIkItp, MString namePoleV, MString nameSwitch, MString namePTrs, MString namePOrt );

	void getFootName( MString nameFoot );

	void getOrientPName( MString nameOrientP );

	void getUdAttr();

	MStatus setData( MString namespaceIn );

	void updateCtlMatrix();

	void flip();

	MMatrix getEachRetargetMatrix( const MMatrix& mtxOrigTrg, const MMatrix& mtxPTrsOrigTrg, const MMatrix& mtxPOrtOrigTrg,
		                           const MMatrix& mtxOrigSrc, const MMatrix& mtxPTrsOrigSrc, const MMatrix& mtxPOrtOrigSrc,
								   const MMatrix& mtxSrc );

	
	MVector getPoleVectorPosition( const MMatrix& mtxShd, const MMatrix& mtxElb, const MMatrix& mtxWrt, double weight );
	
	void setRetargetValues();
	void retargetUdAttr();
	void retarget( double weight );
	void undoRetarget();

	void getBlend( const FkIkCtl& first, const FkIkCtl& second, float wFirst, float wSecond ); 

	MMatrix& removePoint( MMatrix mtx );

public:
	bool m_enable;
	bool m_followEnable;
	double m_weight;

	MString m_namespace;

	MString m_nameShdOrig;
	MString m_nameElbOrig;
	MString m_nameWrtOrig;
	MString m_namePoleVOrig;
	MString m_namePTrsOrig;
	MString m_namePOrtOrig;

	MString m_nameShdCu;
	MString m_nameElbCu;
	MString m_nameWrtCu;
	MString m_nameBallCu;
	MString m_nameToeCu;

	MString m_nameShdFk;
	MString m_nameElbFk;
	MString m_nameWrtFk;
	MString m_nameFootFk;

	MString m_nameIk;
	MString m_namePoleV;
	MString m_nameItp;
	MString m_nameSwitch;
	MString m_nameIkPTrs;
	MString m_nameIkPOrt;
	MString m_nameFoot;

	MString m_nameOrientP;

	MMatrix m_mtxShd;
	MMatrix m_mtxElb;
	MMatrix m_mtxWrt;
	MMatrix m_mtxBall;
	MMatrix m_mtxToe;
	MMatrix m_mtxIk;
	MMatrix m_mtxItp;
	MMatrix m_mtxPoleV;
	MMatrix m_mtxIkPOrt;
	MMatrix m_mtxIkPTrs;
	MMatrix m_mtxShdOrig;
	MMatrix m_mtxElbOrig;
	MMatrix m_mtxWrtOrig;
	MMatrix m_mtxPoleVOrig;
	MMatrix m_mtxPTrsOrig;
	MMatrix m_mtxPOrtOrig;

	MMatrix m_mtxShdResult;
	MMatrix m_mtxElbResult;
	MMatrix m_mtxWrtResult;
	MMatrix m_mtxIkResult;
	MMatrix m_mtxPoleVResult;

	double  ud_handScale;
	double  ud_twist;
	double  ud_interpoleSwitch;
	double  ud_collarFollow;
	double  ud_chestFollow;
	double  ud_hipFollow;
	double  ud_rootFollow;
	double  ud_moveFollow;

	double  ud_poleTwist;;
	double  ud_length;
	double  ud_bias;
	double  ud_stretchAble;
	double  ud_smoothRate;
	double  ud_positionAttach;
	double  ud_kneeAutoAngle;
	double  ud_tapToe;
	double  ud_toeRot;
	double  ud_heelLift;
	double  ud_walkRoll;
	double  ud_walkRollAngle;
	double  ud_heelRot;
	double  ud_ballRot;
	double  ud_heelTwist;
	double  ud_ballTwist;
	double  ud_toeTwist;
	double  ud_bank;

	MDagPath m_pathShd;
	MDagPath m_pathShdFk;
	MDagPath m_pathElb;
	MDagPath m_pathElbFk;
	MDagPath m_pathWrt;
	MDagPath m_pathWrtFk;
	MDagPath m_pathBall;
	MDagPath m_pathToe;
	MDagPath m_pathToeFk;
	MDagPath m_pathIk;
	MDagPath m_pathItp;
	MDagPath m_pathSwitch;
	MDagPath m_pathFoot;
	MDagPath m_pathPoleV;
	MDagPath m_pathIkPTrs;
	MDagPath m_pathIkPOrt;
	MDagPath m_pathOrientP;

	MTransformationMatrix m_trMtxHeelInit;
	MTransformationMatrix m_trMtxBallPivInit;
	MTransformationMatrix m_trMtxBankInInit;
	MTransformationMatrix m_trMtxBankOutInit;
	MTransformationMatrix m_trMtxToePivInit;
	MTransformationMatrix m_trMtxToeInit;
	MTransformationMatrix m_trMtxBallInit;
	MTransformationMatrix m_trMtxAnkleInit;

	MMatrix m_mtxCu3_orig;
	MMatrix m_mtxCu4_orig;

	MMatrix m_mtxAnkleLocalIk_bf;
	MMatrix m_mtxAnkleLocalIk_af;
	MMatrix m_mtxShdOrientOffset;
	MMatrix m_mtxFk3;
	MMatrix m_mtxFk4;

	FkIkCtl* m_pSrc;
	FkIkCtl* m_pBase;
	FkIkCtl* m_pFlip;
};


class FkIkCtlArray
{
public:
	FkIkCtlArray()
	{
		m_pFkIkCtl = new FkIkCtl[0];
		m_length = 0;
	}

	~FkIkCtlArray()
	{
		delete []m_pFkIkCtl;
	}

	void setLength( unsigned int length )
	{
		delete []m_pFkIkCtl;
		m_pFkIkCtl = new FkIkCtl[length];
		m_length = length;
	}

	unsigned int length() const
	{
		return m_length;
	}

	void append( const FkIkCtl& target )
	{
		FkIkCtl* pNew = new FkIkCtl[ m_length+1 ];

		for( int i=0; i< m_length; i++ )
		{
			pNew[i] = m_pFkIkCtl[i];
		}

		pNew[ m_length ] = target;
		delete []m_pFkIkCtl;
		m_pFkIkCtl = pNew;

		m_length += 1;
	}

	FkIkCtl& operator[]( unsigned int index ) const
	{
		return m_pFkIkCtl[index];
	}

	int  m_length;
	FkIkCtl* m_pFkIkCtl;
};


#endif