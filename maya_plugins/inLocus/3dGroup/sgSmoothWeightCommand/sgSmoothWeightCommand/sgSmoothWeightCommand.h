#ifndef _sgSmoothWeightCommandCmd
#define _sgSmoothWeightCommandCmd

#include <maya/MPxCommand.h>
#include <maya/MArgList.h>
#include <maya/MSyntax.h>
#include <maya/MArgDatabase.h>
#include <maya/MFnMesh.h>

#include <maya/MDagPath.h>

#include <maya/MSelectionList.h>

#include <maya/MFnSingleIndexedComponent.h>
#include <maya/MItMeshVertex.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnDependencyNode.h>

#include <maya/MItDependencyGraph.h>

#include <maya/MGlobal.h>


class ConnectedIndices
{
public:
	ConnectedIndices()
	{
		p_indices = new MIntArray[0];
	}

	void setLength( unsigned int length )
	{
		delete[] p_indices;
		p_indices = new MIntArray[ length ];
	}

	~ConnectedIndices()
	{
		delete[] p_indices;
	}

	MIntArray* p_indices;
};


class sgSmoothWeightCommand : public MPxCommand
{
public:
				sgSmoothWeightCommand();
	virtual		~sgSmoothWeightCommand();

	MStatus		doIt( const MArgList& );
	MStatus		redoIt();
	MStatus		undoIt();
	bool		isUndoable() const;
	static MSyntax newSyntax();

	static		void* creator();

	MStatus getShapeNode( MDagPath& path );
	MStatus getSkinClusterNode( MDagPath& path, MObject& oNode );

	MStatus getWeightValueAndIndices( MPlug& plugWeightList,
		              MIntArray& indicesWeights, MFloatArray& valuesWeights );

	MIntArray getConnectedIndices( const MDagPath& pathMesh, int index );
	void normalizeWeights( MFloatArray& valuesWeights );

	void getSmoothWeight( MPlug& plugWeightList, int indexTarget, 
		MIntArray& indicesGet, MFloatArray& valuesGet );

	void getHardWeight( MPlug& plugWeightList, int indexTarget,
		const MIntArray& indicesBefore, const MFloatArray& valuesBefore, 
		MIntArray& indicesAfter, MFloatArray& valuesAfter );

	void editAfterValueByWeight( MIntArray& indicesBefore, MFloatArray& weightsBefore,
		                         MIntArray& indicesAfter, MFloatArray& weightsAfter, float weight );

	void setWeightValue( MPlug& plugWeightList,
		                        const MIntArray& indices, const MFloatArray& values );
	MStatus getInfomaiton( const MArgDatabase& argData );

	void removeMultiInstance( const MIntArray& beforeIndices, const MIntArray& afterIndices );

	MIntArray   m_indicesBefore;
	MFloatArray m_valuesBefore;
	MIntArray   m_indicesAfter;
	MFloatArray m_valuesAfter;
	unsigned int m_index;
	double       m_weight;
	bool         m_isHardWeight;

	static MObject     m_oSkinCluster;
	static MDagPath    m_pathMesh;
	static MPlug       m_plugWeightList;
	static ConnectedIndices m_connectedIndices;
};

#endif
