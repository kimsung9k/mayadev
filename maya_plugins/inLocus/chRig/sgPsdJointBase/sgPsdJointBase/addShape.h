#ifndef _addShape_h
#define _addShape_h


#include <maya/MPxCommand.h>
#include <maya/MSyntax.h>
#include <maya/MArgList.h>
#include <maya/MArgDatabase.h>

#include <maya/MSelectionList.h>

#include <maya/MDagPath.h>
#include <maya/MObject.h>
#include <maya/MObjectArray.h>
#include <maya/MFnDagNode.h>

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>

#include <maya/MFnDependencyNode.h>

#include <maya/MPoint.h>
#include <maya/MPointArray.h>
#include <maya/MVectorArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>

#include <maya/MString.h>

#include <maya/MFnAttribute.h>

#include <maya/MGlobal.h>
#include <maya/MDGModifier.h>
#include <maya/MItDependencyGraph.h>

#include <maya/MString.h>


class MatrixInfo
{
public:

	void setLength( unsigned int length )
	{
		mtxArr.setLength( length );
		mtxArrBindPre.setLength( length );
	}

	void setLengthLogical( unsigned int length )
	{
		indicesLogicalMap.setLength( length );
		for( int i=0; i< indicesLogicalMap.length(); i++ )
		{
			indicesLogicalMap[i]= 0;
		}
	}

	MMatrixArray mtxArr;
	MMatrixArray mtxArrBindPre;
	MIntArray    indicesLogicalMap;
};


class WeightInfo
{
public:
	void setLength( unsigned int length )
	{
		fArrValues.setLength( length );
		indicesLogical.setLength( length );
	}

	MFloatArray fArrValues;
	MIntArray   indicesLogical;
};


class WeightArray
{
public:

	WeightArray()
	{
		m_pWeight = new WeightInfo[0];
		m_length = 0;
	}

	void setLength( unsigned int length )
	{
		delete []m_pWeight;

		m_pWeight = new WeightInfo[ length ];
		m_length = length;
	}

	unsigned int length()
	{
		return m_length;
	}

	WeightInfo& operator[]( unsigned int index )
	{
		return m_pWeight[ index ];
	}

	int         m_length;
	WeightInfo* m_pWeight;
};



class AddShape : MPxCommand
{
public:
	AddShape();
	virtual ~AddShape();

	MStatus doIt( const MArgList& args );
	MStatus redoIt();
	MStatus undoIt();
	bool isUndoable() const;

	static MSyntax newSyntax();
	static void* creator();

	MStatus		getShapeNode( MDagPath& path );
	MStatus     getDeformer( MObject& oPsd, MObject& oSkin );
	MStatus     getDeformer();
	MStatus     getSkinInfo();

	MStatus     getDeltas( MDagPath& pathTarget, MDagPath& pathBase );
	MStatus     getMatrixInfo( const MObject& oSkin );
	MStatus     getWeightInfo( const MObject& oSkin );

	MStatus     getLastLogicalIndex( const MObject& oPsd, unsigned int& index );

	MStatus     multMatrixDelta();

public:
	MDagPath m_pathTarget;
	MDagPath m_pathBase;

	MObject  m_oPsd;
	MObject  m_oSkin;

	WeightArray  m_weightArr;
	MatrixInfo   m_mtxInfo;

	MVectorArray  m_deltas;
	MIntArray    m_logicalDeltas;

	MVectorArray  m_deltasBefore;
	MIntArray     m_logicalsBefore;

	unsigned int m_logicalDeltaInfoAdd;
	int          m_inputIndex;
};


#endif