#pragma once

#include "SGMesh.h"
#include "SGCam.h"
#include <QtGui\qwidget.h>
#include <QtGui\qmainwindow.h>

class SGMainWindow : public QMainWindow
{
public:
	SGMainWindow( QWidget* parent );
	virtual ~SGMainWindow();

	void closeEvent(QCloseEvent* evt);

	void setCentralWidget(QWidget* widget);

	void setCamera(SGCam* cam);
	void appendMesh( SGMesh* mesh );

private:
	QWidget* m_centralWidget;
	
	SGCam* m_ptrCam;
	vector<SGMesh*> m_ptrMesh;
};