#include "precompile.h"
#include "SGBase.h"
#include "SGMarkingMenu.h"
#include "Names.h"
#include <SGPrintf.h>


SGMarkingMenu SGMarkingMenu::menu;

void SGMarkingMenu::createPythonCommand() {
	mmCommandPython = Names::commandName + "_markingMenu";
	parentName = "'\" + $parentName + \"'";

	pythonCommand = "def " + mmCommandPython + "( parentName, **options ):\n"
		"	print parentName\n"
		"	for key, value in options.items():\n"
		"		if key == 'edge' and value == 1:\n"
		"			try:" + mmCommandPython + "_edgeMenu(parentName)\n"
		"			except: print 'edge menu failed '\n"
		"		elif key == 'poly' and value == 1:\n"
		"			try:" + mmCommandPython + "_polyMenu(parentName)\n"
		"			except: print 'poly menu failed '\n"
		"		elif key == 'vtx' and value == 1:\n"
		"			try:" + mmCommandPython + "_vtxMenu(parentName)\n"
		"			except: print 'vtx menu failed '\n";
	//sgPrintf("python command : \n%s", pythonCommand.asChar() );
	MGlobal::executePythonCommand(pythonCommand);
}


MString SGMarkingMenu::origCommand = ""
"global proc buildObjectMenuItemsNow( string $parentName)"
"{"
"	if (`exists DRUseModelingToolkitMM` && DRUseModelingToolkitMM($parentName)) {"
"		return;"
"	}"
""
"	global int $gIsMarkingMenuOn;"
""
"	if (`popupMenu -e -exists $parentName`) {"
"		popupMenu -e -deleteAllItems $parentName;	"
"		if (`popupMenu -q -mm $parentName` != $gIsMarkingMenuOn)"
"			popupMenu -e -mm $gIsMarkingMenuOn $parentName;"
"		"
"		if (!`dagObjectHit -mn $parentName`) {"
"			string $leadObject[] = `ls -sl -tail 1 -typ transform -typ shape`;"
"			if (size($leadObject) > 0) {"
"				dagMenuProc($parentName, $leadObject[0]);"
"			} else {"
"				if (`modelingTookitActive` && (`nexCtx -rmbComplete -q`) ) {"
"					ctxCompletion;"
"					return;"
"				}"
"				setParent -menu $parentName;"
""
"				menuItem"
"					-version \"2014\""
"					-label (uiRes(\"m_buildObjectMenuItemsNow.kSelectAll\"))"
"					-radialPosition \"S\""
"					-command (\"SelectAll\");"
""
"            	menuItem"
"					-label (uiRes(\"m_buildObjectMenuItemsNow.kCompleteTool\"))"
"					-radialPosition \"N\""
"					-command (\"CompleteCurrentTool\");"
""
"            	setParent ..;"
"			}"
"		}"
"	} else {"
"		warning (uiRes(\"m_buildObjectMenuItemsNow.kParentWarn\"));"
"	}"
"}"
"";


void SGMarkingMenu::setMenu(MString menuCommand) {
	MGlobal::executeCommand(menuCommand);
}


#include <SGPrintf.h>
void SGMarkingMenu::setDefaultMenu() {
	MString command = commandStart;
	command += commandEnd;
	setMenu(command);
}


void SGMarkingMenu::setVtxMenu() {
	createPythonCommand();

	MString command = commandStart;
	command += "python( \"" + mmCommandPython + "( " + parentName + ", vtx=1 )\" );\n";
	command += commandEnd;
	setMenu(command);
}


void SGMarkingMenu::setEdgeMenu() {
	createPythonCommand();

	MString command = commandStart;
	command += "python( \"" + mmCommandPython + "( " + parentName + ", edge=1 )\" );\n";
	command += commandEnd;
	setMenu(command);
}


void SGMarkingMenu::setPolyMenu() {
	createPythonCommand();

	MString command = commandStart;
	command += "python( \"" + mmCommandPython + "( " + parentName + ", poly=1 )\" );\n";
	command += commandEnd;
	setMenu(command);

	
}



MString SGMarkingMenu::commandStart = ""
"global proc buildObjectMenuItemsNow( string $parentName)\n"
"{\n"
"	if (`exists DRUseModelingToolkitMM` && DRUseModelingToolkitMM($parentName)) {\n"
"		return;\n"
"	}\n"
"\n"
"	popupMenu -e -deleteAllItems $parentName;\n";


MString SGMarkingMenu::commandEnd = "}\n";
