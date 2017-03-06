#ifndef _coontroler_h
#define _coontroler_h


#include <maya/MStatus.h>

#include <maya/MDoubleArray.h>

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MStringArray.h>
#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MQuaternion.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MTransformationMatrix.h>

#include <maya/MDagPath.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnTransform.h>
#include <maya/MSelectionList.h>


class Ctl
{
public:

	Ctl()
	{
	}

	Ctl( MString nameIn, MString nameOrigIn, MString nameOrigPTrsIn, MString nameOrigPOrtIn )
	{
		m_name = nameIn;
		m_nameOrig = nameOrigIn;
		m_nameOrigPTrs = nameOrigPTrsIn;
		m_nameOrigPOrt = nameOrigPOrtIn;

		m_enable = true;
		m_weight = 1.0;
		m_followEnable = false;
		m_pFlip = NULL;
	}

	void appendUdAttr( MString str )
	{
		m_stringArrUdAttr.append( str );
	}

	MStatus setUdAttr()
	{
		MStatus status;

		MFnTransform tr = m_path;
		
		m_plugArrUdAttr.clear();
		m_valueArrUdAttr.clear();
		m_plugArrUdAttr.setLength( m_stringArrUdAttr.length() );
		m_valueArrUdAttr.setLength( m_stringArrUdAttr.length() );

		m_followExIndexMapper.setLength( m_stringArrUdAttr.length() );
		for( int i=0; i< m_stringArrUdAttr.length(); i++ )
		{
			MPlug tPlug = tr.findPlug( m_stringArrUdAttr[i], &status );
			if( !status ) continue;
			m_plugArrUdAttr[i] = tPlug;
			m_valueArrUdAttr[i] = tPlug.asDouble();

			m_followExIndexMapper[i] = 0;

			int strLength = m_stringArrUdAttr[i].length();
			MString subString = m_stringArrUdAttr[i].substring( strLength-6, strLength );
			if( subString == "Follow" )
			{
				m_followExIndexMapper[i] = 1;
			}
		}
		return MS::kSuccess;
	}

	MStatus setData( const MString& namespaceIn )
	{
		if( !m_enable ) return MS::kSuccess;

		MStatus        status;
		MSelectionList selList;
		MDagPath       path;

		selList.add( namespaceIn + m_name );
		status = selList.getDagPath( 0, path );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		m_mtx = path.inclusiveMatrix()*path.exclusiveMatrixInverse();
		m_path = path;

		setUdAttr();

		selList.add( namespaceIn + m_nameOrig );
		selList.getDagPath( 1, path );
		m_mtxOrig = path.inclusiveMatrix();

		if( !m_nameOrigPTrs.length() )
		{
			m_mtxOrigPTrs = m_mtxOrig;
		}
		else
		{
			selList.add( namespaceIn + m_nameOrigPTrs );
			selList.getDagPath( 2, path );
			m_mtxOrigPTrs = path.inclusiveMatrix();
		}

		if( !m_nameOrigPOrt.length() )
		{
			m_mtxOrigPOrt = m_mtxOrig;
		}
		else
		{
			selList.add( namespaceIn + m_nameOrigPOrt );
			selList.getDagPath( 3, path );		
			m_mtxOrigPOrt = path.inclusiveMatrix();
		}

		m_valueArrUdAttr.clear();
		m_valueArrUdAttr.setLength( m_plugArrUdAttr.length() );
		for( int i=0; i< m_plugArrUdAttr.length(); i++ )
		{
			m_valueArrUdAttr[i] = m_plugArrUdAttr[i].asDouble();
		}

		return MS::kSuccess;
	}

	void updateCtlMatrix()
	{
		if( !m_enable ) return;
		m_mtx = m_path.inclusiveMatrix()*m_path.exclusiveMatrixInverse();

		for( int i=0; i< m_plugArrUdAttr.length(); i++ )
		{
			m_valueArrUdAttr[i] = m_plugArrUdAttr[i].asDouble();
		}
	}

