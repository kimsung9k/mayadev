#ifndef _simpleMeshTranslator_h
#define _simpleMeshTranslator_h

#include <maya/MDagModifier.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MPointArray.h>
#include <maya/MFloatArray.h>
#include <maya/MFloatPointArray.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MFnDagNode.h>
#include <maya/MFnDependencyNode.h>
#include <maya/MItDependencyGraph.h>
#include <maya/MFnMesh.h>
#include <maya/MFnSet.h>
#include <maya/MFnTransform.h>
#include <maya/MGlobal.h>
#include <maya/MIntArray.h>
#include <maya/MItSelectionList.h>
#include <maya/MItDag.h>
#include <maya/MPxFileTranslator.h>
#include <maya/MVector.h>
#include <maya/MPoint.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MDataBlock.h>
#include <maya/MFnMesh.h>

#include <maya/MTransformationMatrix.h>

#include <maya/MFnMatrixData.h>

#include <fstream>

#include <vector>

using namespace std;

const char *const optionScript = "exportWeightOptions";
const char *const defaultOptions = "";


struct fileInfo
{
	MIntArray matrixIndices;
	MPointArray matrixPositions;
	MPointArray vtxPoints;
	vector< MIntArray >   weightListIndices;
	vector< MFloatArray > weightListValues;
};


class sgSkinWeightExportImport : public MPxFileTranslator
{
public:
						sgSkinWeightExportImport();
	virtual				~sgSkinWeightExportImport(); 
	static  void*		creator();

    virtual bool haveReadMethod() const;
	virtual bool haveWriteMethod() const;
	virtual bool canBeOpened() const;
	virtual MString defaultExtension() const;

	virtual MStatus	reader( const MFileObject& file,
        const MString& optionsString,
        FileAccessMode mode );

    virtual MStatus	writer( const MFileObject& file,
        const MString& optionsString,
        FileAccessMode mode );

    MFileKind identifyFile( const MFileObject& fileName,
        const char* buffer,
        short size ) const;

    MStatus parseOptionsString( const MString& optionsString );
    MStatus exportAll( std::ofstream& out );
    MStatus exportSelected( std::ofstream& out );
    MStatus exportWeightInfo( MDagPath& pathDag, std::ofstream& out );
	MStatus getFileInfo( std::ifstream& inFile, fileInfo* pInfo, MFnTransform& targetTransform, MMatrix& getMatrix ); 
    MStatus getSkinClusterNodeFromPath( MDagPath& pathDag, MFnDependencyNode& skinNode );
	/*MStatus targetIndicesMapping( MIntArray& fileInfoIndicesToSkinIndices, 
		                          MIntArray& fileInfoIndices, MPointArray& fileInfoPositions,
								  MIntArray& skinIndices,     MPointArray& skinPositions,
								  int fileInfoMaxIndex );*/
    //void exportString( std::ofstream& out, MString& str );
    //MString importString( std::ifstream& inFile );
	MStatus setInfoToSkinNode( fileInfo& info, MFnDependencyNode& skinNode, MObjectArray& oJoints );
    MStatus importWeightInfo( std::ifstream& inFile, MDagPath& targetPath );

	MStatus getShape( MDagPath& dagPath );

private:
    bool m_exportNormals;
    bool m_exportUVs;
};

#endif
