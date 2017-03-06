#ifndef _polygonToMatrix_h
#define _polygonToMatrix_h

#include <maya/MPxNode.h>

#include <maya/MTypeId.h>

#include <maya/MDataBlock.h>

#include <maya/MDataHandle.h>

#include <maya/MFnTypedAttribute.h>

#include <maya/MFnNumericAttribute.h>

#include <maya/MDagPath.h>

#include <maya/MPlug.h>

#include <maya/MPoint.h>

#include <maya/MVector.h>




class polygonToMatrix : public MPxNode

{

   public:

      // CLASS METHOD DECLARATIONS:

      polygonToMatrix();

      virtual ~polygonToMatrix();

      static void *creator();

      static MStatus initialize();

      virtual MStatus compute(const MPlug &plug, MDataBlock &data);



      // CLASS DATA DECLARATIONS:

      static MTypeId id;

      static MObject aInMesh;

      static MObject aFaceIndex;

	  static MObject aRelative;

      static MObject aParameterU;

      static MObject aParameterV;

      static MObject aPosition;

      static MObject aPositionX;

      static MObject aPositionY;

      static MObject aPositionZ;

      static MObject aNormal;

      static MObject aNormalX;

      static MObject aNormalY;

      static MObject aNormalZ;

};

#endif