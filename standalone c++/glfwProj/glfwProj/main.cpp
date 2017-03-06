#include <GL/glew.h> //1
#include <GLFW/glfw3.h>

#include  "Key.h"


int main(void)
{
	GLFWwindow* window;  //2

	if (!glfwInit()) //3
		return -1;

	window = glfwCreateWindow(640, 480, "Hello World", NULL, NULL); //4
	if (!window)
	{
		glfwTerminate(); //5
		return -1;
	}

	glfwMakeContextCurrent(window); //6
	glewInit(); //7
	glClearColor(0.5, 0.75, 1, 1); //8
	glClear(GL_COLOR_BUFFER_BIT); //9
	glfwSwapBuffers(window); //10

	glfwSetKeyCallback(window, Key::key_callback );

	while (!glfwWindowShouldClose(window))
	{
		glfwPollEvents(); //11
	}

	glfwTerminate(); //12
	return 0;
}