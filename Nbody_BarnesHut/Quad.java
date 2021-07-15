//quadrant class, to divide space into 4 regions and 
//bring down number of calculations
public class Quad{
    double pos_x;
    double pos_y;
    double length;
    //qudrant defined by southwest corner co-ordinate and length of a side
    public Quad(double pos_x,double pos_y,double length){
        this.pos_x=pos_x;
        this.pos_y=pos_y;
        this.length=length;
    }
    //returns if a position is in the quadrant
    public boolean contains(double x, double y){
        boolean t_x=(pos_x<=x)&&(x<=pos_x+length);
        boolean t_y=(pos_y<=y)&&(y<=pos_y+length);
        return (t_x&&t_y);
    }
    //returns length of the qudrant
    public double length(){
        double a = length;
        return a;
    }
    //creates a mini quadrant in northwest corner
    public Quad NW(){
        Quad q=new Quad(pos_x,pos_y+this.length()/2,this.length()/2);
        return q;
    }
    //creates a mini quadrant in northeast corner
    public Quad NE(){
        Quad q=new Quad(pos_x+this.length()/2,pos_y+this.length()/2,this.length()/2);
        return q;
    }
    //creates a mini quadrant in southwest corner
    public Quad SW(){
        Quad q=new Quad(pos_x,pos_y,this.length()/2);
        return q;
    }
    //creates a mini quadrant in southeast corner
    public Quad SE(){
        Quad q=new Quad(pos_x+this.length()/2,pos_y,this.length()/2);
        return q;
    }
    //draws the quadrant
    public void draw(){
        StdDraw.setPenRadius(0.0002);
        StdDraw.setPenColor(StdDraw.GREEN);
        StdDraw.square(pos_x,pos_y,length);
    }
}



