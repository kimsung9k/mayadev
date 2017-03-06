#ifndef _PerlinNoise_h
#define _PerlinNoise_h

static int noiseBase[256];
void setNoiseBase(void);

float getNoise( float value, bool printValue=false );

#endif