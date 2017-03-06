#pragma once

#include <SGSpace.h>
#include <SGSymmetry.h>
#include <SGSplitPoint.h>


class SGToolCondition
{
public:

	enum toolMode {
		kDefault,
		kMoveMode,
		kBrushMode
	};

	SGToolCondition();

	void setSymmetry( int modeNum );
	void setToolMode(int modeNum);
	
	void update();

	float vertexWeight;
	float manipScale;
	SGSymmetry symInfo;
	SGSpace  spaceInfo;
	SGToolCondition::toolMode mode;
	
	static SGToolCondition option;
	static MString getOptionString();
	static bool toolIsOn;
};