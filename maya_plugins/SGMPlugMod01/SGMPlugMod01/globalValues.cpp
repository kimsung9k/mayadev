#include "precompile.h"

#include <SGSplitPoint.h>
#include "SGGeneralManip.h"
#include "SGTransformManip.h"
#include "SGNormalManip.h"
#include "SGPolygonManip.h"
#include "SGSoftSelectionManip.h"
#include "SGDragSelectionManip.h"
#include "SGMoveBrushManip.h"
#include "SGWidget.h"


SGManip*  manip;
SGWidget* toolWidget;
SGEvent*  toolEvent;

vector<SGGeneralManip> GeneralManips;
SGTransformManip       transManip;
SGNormalManip          normalManip;
SGPolygonManip         polygonManip;
SGSoftSelectionManip   softSelectionManip;
SGDragSelectionManip   dragSelectionManip;
SGMoveBrushManip       moveBrushManip;

vector<SGIntersectResult> generalResult;
vector<SGIntersectResult> edgeSplitIntersectResult;

vector<vector<SGSplitPoint>> spPointsArr;
vector<int>  snapIndexArr;