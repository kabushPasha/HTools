#include <voplib.h>
/*
TURBULENT NOISE
op - original pelin
al - alligator
sc - sparse convultion

sx - simplex
pn - perlin noise
cp - centerd perlin noise

AA NOISE
aas - simplex noise
aap - perlin noise

CURL NOISE
cpn - curl perlin noise
can - alligator
cxn - smiplex
csn - sparse convultion
con - original perlin
*/

	// SMIPLE TURBULENT NOISES
// ORIGINAL PERLIN NOISE
float ofn(vector pos;int turb;float rough;float atten){	
	float noise = onoise(pos, turb, rough, atten);	
	return noise;}
float ofn(vector pos;int turb;float rough){	
	float noise = onoise(pos, turb, rough,1);
	return noise;}
float ofn(vector pos;int turb){	
	float noise = onoise(pos, turb, 0.5,1);	
	return noise;}
float ofn(vector pos){	
	float noise = onoise(pos, 3, 0.5,1);	
	return noise;}
	
vector ovn(vector pos;int turb;float rough;float atten){	
	vector noise = onoise(pos, turb, rough, atten);	
	return noise;}
vector ovn(vector pos;int turb;float rough){	
	vector noise = onoise(pos, turb, rough,1);	
	return noise;}
vector ovn(vector pos;int turb){	
	vector noise = onoise(pos, turb, 0.5,1);	
	return noise;}
vector ovn(vector pos){	
	vector noise = onoise(pos, 3, 0.5,1);	
	return noise;}

// ALLIGATOR NOISE
float afn(vector pos;int turb;float rough;float atten){	
	float noise = anoise(pos, turb, rough, atten);	
	return noise;}
float afn(vector pos;int turb;float rough){	
	float noise = anoise(pos, turb, rough,1);	
	return noise;}
float afn(vector pos;int turb){	
	float noise = anoise(pos, turb, 0.5,1);	
	return noise;}
float afn(vector pos){	
	float noise = anoise(pos, 3, 0.5,1);	
	return noise;}

vector avn(vector pos;int turb;float rough;float atten){	
	vector noise = anoise(pos, turb, rough, atten);	
	return noise;}
vector avn(vector pos;int turb;float rough){	
	vector noise = anoise(pos, turb, rough,1);	
	return noise;}
vector avn(vector pos;int turb){	
	vector noise = anoise(pos, turb, 0.5,1);	
	return noise;}
vector avn(vector pos){	
	vector noise = anoise(pos, 3, 0.5,1);	
	return noise;}

// SPARSE CONVULTION NOISE
float sfn(vector pos;int turb;float rough;float atten){	
	float noise = snoise(pos, turb, rough, atten);	
	return noise;}
float sfn(vector pos;int turb;float rough){	
	float noise = snoise(pos, turb, rough,1);	
	return noise;}
float sfn(vector pos;int turb){	
	float noise = snoise(pos, turb, 0.5,1);	
	return noise;}
float sfn(vector pos){	
	float noise = snoise(pos, 3, 0.5,1);	
	return noise;}

vector svn(vector pos;int turb;float rough;float atten){	
	vector noise = snoise(pos, turb, rough, atten);	
	return noise;}
vector svn(vector pos;int turb;float rough){	
	vector noise = snoise(pos, turb, rough,1);	
	return noise;}
vector svn(vector pos;int turb){	
	vector noise = snoise(pos, turb, 0.5,1);	
	return noise;}
vector svn(vector pos){	
	vector noise = snoise(pos, 3, 0.5,1);	
	return noise;}

	// VOP TURBULENT NOISES
// SIMPLEX NOISE	
float xfn(vector pos;int turb;float rough;float atten){	
	float noise = vop_simplexNoiseVF(pos, turb, 1, rough, atten);
	return noise;}
float xfn(vector pos;int turb;float rough){	
	float noise = vop_simplexNoiseVF(pos, turb,1, rough,1);
	return noise;}
float xfn(vector pos;int turb){	
	float noise = vop_simplexNoiseVF(pos, turb,1, 0.5,1);	
	return noise;}
float xfn(vector pos){	
	float noise = vop_simplexNoiseVF(pos, 3,1, 0.5,1);	
	return noise;}
	
vector xvn(vector pos;int turb;float rough;float atten){	
	vector noise = vop_simplexNoiseVF(pos, turb,1, rough, atten);	
	return noise;}
vector xvn(vector pos;int turb;float rough){	
	vector noise = vop_simplexNoiseVV(pos, turb,1, rough,1);	
	return noise;}
vector xvn(vector pos;int turb){	
	vector noise = vop_simplexNoiseVV(pos, turb,1, 0.5,1);	
	return noise;}
