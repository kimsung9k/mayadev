#pragma once

#include <maya/MColor.h>

class SGColor
{
public:
	static const MColor defaultColor;
	static const MColor defaultOppositeColor;
	static const MColor splitEgeColor;
	static const MColor selectionColor;
	static const MColor selectionOppositeColor;

	static const MColor xColor;
	static const MColor yColor;
	static const MColor zColor;
	static const MColor cColor;
	static const MColor selectColor;

	static const MColor normalColor;
	static const MColor horizonColor;

	static const MColor edgeColor;
	static const MColor edgeHighlightColor;
};