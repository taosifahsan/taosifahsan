import java.util.ArrayList;
import java.awt.Font;
//animates multi-body systems interacting with each other
//here, gravitation interaction was chosen
//implements barnes-hut algorithm to calculate net force in o(NlogN)
//uses StdDraw library to animate
public class NBodyFast {
    public static void main(String[] args) {
        //creating  universe
        int n = Integer.parseInt(args[0]);//number of particles
        boolean quads_yes=Boolean.parseBoolean(args[1]);//showing qudrants
        double dt = 0.0001;//time between each frame
        double G = 0.01;//gravitation constant
        int v =10;//velocity range
        double radius = 1;//size of universe
        Quad q = new Quad(0,0,1*radius);//universe quadrant
        //acceleration variable declaration 
        double ax=0;
        double ay=0;
        //declaring arrays
        //position
        double[] rx = new double[n];
        double[] ry = new double[n];
        //velocity
        double[] vx = new double[n];
        double[] vy = new double[n];
        //mass
        double[] m = new double[n];
        double[] r=new double[n];
        double[] theta=new double[n];
        double M=1000;
        //initial condition of the universe
        for(int i=0;i<n;i++){
            r[i]=0.1*radius*Math.random();
            theta[i]=2*Math.PI*Math.random();
        }
 		double sep=0.15;//seperation of galaxies
 		//galaxy 1
        for(int i=0; i < 3*n/4; i++) {
            rx[i] =1.22*r[i]*Math.cos(theta[i])+0.5;
            ry[i] =1.22*r[i]*Math.sin(theta[i])+0.5;
            vx[i] =Math.sin(theta[i])*v;
            vy[i] =-Math.cos(theta[i])*v-Math.sqrt(G*3*n/sep/4)/3/1.5;
            m[i] = 10000/n*Math.random();
        }
        //galaxy 2
        for(int i=3*n/4; i < n; i++) {
            rx[i] =0.71*r[i]*Math.cos(theta[i])+0.5-sep;
            ry[i] =0.71*r[i]*Math.sin(theta[i])+0.5;
            vx[i] =Math.sin(theta[i])*v/2;
            vy[i] =-Math.cos(theta[i])*v/2+Math.sqrt(G*3*n/sep/4)/1.5;
            m[i] = 10000/n*Math.random();
        }
        //initialize standard drawing
        StdDraw.enableDoubleBuffering();
        StdDraw.setCanvasSize(770, 770);
        StdDraw.setXscale(0, 1 * radius);
        StdDraw.setYscale(0, 1 * radius);
        Font font = new Font("Courier", Font.BOLD, 10);
        StdDraw.setFont(font);
        //simulate the universe per frame
        while (true) {
            //creating body array from position and mass
            Body[] bodies= Body.buildBodies(rx,ry,m);
            //creating the Tree
            BHTree tree= BHTree.buildTree(bodies,q);
            //updating position and velocity
            for (int i = 0; i < n; i++){
                //calculating accelaration using BHA
                ax=G*tree.updateForce_x(bodies[i])/m[i];
                ay=G*tree.updateForce_y(bodies[i])/m[i];
                vx[i] += ax * dt;
                vy[i] += ay * dt;
                rx[i] += vx[i] * dt+0.5*ax*dt*dt;
                ry[i] += vy[i] * dt+0.5*ay*dt*dt;
            }    
            //draw the universe
            StdDraw.clear(StdDraw.BLACK);//black background
            if (quads_yes) 
                tree.show_quads(q);//draw quads
            tree.show_total_bodies(q);//show total bodies inside the frame
            //drawing bodies
            for (int i = 0; i < n; i++) {
                //color of body is determined by it's energy
                //energy is prop to v^2
                //temperature is prop to <E>
				double red = ((vx[i] * vx[i] + vy[i] * vy[i]));//whiter~hotter
                double white = 100.0;//color scale constant
                int red_norm = (int) (255 * (red) / (red + white));//scaled
                int white_norm = (int) (255 * (white) / (red + white));//scaled
                //setting color
                StdDraw.setPenColor(255-white_norm, 255, 255);
                //plotting the bodies
                //radius of the bodies is prop to m^(1/3)
                StdDraw.filledCircle(rx[i], ry[i], 0.001*Math.pow((m[i]),1/3.0));
                }
            //show the plot
            StdDraw.show();
            //pause a while
            StdDraw.pause(0);
        }
    }
}
