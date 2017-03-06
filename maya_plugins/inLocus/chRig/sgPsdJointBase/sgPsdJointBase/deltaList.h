#ifndef _deltaList_h
#define _deltaList_h


#include <maya/MPoint.h>
#include <maya/MVectorArray.h>
#include <maya/MMatrixArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MObject.h>


class Delta
{
public:
	Delta(){};
	~Delta(){};

	void append( const MVector& point )
	{
		pointsEachChannel.append( point );
	}
	
	void assignLast( const MVector& point )
	{
		pointsEachChannel[ pointsEachChannel.length()-1] = point;
	}

	void clear()
	{
		pointsEachChannel.clear();
	}

	MVectorArray pointsEachChannel;
};


class Weights
{
public:
	void append( float value, int logicalIndex )
	{
		m_values.append( value );
		m_logicalIndices.append( logicalIndex );
	}

	void clear()
	{
		m_values.clear();
		m_logicalIndices.clear();
	}

	MFloatArray m_values;
	MIntArray   m_logicalIndices;
};



class DeltaList
{
public:
	DeltaList()
	{
		m_pDelta = new Delta[ 0 ];
		m_pWeights = new Weights[ 0 ];
		m_length = 0;
		m_wLength = 0;
	}
	~DeltaList()
	{
		delete []m_pDelta;
	}

	unsigned int length()
	{
		return m_length;
	}

	unsigned int wLength()
	{
		return m_wLength;
	}

	void setLength( unsigned int length )
	{
		delete []m_pDelta;

		m_pDelta = new Delta[ length ];
		m_length = length;
	}

	void setWLength( unsigned int length )
	{
		delete []m_pWeights;

		m_pWeights = new Weights[ length ];
		m_wLength = length;
	}

	Delta& operator[]( unsigned int index )
	{
		return m_pDelta[ index ];
	}

	unsigned int  m_length;
	unsigned int  m_wLength;
	Delta*        m_pDelta;
	Weights*      m_pWeights;
};


#endif