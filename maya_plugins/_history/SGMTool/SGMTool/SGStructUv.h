#pragma once

#include "SGDefault.h"
#include "SGVector2f.h"


struct SGStructUv
{
	vector<int> m_mapVtxToUv;
	vector<int> m_mapPolyToNet;

	vector<SGVector2f>  m_uvs;
	vector<vector<int>> m_mapNetToUvs;
	vector<vector<int>> m_mapUvToNets;

	string m_name;
};