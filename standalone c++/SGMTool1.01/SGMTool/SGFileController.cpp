#include "SGScene.h"
#include "SGFileController.h"


SGFileController::SGFileController()
{

}



SGFileController::~SGFileController()
{

}


void SGFileController::openFile(const char* filePath)
{
	string fileString(filePath);

	int indexDot = fileString.rfind('.');
	string extension = fileString.substr(indexDot+1, fileString.size()-1);

	int beforeNumMesh = SGScene::dagNodeContainer.m_numMeshs;
	if (strcmp(extension.c_str(), "obj") || strcmp(extension.c_str(), "OBJ"))
	{
		SGFile::readObjFile(filePath, SGScene::dagNodeContainer);
		for (int i = beforeNumMesh; i < SGScene::dagNodeContainer.m_numMeshs; i++)
		{
			SGScene::dagNodeContainer.updateBuffer(i);
		}
	}
}