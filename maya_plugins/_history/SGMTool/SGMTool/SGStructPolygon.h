#pragma once

#include "SGDefault.h"
#include "SGVector.h"


struct SGStructPolygon
{
	vector<SGVector>  m_poses;
	vector<SGVector>  m_nors;
	vector<vector<int>> m_mapVtxToNors;
	vector<vector<int>> m_mapVtxToPolys;
	vector<vector<int>> m_mapPolyToVtxs;
	vector<vector<int>> m_mapPolyToNors;
};