vector xvn(vector pos){	
	vector noise = vop_simplexNoiseVV(pos, 3,1, 0.5,1);	
	return noise;}
	
// PERLIN NOISE	
float pfn(vector pos;int turb;float rough;float atten){	
	float noise = vop_perlinNoiseVF(pos, turb, 1, rough, atten);
	return noise;}
float pfn(vector pos;int turb;float rough){	
	float noise = vop_perlinNoiseVF(pos, turb,1, rough,1);
	return noise;}
float pfn(vector pos;int turb){	
	float noise = vop_perlinNoiseVF(pos, turb,1, 0.5,1);	
	return noise;}
float pfn(vector pos){	
	float noise = vop_perlinNoiseVF(pos, 3,1, 0.5,1);	
	return noise;}
	
vector pvn(vector pos;int turb;float rough;float atten){	
	vector noise = vop_perlinNoiseVV(pos, turb,1, rough, atten);	
	return noise;}
vector pvn(vector pos;int turb;float rough){	
	vector noise = vop_perlinNoiseVV(pos, turb,1, rough,1);	
	return noise;}
vector pvn(vector pos;int turb){	
	vector noise = vop_perlinNoiseVV(pos, turb,1, 0.5,1);	
	return noise;}
vector pvn(vector pos){	
	vector noise = vop_perlinNoiseVV(pos, 3,1, 0.5,1);	
	return noise;}	
	
// CORRECTED PERLIN NOISE	
float cfn(vector pos;int turb;float rough;float atten){	
	float noise = vop_correctperlinNoiseVF(pos, turb, 1, rough, atten);
	return noise;}
float cfn(vector pos;int turb;float rough){	
	float noise = vop_correctperlinNoiseVF(pos, turb,1, rough,1);
	return noise;}
float cfn(vector pos;int turb){	
	float noise = vop_correctperlinNoiseVF(pos, turb,1, 0.5,1);	
	return noise;}
float cfn(vector pos){	
	float noise = vop_correctperlinNoiseVF(pos, 3,1, 0.5,1);	
	return noise;}
	
vector cvn(vector pos;int turb;float rough;float atten){	
	vector noise = vop_correctperlinNoiseVV(pos, turb,1, rough, atten);	
	return noise;}
vector cvn(vector pos;int turb;float rough){	
	vector noise = vop_correctperlinNoiseVV(pos, turb,1, rough,1);	
	return noise;}
vector cvn(vector pos;int turb){	
	vector noise = vop_correctperlinNoiseVV(pos, turb,1, 0.5,1);	
	return noise;}
vector cvn(vector pos){	
	vector noise = vop_correctperlinNoiseVV(pos, 3,1, 0.5,1);	
	return noise;}		
	
	
	// AA NOISES
//PERLIN
// 3D 
float apfn(vector pos;int turb;float rough){	
	float noise = vop_fbmNoiseFV(pos,rough,turb,"noise");	
	return noise;}
float apfn(vector pos;int turb){	
	float noise = vop_fbmNoiseFV(pos, 0.5,turb,"noise");	
	return noise;}
float apfn(vector pos){	
	float noise = vop_fbmNoiseFV(pos, 0.5,3,"noise");	
	return noise;}

vector apvn(vector pos;int turb;float rough){	
	vector noise = vop_fbmNoiseVV(pos,rough,turb,"noise");	
	return noise;}
vector apvn(vector pos;int turb){	
	vector noise = vop_fbmNoiseVV(pos,0.5, turb,"noise");	
	return noise;}
vector apvn(vector pos){	
	vector noise = vop_fbmNoiseVV(pos, 0.5,3,"noise");	
	return noise;}
//1D
float apfn(float pos;int turb;float rough){	
	float noise = vop_fbmNoiseFF(pos,rough,turb,"noise");	
	return noise;}
float apfn(float pos;int turb){	
	float noise = vop_fbmNoiseFF(pos, 0.5,turb,"noise");	
	return noise;}
float apfn(float pos){	
	float noise = vop_fbmNoiseFF(pos, 0.5,3,"noise");	
	return noise;}

vector apvn(float pos;int turb;float rough){	
	vector noise = vop_fbmNoiseVF(pos,rough,turb,"noise");	
	return noise;}
vector apvn(float pos;int turb){	
	vector noise = vop_fbmNoiseVF(pos,0.5, turb,"noise");	
	return noise;}
vector apvn(float pos){	
	vector noise = vop_fbmNoiseVF(pos, 0.5,3,"noise");	
	return noise;}
//4D
float apfn(vector4 pos;int turb;float rough){	
	float noise = vop_fbmNoiseFP(pos,rough,turb,"noise");	
	return noise;}
float apfn(vector4 pos;int turb){	
	float noise = vop_fbmNoiseFP(pos, 0.5,turb,"noise");	
	return noise;}
