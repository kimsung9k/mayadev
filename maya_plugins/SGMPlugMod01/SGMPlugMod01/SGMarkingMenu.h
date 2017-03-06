#pragma once

#include <maya/MGlobal.h>
#include <maya/MString.h>


class SGMarkingMenu
{
public:
	MString parentName;
	MString pythonCommand;
	MString mmCommandPython;
	void createPythonCommand();

	static MString origCommand;
	void setVtxMenu();
	void setEdgeMenu();
	void setPolyMenu();
	void setDefaultMenu();
	
	static MString commandStart;
	static MString commandEnd;

	static MString edgeSplitMenuItem;
	static MString edgeSplitRingMenuItem;

	void setMenu( MString menuCommand );

	static SGMarkingMenu menu;
};