#include "precompile.h"

#include "SGManip.h"
#include "SGPrintf.h"

#include <QtGui/qwidget.h>
#include <QtOpenGL\qgl.h>


#define PI 3.14159265359

vector<vtxManipStruct>  SGManip::vtxs[MANIPLENGTH];
vector<edgeManipStruct> SGManip::edges[MANIPLENGTH];
vector<polyManipStruct> SGManip::polygons[MANIPLENGTH];
vector<shapeManipStruct> SGManip::shapes[MANIPLENGTH];
vector<curveManipStruct> SGManip::curves[MANIPLENGTH];


MTypeId SGManip::id((unsigned int)0x2016053049);


SGManip::SGManip()
{
	rend = MHardwareRenderer::theRenderer();
	gGLFT = rend->glFunctionTable();
}



SGManip::~SGManip()
{
	clearAll();
}



void *SGManip::creator()
{
	return new SGManip();
}



MStatus SGManip::initialize()
{
	MStatus stat;
	stat = MPxManipContainer::initialize();
	return stat;
}


void SGManip::draw(M3dView & view,
	const MDagPath & path,
	M3dView::DisplayStyle style,
	M3dView::DisplayStatus status)
{
	view.beginGL();

	MIntArray enableList;
	MIntArray disableList;
	GLint originPattern;
	GLint originLineWidth;
	GLint originPointSize;

	gGLFT->glGetIntegerv(GL_LINE_STIPPLE_PATTERN, &originPattern);
	gGLFT->glGetIntegerv(GL_LINE_WIDTH, &originLineWidth);
	gGLFT->glGetIntegerv(GL_POINT_SIZE, &originPointSize);

	int enableCheckList[3] = { GL_LINE_STIPPLE ,GL_POLYGON_STIPPLE, GL_DEPTH_TEST };

	for (int i = 0; i < 3; i++) {
		if (gGLFT->glIsEnabled(enableCheckList[i]))
			enableList.append(enableCheckList[i]);
		else
			disableList.append(enableCheckList[i]);
	}
	gGLFT->glEnableVertexAttribArray(0);

	gGLFT->glDisable(GL_LINE_STIPPLE);
	gGLFT->glEnable(GL_POLYGON_STIPPLE);

	for (int k = 0; k < MANIPLENGTH; k++)
	{
		//if (k == 1) gGLFT->glEnable(GL_DEPTH_TEST);
		//else if (k == 0) gGLFT->glDisable(GL_DEPTH_TEST);

		for (int i = (int)polygons[k].size() - 1; i >= 0; i--) {
			gGLFT->glColor3f(polygons[k][i].color.r, polygons[k][i].color.g, polygons[k][i].color.b);
			gGLFT->glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, polygons[k][i].points);
			gGLFT->glDrawArrays(GL_POLYGON, 0, polygons[k][i].numPoint);
		}

		for (int i = 0; i < edges[k].size(); i++) {
			gGLFT->glColor3f(edges[k][i].color.r, edges[k][i].color.g, edges[k][i].color.b);
			gGLFT->glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, edges[k][i].points);

			if (edges[k][i].pattern != 0) {
				gGLFT->glEnable(GL_LINE_STIPPLE);
				gGLFT->glLineStipple(0, edges[k][i].pattern);
			}
			gGLFT->glLineWidth(edges[k][i].lineWidth);
			gGLFT->glDrawArrays(GL_LINE_STRIP, 0, edges[k][i].numPoint);
			gGLFT->glLineWidth((MGLfloat)originLineWidth);
			if (edges[k][i].pattern != 0) gGLFT->glDisable(GL_LINE_STIPPLE);
		}

		for (int i = 0; i < vtxs[k].size(); i++) {
			gGLFT->glPointSize(vtxs[k][i].pointSise);
			gGLFT->glColor3f(vtxs[k][i].color.r, vtxs[k][i].color.g, vtxs[k][i].color.b);
			gGLFT->glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, &vtxs[k][i].point);
			gGLFT->glDrawArrays(GL_POINTS, 0, 1);
			gGLFT->glPointSize((MGLfloat)originPointSize);
		}


		for (int i = 0; i < curves[k].size(); i++) {
			gGLFT->glColor3f(curves[k][i].color.r, curves[k][i].color.g, curves[k][i].color.b);
			gGLFT->glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, curves[k][i].points);
			gGLFT->glPushMatrix();
			gGLFT->glMultMatrixf(curves[k][i].matrix);
			gGLFT->glDrawArrays(GL_LINE_STRIP, 0, curves[k][i].numPoints);
			gGLFT->glPopMatrix();
		}

		for (int i = 0; i < shapes[k].size(); i++) {
			gGLFT->glDisable(GL_POLYGON_STIPPLE);
			gGLFT->glColor3f(shapes[k][i].color.r, shapes[k][i].color.g, shapes[k][i].color.b);
			gGLFT->glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, shapes[k][i].points);
			int mode = GL_TRIANGLES;
			if (shapes[k][i].interval == 4) mode = GL_QUADS;
			gGLFT->glPushMatrix();
			gGLFT->glMultMatrixf(shapes[k][i].matrix);
			gGLFT->glDrawElements(mode, shapes[k][i].numPolygon * shapes[k][i].interval, GL_UNSIGNED_INT, shapes[k][i].elements);
			gGLFT->glPopMatrix();
			gGLFT->glEnable(GL_POLYGON_STIPPLE);
			int a = ( 0 > 10 ) ? 10 : 1;
		}
	}

	for (int i = 0; i < (int)enableList.length(); i++)
		gGLFT->glEnable(enableList[i]);
	for (int i = 0; i < (int)disableList.length(); i++)
		gGLFT->glDisable(disableList[i]);
	gGLFT->glLineStipple(0, originPattern);
	gGLFT->glLineWidth((MGLfloat)originLineWidth);
	gGLFT->glPointSize((MGLfloat)originPointSize);

	gGLFT->glDisableVertexAttribArray(0);

	view.endGL();

	MPxManipContainer::draw(view, path, style, status);
}



