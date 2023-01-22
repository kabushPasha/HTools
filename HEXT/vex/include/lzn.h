#include <voplib.h>
	
// Vnoise
int vseed(vector P)
{
	int seed;
	float f1,f2;
	vector p1,p2;
	vnoise(P,1,seed,f1,f2,p1,p2);

	return random_fhash( float(rand(p1)) );	
}
	
// WORLEY NOISES
float wseed(vector P)	
{
	int seed;
	float f1,f2;
	wnoise(P, seed, f1, f2);
	return seed;	
}
float wf1(vector P)	
{
	int seed;
	float f1,f2;
	wnoise(P, seed, f1, f2);
	return f1;	
}
float wf2(vector P)	
{
	int seed;
	float f1,f2;
	wnoise(P, seed, f1, f2);
	return f2;	
}

float cwseed(vector P)	
{
	int seed;
	float f1,f2;
	cwnoise(P, seed, f1, f2);
	return seed;	
}
float cwf1(vector P)	
{
	int seed;
	float f1,f2;
	cwnoise(P, seed, f1, f2);
	return f1;	
}
float cwf2(vector P)	
{
	int seed;
	float f1,f2;
	cwnoise(P, seed, f1, f2);
	return f2;	
}

float mwseed(vector P)	
{
	int seed;
	float f1,f2;
	mwnoise(P, seed, f1, f2);
	return seed;	
}
float mwf1(vector P)	
{
	int seed;
	float f1,f2;
	mwnoise(P, seed, f1, f2);
	return f1;	
}
float mwf2(vector P)	
{
	int seed;
	float f1,f2;
	mwnoise(P, seed, f1, f2);
	return f2;	
}


float boxes(vector _pos)
{
	vector pos = _pos;
	pos -= {0.5,0.5,0.5};
	pos = abs(pos % 1);	
	return max(abs(pos - {0.5,0.5,0.5}));
}	
float spheres(vector _pos)
{
	vector pos = _pos;
	pos -= {0.5,0.5,0.5};
	pos = abs(pos % 1);	
	return length(pos - {0.5,0.5,0.5});
}		
	

	
	
// UBER NOISES
// CURL with sdf  /////////////////////////////////
vector curl(vector4 pos;float freq;int turb;float rough;float atten;string type;string path;float surfaceEffectRadius)
{	
	//float surfaceEffectRadius = 1;
	float distanceToSurface = 1;
	float stepSize = 0.0001;
	string noiseType = type + "noise";
	// p,o,s,a,x
	string sdf = "";	 
	if(path!=""){sdf = "op:"+path;}
	// distance to surface might need fixes
	vector noise =  vop_curlNoiseVP(pos,set(freq,freq,freq),{0,0,0},{0,0,0},noiseType,sdf,turb,0,1,rough,atten,distanceToSurface,surfaceEffectRadius,stepSize);
	return noise;
	}
// Turbulent
float turb(vector pos;int turb;float rough;float atten;string type)
{
	float noise;
	if (type=="o")	noise = onoise(pos, turb, rough, atten);
	if (type=="a")	noise = anoise(pos, turb, rough, atten);
	if (type=="s")	noise = snoise(pos, turb, rough, atten);
	if (type=="x")	noise = vop_simplexNoiseVF(pos, turb, 1, rough, atten);
	if (type=="p")	noise = vop_perlinNoiseVF(pos, turb, 1, rough, atten);
	if (type=="c")	noise = vop_correctperlinNoiseVF(pos, turb, 1, rough, atten);	
	return noise;	
}
vector turbv(vector pos;int turb;float rough;float atten;string type)
{
	vector noise;
	if (type=="o")	noise = onoise(pos, turb, rough, atten);
	if (type=="a")	noise = anoise(pos, turb, rough, atten);
	if (type=="s")	noise = snoise(pos, turb, rough, atten);
	if (type=="x")	noise = vop_simplexNoiseVV(pos, turb, 1, rough, atten);
	if (type=="p")	noise = vop_perlinNoiseVV(pos, turb, 1, rough, atten);
	if (type=="c")	noise = vop_correctperlinNoiseVV(pos, turb, 1, rough, atten);	
	return noise;
}
// Flow
float flow(vector pos;int turb;float rough;float flow;float flowRate;float selfAdvect)
{
	float noise = vop_fbmFlowNoiseFV(pos, rough, turb, flow, flowRate, selfAdvect);
	return noise;
}
float flow(vector4 pos;int turb;float rough;float flow;float flowRate;float selfAdvect)
{
	float noise = vop_fbmFlowNoiseFP(pos, rough, turb, flow, flowRate, selfAdvect);
	return noise;
}
vector flowv(vector pos;int turb;float rough;float flow;float flowRate;float selfAdvect)
{	
	vector noise = vop_fbmFlowNoiseVV(pos, rough, turb, flow, flowRate, selfAdvect);
	return noise;	
}
vector flowv(vector4 pos;int turb;float rough;float flow;float flowRate;float selfAdvect)
{	
	vector noise = vop_fbmFlowNoiseVP(pos, rough, turb, flow, flowRate, selfAdvect);	
	return noise;
}
// Anti Alised
float aa(vector pos;int turb;float rough;int x)
{	
	string type = "noise";
	if (x!=0)  type = "xnoise";
	float noise = vop_fbmNoiseFV(pos,rough,turb,type);	
	return noise;
}
float aa(float pos;int turb;float rough;int x)
{	
	string type = "noise";
	if (x!=0)  type = "xnoise";
	float noise = vop_fbmNoiseFF(pos,rough,turb,type);	
	return noise;
}
float aa(vector4 pos;int turb;float rough;int x)
{	
	string type = "noise";
	if (x!=0)  type = "xnoise";
	float noise = vop_fbmNoiseFP(pos,rough,turb,type);	
	return noise;
}
vector aav(vector pos;int turb;float rough;int x)
{	
	string type = "noise";
	if (x!=0)  type = "xnoise";
	vector noise = vop_fbmNoiseVV(pos,rough,turb,type);	
	return noise;
}
vector aav(float pos;int turb;float rough;int x)
{	
	string type = "noise";
	if (x!=0)  type = "xnoise";
	vector noise = vop_fbmNoiseVF(pos,rough,turb,type);	
	return noise;
}
vector aav(vector4 pos;int turb;float rough;int x)
{	
	string type = "noise";
	if (x!=0)  type = "xnoise";
	vector noise = vop_fbmNoiseVP(pos,rough,turb,type);	
	return noise;
}


// set remapping
vector4 set(vector P;float x)
{
	return set(P.x,P.y,P.z,x);	
}

// unpacking matrix
vector mx(matrix matx){
	return set(matx.xx, matx.xy, matx.xz);
}
vector my(matrix matx){
	return set(matx.yx, matx.yy, matx.yz);
}
vector mz(matrix matx){
	return set(matx.zx, matx.zy, matx.zz);
}		
vector mx(vector4 orient){
	matrix matx = qconvert(orient);
	return set(matx.xx, matx.xy, matx.xz);
}
vector my(vector4 orient){
	matrix matx = qconvert(orient);
	return set(matx.yx, matx.yy, matx.yz);
}
vector mz(vector4 orient){
	matrix matx = qconvert(orient);
	return set(matx.zx, matx.zy, matx.zz);
}	
	
// Polar Coords
vector topolar(vector P){
	return vop_topolar(set(P.x,P.z,P.y));
}
vector frompolar(vector polar){
	vector P = vop_frompolar(polar.x,polar.y,polar.z);
	return set(P.x,P.z,P.y);
}		
	
	
	
	
	








