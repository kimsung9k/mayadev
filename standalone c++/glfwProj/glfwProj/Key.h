#pragma once

#include <GLFW/glfw3.h>


class Key
{
public:
	Key();
	~Key();

	static void key_callback(GLFWwindow* wnd, int key, int scancode, int action, int mods);
};