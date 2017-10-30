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

*/

	// SMIPLE TURBULENT NOISES
// ORIGINAL PERLIN NOISE
float opfn(vector pos;int turb;float rough;float atten){	
	float noise = onoise(pos, turb, rough, atten);	
	return noise;}
float opfn(vector pos;int turb;float rough){	
	float noise = onoise(pos, turb, rough,1);
	return noise;}
float opfn(vector pos;int turb){	
	float noise = onoise(pos, turb, 0.5,1);	
	return noise;}
float opfn(vector pos){	
	float noise = onoise(pos, 3, 0.5,1);	
	return noise;}
float opfn1(vector pos){	
	float noise = onoise(pos, 1, 0.5,1);	
	return noise;}
	
vector opvn(vector pos;int turb;float rough;float atten){	
	vector noise = onoise(pos, turb, rough, atten);	
	return noise;}
vector opvn(vector pos;int turb;float rough){	
	vector noise = onoise(pos, turb, rough,1);	
	return noise;}
vector opvn(vector pos;int turb){	
	vector noise = onoise(pos, turb, 0.5,1);	
	return noise;}
vector opvn(vector pos){	
	vector noise = onoise(pos, 3, 0.5,1);	
	return noise;}
vector opvn1(vector pos){	
	vector noise = onoise(pos, 1, 0.5,1);	
	return noise;}
	
// ALLIGATOR NOISE
float alfn(vector pos;int turb;float rough;float atten){	
	float noise = anoise(pos, turb, rough, atten);	
	return noise;}
float alfn(vector pos;int turb;float rough){	
	float noise = anoise(pos, turb, rough,1);	
	return noise;}
float alfn(vector pos;int turb){	
	float noise = anoise(pos, turb, 0.5,1);	
	return noise;}
float alfn(vector pos){	
	float noise = anoise(pos, 3, 0.5,1);	
	return noise;}

vector alfn(vector pos;int turb;float rough;float atten){	
	vector noise = anoise(pos, turb, rough, atten);	
	return noise;}
vector alfn(vector pos;int turb;float rough){	
	vector noise = anoise(pos, turb, rough,1);	
	return noise;}
vector alfn(vector pos;int turb){	
	vector noise = anoise(pos, turb, 0.5,1);	
	return noise;}
vector alfn(vector pos){	
	vector noise = anoise(pos, 3, 0.5,1);	
	return noise;}

// SPARSE CONVULTION NOISE
float scfn(vector pos;int turb;float rough;float atten){	
	float noise = snoise(pos, turb, rough, atten);	
	return noise;}
float scfn(vector pos;int turb;float rough){	
	float noise = snoise(pos, turb, rough,1);	
	return noise;}
float scfn(vector pos;int turb){	
	float noise = snoise(pos, turb, 0.5,1);	
	return noise;}
float scfn(vector pos){	
	float noise = snoise(pos, 3, 0.5,1);	
	return noise;}

vector scvn(vector pos;int turb;float rough;float atten){	
	vector noise = snoise(pos, turb, rough, atten);	
	return noise;}
vector scvn(vector pos;int turb;float rough){	
	vector noise = snoise(pos, turb, rough,1);	
	return noise;}
vector scvn(vector pos;int turb){	
	vector noise = snoise(pos, turb, 0.5,1);	
	return noise;}
vector scvn(vector pos){	
	vector noise = snoise(pos, 3, 0.5,1);	
	return noise;}

	// VOP TURBULENT NOISES
// SIMPLEX NOISE	
float sxfn(vector pos;int turb;float rough;float atten){	
	float noise = vop_simplexNoiseVF(pos, turb, 1, rough, atten);
	return noise;}
float sxfn(vector pos;int turb;float rough){	
	float noise = vop_simplexNoiseVF(pos, turb,1, rough,1);
	return noise;}
float sxfn(vector pos;int turb){	
	float noise = vop_simplexNoiseVF(pos, turb,1, 0.5,1);	
	return noise;}
float sxfn(vector pos){	
	float noise = vop_simplexNoiseVF(pos, 3,1, 0.5,1);	
	return noise;}
	
vector sxvn(vector pos;int turb;float rough;float atten){	
	vector noise = vop_simplexNoiseVF(pos, turb,1, rough, atten);	
	return noise;}
