/* *****************************************************************************
 *  Name:    Taosif Ahsan
 *  NetID:   tahsan
 *  Precept: P13
 *
 *  Partner Name:    Declan Farmer
 *  Partner NetID:   dfarmer
 *  Partner Precept: P13
 *
 *  Description:  This program finds out the path of least length by using
 *                nearest insertion method and smallest insertion method
 *
 **************************************************************************** */

public class Tour {
    private Node start;  // initial reference node

    private class Node {
        private Point p;   // holds the value in the node
        private Node next; // links to the next node
    }

    // creates an empty tour
    public Tour() {
        start = null;
    }

    // creates the 4-point tour a->b->c->d->a (for debugging)
    public Tour(Point a, Point b, Point c,
                Point d) {
        // creating four nodes
        Node n1 = new Node();
        Node n2 = new Node();
        Node n3 = new Node();
        Node n4 = new Node();

        // inserting values
        n1.p = a;
        n2.p = b;
        n3.p = c;
        n4.p = d;

        // linking them
        n1.next = n2;
        n2.next = n3;
        n3.next = n4;
        n4.next = n1;

        // creating circle
        start = n1;
    }

    // returns the number of points in this tour
    public int size() {
        // empty quote
        if (start == null) return 0;


        // initializing variables and nodes;
        Node card = start;
        int total = 0;

        // loop
        do {
            total++;   // incrementing the count
            card = card.next; // moving to the next node
        } while (card != start); // loop stops when it gets to the beginning
        return total;
    }

    // returns the length of this tour
    public double length() {
        // empty quote
        if (start == null) return 0.0;

        // initializing variables and nodes;
        double total = 0.0;
        Node card = start;

        // loop
        do {
            card = card.next;  // moving the next node
            total += card.p.distanceTo(card.next.p); // increasing the length
        } while (card != start); // loop stops when it gets to the beginning
        return total;
    }

    // returns a string representation of this tour
    public String toString() {
        // initializing string builder
        StringBuilder str = new StringBuilder();

        // corner case
        if (start == null)
            return "";

        else {
            // initializing node
            Node current = start;

            // loop
            do {

                // creating string representation
                str.append(current.p);
                str.append("\n");

                current = current.next; // moving to the next node
            }
            while (current != start); // loop stops when it gets to the beginning
        }
        return str.toString();
    }

    // draws this tour to standard drawing
    public void draw() {
        if (start != null) // corner case

        {
            Node current = start; // initializing node
            do {
                // drawing the path
                current.p.draw();
                current.p.drawTo(current.next.p);


                current = current.next; // moving to the next node
            }
            while (current != start); // loop stops when it gets to the beginning
        }
    }

    // inserts a point after a specified point
    private void insert(Point candidate, Point p) {

        // initializing necessary objects
        Node card = start;
        Node newNode = new Node();

        // taking the point as input
        newNode.p = p;
        do {

            card = card.next; // moving to the next node

            // inserting p after candidate
            if (card.p == candidate) {
                newNode.next = card.next;
                card.next = newNode;
            }
        }
        while (card != start);  // controlling the ending of the loop

    }


    // inserts p using the nearest neighbor heuristic
    public void insertNearest(Point p) {

        // corner case
        if (start == null) {
            Node newNode = new Node();
            newNode.p = p;
            start = newNode;
            start.next = start;  // circle
        }
        else {

            // initializing necessary variables and objects
            Node card = start;
            double best = Double.POSITIVE_INFINITY;
            Point temp = card.p;

            // finding out the right spot to insert the point
            do {
                // updating the best position till now
                double tempBest = card.p.distanceTo(p);
                if (tempBest < best) {
                    temp = card.p;
                    best = tempBest;
                }

                // moving to the next node
                card = card.next;
            } while (card != start);

            // inserting the point p
            insert(temp, p);
        }
    }

    // inserts p using the smallest increase heuristic
    public void insertSmallest(Point p) {

        // corner case
        if (start == null) {
            Node newNode = new Node();
            newNode.p = p;
            start = newNode;
            start.next = start; // circle
        }
        else {

            // initializing necessary variables and objects
            Node card = start;
            double best = Double.POSITIVE_INFINITY;
            Point temp = card.p;

            // finding out the right spot to insert the point
            do {

                // updating the best position till now

                // the formula to figure that out
                double tempBest = card.p.distanceTo(p)
                        + card.next.p.distanceTo(p)
                        - card.p.distanceTo(card.next.p);

                // updating if necessary
                if (tempBest < best) {
                    temp = card.p;
                    best = tempBest;
                }
                card = card.next; // moving to the next node
            } while (card != start);
            insert(temp, p); // inserting the point p
        }
    }

    // tests this class by directly calling all constructors and instance methods
    public static void main(String[] args) {
        Tour square = new Tour(new Point(0.2, 0.2),
                               new Point(0.2, 0.8),
                               new Point(0.8, 0.8),
                               new Point(0.8, 0.2));

        square.insertNearest(new Point(0.24, 0.5));
        square.insertSmallest(new Point(0.3, 0.4));
        StdOut.print(square);
        StdOut.println(square.length());
        StdOut.println(square.size());
        square.draw();
    }
}
