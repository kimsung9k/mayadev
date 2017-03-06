#include "polygonToMatrix.h"
#include <maya/MIOStream.h>


// DEFINE CLASS'S STATIC DATA MEMBERS:
MTypeId polygonToMatrix::id(0x00105480);
MObject polygonToMatrix::aInMesh;
MObject polygonToMatrix::aFaceIndex;
MObject polygonToMatrix::aRelative;
MObject polygonToMatrix::aParameterU;
MObject polygonToMatrix::aParameterV;
MObject polygonToMatrix::aPosition;
MObject polygonToMatrix::aPositionX;
MObject polygonToMatrix::aPositionY;
MObject polygonToMatrix::aPositionZ;
MObject polygonToMatrix::aNormal;
MObject polygonToMatrix::aNormalX;
MObject polygonToMatrix::aNormalY;
MObject polygonToMatrix::aNormalZ;


// CONSTRUCTOR DEFINITION:
polygonToMatrix::polygonToMatrix()
{
}


// DESTRUCTOR DEFINITION:
polygonToMatrix::~polygonToMatrix()
{
}


// FOR CREATING AN INSTANCE OF THIS NODE:
void *polygonToMatrix::creator()
{
   return new polygonToMatrix();
}


// INITIALIZES THE NODE BY CREATING ITS ATTRIBUTES:
MStatus polygonToMatrix::initialize()
{
   // CREATE AND ADD ".inMesh" ATTRIBUTE:
   MFnTypedAttribute inMeshAttrFn;
   MFnNumericAttribute 

   return MS::kSuccess;
}


// COMPUTE METHOD'S DEFINITION:
MStatus polygonToMatrix::compute(const MPlug &plug, MDataBlock &data)
{

   // DO THE COMPUTE ONLY FOR THE *OUTPUT* PLUGS THAT ARE DIRTIED:
   if ((plug == aPosition)  || (plug == aPositionX)  || (plug == aPositionY)  || (plug == aPositionZ)
    || (plug == aNormal) || (plug == aNormalX) || (plug == aNormalY) || (plug == aNormalZ))
   {
      // READ IN ".inMesh" DATA:
      MDataHandle inMeshDataHandle = data.inputValue(aInMesh);
      MObject inMesh = inMeshDataHandle.asMesh();

      // READ IN ".faceIndex" DATA:
      MDataHandle faceIndexDataHandle = data.inputValue(aFaceIndex);
      int faceIndex = faceIndexDataHandle.asLong();

      // READ IN ".relative" DATA:
      MDataHandle relativeDataHandle = data.inputValue(aRelative);
      bool relative = relativeDataHandle.asBool();

      // READ IN ".parameterU" DATA:
      MDataHandle parameterUDataHandle = data.inputValue(aParameterU);
      double parameterU = parameterUDataHandle.asDouble();

      // READ IN ".parameterV" DATA:
      MDataHandle parameterVDataHandle = data.inputValue(aParameterV);
      double parameterV = parameterVDataHandle.asDouble();

      // GET THE POINT AND NORMAL:
      MPoint point;
      MVector normal;
      MDagPath dummyDagPath;
      getPointAndNormal(dummyDagPath, faceIndex, relative, parameterU, parameterV, point, normal, inMesh);

      // WRITE OUT ".position" DATA:
      MDataHandle pointDataHandle = data.outputValue(aPosition);
      pointDataHandle.set(point.x, point.y, point.z);
      data.setClean(plug);

      // WRITE OUT ".normal" DATA:
      MDataHandle normalDataHandle = data.outputValue(aNormal);
      normalDataHandle.set(normal.x, normal.y, normal.z);
      data.setClean(plug);
   }
   else
      return MS::kUnknownParameter;

   return MS::kSuccess;
}