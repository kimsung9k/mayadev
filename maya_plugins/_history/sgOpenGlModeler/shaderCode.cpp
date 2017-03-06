#include "SGShaderProgram.h"

#ifndef GLSL
#define GLSL( A ) #A
#endif

/**/
const char* SGShaderProgram::defaultVS_code = GLSL(

	attribute vec3 position;
	attribute vec3 normal;

	uniform mat4 projection;
	uniform mat4 objectMatrix;

	out vec3 thePosition;
	out vec3 theNormal;

	void main()
	{
		vec4 worldPosition = vec4(position, 1);

		thePosition = worldPosition.xyz;
		theNormal = normalize((vec4(normal, 0)).xyz);

		gl_Position = projection*worldPosition;
	}
);



const char* SGShaderProgram::defaultFS_code = GLSL(

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
		//outColor = vec4(theNormal, 1);
	}
);/**/