vector sxvn(vector pos;int turb;float rough){	
	vector noise = vop_simplexNoiseVV(pos, turb,1, rough,1);	
	return noise;}
vector sxvn(vector pos;int turb){	
	vector noise = vop_simplexNoiseVV(pos, turb,1, 0.5,1);	
	return noise;}
vector sxvn(vector pos){	
	vector noise = vop_simplexNoiseVV(pos, 3,1, 0.5,1);	
	return noise;}
	
// PERLIN NOISE	
float pnfn(vector pos;int turb;float rough;float atten){	
	float noise = vop_perlinNoiseVF(pos, turb, 1, rough, atten);
	return noise;}
float pnfn(vector pos;int turb;float rough){	
	float noise = vop_perlinNoiseVF(pos, turb,1, rough,1);
	return noise;}
float pnfn(vector pos;int turb){	
	float noise = vop_perlinNoiseVF(pos, turb,1, 0.5,1);	
	return noise;}
float pnfn(vector pos){	
	float noise = vop_perlinNoiseVF(pos, 3,1, 0.5,1);	
	return noise;}
	
vector pnvn(vector pos;int turb;float rough;float atten){	
	vector noise = vop_perlinNoiseVV(pos, turb,1, rough, atten);	
	return noise;}
vector pnvn(vector pos;int turb;float rough){	
	vector noise = vop_perlinNoiseVV(pos, turb,1, rough,1);	
	return noise;}
vector pnvn(vector pos;int turb){	
	vector noise = vop_perlinNoiseVV(pos, turb,1, 0.5,1);	
	return noise;}
vector pnvn(vector pos){	
	vector noise = vop_perlinNoiseVV(pos, 3,1, 0.5,1);	
	return noise;}	
	
// CORRECTED PERLIN NOISE	
float cpfn(vector pos;int turb;float rough;float atten){	
	float noise = vop_correctperlinNoiseVF(pos, turb, 1, rough, atten);
	return noise;}
float cpfn(vector pos;int turb;float rough){	
	float noise = vop_correctperlinNoiseVF(pos, turb,1, rough,1);
	return noise;}
float cpfn(vector pos;int turb){	
	float noise = vop_correctperlinNoiseVF(pos, turb,1, 0.5,1);	
	return noise;}
float cpfn(vector pos){	
	float noise = vop_correctperlinNoiseVF(pos, 3,1, 0.5,1);	
	return noise;}
	
vector cpvn(vector pos;int turb;float rough;float atten){	
	vector noise = vop_correctperlinNoiseVV(pos, turb,1, rough, atten);	
	return noise;}
vector cpvn(vector pos;int turb;float rough){	
	vector noise = vop_correctperlinNoiseVV(pos, turb,1, rough,1);	
	return noise;}
vector cpvn(vector pos;int turb){	
	vector noise = vop_correctperlinNoiseVV(pos, turb,1, 0.5,1);	
	return noise;}
vector cpvn(vector pos){	
	vector noise = vop_correctperlinNoiseVV(pos, 3,1, 0.5,1);	
	return noise;}		
	
	
	// AA NOISES
//PERLIN
// 3D 
float aapfn(vector pos;int turb;float rough){	
	float noise = vop_fbmNoiseFV(pos,rough,turb,"noise");	
	return noise;}
float aapfn(vector pos;int turb){	
	float noise = vop_fbmNoiseFV(pos, 0.5,turb,"noise");	
	return noise;}
float aapfn(vector pos){	
	float noise = vop_fbmNoiseFV(pos, 0.5,3,"noise");	
	return noise;}

vector aapvn(vector pos;int turb;float rough){	
	vector noise = vop_fbmNoiseVV(pos,rough,turb,"noise");	
	return noise;}
vector aapvn(vector pos;int turb){	
	vector noise = vop_fbmNoiseVV(pos,0.5, turb,"noise");	
	return noise;}
vector aapvn(vector pos){	
	vector noise = vop_fbmNoiseVV(pos, 0.5,3,"noise");	
	return noise;}
//1D
float aapfn(float pos;int turb;float rough){	
	float noise = vop_fbmNoiseFF(pos,rough,turb,"noise");	
	return noise;}
float aapfn(float pos;int turb){	
	float noise = vop_fbmNoiseFF(pos, 0.5,turb,"noise");	
	return noise;}
