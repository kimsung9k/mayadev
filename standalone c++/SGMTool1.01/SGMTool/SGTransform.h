#pragma once

#include "SGDefault.h"
#include "SGShape.h"
#include "SGMatrix.h"


class SGTransform : public SGNode
{
public:
	SGTransform();
	virtual ~SGTransform();

	SGTransform*	getParentPtr() const;
	unsigned int numChildren() const;
	SGTransform*	getChildPtr(unsigned int index) const;
	void     updateMatrix();
	void     updateMatrix( SGMatrix );

	SGTransform* m_ptrParent;
	vector<SGTransform*> m_ptrsChild;

	SGMatrix m_mtxLocal;
	SGMatrix m_mtxWorld;

	SGShape* m_ptrShape;
};