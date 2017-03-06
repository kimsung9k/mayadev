#include "SGNode.h"


SGNode::SGNode()
{
}


SGNode::~SGNode()
{
}


string SGNode::type() const
{
	return m_typeName;
}


string SGNode::name() const
{
	return m_name;
}