vector clamp_vector(vector v) 
{ 
	return normalize(v)*clamp(length(v),0,1);
}

struct Steer
{
	vector P = 0;
	vector v = 0;
	int nforces = 0;
	vector steerForces[];
	float steerWeights[];
	
	void set(vector _P;vector _v)
	{
		this.P = _P;
		this.v = _v;		
	}
	
	void addForce(vector force;float weight)
	{
		push(this.steerForces,force);
		push(this.steerWeights,weight);		
		nforces++;
	}
	
	void addClampedForce(vector force;float weight)
	{
		this->addForce(clamp_vector(force),weight);
	}	
	
	vector simpleMind()
	{
		vector finalSteer = {0,0,0};
		for(int i=0;i<nforces;i++)
		{
			vector steerForce = steerForces[i];
			float steerWeight = steerWeights[i];
			finalSteer += steerWeight*steerForce;
		}
		return finalSteer;			
	}
	
	
	void addArriveSteer(vector target;float maxRadius;float forceScale;float weight)
	{
		vector dir = target - P;
		vector desiredVel = normalize(dir)*fit(length(dir),0,maxRadius,0,length(dir));
		vector accel = desiredVel - v;
		accel *= forceScale;
		this->addClampedForce(accel,weight);
	}	
	
	void addSeparationSteer(float radius;float scale;float weight)
	{
		int handle =  pcopen(0,'P',P,radius,1000);
		vector separation = {0,0,0}; 
		int niegbours = 0;
		if(pciterate(handle))
			while (pciterate(handle)) 
			{
				float d;vector nP;
				pcimport(handle,'point.distance',d);
				pcimport(handle,"P",nP);  
				separation += normalize(( P - nP))*fit(d,0,radius,1,0);  
				niegbours++;                                       
			}
		separation /= niegbours;		
		separation *= scale;
		this->addClampedForce(separation,weight);
	}	
	
	void addCohesionForce(float radius;float scale;float weigth)
	{
		int handle =  pcopen(0,'P',P,radius,1000);
		vector avg_position = 0;
		int niegbours = 0;
		if(pciterate(handle))
			while (pciterate(handle)) 
			{
				vector nP;
				pcimport(handle,"P",nP);     
				avg_position += nP;                                  
				niegbours++;                                      
			} 
		avg_position /= niegbours;
		vector force = (avg_position - P)*scale;
		if(niegbours>0)
			this->addClampedForce(force,weigth);
	}	
	
	void addAlingForce(float radius;float scale;float weigth)
	{
		int handle =  pcopen(0,'P',P,radius,1000);
		vector avg_vel = 0;
		int niegbours = 0;
		if(pciterate(handle))
			while (pciterate(handle)) 
			{
				vector nv;
				pcimport(handle,"v",nv);     
				avg_vel += nv;                                  
				niegbours++;                                      
			} 
		avg_vel /= niegbours;
		vector force = (avg_vel - v)*scale;
		this->addClampedForce(force,weigth);
	}	
	
	
}

