struct gear
{
	int pt;
	int geo = 0;
	float tooth_length;
	vector P;
	
	int n_teeth;	
	matrix3 t;
	float motor = 1;
	
	// Extractable
	float pscale;
	
	void init(int _pt)
	{
		this.pt = _pt;
		this.P = point( this.geo, "P", this.pt );		
	}
	
	void init(int _pt; float _tooth_length)
	{
		this.pt = _pt;
		this.P = point( this.geo, "P", this.pt );
		this.tooth_length = _tooth_length;		
	}
	
	vector getN()	{
		return normalize(this.t*{0,1,0});
	}	
	vector getZ()	{
		return normalize(this.t*{0,0,1});
	}
	vector getX()	{
		return normalize(this.t*{1,0,0});
	}
	float fixScale()
	{			
		float old_scale = this.pscale;
		this.n_teeth = (int)rint(PI*this.pscale/this.tooth_length);
		this.pscale = this.tooth_length*this.n_teeth/(PI);	
		float scale_offset = this.pscale - old_scale;
		return scale_offset;
	}
		
	float t2scale ( int _n_teeth)	{
		return this.tooth_length*_n_teeth/(PI);
	}	
	int scale2t ( float _pscale)	{
		return (int)rint(PI*_pscale/this._tooth_length);
	}	
	float t2scale ( int _n_teeth; float _tooth_length)	
	{
		return _tooth_length*_n_teeth/(PI);
	}	
	int scale2t ( float _pscale; float _tooth_length)	
	{
		return (int)rint(PI*_pscale/_tooth_length);
	}
	
		
	void fromTeeth(int _n_teeth)
	{
		this.n_teeth = _n_teeth;
		this.pscale = this.tooth_length*this.n_teeth/(PI);	
		this.t = maketransform({0,0,1},{0,1,0}) * this.pscale;		
	}
		
	void fromPscale(float _pscale)
	{
		this.pscale = _pscale;
		// Fix the real scale based on the tooth_length
		this->fixScale();		
		this.t = maketransform({0,0,1},{0,1,0}) * this.pscale;
	}	
	
	float getRate(gear g) 	{
		return g.pscale/this.pscale;
	}
	
	void setMotor(gear g)	{		
		this.motor = -g.motor * this->getRate(g);
	}
			
	void fixRotation3d(gear g)
	{
		matrix3 t0 = g.t;
		matrix3 t1 = this.t;

		float scalefactor = this->getRate(g);

		vector n0 = g->getN();
		vector n1 = this->getN();

		vector dir1 = -this->getZ();		
		vector dir0 = normalize( this.P + dir1*this.pscale - g.P);

		matrix3 r0 = maketransform( dir0, n0 );
		matrix3 r1 = maketransform( dir1, n1 );

		vector ang_ax0 = qconvert(quaternion(invert(t0) * r0));
		float sign0 = sign(dot(ang_ax0,n0));

		vector ang_ax1 = qconvert(quaternion( invert(t1) * r1 ));
		float sign1 = sign(dot(ang_ax1,n1));

		// Fix teeth
		int nt0 = g.n_teeth;
		int nt1 = this.n_teeth;
		float axes_align = dot(n0,n1) >= 0;
		vector t_angax = n1;		
		t_angax *= ( 0.5 * PI * ((nt1 - nt0)%4 +  ((nt0)%2)*2 ) )/ nt1;
				
		// calc combined pre rotation
		float pre_rotate = 0;
		pre_rotate += sign0 * length(ang_ax0) * scalefactor;
		pre_rotate += sign1 * length(ang_ax1);
		pre_rotate += -length(t_angax);
		rotate(t1,pre_rotate,n1);

		// Set Attribs
		this.t = t1;
	}
			
