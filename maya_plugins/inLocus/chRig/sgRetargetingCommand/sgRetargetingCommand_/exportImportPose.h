#ifndef _ExportImportPose_h
#define _ExportImportPose_h


#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MMatrix.h>
#include <maya/MFnTransform.h>
#include <maya/MItSelectionList.h>
#include <maya/MDataBlock.h>
#include <maya/MFnMatrixData.h>
#include <maya/MIntArray.h>

#include <maya/MGlobal.h>

#include <maya/MPxFileTranslator.h>

#include <fstream>

const char *const optionScript = "exportCPoseOption";
const char *const defaultOptions = "head=1;body=1;armL=1;armR=1;legL=1;legR=1;handL=1;handR=1;";


class ExportImportPose : public MPxFileTranslator
{
public:
	ExportImportPose();
	virtual ~ExportImportPose();
	static void* creator();

	virtual bool haveReadMethod() const;
	virtual bool haveWriteMethod() const;
	virtual bool canBeOpened() const;
	virtual MString defaultExtension() const;

	virtual MStatus reader( const MFileObject& file,
		const MString& optionString, FileAccessMode mode );

	virtual MStatus writer( const MFileObject& file,
		const MString& optionString, FileAccessMode mode );

	MFileKind identifyFile( const MFileObject& fileName,
		const char* buffer,
		short size ) const;

	MStatus parseOptionString( const MString& optionString );
	MStatus getNamespaceFromWorldCtl( MString& namespaceGet );
	MStatus exportData( std::ofstream& outFile );
	MStatus importData( std::ifstream& inFile );

public:

	enum enOption
	{
		head, body, armL, armR, 
		legL, legR, handL, handR
	};

	MIntArray m_enOptions;
};


#endif