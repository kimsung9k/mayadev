TEMPLATE = app

QT += qml quick
CONFIG += c++11

RESOURCES += qt.qrc

qml.files = qt.qml

launch_modeall {
	CONFIG(debug, debug|release) {
	    DESTDIR = debug
	} else {
	    DESTDIR = release
	}
}

SOURCES += qt.cpp
