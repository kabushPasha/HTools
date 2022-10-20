// NEW GXNoise Noises
float3 Noise3(float3 p,float amp,float4 freq,float rough,int oct,float4 offset)
{
    // Usage:
    // float3 n0 = Noise3(vp,n0_amp,n0_freq,n0_rough,n0_oct,n0_off);
    float4 pos = ((float4)(p,0) + offset) * freq;
    float3 noise = 0;    
    for (int i = 0; i < oct; i++, pos *= 2.0f, amp *= rough) 
        noise += amp * VEXcurlgxnoise_4(pos); 
    return noise; 
}

float Noise(float3 p,float amp,float4 freq,float rough,int oct,float4 offset)
{
    // Usage:
    // float n0 = Noise(vp,n0_amp,n0_freq,n0_rough,n0_oct,n0_off);
    float4 pos = ((float4)(p,0) + offset) * freq;
    float noise = 0;    
    for (int i = 0; i < oct; i++, pos *= 2.0f, amp *= rough) 
        noise += amp * VEXgxnoise_4_1(pos); 
    return noise; 
}
/*
// OLD Xnoise Noises
float3 LZ_CurlNoise4(float3 p,float amp,float4 freq,float rough,int oct,float4 offset,global const void *theXNoise)
{
    // Usage:
    // float3 n0 = LZ_SimpleNoise(vp,n0_amp,n0_freq,n0_rough,n0_oct,n0_off,theXNoise);
    // global const void *theXNoise, 
    float4 pos = ((float4)(p,0) + offset) * freq;
    float3 noise = 0;    
    for (int i = 0; i < oct; i++, pos *= 2.0f, amp *= rough) 
        noise += amp * curlxnoise4(theXNoise, pos); 
    return noise; 
}

float LZ_XNoise4(float3 p,float amp,float4 freq,float rough,int oct,float4 offset,global const void *theXNoise)
{
    // Usage:
    // float3 n0 = LZ_SimpleNoise(vp,n0_amp,n0_freq,n0_rough,n0_oct,n0_off,theXNoise);
    // global const void *theXNoise, 
    float4 pos = ((float4)(p,0) + offset) * freq;
    float noise = 0;    
    for (int i = 0; i < oct; i++, pos *= 2.0f, amp *= rough) 
        noise += amp * xnoise4(theXNoise, pos); 
    return noise; 
}
*/
// LZ Voronoi Function
float LZ_Voronoi_all(float3 vp,int global_seed,int shape)
{
    float3 i_vp = floor(vp);
    float3 f_vp = vp - i_vp;
    
    float f1 = 100;
    float f2 = 100;
    
    int seed = 0;    
    for (int x=-1; x<=1; x++) {
        for (int y=-1; y<=1; y++) {
            for (int z=-1; z<=1; z++) {
                float3 neighbour = (float3)(x,y,z);                
                
                // cacl the point position
                float3 pos = i_vp + neighbour;
                int f_hash = VEXrandom_fhash_3(pos.x,pos.y,pos.z) + global_seed;
                int temp_hash = f_hash;
                float rx = SYSfastRandom(&f_hash);   
                float ry = SYSfastRandom(&f_hash);  
                float rz = SYSfastRandom(&f_hash);        
                float3 point = (float3) (rx,ry,rz);
                
                float3 diff = neighbour + point - f_vp;
                float d = length(diff);                
                //f1 = min(f1,dist);                
                
                if( d < f1) {
                    f2 = f1;                    
                    f1 = d;   
                    seed = f_hash;
                }
                else if( d < f2 )
                { f2 = d; }
            }
        }
    }
     
    float surf;
    if (shape == 0) {    surf = f1;    }
    else if (shape==1) { surf = (f2-f1);}
    else {    surf = SYSfastRandom(&seed);}
  
    return surf;
}