float apfn(vector4 pos){	
	float noise = vop_fbmNoiseFP(pos, 0.5,3,"noise");	
	return noise;}

vector apvn(vector4 pos;int turb;float rough){	
	vector noise = vop_fbmNoiseFP(pos,rough,turb,"noise");	
	return noise;}
vector apvn(vector4 pos;int turb){	
	vector noise = vop_fbmNoiseFP(pos,0.5, turb,"noise");	
	return noise;}
vector apvn(vector4 pos){	
	vector noise = vop_fbmNoiseFP(pos, 0.5,3,"noise");	
	return noise;}	


//SIMPLEX 
//3D
float asfn(vector pos;int turb;float rough){	
	float noise = vop_fbmNoiseFV(pos,rough,turb,"xnoise");	
	return noise;}
float asfn(vector pos;int turb){	
	float noise = vop_fbmNoiseFV(pos, 0.5,turb,"xnoise");	
	return noise;}
float asfn(vector pos){	
	float noise = vop_fbmNoiseFV(pos, 0.5,3,"xnoise");	
	return noise;}

vector asvn(vector pos;int turb;float rough){	
	vector noise = vop_fbmNoiseVV(pos,rough,turb,"xnoise");	
	return noise;}
vector asvn(vector pos;int turb){	
	vector noise = vop_fbmNoiseVV(pos,0.5, turb,"xnoise");	
	return noise;}
vector asvn(vector pos){	
	vector noise = vop_fbmNoiseVV(pos, 0.5,3,"xnoise");	
	return noise;}
//1D
float asfn(float pos;int turb;float rough){	
	float noise = vop_fbmNoiseFF(pos,rough,turb,"xnoise");	
	return noise;}
float asfn(float pos;int turb){	
	float noise = vop_fbmNoiseFF(pos, 0.5,turb,"xnoise");	
	return noise;}
float asfn(float pos){	
	float noise = vop_fbmNoiseFF(pos, 0.5,3,"xnoise");	
	return noise;}

vector asvn(float pos;int turb;float rough){	
	vector noise = vop_fbmNoiseVF(pos,rough,turb,"xnoise");	
	return noise;}
vector asvn(float pos;int turb){	
	vector noise = vop_fbmNoiseVF(pos,0.5, turb,"xnoise");	
	return noise;}
vector asvn(float pos){	
	vector noise = vop_fbmNoiseVF(pos, 0.5,3,"xnoise");	
	return noise;}
//4D
float asfn(vector4 pos;int turb;float rough){	
	float noise = vop_fbmNoiseFP(pos,rough,turb,"xnoise");	
	return noise;}
float asfn(vector4 pos;int turb){	
	float noise = vop_fbmNoiseFP(pos, 0.5,turb,"xnoise");	
	return noise;}
float asfn(vector4 pos){	
	float noise = vop_fbmNoiseFP(pos, 0.5,3,"xnoise");	
	return noise;}

vector asvn(vector4 pos;int turb;float rough){	
	vector noise = vop_fbmNoiseFP(pos,rough,turb,"xnoise");	
	return noise;}
vector asvn(vector4 pos;int turb){	
	vector noise = vop_fbmNoiseFP(pos,0.5, turb,"xnoise");	
	return noise;}
vector asvn(vector4 pos){	
	vector noise = vop_fbmNoiseFP(pos, 0.5,3,"xnoise");	
	return noise;}	
	
	
// CURL NOISE
vector curlNoiseVV(vector pos;int turb;float rough;float atten;string type){	
	vector noise =  vop_curlNoiseVV(pos,{1,1,1},{0,0,0},{0,0,0},type,"",turb,0,1,rough,atten,1,1,0.0001);
	return noise;}
vector curlNoiseVV(vector4 pos;int turb;float rough;float atten;string type){	
	vector noise =  vop_curlNoiseVP(pos,{1,1,1},{0,0,0},{0,0,0},type,"",turb,0,1,rough,atten,1,1,0.0001);
	return noise;}
	
// perlin	
vector cpn(vector pos;int turb;float rough;float atten){
	return curlNoiseVV(pos,turb,rough,atten,"pnoise");}
vector cpn(vector pos;int turb;float rough){
	return curlNoiseVV(pos,turb,rough,1,"pnoise");}
vector cpn(vector pos;int turb){
	return curlNoiseVV(pos,turb,0.5,1,"pnoise");}	
vector cpn(vector pos){
	return curlNoiseVV(pos,3,0.5,1,"pnoise");}	
	
vector cpn(vector4 pos;int turb;float rough;float atten){
	return curlNoiseVV(pos,turb,rough,atten,"pnoise");}
vector cpn(vector4 pos;int turb;float rough){
	return curlNoiseVV(pos,turb,rough,1,"pnoise");}
