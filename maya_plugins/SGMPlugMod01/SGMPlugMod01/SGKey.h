#pragma once

#include <SGBase.h>
#include <QtGui/qevent.h>
#include <maya/MString.h>


class SGKey
{
public:
	enum KeyCondition
	{
		kPressed,
		kReleased
	};
	enum KeyEvent
	{
		kNone,
		kPress,
		kRelease
	};
	SGKey( MString keyName, unsigned short keyIndex, bool breakEvent =false );
	static bool translateEvent(QEvent* evt );

	MString keyName;
	unsigned short keyIndex;
	bool breakEvent;
	KeyCondition m_condition;
	KeyEvent     m_eventType;

	static SGKey* key(MString keyName);
	static SGKey* key(unsigned short keyindex);
	static void initializeKeys();
	static vector<SGKey> KEYS;
};