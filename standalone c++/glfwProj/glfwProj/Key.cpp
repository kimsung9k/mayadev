#include "Key.h"
#include <stdio.h>


Key::Key()
{
}


Key::~Key()
{
}


void Key::key_callback(GLFWwindow* wnd, int key, int scancode, int action, int mods) {
	printf("key : %d, scancode : %d, action : %d, mods:%d\n", key, scancode, action, mods );
}