#ifndef _weightList_h
#define _weightList_h


#include <maya/MPoint.h>
#include <maya/MMatrixArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MObject.h>


class Weights
{
public:
	Weights(){};
	~Weights(){};

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


class WeightList
{
public:
	WeightList()
	{
		m_pWeights = new Weights[0];
	}

	~WeightList()
	{
		delete []m_pWeights;
	}

	unsigned int length()
	{
		return m_length;
	}

	void setLength( unsigned int length )
	{
		delete []m_pWeights;
		m_pWeights = new Weights[ length ];
		m_length = length;
	}

	Weights& operator[]( unsigned int index )
	{
		return m_pWeights[ index ];
	}

	unsigned int m_length;
	Weights* m_pWeights;
};


#endif