	void fromGear3d(gear g)
	{
		// Copy Tooth length since gears hould have the same
		this.tooth_length = g.tooth_length;
		
		vector p1 = this.P;
		vector p0 = g.P;		
		
		float pscale0 = g.pscale;    
		vector dir = p1 - p0;
		vector n0 = g->getN();
		// Find all the parts
		vector dir_perpendicular = n0 * dot(n0,dir);
		vector dir_parralel = dir - dir_perpendicular;
		vector p0_cross = normalize(dir_parralel) * pscale0;		
		vector cross_p1 = dir  - p0_cross;
		vector z = cross_p1;
		float pscale = length(z);
		
		// Fix the real scale based on the tooth_length 
		float scale_offset = this->fixScale();
		
		// Fix position bsed on new scale
		z = normalize(z);
		this.P += z * scale_offset;
		//vector y = normalize(cross(z,cross(n0,z)));
		vector y = normalize(cross(cross( normalize(p0_cross) , n0 ),z));
		this.t = maketransform(z,y) * this.pscale;
		
		// FIX PreRotation
		this->fixRotation3d(g);
		
		// Calc Motor
		this->setMotor(g);	
	}	
	
	void fromGear(gear g)
	{
		// Copy Tooth length since gears hould have the same
		this.tooth_length = g.tooth_length;
		
		vector p1 = this.P;
		vector p0 = g.P;	
		p0.y = p1.y;
		
		float pscale0 = g.pscale;    
		float pscale =  length(p0 - p1) - pscale0;
		
		// Fix the real scale based on the tooth_length 
		float scale_offset = this->fixScale();
		
		// Fix position bsed on new scale
		this.P += normalize(p1-p0) * scale_offset;		
		this.t = maketransform({0,0,1},{0,1,0}) * this.pscale;
		
		// FIX PreRotation
		this->fixRotation3d(g);
		
		// Calc Motor
		this->setMotor(g);	
	}	
	
	void fromPoint(int _geo;int _pt)
	{
		this.pt = _pt;
		this.geo = _geo;
		
		this.tooth_length 	= point(_geo,"tooth_length",_pt);
		this.P 				= point(_geo,"P",_pt);		
		this.n_teeth 		= point(_geo,"n_cuts",_pt);		
		this.t 				= point(_geo,"transform",_pt);		
		this.pscale 		= cracktransform(0,0,2,{0,0,0},this.t).x;
		this.motor 		    = point(_geo,"motor",_pt);		
		
	}
		
	void setGear()
	{
		setpointattrib(0,"transform",this.pt,this.t);
		setpointattrib(0,"n_cuts",this.pt,this.n_teeth);
		setpointattrib(0,"tooth_length",this.pt,this.tooth_length);
		setpointattrib(0,"P",this.pt,this.P);
		setpointattrib(0,"motor",this.pt,this.motor);
		
		setpointattrib(0,"name",this.pt,"gear_" + itoa(this.n_teeth));		
		//setpointattrib(0,"N",this.pt,this->getN());
	}
	
	void rotate( float ammount)
	{
		rotate(this.t, ammount , normalize(this.t*{0,1,0}));		
		setpointattrib(0,"transform",this.pt,this.t);
	}
	
	// Creation shortcuts
	void fromPoint(int _pt; int _geo0;int _pt0)
	{
		gear g0;
		g0->fromPoint(_geo0,_pt0);		
		this->init(_pt);
		this->fromGear(g0);
		this->setGear();		
	}
	
	void fromPscale(int _pt;float _tooth_length; float _pscale)
	{
		this->init(0,_tooth_length);
		this->fromPscale(_pscale);
		this->setGear();			
	}
	
	void fromGear3d(int _pt;gear g)
	{
		this->init(_pt);
		this->fromGear3d(g);
		this->setGear();		
	}
	
	void fromGear(int _pt;gear g)
	{
		this->init(_pt);
		this->fromGear(g);
		this->setGear();		
	}
	
	void addFromGear(vector pos;gear g0)
	{
		int pt = addpoint(0,pos);
		this->init(pt);
		this.P  = pos;
		this->fromGear(g0);
		this->setGear();	
	}
	
	void addFromGear3d(vector pos;gear g0)
	{
		int pt = addpoint(0,pos);
		this->init(pt);
		this.P  = pos;
		this->fromGear3d(g0);
		this->setGear();	
	}		
	
