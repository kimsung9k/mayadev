#ifndef _fingerControler_h
#define _fingerControler_h


#include <maya/MStatus.h>

#include <maya/MStringArray.h>
#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MQuaternion.h>

#include <maya/MFnDependencyNode.h>
#include <maya/MTransformationMatrix.h>

#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnTransform.h>
#include <maya/MSelectionList.h>

#include <maya/MGlobal.h>


class FingerCtl
{
public:
	FingerCtl(){}

	FingerCtl( MString nameIn, MString nameOrigIn )
	{
		m_name = nameIn;
		m_nameOrig = nameOrigIn;
		m_length = 0;
		m_enable = true;
		m_weight = 1.0;
		m_pFlip = NULL;
	}

	void setLength( int length )
	{
		m_length = length;
		m_mtxArr.setLength( length );
		m_mtxArrOrig.setLength( length );
		m_mtxArrOrigP.setLength( length );
	}

	MStatus setData( const MString& namespaceIn )
	{
		if( !m_enable ) return MS::kSuccess;

		MStatus status;

		char buffer[512];
		MStringArray m_names;
		MStringArray m_namesOrig;
		MStringArray m_namesOrigP;

		sprintf( buffer, "ls \"%s%s\";", namespaceIn.asChar(), m_name.asChar() );
		status = MGlobal::executeCommand( buffer, m_names );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		sprintf( buffer, "ls \"%s%s\";", namespaceIn.asChar(), m_nameOrig.asChar() );
		status = MGlobal::executeCommand( buffer, m_namesOrig );
		CHECK_MSTATUS_AND_RETURN_IT( status );

		m_length = m_names.length();

		m_pathArr.setLength( m_length );
		m_mtxArr.setLength( m_length );
		m_mtxArrOrig.setLength( m_length );
		m_mtxArrOrigP.setLength( m_length );
		m_mtxArrResult.setLength( m_length );

		MSelectionList selList;
		MDagPath path;

		for( int i=0; i< m_length; i++ )
		{
			selList.clear();

			selList.add( m_names[i] );
			selList.getDagPath( 0, path ); m_pathArr[i] = path;
			m_mtxArr[i]     = path.inclusiveMatrix() * path.exclusiveMatrixInverse();
			selList.add( m_namesOrig[i] );
			selList.getDagPath( 1, path );
			m_mtxArrOrig[i]  = path.inclusiveMatrix();
			m_mtxArrOrigP[i] = path.exclusiveMatrix();
		}

		return MS::kSuccess;
	}


	void updateCtlMatrix()
	{
		if( !m_enable ) return;

		for( int i=0; i< m_length; i++ )
		{
			m_mtxArr[i] = m_pathArr[i].inclusiveMatrix()*m_pathArr[i].exclusiveMatrixInverse();
		}
	}


	void flip()
	{
		if( m_pFlip == NULL ) return;

		bool    enableTemp;
		MMatrix mtxTemp;

		enableTemp = m_enable;
		m_enable = m_pFlip->m_enable;
		m_pFlip->m_enable = enableTemp;

		for( int i=0; i< m_length; i++ )
		{
			mtxTemp = m_mtxArr[i];
			m_mtxArr[i] = m_pFlip->m_mtxArr[i];
			m_pFlip->m_mtxArr[i] = mtxTemp;
		}
	}


	void setRetargetValues()
	{
		if( !m_enable || !m_pSrc->m_enable ) return;
		if( m_pSrc->m_length != m_length ) return;

		MMatrixArray& srcMtxArr      = m_pSrc->m_mtxArr;
		MMatrixArray& srcMtxArrOrig  = m_pSrc->m_mtxArrOrig;
		MMatrixArray& srcMtxArrOrigP = m_pSrc->m_mtxArrOrigP;

		for( int i=0 ; i< m_pSrc->m_length; i++ )
		{
			MMatrix mtxTrgOrigLocalTrs = m_mtxArrOrig[i] * m_mtxArrOrigP[i].inverse();
			MMatrix mtxSrcOrigLocalTrs = srcMtxArrOrig[i] * srcMtxArrOrigP[i].inverse();
			
			MVector trsTrg = mtxTrgOrigLocalTrs[3];
			MVector trsSrc = mtxSrcOrigLocalTrs[3];

			double distRate;
			if( trsSrc.length() == 0 )
				distRate = 1;
			else
				distRate = trsTrg.length() / trsSrc.length();

			trsSrc *= distRate;

			MMatrix mtxOrigLoc	= removePoint( m_mtxArrOrig[i]*m_mtxArrOrigP[i].inverse() );
			MMatrix srcMtxOrigLoc	= removePoint( srcMtxArrOrig[i]*srcMtxArrOrigP[i].inverse() );
			
			m_mtxArrResult[i] = srcMtxArr[i] * srcMtxOrigLoc * mtxOrigLoc.inverse();
			m_mtxArrResult[i]( 3, 0 ) *= distRate;
			m_mtxArrResult[i]( 3, 1 ) *= distRate;
			m_mtxArrResult[i]( 3, 2 ) *= distRate;

			if( i == 0 )
			{
				m_mtxArrResult[i]( 3, 0 ) *= 0.0;
				m_mtxArrResult[i]( 3, 1 ) *= 0.0;
				m_mtxArrResult[i]( 3, 2 ) *= 0.0;
			}
		}
	}