float aapfn(float pos){	
	float noise = vop_fbmNoiseFF(pos, 0.5,3,"noise");	
	return noise;}

vector aapvn(float pos;int turb;float rough){	
	vector noise = vop_fbmNoiseVF(pos,rough,turb,"noise");	
	return noise;}
vector aapvn(float pos;int turb){	
	vector noise = vop_fbmNoiseVF(pos,0.5, turb,"noise");	
	return noise;}
vector aapvn(float pos){	
	vector noise = vop_fbmNoiseVF(pos, 0.5,3,"noise");	
	return noise;}
//4D
float aapfn(vector4 pos;int turb;float rough){	
	float noise = vop_fbmNoiseFP(pos,rough,turb,"noise");	
	return noise;}
float aapfn(vector4 pos;int turb){	
	float noise = vop_fbmNoiseFP(pos, 0.5,turb,"noise");	
	return noise;}
float aapfn(vector4 pos){	
	float noise = vop_fbmNoiseFP(pos, 0.5,3,"noise");	
	return noise;}

vector aapvn(vector4 pos;int turb;float rough){	
	vector noise = vop_fbmNoiseFP(pos,rough,turb,"noise");	
	return noise;}
vector aapvn(vector4 pos;int turb){	
	vector noise = vop_fbmNoiseFP(pos,0.5, turb,"noise");	
	return noise;}
vector aapvn(vector4 pos){	
	vector noise = vop_fbmNoiseFP(pos, 0.5,3,"noise");	
	return noise;}	


//SIMPLEX 
//3D
float aasfn(vector pos;int turb;float rough){	
	float noise = vop_fbmNoiseFV(pos,rough,turb,"xnoise");	
	return noise;}
float aasfn(vector pos;int turb){	
	float noise = vop_fbmNoiseFV(pos, 0.5,turb,"xnoise");	
	return noise;}
float aasfn(vector pos){	
	float noise = vop_fbmNoiseFV(pos, 0.5,3,"xnoise");	
	return noise;}

vector aasvn(vector pos;int turb;float rough){	
	vector noise = vop_fbmNoiseVV(pos,rough,turb,"xnoise");	
	return noise;}
vector aasvn(vector pos;int turb){	
	vector noise = vop_fbmNoiseVV(pos,0.5, turb,"xnoise");	
	return noise;}
vector aasvn(vector pos){	
	vector noise = vop_fbmNoiseVV(pos, 0.5,3,"xnoise");	
	return noise;}
//1D
float aasfn(float pos;int turb;float rough){	
	float noise = vop_fbmNoiseFF(pos,rough,turb,"xnoise");	
	return noise;}
float aasfn(float pos;int turb){	
	float noise = vop_fbmNoiseFF(pos, 0.5,turb,"xnoise");	
	return noise;}
float aasfn(float pos){	
	float noise = vop_fbmNoiseFF(pos, 0.5,3,"xnoise");	
	return noise;}

vector aasvn(float pos;int turb;float rough){	
	vector noise = vop_fbmNoiseVF(pos,rough,turb,"xnoise");	
	return noise;}
vector aasvn(float pos;int turb){	
	vector noise = vop_fbmNoiseVF(pos,0.5, turb,"xnoise");	
	return noise;}
vector aasvn(float pos){	
	vector noise = vop_fbmNoiseVF(pos, 0.5,3,"xnoise");	
	return noise;}
//4D
float aasfn(vector4 pos;int turb;float rough){	
	float noise = vop_fbmNoiseFP(pos,rough,turb,"xnoise");	
	return noise;}
float aasfn(vector4 pos;int turb){	
	float noise = vop_fbmNoiseFP(pos, 0.5,turb,"xnoise");	
	return noise;}
float aasfn(vector4 pos){	
	float noise = vop_fbmNoiseFP(pos, 0.5,3,"xnoise");	
	return noise;}

vector aasvn(vector4 pos;int turb;float rough){	
	vector noise = vop_fbmNoiseFP(pos,rough,turb,"xnoise");	
	return noise;}
vector aasvn(vector4 pos;int turb){	
	vector noise = vop_fbmNoiseFP(pos,0.5, turb,"xnoise");	
	return noise;}
vector aasvn(vector4 pos){	
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

	
	
	
	
	
	
	
	






	
	

	
	
	
	
	
	
	








