#include "SGScene.h"


void SGScene::newScene()
{
	for (int i = 0; i < m_nodePtrs.size(); i++) {
		delete m_nodePtrs[i];
	}
	m_nodePtrs.clear();
	SGShader* shaderPtr = new SGShader();
	shaderPtr->createDefaultShader();
	SGCamera* cameraPtr = new SGCamera();

	m_nodePtrs.push_back(shaderPtr);
	m_nodePtrs.push_back(cameraPtr);
}


vector<SGNode*> SGScene::getNodes(const string nodeType) {
	vector<SGNode*> nodePtrs;
	for (int i = 0; i < m_nodePtrs.size(); i++) {
		if (nodeType == m_nodePtrs[i]->type)
			nodePtrs.push_back(m_nodePtrs[i] );
	}
	return nodePtrs;
}