	void retarget( double weight )
	{
		if( !m_enable || !m_pSrc->m_enable ) return;

		weight *= m_pBase->m_weight;

		double invWeight = 1 - weight;

		for( int i=0; i< m_length; i++ )
		{
			MTransformationMatrix trMtx( m_mtxArrResult[i]*weight + m_pBase->m_mtxArr[i] *invWeight );

			MFnTransform tr = m_pathArr[i];
			tr.setTranslation( trMtx.translation( MSpace::kTransform ), MSpace::kTransform );
			tr.setRotation( trMtx.rotation(), MSpace::kTransform );
		}
	}


	void undoRetarget()
	{
		if( !m_enable || !m_pSrc->m_enable ) return;

		for( int i=0; i< m_length; i++ )
		{
			MTransformationMatrix trMtx( m_mtxArr[i] );

			MFnTransform tr = m_pathArr[i];
			tr.setTranslation( trMtx.translation( MSpace::kTransform ), MSpace::kTransform );
			tr.setRotation( trMtx.rotation(), MSpace::kTransform );
		}
	}


	MMatrix& removePoint( MMatrix mtx )
	{
		mtx( 3,0 ) = 0.0;
		mtx( 3,1 ) = 0.0;
		mtx( 3,2 ) = 0.0;
		return mtx;
	}


	void getBlend( const FingerCtl& first, const FingerCtl& second, float wFirst, float wSecond )
	{
		m_enable = first.m_enable;

		if( !m_enable ) return;

		m_length = first.m_mtxArr.length();

		m_mtxArr.setLength( m_length );
		m_mtxArrOrig.setLength( m_length );
		m_mtxArrOrigP.setLength( m_length );

		for( int i=0; i< m_length; i++ )
		{
			m_mtxArr[i]      = first.m_mtxArr[i]      * wFirst + second.m_mtxArr[i]      * wSecond;
			m_mtxArrOrig[i]  = first.m_mtxArrOrig[i]  * wFirst + second.m_mtxArrOrig[i]  * wSecond;
			m_mtxArrOrigP[i] = first.m_mtxArrOrigP[i] * wFirst + second.m_mtxArrOrigP[i] * wSecond;
		}
	}


	~FingerCtl(){}

public:
	bool m_enable;

	int m_length;
	double m_weight;

	MDagPathArray m_pathArr;

	MString m_name;
	MString m_nameOrig;

	MMatrixArray m_mtxArr;
	MMatrixArray m_mtxArrOrig;
	MMatrixArray m_mtxArrOrigP;

	MMatrixArray m_mtxArrResult;

	FingerCtl* m_pSrc;
	FingerCtl* m_pBase;
	FingerCtl* m_pFlip;
};



class FingerCtlArray
{
public:
	FingerCtlArray()
	{
		m_pFingerCtl = new FingerCtl[0];
		m_length = 0;
	}

	~FingerCtlArray()
	{
		delete []m_pFingerCtl;
	}

	void setLength( unsigned int length )
	{
		delete []m_pFingerCtl;
		m_pFingerCtl = new FingerCtl[length];
		m_length = length;
	}

	unsigned int length() const
	{
		return m_length;
	}

	void append( const FingerCtl& target )
	{
		FingerCtl* pNew = new FingerCtl[ m_length+1 ];

		for( int i=0; i< m_length; i++ )
		{
			pNew[i] = m_pFingerCtl[i];
		}

		pNew[ m_length ] = target;
		delete []m_pFingerCtl;
		m_pFingerCtl = pNew;

		m_length += 1;
	}

	FingerCtl& operator[]( unsigned int index ) const
	{
		return m_pFingerCtl[index];
	}

	int  m_length;
	FingerCtl* m_pFingerCtl;
};


#endif