vector cpn(vector4 pos;int turb){
	return curlNoiseVV(pos,turb,0.5,1,"pnoise");}	
vector cpn(vector4 pos){
	return curlNoiseVV(pos,3,0.5,1,"pnoise");}		
	
// original perlin
vector con(vector pos;int turb;float rough;float atten){
	return curlNoiseVV(pos,turb,rough,atten,"onoise");}
vector con(vector pos;int turb;float rough){
	return curlNoiseVV(pos,turb,rough,1,"onoise");}
vector con(vector pos;int turb){
	return curlNoiseVV(pos,turb,0.5,1,"onoise");}	
vector con(vector pos){
	return curlNoiseVV(pos,3,0.5,1,"onoise");}	
	
vector con(vector4 pos;int turb;float rough;float atten){
	return curlNoiseVV(pos,turb,rough,atten,"onoise");}
vector con(vector4 pos;int turb;float rough){
	return curlNoiseVV(pos,turb,rough,1,"onoise");}
vector con(vector4 pos;int turb){
	return curlNoiseVV(pos,turb,0.5,1,"onoise");}	
vector con(vector4 pos){
	return curlNoiseVV(pos,3,0.5,1,"onoise");}

// sparse convultion noise
vector csn(vector pos;int turb;float rough;float atten){
	return curlNoiseVV(pos,turb,rough,atten,"snoise");}
vector csn(vector pos;int turb;float rough){
	return curlNoiseVV(pos,turb,rough,1,"snoise");}
vector csn(vector pos;int turb){
	return curlNoiseVV(pos,turb,0.5,1,"snoise");}	
vector csn(vector pos){
	return curlNoiseVV(pos,3,0.5,1,"snoise");}	
	
vector csn(vector4 pos;int turb;float rough;float atten){
	return curlNoiseVV(pos,turb,rough,atten,"snoise");}
vector csn(vector4 pos;int turb;float rough){
	return curlNoiseVV(pos,turb,rough,1,"snoise");}
vector csn(vector4 pos;int turb){
	return curlNoiseVV(pos,turb,0.5,1,"snoise");}	
vector csn(vector4 pos){
	return curlNoiseVV(pos,3,0.5,1,"snoise");}

// alligator 
vector can(vector pos;int turb;float rough;float atten){
	return curlNoiseVV(pos,turb,rough,atten,"anoise");}
vector can(vector pos;int turb;float rough){
	return curlNoiseVV(pos,turb,rough,1,"anoise");}
vector can(vector pos;int turb){
	return curlNoiseVV(pos,turb,0.5,1,"anoise");}	
vector can(vector pos){
	return curlNoiseVV(pos,3,0.5,1,"anoise");}	
	
vector can(vector4 pos;int turb;float rough;float atten){
	return curlNoiseVV(pos,turb,rough,atten,"anoise");}
vector can(vector4 pos;int turb;float rough){
	return curlNoiseVV(pos,turb,rough,1,"anoise");}
vector can(vector4 pos;int turb){
	return curlNoiseVV(pos,turb,0.5,1,"anoise");}	
vector can(vector4 pos){
	return curlNoiseVV(pos,3,0.5,1,"anoise");}	

//SIMPLEX NOISE
vector cxn(vector pos;int turb;float rough;float atten){
	return curlNoiseVV(pos,turb,rough,atten,"xnoise");}
vector cxn(vector pos;int turb;float rough){
	return curlNoiseVV(pos,turb,rough,1,"xnoise");}
vector cxn(vector pos;int turb){
	return curlNoiseVV(pos,turb,0.5,1,"xnoise");}	
vector cxn(vector pos){
	return curlNoiseVV(pos,3,0.5,1,"xnoise");}	
	
vector cxn(vector4 pos;int turb;float rough;float atten){
	return curlNoiseVV(pos,turb,rough,atten,"xnoise");}
vector cxn(vector4 pos;int turb;float rough){
	return curlNoiseVV(pos,turb,rough,1,"xnoise");}
vector cxn(vector4 pos;int turb){
	return curlNoiseVV(pos,turb,0.5,1,"xnoise");}	
vector cxn(vector4 pos){
	return curlNoiseVV(pos,3,0.5,1,"xnoise");}	

	
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
	
// SATURATE	
vector saturate(vector _v)
{
	vector v = _v;
	v.x = clamp(v.x,0,1);
	v.y = clamp(v.y,0,1);
	v.z = clamp(v.z,0,1);
	return v;
}	
vector2 saturate(vector2 _v)
{
	vector2 v = _v;
	v.x = clamp(v.x,0,1);
	v.y = clamp(v.y,0,1);
	return v;
}
float saturate(float v)
{
	return clamp(v,0,1);
}	





	
	

	
	
	
	
	
	
	








