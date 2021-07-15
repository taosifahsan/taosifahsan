//body class (particles, stars, plasma) and methods (their interactive force)
public class Body{
    double px;
    double py;
    double mass;
    //particle body defined by position and mass
    public Body(double px,double py,double mass){
        this.px=px;
        this.py=py;
        this.mass=mass;
    }
    //returns if body is in a qudrant
    public boolean in(Quad q){
        return q.contains(px,py);
    }
    //replaces two bodies with their COM and total mass
    public static Body add(Body a, Body b){
        double M=a.mass+b.mass;
        double pX=((a.px)*(a.mass)+(b.px)*(b.mass))/M;
        double pY=((a.py)*(a.mass)+(b.py)*(b.mass))/M;
        return new Body(pX,pY,M);
    }
    //returns the distance of two bodies
    public static double distance(Body a, Body b){
        double rx=a.px-b.px;
        double ry=a.py-b.py;
        double r=Math.sqrt(rx*rx+ry*ry);
        return r;
    }
    //defines radial force between two unit mass body
    public static double unit_force_rad(double r)
    {   
        double r0=0.02;//radius of bodies
        if (r>r0)
            return 1/(r*r);//inverse square attractive force
        else
            return r/(r0*r0);//force after collision
    }
    //returns force between two bodies 
    //x-component
    public static double force_x(Body a, Body b)
    {
        double rx=a.px-b.px;
        double ry=a.py-b.py;
        double r=Math.sqrt(rx*rx+ry*ry);
        return a.mass*b.mass*rx/r*unit_force_rad(r);
    }
    //y-component
    public static double force_y(Body a, Body b)
    {
        double rx=a.px-b.px;
        double ry=a.py-b.py;
        double r=Math.sqrt(rx*rx+ry*ry);
        return a.mass*b.mass*ry/r*unit_force_rad(r);
    }
    //creating array of Body type from position and mass array
    public static Body[] buildBodies(double[] px,double[] py,double[] mass){
        int n=px.length;
        Body[] bodies=new Body[n];
        for(int i=0;i<n;i++)
            bodies[i]=new Body(px[i], py[i], mass[i]);
        return bodies;
    }
    //calculating total force on a body
    //every single body is taken into account, so brute calculation
    //o(n^2), slow
    //x-component
    public static double updateForceBrute_x(Body[] bodies, Body b){
       int n=bodies.length;
       double F=0;
       for(int i=0;i<n;i++){
        if (b!=bodies[i])//a body exters no force on itself
            F+=force_x(bodies[i],b);
       }
       return F;
    }
    //y-component
    public static double updateForceBrute_y(Body[] bodies, Body b){
       int n=bodies.length;
       double F=0;
       for(int i=0;i<n;i++){
        if (b==bodies[i]) continue;
        F+=force_y(bodies[i],b);
       }
       return F;
    }        
}

