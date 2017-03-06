#include <Windows.h>
#include <stdio.h>
#include "SGViewControl.h"
#include "SGGLWindow.h"
#include "resource.h"
#include "SGScene.h"
#include "SGFileController.h"


#define MSG_CHECKNEXT 0
#define MSG_CHECKEND  1
#define MSG_MOUSEEVENT 2
#define MSG_RESULT int
#define MOUSE_EVT_RESULT int
#define MOUSE_EVT_UPDATE 1
#define MOUSE_EVT_NOUPDATE 0


SGGLWindow GLWindow;
HINSTANCE g_hInst;
HWND  g_hWnd;
HDC   g_hDC;
HGLRC g_hRC;
LRESULT CALLBACK WndProc(HWND hWnd, UINT iMessage, WPARAM wParam, LPARAM lParam);
MSG_RESULT mouseEventMessage(HWND, UINT, WPARAM, LPARAM);
MSG_RESULT menuEventMessage(HWND, UINT, WPARAM, LPARAM);
LPSTR lpszClass = "Consol Window";

GLvoid initializeGL();
GLvoid resize(GLsizei width, GLsizei height);
GLvoid drawScene();

SGViewControl ViewControl;

BOOL bSetupPixelFormat(HDC hdc)
{
	PIXELFORMATDESCRIPTOR pfd, *ppfd;
	int pixelformat;

	ppfd = &pfd;

	ppfd->nSize = sizeof(PIXELFORMATDESCRIPTOR);
	ppfd->nVersion = 1;
	ppfd->dwFlags = PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL |
		PFD_DOUBLEBUFFER;
	ppfd->dwLayerMask = PFD_MAIN_PLANE;
	ppfd->iPixelType = PFD_TYPE_RGBA;
	ppfd->iLayerType = PFD_MAIN_PLANE;
	ppfd->cColorBits = 32;
	ppfd->cDepthBits = 32;
	ppfd->cStencilBits = 32;
	ppfd->cAlphaBits = 32;

	pixelformat = ChoosePixelFormat(hdc, ppfd);

	if ((pixelformat = ChoosePixelFormat(hdc, ppfd)) == 0)
	{
		MessageBox(NULL, TEXT("ChoosePixelFormat failed"), TEXT("Error"), MB_OK);
		return FALSE;
	}

	if (SetPixelFormat(hdc, pixelformat, ppfd) == FALSE)
	{
		MessageBox(NULL, TEXT("SetPixelFormat failed"), TEXT("Error"), MB_OK);
		return FALSE;
	}

	return TRUE;
}


int main()
{
	MSG Message;
	WNDCLASS wndclass;

	HINSTANCE hInstance = GetModuleHandle(NULL);
	g_hInst = hInstance;

	wndclass.style = 0;
	wndclass.lpfnWndProc = (WNDPROC)WndProc;
	wndclass.cbClsExtra = 0;
	wndclass.cbWndExtra = 0;
	wndclass.hInstance = hInstance;
	wndclass.hIcon = LoadIcon(hInstance, lpszClass);
	wndclass.hCursor = LoadCursor(NULL, IDC_ARROW);
	wndclass.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
	wndclass.lpszMenuName = MAKEINTRESOURCE(IDR_MENU1);
	wndclass.lpszClassName = lpszClass;
	RegisterClass(&wndclass);

	g_hWnd = CreateWindowEx(WS_EX_TOPMOST, lpszClass,
		lpszClass,
		WS_OVERLAPPEDWINDOW | WS_CLIPSIBLINGS | WS_CLIPCHILDREN,
		700, 100,
		1200, 800,
		NULL, NULL, hInstance, NULL);

	ShowWindow(g_hWnd, SW_SHOW);
	UpdateWindow(g_hWnd);

	SGViewControl::initializeCamera();
	SGScene::createBase();

	while (GetMessage(&Message, 0, 0, 0)) {
		TranslateMessage(&Message);
		DispatchMessage(&Message);
	}
	return 0;
}