	void mirrorPosition( MMatrix& mtx )
	{
		mtx(3,0) *= -1; mtx(3,1) *= -1; mtx(3,2) *= -1;
	}

	void flip()
	{
		if( m_pFlip == NULL )
		{
			m_mtx( 0,1 ) *= -1; m_mtx( 0,2 ) *= -1;
			m_mtx( 1,0 ) *= -1; m_mtx( 2,0 ) *= -1; m_mtx( 3,0 ) *= -1;
		}
		else
		{
			bool enableTemp = m_enable;
			m_enable = m_pFlip->m_enable;
			m_pFlip->m_enable = enableTemp;

			MMatrix mtxTemp = m_mtx;
			m_mtx = m_pFlip->m_mtx;
			m_pFlip->m_mtx = mtxTemp;

			mirrorPosition( m_mtx );
			mirrorPosition( m_pFlip->m_mtx );

			for( int i=0; i< m_plugArrUdAttr.length(); i++ )
			{
				double temp = m_valueArrUdAttr[i];
				m_valueArrUdAttr[i] = m_pFlip->m_valueArrUdAttr[i];
				m_pFlip->m_valueArrUdAttr[i] = temp;
			}
		}
	}

	void setRetargetValues()
	{
		if( !m_enable || !m_pSrc->m_enable ) return;

		MMatrix& srcMtx			= m_pSrc->m_mtx;
		MMatrix& srcMtxOrig		= m_pSrc->m_mtxOrig;
		MMatrix& srcMtxOrigPTrs	= m_pSrc->m_mtxOrigPTrs;
		MMatrix& srcMtxOrigPOrt	= m_pSrc->m_mtxOrigPOrt;

		MMatrix mtxOrigLocTrs	= m_mtxOrig*m_mtxOrigPTrs.inverse();
		MMatrix sMtxOrigLocTrs	= srcMtxOrig*srcMtxOrigPTrs.inverse();

		MVector trs  = mtxOrigLocTrs[3];
		MVector sTrs = sMtxOrigLocTrs[3];

		double distRate;
		if( sTrs.length() < 0.0001 )
		{
			distRate = 0;
		}
		else
		{
			distRate = trs.length() / sTrs.length();
		}

		sTrs *= distRate;
		MVector offset = sTrs - trs;

		MMatrix mtxOrigLocOrt	= removePoint( m_mtxOrig*m_mtxOrigPOrt.inverse() );
		MMatrix sMtxOrigLocOrt	= removePoint( srcMtxOrig*srcMtxOrigPOrt.inverse() );

		m_mtxResult = srcMtx * sMtxOrigLocOrt * mtxOrigLocOrt.inverse();
		m_mtxResult( 3, 0 ) *= distRate;
		m_mtxResult( 3, 1 ) *= distRate;
		m_mtxResult( 3, 2 ) *= distRate;
		m_mtxResult( 3, 0 ) += offset.x;
		m_mtxResult( 3, 1 ) += offset.y;
		m_mtxResult( 3, 2 ) += offset.z;
	}

	void retarget( double weight )
	{
		if( !m_enable || !m_pSrc->m_enable )return;

		weight *= m_pBase->m_weight;

		double invWeight = 1 - weight;

		for( int i=0; i<m_pSrc->m_valueArrUdAttr.length(); i++ )
		{
			if( !m_followEnable )
			{
				if( m_followExIndexMapper[i] ){}
				else
				m_plugArrUdAttr[i].setDouble( m_pSrc->m_valueArrUdAttr[i]*weight + m_pBase->m_valueArrUdAttr[i]*invWeight );
			}
			else
			{
				m_plugArrUdAttr[i].setDouble( m_pSrc->m_valueArrUdAttr[i]*weight + m_pBase->m_valueArrUdAttr[i]*invWeight );
			}
		}

		MFnTransform tr = m_path;
		MTransformationMatrix trMtx( m_mtxResult*weight + m_pBase->m_mtx *invWeight );
		tr.setTranslation( trMtx.translation( MSpace::kTransform ), MSpace::kTransform );
		tr.setRotation( trMtx.rotation(), MSpace::kTransform );
	}

