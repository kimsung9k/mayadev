#ifndef _sgData_h
#define _sgData_h

#include <maya/MGlobal.h>

#include <maya/MObject.h>
#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>

#include <maya/MVector.h>
#include <maya/MVectorArray.h>
#include <maya/MMatrix.h>
#include <maya/MMatrixArray.h>
#include <maya/MIntArray.h>
#include <maya/MFloatArray.h>
#include <maya/MFloatPointArray.h>

#include <maya/MSelectionList.h>

#include <maya/MFnSet.h>
#include <maya/MFnTransform.h>

#include <fstream>

#include <maya/MPlug.h>
#include <maya/MPlugArray.h>


MStatus assignInitialShadingGroup( MObject& oMesh );
MStatus getParents( const MDagPath& pathMesh, MDagPathArray& dagPathArr );
MObject getExistObjectByName( MString fullPathName );

bool    plugsHasConnection( const MPlugArray& plugsTarget );

MStatus    getShapeNode( MDagPath& path );

void     writeUnsignedInt( const unsigned int& value, std::ofstream& outFile );
void     writeDouble( const double& value, std::ofstream& outFile );
void     writePointArray( const MFloatPointArray& pointArr, std::ofstream& outFile );
void     writeFloatArray( const MFloatArray& floatArr, std::ofstream& outFile );
void     writeDoubleArray( const MDoubleArray& doubleArr, std::ofstream& outFile );
void     writeUnsignedIntArray( const MIntArray& intArr, std::ofstream& outFile );
void     writeString( const MString& str, std::ofstream& outFile );
void     writeMatrix( const MMatrix& mtx, std::ofstream& outFile );
void     writeVector( const MVector& vector, std::ofstream& outFile );
void     writeStringArray( const MStringArray& stringArr, std::ofstream& outFile );
void     writeMatrixArray( const MMatrixArray& matrixArr, std::ofstream& outFile );
void     writeVectorArray( const MVectorArray& vectorArr, std::ofstream& outFile );


void     readUnsignedInt( unsigned int& value, std::ifstream& inFile );
void     readDouble( double& value, std::ifstream& inFile );
void     readPointArray( MFloatPointArray& pointArr, std::ifstream& inFile );
void     readFloatArray( MFloatArray& floatArr, std::ifstream& inFile );
void     readDoubleArray( MDoubleArray& doubleArr, std::ifstream& inFile );
void     readUnsignedIntArray( MIntArray& intArr, std::ifstream& inFile );
void     readString( MString& str, std::ifstream& inFile );
void     readMatrix( MMatrix& mtx, std::ifstream& inFile );
void     readVector( MVector& vector, std::ifstream& inFile );
void     readStringArray( MStringArray& stringArr, std::ifstream& inFile );
void     readMatrixArray( MMatrixArray& matrixArr, std::ifstream& inFile );
void     readVectorArray( MVectorArray& vectorArr, std::ifstream& inFile );

#endif