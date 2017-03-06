#pragma once

#include "SGShape.h"
#include "SGStructPolygon.h"
#include "SGStructUv.h"
#include "SGBufferMesh.h"
#include <GL/glew.h>

class SGMesh : public SGShape
{
public:
	SGMesh();
	virtual ~SGMesh();

	void rebuildBuffer();
	virtual void update();
	virtual void display();
	
	SGStructPolygon*    m_pPoly;
	vector<SGStructUv*> m_pUvs;
	vector<SGBufferMesh*> m_pBufferMeshs;
	vector<int> m_mapPolyToShader;
};