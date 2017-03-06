#include "SGTransform.h"


SGTransform::SGTransform()
{
	m_typeName = "transform";
	m_ptrParent = NULL;
	m_ptrShape  = NULL;
}


SGTransform::~SGTransform()
{
}


unsigned int SGTransform::numChildren() const
{
	return m_ptrsChild.size();
}



SGTransform* SGTransform::getParentPtr() const
{
	return m_ptrParent;
}



SGTransform* SGTransform::getChildPtr(unsigned int index) const
{
	return m_ptrsChild[index];
}


void SGTransform::updateMatrix()
{
	if (m_ptrParent != NULL)
		m_mtxWorld = m_ptrParent->m_mtxWorld * m_mtxLocal;

	for (int i = 0; i < m_ptrsChild.size(); i++)
		m_ptrsChild[i]->updateMatrix();
}


void SGTransform::updateMatrix(SGMatrix mtxUpdate)
{
	m_mtxLocal = mtxUpdate;
	updateMatrix();
}