	void addFromGear(float _angle;int _n_teeth;gear g0)
	{
		float pscale = this->t2scale(_n_teeth, g0.tooth_length);
		vector dir = {0,0,1} * (pscale + g0.pscale);
		dir = qrotate(quaternion(_angle * 2*PI,{0,1,0}),dir);
		vector pos = g0.P + dir;
		
		this->addFromGear(pos,g0);
	}
	
	void addFromGear(float _angle;float fi;int _n_teeth;gear g0)
	{	
		float pscale = this->t2scale(_n_teeth, g0.tooth_length);
		vector dir = g0->getZ() * (g0.pscale);
		dir += pscale * qrotate(quaternion(fi * 2*PI,g0->getX()),g0->getZ());
		dir = qrotate(quaternion(_angle * 2*PI,g0->getN()),dir);
		vector pos = g0.P + dir;
		
		this->addFromGear3d(pos,g0);
	}
	
	void addFromPoint(vector pos;int _geo0;int _pt0)
	{
		int pt = addpoint(0,pos);		
		gear g0;		
		g0->fromPoint(_geo0,_pt0);
		
		this->addFromGear(pos,g0);
	}
	
	// Add Point From teeth and direction in 2d
	void addFromPoint(float _angle;int _n_teeth;int _geo0;int _pt0)
	{		
		gear g0;
		g0->fromPoint(_geo0,_pt0);	
		this.tooth_length = g0.tooth_length;		
		float pscale = this->t2scale(_n_teeth);
		vector dir = {0,0,1} * (pscale + g0.pscale);
		dir = qrotate(quaternion(_angle * 2*PI,{0,1,0}),dir);
		vector pos = g0.P + dir;
		
		this->addFromGear(pos,g0);
	}
	
	void addFromPscale(vector pos;float _tooth_length; float _pscale)
	{
		int pt = addpoint(0,pos);
		this->init(0,_tooth_length);
		this.P  = pos;
		this->fromPscale(_pscale);
		this->setGear();	
	}
	
	void addFromTeeth(vector pos;float _tooth_length; int _n_teeth)
	{
		float pscale = this->t2scale(_n_teeth,_tooth_length);		
		this->addFromPscale(pos,_tooth_length,pscale);
	}
	
}

// Shortcut functions
gear fromPscale(int _pt;float _tooth_length; float _pscale){
	gear g1;
	g1->fromPscale(_pt,_tooth_length,_pscale);
	return g1;
}

gear fromGear(int _pt;gear g){
	gear g1;
	g1->fromGear(_pt,g);
	return g1;		
}

gear fromGear3d(int _pt;gear g){
	gear g1;
	g1->fromGear3d(_pt,g);
	return g1;		
}

gear addFromTeeth(vector pos; float _tooth_length;int _n_teeth){
	gear g1;
	g1->addFromTeeth(pos,_tooth_length,_n_teeth);
	return g1;
}

gear addFromPscale(vector pos; float _tooth_length;float  _pscale){
	gear g1;
	g1->addFromPscale(pos,_tooth_length,_pscale);
	return g1;
}

gear addFromGear3d(vector pos;gear g){
	gear g1;
	g1->addFromGear3d(pos,g);	
	return g1;	
}

gear addFromGear(vector pos;gear g){
	gear g1;
	g1->addFromGear(pos,g);	
	return g1;	
}

gear addFromGear(float angle;int _n_teeth;gear g){
	gear g1;
	g1->addFromGear(angle,_n_teeth,g);	
	return g1;	
}

gear addFromGear(float angle;float fi;int _n_teeth;gear g){
	gear g1;
	g1->addFromGear(angle,fi,_n_teeth,g);	
	return g1;	
}

gear addFromPoint(vector pos;int _geo;int _pt){
	gear g1;
	g1->addFromPoint(pos,_geo,_pt);
	return g1;	
}

gear addFromPoint(float angle;int _n_teeth;int _geo;int _pt){
	gear g1;
	g1->addFromPoint(angle,_n_teeth,_geo,_pt);
	return g1;	
}
