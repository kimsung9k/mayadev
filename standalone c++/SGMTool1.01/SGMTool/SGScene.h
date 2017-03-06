#pragma once

#include "SGDefault.h"
#include <GL/glew.h>
#include "SGNode.h"
#include "SGShader.h"
#include "SGCamera.h"


class SGScene
{
public:
	static void newScene();

	static vector<SGNode*> getNodes( const string nodeType);
	static vector<SGNode*> m_nodePtrs;
};