#include "precompile.h"
#include "SGPermit.h"

#include <stdio.h>
#include <string>

#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "Ole32.lib")

#include "SGPrintf.h"


SGPermit::SGPermit() {
	getMyIP();
}

int SGPermit::getMyIP()
{
	bool bInit = false;
	
	WSADATA wsaData;
	WSAStartup(MAKEWORD(2, 2), &wsaData);

	PHOSTENT hostinfo;
	char hostname[50];
	char ipaddr[50];
	memset(hostname, 0, sizeof(hostname));
	memset(ipaddr, 0, sizeof(ipaddr));

	int nError = gethostname(hostname, sizeof(hostname));
	if (nError == 0)
	{
		hostinfo = gethostbyname(hostname);
		strcpy(ipaddr, inet_ntoa(*(struct in_addr*)hostinfo->h_addr_list[0]));
	}
	WSACleanup();

	sgPrintf("host name : %s", hostname);
	sgPrintf("ip iddr : %s", ipaddr);
	return true;
}