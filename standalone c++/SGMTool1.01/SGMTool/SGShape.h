#pragma once

#include "SGDefault.h"
#include "SGNode.h"
#include "SGShader.h"


class SGShape : public SGNode
{
public:
	SGShape();
	virtual ~SGShape();

	virtual void update();
	virtual void display();
	vector<SGShader*> m_pShaders;
};