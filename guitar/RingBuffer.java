/* *****************************************************************************
 *  Name:             Taosif Ahsan
 *  NetID:            tahsan
 *  Precept:          P13
 *
 *  Partner Name:    Declan Farmer
 *  Partner NetID:   dfarmer
 *  Partner Precept: P13
 *
 *  Description:  It creates RingBuffer variable and necessary variables
 *                which will be used in GuitarString and GuitarHero to play \
 *               Guitar.
 **************************************************************************** */

public class RingBuffer {
    // YOUR INSTANCE VARIABLES HERE
    private double[] rb;          // items in the buffer
    private int first;            // index for the next dequeue or peek
    private int last;             // index for the next enqueue
    private int size;             // number of items in the buffer

    // creates an empty ring buffer with the specified capacity
    public RingBuffer(int capacity) {
        // YOUR CODE HERE
        rb = new double[capacity];
        first = 0;
        last = 0;
        size = 0;
    }

    // return the capacity of this ring buffer
    public int capacity() {
        // YOUR CODE HERE
        return rb.length;
    }

    // return number of items currently in this ring buffer
    public int size() {
        // YOUR CODE HERE
        return size;
    }

    // is this ring buffer empty (size equals zero)?
    public boolean isEmpty() {
        // YOUR CODE HERE
        return size == 0;
    }

    // is this ring buffer full (size equals capacity)?
    public boolean isFull() {
        // YOUR CODE HERE
        return size == capacity();
    }

    // adds item x to the end of this ring buffer
    public void enqueue(double x) {
        // YOUR CODE HERE

        // corner case
        if (isFull()) throw new RuntimeException("Running buffer is full");


        rb[last] = x;
        // creating circle using modular arithmetic
        // increasing the value by one until it hits capacity-1
        // then the value become 0
        last = (last + 1) % capacity();

        // updating the size
        size++;

    }

    // deletes and returns the item at the front of this ring buffer
    public double dequeue() {
        // YOUR CODE HERE

        // temporarily storing the value of front element
        double temp = rb[first];

        // corner case
        if (isEmpty()) throw new RuntimeException("Running buffer is empty!");

        // creating circle using modular arithmetic
        // increasing the value by one until it hits capacity-1
        // then the value become 0
        first = (first + 1) % capacity();

        // updating the size
        size--;

        // returning the value of front element
        return temp;
    }

    // returns the item at the front of this ring buffer
    public double peek() {
        // YOUR CODE HERE

        // corner case
        if (isEmpty()) throw new RuntimeException("Running buffer is empty!");

        return rb[first];

    }

    // tests and calls every instance method in this class
    public static void main(String[] args) {

        // creating a RingBuffer
        RingBuffer RB = new RingBuffer(10);

        // testing capacity()
        int capacity = RB.capacity();
        System.out.println(capacity);
        // testing enqueue
        for (int i = 0; i < RB.capacity(); i++) {
            RB.enqueue(1.0);
            // testing peek
            double peek = RB.peek();
            System.out.print(peek + " ");
        }
        System.out.println();

        // testing Size
        int size = RB.size();
        System.out.println(size);

        // testing isFull()
        boolean full = RB.isFull();
        System.out.println(full);

        double val;
        // testing dequeue
        for (int i = 0; i < RB.capacity(); i++) {
            val = RB.dequeue();
            System.out.print(val + " ");
        }

        System.out.println();

        // testing isEmpty
        boolean empty = RB.isEmpty();
        System.out.println(empty);
    }


}
