#ifndef _retargetInfo_h
#define _retargetInfo_h

#include <maya/MStatus.h>

#include <maya/MString.h>
#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MEulerRotation.h>
#include <maya/MStringArray.h>
#include <maya/MDoubleArray.h>
#include <maya/MMatrixArray.h>

#include <maya/MSelectionList.h>
#include <maya/MObject.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MFnTransform.h>
#include <maya/MDagPath.h>

#include <maya/MPlug.h>

#include <vector>

#include <maya/MMatrix.h>

#include <maya/MString.h>


class DistInfo
{
public:

	DistInfo( char* nameIn, MStringArray& sArrIn )
	{
		m_name = nameIn;
		m_sArr = sArrIn;
	}

	DistInfo( MString& nameIn, MStringArray& sArrIn )
	{
		m_name = nameIn;
		m_sArr = sArrIn;
	}

	void setNamespace( MString& namespaceIn )
	{
		if( m_sArr.length() < 1 )
			return;

		m_ns = namespaceIn;

		for( int i=0; i< m_sArr.length(); i++ )
		{
			m_selList.clear();
			m_selList.add( m_ns + m_sArr[i] );

			MDagPath pathFirst;

			m_selList.getDagPath( 0, pathFirst );

			MFnTransform fnTrFirst( pathFirst );
			MPlug plugTx = fnTrFirst.findPlug( "translateX" );
			MPlug plugTy = fnTrFirst.findPlug( "translateY" );
			MPlug plugTz = fnTrFirst.findPlug( "translateZ" );

			double xDist = plugTx.asDouble();
			double yDist = plugTy.asDouble();
			double zDist = plugTz.asDouble();

			m_dArr.append( sqrt( pow( xDist, 2.0 ) + pow( yDist, 2.0 ) + pow( zDist, 2.0 ) ) );
		}
	}

	MString name()
	{
		return m_name;
	}

	MDoubleArray distArr()
	{
		return m_dArr;
	}

	double sumDist()
	{
		double sumDist = 0.0;
		for( int i=0; i< m_dArr.length(); i++ )
		{
			sumDist += m_dArr[i];
		}
		return sumDist;
	}

	double indexDist( unsigned int index )
	{
		if( index >= m_dArr.length() )
			return 0.0;

		return m_dArr[ index ];
	}

public:
	MSelectionList	m_selList;
	MString         m_ns;
	MString			m_name;
	MStringArray	m_sArr;
	MDoubleArray	m_dArr;
};



class DistInfos
{
public:
	DistInfos(){};
	~DistInfos(){};

	void clear()
	{
		m_distInfo.clear();
	}

	void append( char* strNameIn, MStringArray& sArrIn )
	{
		DistInfo distInfo( strNameIn, sArrIn );
		m_distInfo.push_back( distInfo );
	}

	void append( MString& strNameIn, MStringArray& sArrIn )
	{
		DistInfo distInfo( strNameIn, sArrIn );
		m_distInfo.push_back( distInfo );
	}

	const DistInfo& operator[]( unsigned int index )
	{
		return m_distInfo[ index ];
	}

	void setNamespace( MString& namespaceIn )
	{
		for( int i=0; i< m_distInfo.size(); i++ )
		{
			m_distInfo[i].setNamespace( namespaceIn );
		}
	}

	unsigned int length()
	{
		return m_distInfo.size();
	}

private:
	std::vector<DistInfo> m_distInfo;
};


#endif