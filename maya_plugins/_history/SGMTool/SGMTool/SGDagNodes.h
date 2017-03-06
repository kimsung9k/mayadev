#pragma once

#include <vector>
#include "SGDagNodeMesh.h"

using namespace std;


class SGDagNodes
{
public:
	void appendDagNodes(vector<SGDagNodeMesh> dagMeshs);

	vector<SGDagNodeMesh> m_meshs;
};