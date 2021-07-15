/******************************************************************************
 *Name:Taosif Ahsan
 *NetID:tahsan
 *Precept:P13
 *
 *Description:a program that produces pseudo-random bits by simulating a
 *             linear-feedback shift register
 *
 *****************************************************************************/

public class LFSR {

    // contains bits
    private int[] bit;
    // used for tap
    private final int tap0;

    // creates an LFSR with the specified seed and tap
    public LFSR(String seed, int tap) {
        // PUT YOUR CODE HERE
        int n = seed.length();
        bit = new int[n];
        // converts from char to int
        for (int i = 0; i < n; i++) {
            if (seed.charAt(i) == '1') bit[n - 1 - i] = 1;
            else bit[n - 1 - i] = 0;
        }
        // takes the value of tap
        tap0 = tap;
    }

    // returns the number of bits in this LFSR
    public int length() {
        // PUT YOUR CODE HERE
        // returns length
        return bit.length;
    }

    // returns the ith bit of this LFSR (as 0 or 1)
    public int bitAt(int i) {
        // PUT YOUR CODE HERE
        // returns ith bit
        return bit[i - 1];
    }

    // returns a string representation of this LFSR
    public String toString() {
        // PUT YOUR CODE HERE
        int n = length();
        // initializing string
        String str = "";
        // creating the string
        for (int i = 0; i < n; i++) {
            str = bit[i] + str;
        }
        return str;
    }

    // simulates one step of this LFSR and returns the new bit (as 0 or 1)
    public int step() {
        // PUT YOUR CODE HERE
        int n = length();
        // saving previous value of bit[0]
        int t = bit[0];
        // xor operation saved in bit[0]
        bit[0] = bit[n - 1] ^ bit[tap0 - 1];

        // moving bits
        for (int i = n - 1; i > 1; i--) {
            bit[i] = bit[i - 1];
        }
        // moving previous bit0 to bit1
        // ignoring this step if length()=1 to avoid out of bounds error
        if (n > 1) bit[1] = t;
        return bit[0];
    }

    // simulates k steps of this LFSR and returns the k bits as a k-bit integer
    public int generate(int k) {
        // PUT YOUR CODE HERE
        int sum = 0;
        // converting binary to number
        for (int i = 0; i < k; i++) {
            int tempbit = step();
            sum = 2 * sum + tempbit;
        }
        return sum;
    }

    // tests this class by directly calling all instance methods
    public static void main(String[] args) {
        // PUT YOUR TEST CODE HERE

        // absract data type
        LFSR lfsr0 = new LFSR("01101000010", 9);

        // testing length method
        StdOut.println(lfsr0.length());
        StdOut.println();

        // testing bitAt method
        StdOut.println(lfsr0.bitAt(1));
        StdOut.println();

        // testing toString method
        StdOut.println(lfsr0);
        StdOut.println();

        // testing step method
        for (int i = 0; i < 10; i++) {
            int bit = lfsr0.step();
            StdOut.println(lfsr0 + " " + bit);
        }
        StdOut.println();

        // testing generate method
        LFSR lfsr1 = new LFSR("01101000010", 9);
        for (int i = 0; i < 10; i++) {
            int r = lfsr1.generate(5);
            StdOut.println(lfsr1 + " " + r);
        }
    }
}