void SGManip::clearManip(int index) {
	vtxs[index].clear();
	edges[index].clear();
	for (int i = 0; i < polygons[index].size(); i++) {
		delete[] polygons[index][i].points;
	}
	polygons[index].clear();
	shapes[index].clear();
	curves[index].clear();
}



void SGManip::clearAll() {
	for (int i = 0; i < MANIPLENGTH - 1; i++) {
		vtxs[i].clear();
		edges[i].clear();
		polygons[i].clear();
		shapes[i].clear();
		curves[i].clear();
	}
}



void SGManip::pushPoint(int index, MPoint point, MColor color, short pointSize) {
	vtxManipStruct vtx;
	vtx.point.x = (float)point.x;
	vtx.point.y = (float)point.y;
	vtx.point.z = (float)point.z;
	vtx.point.w = (float)point.w;

	vtx.color.r = color.r;
	vtx.color.g = color.g;
	vtx.color.b = color.b;
	vtx.pointSise = pointSize;
	vtxs[index].push_back(vtx);
}



void SGManip::pushLine(int index, const MPointArray& points, MColor color, short lineWidth, GLushort* stiple) {
	edgeManipStruct edge;
	edge.points = new SGVec4[points.length()];
	edge.numPoint = points.length();
	for (int i = 0; i < edge.numPoint; i++) {
		edge.points[i].x = (float)points[i].x;
		edge.points[i].y = (float)points[i].y;
		edge.points[i].z = (float)points[i].z;
		edge.points[i].w = (float)points[i].w;
	}
	edge.color.r = color.r;
	edge.color.g = color.g;
	edge.color.b = color.b;
	edge.lineWidth = lineWidth;
	if (stiple == NULL)
		edge.pattern = 0;
	else
		edge.pattern = *stiple;
	edges[index].push_back(edge);
}



void SGManip::pushPolygon(int index, const MPointArray& points, MColor color, short lineWidth, GLushort* stiple) {
	polyManipStruct polygon;
	polygon.points = new SGVec4[points.length()];
	polygon.numPoint = points.length();
	for (int i = 0; i < polygon.numPoint; i++) {
		polygon.points[i].x = (float)points[i].x;
		polygon.points[i].y = (float)points[i].y;
		polygon.points[i].z = (float)points[i].z;
		polygon.points[i].w = (float)points[i].w;
	}
	polygon.color.r = color.r;
	polygon.color.g = color.g;
	polygon.color.b = color.b;
	polygon.lineWidth = lineWidth;
	if (stiple == NULL)
		polygon.pattern = 0;
	else
		polygon.pattern = *stiple;
	polygons[index].push_back(polygon);
}



void SGManip::pushShape(int index, const SGShape& shape, MMatrix mtx,
	MColor color)
{
	shapeManipStruct manipStruct;
	manipStruct.points = shape.points;
	manipStruct.elements = shape.indices;
	manipStruct.interval = shape.interval;
	manipStruct.numPolygon = shape.numPoly;
	manipStruct.color.r = color.r; manipStruct.color.g = color.g;
	manipStruct.color.b = color.b; manipStruct.color.a = color.a;

	for (int i = 0; i < 4; i++) {
		for (int j = 0; j < 4; j++) {
			manipStruct.matrix[i * 4 + j] = (float)mtx(i, j);
		}
	}
	shapes[index].push_back(manipStruct);
}



void SGManip::pushCurve(int index, float* pointList, unsigned int numPoints, MMatrix mtx, MColor color)
{
	curveManipStruct curve;
	curve.points = pointList;
	curve.numPoints = numPoints;
	curve.color.r = color.r; curve.color.g = color.g;
	curve.color.b = color.b; curve.color.a = color.a;

	for (int i = 0; i < 4; i++) {
		for (int j = 0; j < 4; j++) {
			curve.matrix[i * 4 + j] = (float)mtx(i, j);
		}
	}
	curves[index].push_back(curve);
}



MStatus SGManip::connectToDependNode(const MObject & node) {
	MStatus stat;
	MFnDependencyNode nodeFn(node);
	MPlug tPlug = nodeFn.findPlug("translate", &stat);

	MFnFreePointTriadManip freePointManipFn(transManip);
	freePointManipFn.connectToPointPlug(tPlug);

	MFnDagNode dagNodeFn(node);
	MDagPath nodePath;
	dagNodeFn.getPath(nodePath);

	MFnFreePointTriadManip manipFn(transManip);
	MTransformationMatrix m(nodePath.exclusiveMatrix());

	double rot[3];
	MTransformationMatrix::RotationOrder rOrder;
	m.getRotation(rot, rOrder, MSpace::kWorld);
	manipFn.setRotation(rot, rOrder);

	MVector trans = m.getTranslation(MSpace::kWorld);
	manipFn.setTranslation(trans, MSpace::kWorld);

	MPxManipContainer::connectToDependNode(node);
	return stat;
}



MStatus SGManip::createChildren() {
	finishAddingManips();
	return MS::kSuccess;
}