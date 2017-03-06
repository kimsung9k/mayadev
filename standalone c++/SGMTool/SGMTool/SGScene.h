#pragma once

#include "SGDagNodeContainer.h"
#include "SGShaderContainer.h"


class SGScene
{
public:
	static void createBase();
	static bool checkShaderStatus(GLuint shaderID);

	static void newScene();

	static SGShaderStruct     defaultShader;

	static SGDagNodeContainer dagNodeContainer; 
	static SGShaderContainer  shaderContainer;
};