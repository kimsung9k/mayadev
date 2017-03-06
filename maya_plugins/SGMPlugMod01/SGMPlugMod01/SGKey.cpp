#include "precompile.h"

#include "SGKey.h"
#include "SGPrintf.h"


vector<SGKey> SGKey::KEYS;

SGKey::SGKey(MString keyName, unsigned short keyIndex, bool breakEvent)
{
	this->keyName = keyName;
	this->keyIndex = keyIndex;
	this->breakEvent = breakEvent;

	m_condition = kReleased;
	m_eventType = kNone;
}


void SGKey::initializeKeys()
{
	SGKey::KEYS.clear();
	SGKey::KEYS.push_back(SGKey("shift", 32));
	SGKey::KEYS.push_back(SGKey("ctrl", 33));
	SGKey::KEYS.push_back(SGKey("alt", 35));
	SGKey::KEYS.push_back(SGKey("backspace", 3, true ));
	SGKey::KEYS.push_back(SGKey("delete", 7, true));
	SGKey::KEYS.push_back(SGKey("z", 90));
	SGKey::KEYS.push_back(SGKey("w", 87));
	SGKey::KEYS.push_back(SGKey("s", 83));
	SGKey::KEYS.push_back(SGKey("b", 66));
	SGKey::KEYS.push_back(SGKey("v", 86));
	SGKey::KEYS.push_back(SGKey("d", 68));
	SGKey::KEYS.push_back(SGKey("f", 70));
	SGKey::KEYS.push_back(SGKey(">", 62));
	SGKey::KEYS.push_back(SGKey("<", 60));
	SGKey::KEYS.push_back(SGKey("esc", 0, true));
}


SGKey* SGKey::key(MString keyName)
{
	for (int i = 0; i < KEYS.size(); i++) {
		if (KEYS[i].keyName == keyName) return &KEYS[i];
	}
	return NULL;
}


SGKey* SGKey::key(unsigned short keyIndex)
{
	for (int i = 0; i < KEYS.size(); i++){
		if (KEYS[i].keyIndex == keyIndex) return &KEYS[i];
	}
	return NULL;
}


bool SGKey::translateEvent(QEvent* evt)
{
	int keyIndex;

	for (int i = 0; i < KEYS.size(); i++) {
		KEYS[i].m_eventType = kNone;
	}

	if (evt->type() == QEvent::KeyPress ||
		evt->type() == QEvent::KeyRelease) {
		QKeyEvent* keyEvt = (QKeyEvent*)evt;
		if (keyEvt->isAutoRepeat()) return false;
		keyIndex = keyEvt->key();
	}
	else return false;

	//sgPrintf("keyIndex : %d", keyIndex);

	SGKey* ptrKey = key(keyIndex);
	SGKey* compairKey = key("ctrl");

	if (ptrKey == NULL) return false;

	if (evt->type() == QEvent::KeyPress) {
		ptrKey->m_condition = kPressed;
		ptrKey->m_eventType = kPress;
	}
	else if (evt->type() == QEvent::KeyRelease) {
		ptrKey->m_condition = kReleased;
		ptrKey->m_eventType = kRelease;
	}
	return true;
}