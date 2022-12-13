struct gear
{
	int pt;
	int geo = 0;
	float tooth_length;
	vector P;
	
	int n_teeth;	
	matrix3 t;
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
	
	vector getN()
	{
		return normalize(this.t*{0,1,0});
	}	
	
	float fixScale()
	{			
		float old_scale = this.pscale;
		this.n_teeth = (int)rint(PI*this.pscale/this.tooth_length);
		this.pscale = this.tooth_length*this.n_teeth/(PI);	
		float scale_offset = this.pscale - old_scale;
		return scale_offset;
	}
		
	void fromPscale(float _pscale)
	{
		this.pscale = _pscale;
		// Fix the real scale based on the tooth_length
		this->fixScale();		
		this.t = maketransform({0,0,1},{0,1,0}) * this.pscale;
	}	
	
	vector toGearDir(gear g)
	{
		vector p1 = g.P;
		vector p0 = this.P;
		vector dir = p1 - p0;		
		vector n0 = this->getN();
		return normalize(dir  - n0*dot(n0,dir));
	}
	
	void fixRotation(gear g)
	{
		matrix3 t0 = g.t;
		matrix3 t1 = this.t;

		vector dir = g.P - this.P;
		dir.y = 0;
		matrix3 r0 = maketransform( normalize(dir), {0,1,0});
		matrix3 r1 = maketransform( -normalize(dir), {0,1,0});

		// Get scale factor
		float s0 = g.pscale;
		float s1 = this.pscale;
		float scalefactor = s0/s1;

		vector rotator = qconvert(quaternion(r0*invert(t0)));
		rotator *=  scalefactor;
		matrix3 r0i = qconvert(quaternion(rotator));
		matrix3 r = r1*r0i;

		// Fix teeth
		int nt0 = g.n_teeth;
		int nt1 = this.n_teeth;
		vector my_ax = normalize(qconvert(quaternion(t1* {0,1,0})));
		my_ax *= ( 0.5 * PI * ((nt1 - nt0)%4 +  ((nt0)%2)*2 ) )/ nt1;
		matrix3 fix_rot = qconvert(quaternion( my_ax  ));
		r*= fix_rot;

		this.t = t1*r;		
	}
	
	void fixRotation3d(gear g)
	{
		matrix3 t0 = g.t;
		matrix3 t1 = this.t;

		float scalefactor = g.pscale/this.pscale;

		vector n0 = g->getN();
		vector n1 = this->getN();

		vector dir0 = g->toGearDir(this);
		vector dir1 = this->toGearDir(g);

		matrix3 r0 = maketransform( dir0, n0 );
		matrix3 r1 = maketransform( dir1, n1 );

		vector ang_ax0 = qconvert(quaternion(r0 * invert(t0)));
		float ang0 = -length(ang_ax0);
		float sign0 = sign(dot(ang_ax0,n0));

		vector ang_ax1 = qconvert(quaternion(r1 * invert(t1)));
		float ang1 = -length(ang_ax1);
		float sign1 = sign(dot(ang_ax1,n1));

		//rotate(t0,length(ang_ax0)*sign0,n0);
		setpointattrib(0,"angax",this.pt, length(ang_ax0) );
		rotate(t1,sign0 * length(ang_ax0) * scalefactor,n1);
		rotate(t1,sign1 * length(ang_ax1),n1);

		// Fix teeth
		int nt0 = g.n_teeth;
		int nt1 = this.n_teeth;
		vector t_angax = n1;
		t_angax *= ( 0.5 * PI * ((nt1 - nt0)%4 +  ((nt0)%2)*2 ) )/ nt1;
		matrix3 fix_rot = qconvert(quaternion( -t_angax  ));
		t1*= fix_rot;

		// post rotate just to check
		//rotate(t0,chf("ang") * PI*2,n0);
		//rotate(t1,-chf("ang") * PI*2 * scalefactor ,n1);

		// Set Attribs
		this.t = t1;
		
		//setpointattrib(0,"transform",0,t0);
		//setpointattrib(0,"transform",1,t1);
	}
			
	void fromGear3d(gear g)
	{
		// Copy Tooth length since gears hould have the same
		this.tooth_length = g.tooth_length;
		
		vector p1 = this.P;
		vector p0 = g.P;		
		
		float pscale0 = g.pscale;    
		// 2D
		//float pscale =  length(p0 - p1) - pscale0;
		// 3D
		vector dir = p1 - p0;
		vector n0 = g->getN();
		vector z = dir - normalize(dir  - n0*dot(n0,dir)) * pscale0;
		float pscale = length(z);
		
		// Fix the real scale based on the tooth_length 
		float scale_offset = this->fixScale();
		
		// Fix position bsed on new scale
		// 2D 
		//this.P += normalize(p1-p0) * scale_offset;		
		//this.t = maketransform({0,0,1},{0,1,0}) * this.pscale;	
		// 3D		
		z = normalize(z);
		this.P += z * scale_offset;
		vector y = normalize(cross(z,cross(n0,z)));
		this.t = maketransform(z,{0,1,0}) * this.pscale;
		
		// FIX PreRotation
		this->fixRotation(g);
	}	
	
	void fromGear(gear g)
	{
		// Copy Tooth length since gears hould have the same
		this.tooth_length = g.tooth_length;
		
		vector p1 = this.P;
		vector p0 = g.P;		
		
		float pscale0 = g.pscale;    
		float pscale =  length(p0 - p1) - pscale0;
		
		// Fix the real scale based on the tooth_length 
		float scale_offset = this->fixScale();
		
		// Fix position bsed on new scale
		this.P += normalize(p1-p0) * scale_offset;		
		this.t = maketransform({0,0,1},{0,1,0}) * this.pscale;
		
		// FIX PreRotation
		this->fixRotation(g);
	}	
	
	void fromPoint(int _geo;int _pt)
	{
		this.pt - _pt;
		this.geo = _geo;
		
		this.tooth_length 	= point(_geo,"tooth_length",_pt);
		this.P 				= point(_geo,"P",_pt);		
		this.n_teeth 		= point(_geo,"n_cuts",_pt);		
		this.t 				= point(_geo,"transform",_pt);		
		this.pscale 		= cracktransform(0,0,2,{0,0,0},this.t).x;
	}
		
	void setGear()
	{
		setpointattrib(0,"transform",this.pt,this.t);
		setpointattrib(0,"n_cuts",this.pt,this.n_teeth);
		setpointattrib(0,"tooth_length",this.pt,this.tooth_length);
		setpointattrib(0,"P",this.pt,this.P);
		
		setpointattrib(0,"N",this.pt,this->getN());
	}
	
	void rotate( float ammount)
	{
		rotate(this.t, ammount , normalize(this.t*{0,1,0}));		
		setpointattrib(0,"transform",this.pt,this.t);
	}
	
	// Creation shortcuts
	void fromPoint(int pt; int _geo0;int _pt0)
	{
		gear g0;
		g0->fromPoint(_geo0,_pt0);		
		this->init(pt);
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
}


