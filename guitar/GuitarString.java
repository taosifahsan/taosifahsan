/* *****************************************************************************
 *  Name:            Taosif Ahsan
 *  NetID:           tahsan
 *  Precept:         P13
 *
 *  Partner Name:   Declan Farmer
 *  Partner NetID:  dfarmer
 *  Partner Precept: P13
 *
 *  Description:  This file creates GuitarString variable and necessary
 *                functions which will be used in GuitarHero.java to play
 *                guitar. It uses the Karplus-Strong method to simulate the
 *                behaviour of a GuitarString
 **************************************************************************** */

public class GuitarString {
    // YOUR INSTANCE VARIABLES HERE

    private final RingBuffer gs; // Guiterstring in a ringbuffer

    // creates a guitar string of the specified frequency,
    // using sampling rate of 44,100
    public GuitarString(double frequency) {
        // YOUR CODE HERE
        int n = (int) Math.ceil(44100 / frequency);
        gs = new RingBuffer(n);
        for (int i = 0; i < n; i++) {
            gs.enqueue(0.0);
        }
    }

    // creates a guitar string whose size and initial values are given by
    // the specified array
    public GuitarString(double[] init) {
        // YOUR CODE HERE
        int m = init.length;
        gs = new RingBuffer(m);
        for (int i = 0; i < m; i++) {
            gs.enqueue(init[i]);
        }

    }

    // returns the number of samples in the ring buffer
    public int length() {
        // YOUR CODE HERE
        return gs.capacity();
    }

    // plucks the guitar string (by replacing the buffer with white noise)
    public void pluck() {
        // YOUR CODE HERE
        int temp = length();

        while (!gs.isEmpty()) {
            gs.dequeue();
        }

        for (int i = 0; i < temp; i++)
            gs.enqueue(StdRandom.uniform(-0.5, 0.5));
    }

    // advances the Karplus-Strong simulation one time step
    public void tic() {
        // YOUR CODE HERE
        double x = gs.dequeue();
        double y = gs.peek();
        double z = 0.996 * 0.5 * (x + y);
        gs.enqueue(z);
    }

    // returns the current sample
    public double sample() {
        // YOUR CODE HERE
        return gs.peek();
    }


    // tests and calls every constructor and instance method in this class
    public static void main(String[] args) {
        // YOUR CODE HERE

        // creating variable by capacity
        GuitarString string = new GuitarString(4410);

        // testing length
        int length = string.length();
        System.out.println(length);

        // testing pluck
        string.pluck();

        double[] samples = {
                0.2, 0.4, 0.5, 0.3, -0.2, 0.4, 0.3,
                0.0, -0.1, -0.3
        };

        // creating variable by array
        GuitarString testString = new GuitarString(samples);

        int m = 25; // 25 tics
        for (int i = 0; i < m; i++) {

            // testing sample
            double sample = testString.sample();
            StdOut.printf("%6d %8.4f\n", i, sample);

            // testing tic
            testString.tic();
        }

    }

}
