#ifndef GLSL
#define GLSL( version,A ) "#version " #version"\n" #A
#endif

#include "SGShaderContainer.h"


const char* defaultVertexShaderCode = GLSL(430,

	in layout(location = 0) vec3 position;
in layout(location = 1) vec3 normal;

uniform mat4 worldToViewMatrix;
uniform mat4 objectMatrix;

out vec3 thePosition;
out vec3 theNormal;

void main()
{
	vec4 worldPosition = objectMatrix*vec4(position, 1);

	thePosition = worldPosition.xyz;
	theNormal = normalize((objectMatrix * vec4(normal, 0)).xyz);

	gl_Position = worldToViewMatrix*worldPosition;
}

);



const char* defaultFragmentShaderCode = GLSL(430,

	uniform vec3 camPosition;
uniform vec3 camVector;

in vec3 thePosition;
in vec3 theNormal;

out vec4 outColor;

void main()
{
	vec3 vec3Light = camPosition - thePosition;

	float dotValue = dot(normalize(vec3Light), theNormal);
	float offset = 0;
	float amientLight = 0.2;
	float oppositeValue = 0.7;

	if (gl_FrontFacing)
	{
		dotValue = ((dotValue - offset) / (1 - offset));
		dotValue = dotValue*(1 - amientLight) + amientLight;
		outColor = vec4(dotValue, dotValue, dotValue, 1);
	}
	else
	{
		dotValue = (-(dotValue - offset) / (1 + offset))*(1 - amientLight) + amientLight;
		dotValue *= oppositeValue;
		outColor = vec4(dotValue*0.85, dotValue*0.95, dotValue, 1);
	}
	//outColor = vec4(1, 1, 1, 1);
}

);