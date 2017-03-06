#include "precompile.h"
#include "SGToolCondition.h"
#include "SGGeneralManip.h"
#include "SGTransformManip.h"
#include "SGNormalManip.h"
#include "SGPolygonManip.h"
#include "SGSoftSelectionManip.h"
#include <SGSelection.h>
#include <SGIntersectResult.h>
#include "SGPrintf.h"


extern vector<SGGeneralManip> GeneralManips;
extern SGTransformManip       transManip;
extern SGNormalManip          normalManip;
extern SGPolygonManip         polygonManip;
extern SGSoftSelectionManip   softSelectionManip;

extern vector<SGIntersectResult> generalResult;
extern vector<SGIntersectResult> edgeSplitIntersectResult;

extern vector<vector<SGSplitPoint>> spPointsArr;
extern vector<int>  snapIndexArr;

SGToolCondition SGToolCondition::option;
bool SGToolCondition::toolIsOn;

SGToolCondition::SGToolCondition() {
	vertexWeight = 1;
	manipScale = 1;
	symInfo.setNoMirror();
	update();
	toolIsOn = false;
	mode = SGToolCondition::kDefault;
}

void SGToolCondition::update() {
	
	if (symInfo.isNoMirror()) {
		sgPrintf("is no mirror");
		spPointsArr.resize(1);
		snapIndexArr.resize(1);
		generalResult.resize(1);
		edgeSplitIntersectResult.resize(1);
	}
	if (symInfo.isXMirror()) {
		sgPrintf("is x mirror");
		spPointsArr.resize(2);
		snapIndexArr.resize(2);
		generalResult.resize(2);
		edgeSplitIntersectResult.resize(2);
	}
	for (int i = 0; i < spPointsArr.size(); i++) {
		spPointsArr[i].clear();
	}
}


void SGToolCondition::setSymmetry(int modeNum)
{
	if (modeNum == 1) {
		symInfo.setXMirror();
	}
	else {
		symInfo.setNoMirror();
	}
	update();
}


void SGToolCondition::setToolMode(int modeNum)
{
	if (modeNum == 0) {
		mode = kDefault;
	}
	else if(modeNum == 1) {
		mode = kMoveMode;
	}
	else if (modeNum == 2) {
		mode = kBrushMode;
	}
}


MString SGToolCondition::getOptionString()
{
	MString stringResults;
	MString mirrorResults = "mirror:None;";
	MString vertexWeightResults = "weight:1.0;";
	MString manipScaleResults = "manipScale:1.0;";

	if (option.symInfo.isXMirror()) {
		mirrorResults = "mirror:x;";
	}
	if (option.vertexWeight != 1.0 ) {
		char buffer[128];
		sprintf(buffer, "weight:%f;", option.vertexWeight);
		vertexWeightResults = buffer;
	}
	if (option.manipScale != 1.0) {
		char buffer[128];
		sprintf(buffer, "manipScale:%f;", option.manipScale );
		manipScaleResults = buffer;
	}
	stringResults += mirrorResults;
	stringResults += vertexWeightResults;
	stringResults += manipScaleResults;

	return stringResults;
}