LRESULT CALLBACK WndProc(HWND hWnd, UINT iMessage, WPARAM wParam, LPARAM lParam)
{
	RECT rt;

	switch (iMessage)
	{
	case WM_CREATE:
		g_hDC = GetDC(hWnd);
		if (!bSetupPixelFormat(g_hDC))
			PostQuitMessage(0);
		g_hRC = wglCreateContext(g_hDC);
		wglMakeCurrent(g_hDC, g_hRC);
		GetClientRect(hWnd, &rt);
		initializeGL();
		ViewControl.initializeCamera();
		break;

	case WM_PAINT:
	case WM_SIZE:
		GetClientRect(hWnd, &rt);
		ViewControl.SetWindowWidthHeight(rt.right, rt.bottom);
		resize(rt.right, rt.bottom);
		drawScene();
		break;

	case WM_DESTROY:
		if (g_hRC)
			wglDeleteContext(g_hRC);
		if (g_hDC)
			ReleaseDC(hWnd, g_hDC);
		PostQuitMessage(0);
		break;
	}

	MSG_RESULT msgResultMenu  = menuEventMessage(hWnd, iMessage, wParam, lParam);
	if (msgResultMenu == MSG_CHECKEND) return TRUE;
	MSG_RESULT msgResultMouse = mouseEventMessage(hWnd, iMessage, wParam, lParam);
	if (ViewControl.mouseEventControl() == MOUSE_EVT_UPDATE) drawScene();
	if (msgResultMouse == MSG_CHECKEND) return TRUE;
	return (LONG)DefWindowProc(hWnd, iMessage, wParam, lParam);
}


MSG_RESULT menuEventMessage(HWND hWnd, UINT iMessage, WPARAM wParam, LPARAM lParam)
{
	OPENFILENAME OFN;
	char lpstrFile[MAX_PATH] = "";
	char str[300];

	if(iMessage != WM_COMMAND) return MSG_CHECKNEXT;

	switch(LOWORD(wParam))
	{
	case ID_FILE_NEWSCENE:
		SGScene::newScene();
		drawScene();
		return MSG_CHECKEND;
	case ID_FILE_OPENFILE:
		memset(&OFN, 0, sizeof(OPENFILENAME));
		OFN.lStructSize = sizeof(OPENFILENAME);
		OFN.hwndOwner=hWnd;
		OFN.lpstrFilter="모든 파일(*.*)\0*.*\0";
		OFN.lpstrFile=lpstrFile;
		OFN.nMaxFile=MAX_PATH;
		if (GetOpenFileName(&OFN)!=0) {
			SGFileController::openFile(OFN.lpstrFile);
		}
		drawScene();
		return MSG_CHECKEND;
	}
	return MSG_CHECKNEXT;
}


MSG_RESULT mouseEventMessage(HWND hWnd, UINT iMessage, WPARAM wParam, LPARAM lParam)
{
	switch (iMessage)
	{
	case WM_LBUTTONDOWN:
	case WM_RBUTTONDOWN:
	case WM_MBUTTONDOWN:
		SetCapture(hWnd);
		break;

	case WM_LBUTTONUP:
	case WM_RBUTTONUP:
	case WM_MBUTTONUP:
		ReleaseCapture();
		break;
	}

	switch (iMessage)
	{
	case WM_LBUTTONDOWN:
		ViewControl.SetLButtonDown(TRUE); break;
	case WM_LBUTTONUP:
		ViewControl.SetLButtonDown(FALSE); break;
	case WM_RBUTTONDOWN:
		ViewControl.SetRButtonDown(TRUE); break;
	case WM_RBUTTONUP:
		ViewControl.SetRButtonDown(FALSE); break;
	case WM_MBUTTONDOWN:
		ViewControl.SetMButtonDown(TRUE); break;
	case WM_MBUTTONUP:
		ViewControl.SetMButtonDown(FALSE); break;
	}

	switch (iMessage)
	{
	case WM_LBUTTONDOWN:
	case WM_LBUTTONUP:
	case WM_RBUTTONDOWN:
	case WM_RBUTTONUP:
	case WM_MBUTTONDOWN:
	case WM_MBUTTONUP:
	case WM_MOUSEMOVE:
		ViewControl.SetPMouseClient(LOWORD(lParam), HIWORD(lParam));
		return MSG_CHECKEND;
	}
	return MSG_CHECKNEXT;
}


GLvoid initializeGL()
{
	GLWindow.initializeGL();
}


GLvoid resize(GLsizei width, GLsizei height )
{
	GLWindow.resizeGL(width, height);
}


GLvoid drawScene()
{
	GLWindow.paintGL();
	SwapBuffers(g_hDC);
}