//barnes-hut tree algorithm to calculate net force in o(NlogN)
import java.util.ArrayList;
public class BHTree {
    private Body body;     // body or aggregate body stored in this node
    private Quad quad;     // square region that the tree represents
    private BHTree nw;     // tree representing northwest quadrant
    private BHTree ne;     // tree representing northeast quadrant
    private BHTree sw;     // tree representing southwest quadrant
    private BHTree se;     // tree representing southeast quadrant
    private int n;         // total entry in a tree

    //Tree defined by
    // center of mass,
    // total mass,
    // the square cell center of mass is in
    // the trees and nodes underneath it
    public BHTree(Body body, Quad quad){
        this.body=body;
        this.quad=quad;
        this.nw=null; 
        this.ne=null;
        this.sw=null;
        this.se=null;
        this.n=1;
    }
    //returns if a node has childs
    public boolean internal(){
        boolean nw_ex=(this.nw!=null);
        boolean ne_ex=(this.ne!=null);
        boolean sw_ex=(this.sw!=null);
        boolean se_ex=(this.se!=null);
        return  (nw_ex|| ne_ex || sw_ex || se_ex);
    }
    //inserts a body in the a node of the Tree
    public void insert(Body b){
        //if node does not contain a body, put the new body
        if (body==null){
            body=b;
            return;
        }
        //if node is an internal node,
        if (this.internal()){
            //update the COM and total mass
            this.body=Body.add(this.body,b);
            //recursively insert the body
            if (b.in(this.nw.quad))
                this.nw.insert(b);
            else if  (b.in(this.ne.quad))
                this.ne.insert(b);
            else if (b.in(this.sw.quad))
                this.sw.insert(b);
            else
                this.se.insert(b);
        }
        //if node is an external node
        else{
            //subdivide the region further
            this.nw=new BHTree(null,this.quad.NW());
            this.ne=new BHTree(null,this.quad.NE());
            this.sw=new BHTree(null,this.quad.SW());
            this.se=new BHTree(null,this.quad.SE());
            //recursively insert both bodies
            //previous body
            if (this.body.in(this.nw.quad))
                this.nw.insert(this.body);
            else if (this.body.in(this.ne.quad))
                this.ne.insert(this.body);
            else if (this.body.in(this.sw.quad))
                this.sw.insert(this.body);
            else
                this.se.insert(this.body);
            //new body
            if (b.in(this.nw.quad))
                this.nw.insert(b);
            else if (b.in(this.ne.quad))
                this.ne.insert(b);
            else if (b.in(this.sw.quad))
                this.sw.insert(b);
            else
                this.se.insert(b);
            this.body=Body.add(this.body,b);
        }
        this.n++;
    }
    //calculates total force on a body 
    //x-component
    public double updateForce_x(Body b){
        double theta=0.5;
        //if there is no body in node
        if (this.body==null)
            //then there is no force from the node
            return 0;
        //if the current node is an external node
        if (!this.internal()){
            //and it is not the body itthis
            if (this.body==b)
                return 0;
            //calculate the force exerted by the current node
            //on body, and add this amount to body's net force
            else
                return Body.force_x(this.body,b);
        } 
        //otherwise 
        else{
            //calculate the ratio s/d
            double d=Body.distance(this.body,b);
            double s=this.quad.length();
            //if s/d<theta
            if (s/d<theta)
                //treat this internal node as a single body,
                //and calculate the force it exerts on given
                //body, and add this amount to body's net force
                return Body.force_x(this.body,b);
            //otherwise
            else{
                //run the procedure recursively on
                //each of the current node's children
                double force_nw=this.nw.updateForce_x(b);
                double force_ne=this.ne.updateForce_x(b);
                double force_sw=this.sw.updateForce_x(b);
                double force_se=this.se.updateForce_x(b);
                return force_nw+force_ne+force_sw+force_se;
            }
        }
    }
    //y-component
    //same algorithm as x-component  
    public double updateForce_y(Body b){
        double theta=0.5;
        if (this.body==null)
            return 0;
        if (!this.internal()){
            if (this.body==b)
                return 0;
            else
                return Body.force_y(this.body,b);
        }
        else{
            double d=Body.distance(this.body,b);
            double s=this.quad.length();
            if (s/d<theta)
                return Body.force_y(this.body,b);
            else{
                double force_nw=this.nw.updateForce_y(b);
                double force_ne=this.ne.updateForce_y(b);
                double force_sw=this.sw.updateForce_y(b);
                double force_se=this.se.updateForce_y(b);
                return force_nw+force_ne+force_sw+force_se;
            }
        }  
    }
    //outputs all quadrants in Tree in arraylist
    public ArrayList<Quad> read_quad(){
        ArrayList<Quad> elements = new ArrayList<Quad>(0);
        //if the node is external
        //add that body to arraylist
        if (!this.internal())
            elements.add(this.quad);
        //if there are further childrens beneath 
        //the node, recursively add the associated arrays
        //with trees to the main arraylist
        else{
            if (this.nw!=null)
                elements.addAll(this.nw.read_quad());
            if (this.ne!=null)
                elements.addAll(this.ne.read_quad());
            if (this.sw!=null)
                elements.addAll(this.sw.read_quad());
            if (this.se!=null)
                elements.addAll(this.se.read_quad());
        }   
        return elements;
    }  
    //returns the number of total bodies in BHTree
    public int total_bodies(){
    	if (this.body==null)
    		return 0;
    	else
    		return this.n;
    }
    //shows the number in text
    public void show_total_bodies(Quad q_root){
    	StdDraw.setPenColor(StdDraw.CYAN);
    	double rx=q_root.pos_x+q_root.length()*0.885;
        double ry=q_root.pos_x+q_root.length()*0.965;
        StdDraw.text(rx,ry,"No of Bodies = "+Integer.toString(this.total_bodies()));
    }
    //show quadrants in a a Quad arraylist
    public void show_quads(Quad q_root){
        ArrayList<Quad> quads=this.read_quad();
            //drawing quadrants 
            //qudrant color is GREEN
            for(Quad q: quads){
            q.draw();
        }
        //show number of quadrants in arraylist
        StdDraw.setPenColor(StdDraw.CYAN);
        double px=q_root.pos_x+q_root.length()*0.885;
        double py=q_root.pos_x+q_root.length()*0.985;
        StdDraw.text(px,py,"No of Quads = "+Integer.toString(quads.size()));
    } 
    //builds Tree from a body objects
    public static BHTree buildTree(Body[] bodies, Quad q){
        //first node in the Tree
        BHTree root = new BHTree(null, q);
        int n=bodies.length;
        //add other bodies in Tree
        for(int i=0;i<n;i++){
            //possible bug correction
            //do not add body unless they are
            //within the largest qudrant
            if (bodies[i].in(q))
                root.insert(bodies[i]);
        }
    return root;
    } 
   
}

