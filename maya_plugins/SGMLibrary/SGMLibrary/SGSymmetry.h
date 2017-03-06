#pragma once

#include "SGComponentType.h"
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MMatrix.h>
#include <maya/MPointArray.h>


class SGSymmetry
{
public:
	enum SymmetryType {
		kNoMirror,
		kXMirror,
	};

	static MMatrix xMirrorMatrix();
	static MMatrix yMirrorMatrix();
	static MMatrix zMirrorMatrix();

	SGSymmetry::SGSymmetry();
	
	SymmetryType mirrorTyp;

	void setNoMirror();
	void setXMirror();

	bool isNoMirror() const;
	bool isXMirror() const;

	MMatrix mirrorMatrix()  const;

	MPoint      getMirroredViewPoint(const MPoint& viewPoint, const MMatrix& camMatrix ) const;
	MPointArray getMirroredViewPoints(const MPointArray& viewPoints, const MMatrix& camMatrix) const;

	void    convertPointToCenter(MPoint& pointToConvert)  const;
	MPoint  convertPointByMirror(const MPoint& pointSrc)  const;
	bool    compairIsMirror(const MPoint& base, const MPoint& target)  const;
	MVector convertVectorByMirror(const MPoint& source, const MPoint& dest, const MVector& vector, bool isCenter = false )  const;
};