	void undoRetarget()
	{
		if( !m_enable || !m_pSrc->m_enable ) return;

		MTransformationMatrix trMtx( m_mtx );

		MFnTransform tr = m_path;
		tr.setTranslation( trMtx.translation( MSpace::kTransform ), MSpace::kTransform );
		tr.setRotation( trMtx.rotation(), MSpace::kTransform );

		for( int i=0; i<m_valueArrUdAttr.length(); i++ )
		{
			m_plugArrUdAttr[i].setDouble( m_valueArrUdAttr[i] );
		}
	}

	MMatrix& removePoint( MMatrix mtx )
	{
		mtx( 3,0 ) = 0.0;
		mtx( 3,1 ) = 0.0;
		mtx( 3,2 ) = 0.0;
		return mtx;
	}

	void getBlend( const Ctl& first, const Ctl& second, float wFirst, float wSecond )
	{
		m_enable = first.m_enable;

		if( !m_enable ) return;

		m_mtx = first.m_mtx * wFirst + second.m_mtx * wSecond;
		m_mtxOrt = first.m_mtxOrt * wFirst + second.m_mtxOrt * wSecond;
		m_mtxOrig = first.m_mtxOrig * wFirst + second.m_mtxOrig * wSecond;
		m_mtxOrigPTrs = first.m_mtxOrigPTrs * wFirst + second.m_mtxOrigPTrs * wSecond;
		m_mtxOrigPOrt = first.m_mtxOrigPOrt * wFirst + second.m_mtxOrigPOrt * wSecond;
		m_mtxOrigBase = first.m_mtxOrigBase * wFirst + second.m_mtxOrigBase * wSecond;

		m_valueArrUdAttr.setLength( first.m_valueArrUdAttr.length() );

		for( int i=0; i< first.m_valueArrUdAttr.length(); i++)
		{
			m_valueArrUdAttr[i] = first.m_valueArrUdAttr[i] * wFirst + second.m_valueArrUdAttr[i] * wSecond;
		}
	}

public:
	bool     m_enable;
	bool     m_followEnable;
	double   m_weight;

	MDagPath m_path;

	MString m_name;
	MString m_nameOrig;
	MString m_nameOrigPTrs;
	MString m_nameOrigPOrt;

	MPlugArray   m_plugArrUdAttr;
	MStringArray m_stringArrUdAttr;
	MDoubleArray m_valueArrUdAttr;

	MIntArray    m_followExIndexMapper;

	MMatrix m_mtx;
	MMatrix m_mtxOrt;
	MMatrix m_mtxOrig;
	MMatrix m_mtxOrigPTrs;
	MMatrix m_mtxOrigPOrt;
	MMatrix m_mtxOrigBase;

	MMatrix m_mtxResult;

	Ctl* m_pSrc;
	Ctl* m_pBase;
	Ctl* m_pFlip;
};


class CtlArray
{
public:
	CtlArray()
	{
		m_pCtl = new Ctl[0];
		m_length = 0;
	}

	~CtlArray()
	{
		delete []m_pCtl;
	}

	void setLength( unsigned int length )
	{
		delete []m_pCtl;
		m_pCtl = new Ctl[length];
		m_length = length;
	}

	unsigned int length() const
	{
		return m_length;
	}

	Ctl& operator[]( unsigned int index ) const
	{
		return m_pCtl[index];
	}

	void append( const Ctl& target )
	{
		Ctl* pNew = new Ctl[ m_length+1 ];

		for( int i=0; i< m_length; i++ )
		{
			pNew[i] = m_pCtl[i];
		}

		pNew[ m_length ] = target;
		delete []m_pCtl;
		m_pCtl = pNew;

		m_length += 1;
	}

	int  m_length;
	Ctl* m_pCtl;
};


#endif