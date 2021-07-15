/* *****************************************************************************
 *  Name:    Taosif
 *  NetID:   Ahsan
 *  Precept: P13
 *
 *  Partner Name:    Declan Farmer
 *  Partner NetID:   dfarmer
 *  Partner Precept: P13
 *
 *  Description:  Creates markovmodel and necessary functions associated
 *                with the markovmodel.
 *
 **************************************************************************** */

public class MarkovModel {

    private static final int ASCII = 128;

    // stores MarkovModel with frequency of kgrams
    private final ST<String, Integer> sb1;
    // stores MarkovModel with frecuency of characters after kgrams
    private final ST<String, int[]> sb2;

    // stores order of the MarkovModel
    private final int order;


    // creates a Markov model of order k for the specified text
    public MarkovModel(String text, int k) {

        order = k;

        // creating the cyclic string
        text = text + text.substring(0, k);

        // initializing the markovmodel
        sb1 = new ST<String, Integer>();
        sb2 = new ST<String, int[]>();

        // loop to create markovmodel
        for (int i = 0; i < text.length() - k; i++) {

            // creating substring and next character
            String substr = text.substring(i, i + k);
            char letter = text.charAt(i + k);

            // 1st markovmodel
            if (sb1.contains(substr)) {
                sb1.put(substr, sb1.get(substr) + 1);
            }
            else {

                sb1.put(substr, 1);
            }

            // 2nd markovmodel
            if (sb2.contains(substr)) {

                int[] array = sb2.get(substr);
                array[letter]++;
                sb2.put(substr, array);
            }
            else {
                int[] array = new int[ASCII];
                sb2.put(substr, array);
                array[letter]++;
                sb2.put(substr, array);
            }

        }
    }

    // returns the order k of this Markov model
    public int order() {
        return order;
    }

    // returns a string representation of the Markov model (as described below)
    public String toString() {

        // initializing the stringbuilder
        StringBuilder result = new StringBuilder();

        // appending the stringbuilder
        for (String word : sb2.keys()) {

            // getting the array associated with kgrams
            int[] keys = sb2.get(word);

            // appending the array associated with the kgrams
            StringBuilder c = new StringBuilder();
            for (int m = 0; m < ASCII; m++) {
                if (keys[m] != 0) c.append((char) m + " " + keys[m] + " ");
            }

            // converting to string
            String array = c.toString();

            // creating the markov model representation
            result.append(word + ": " + array + "\n");
        }
        return result.toString();
    }

    // returns the number of times the specified kgram appears in the text
    public int freq(String kgram) {

        // in case the length of kgram doesn't equal to the order
        if (kgram.length() != order())
            throw new IllegalArgumentException("length is invalid");

        // frequency of a kgram is zero if it does not exists
        if (!sb1.contains(kgram)) return 0;

        // returning the frequency
        return sb1.get(kgram);
    }

    // returns the number of times the character c follows the specified
    // kgram in the text
    public int freq(String kgram, char c) {

        // in case the length of kgram doesn't equal to the order
        if (kgram.length() != order())
            throw new IllegalArgumentException("length is invalid");

        // frequency of a certain character after a kgram is zero if that
        // kgram does not exists
        if (!sb1.contains(kgram)) return 0;

        // returning the frequency
        int[] arr = sb2.get(kgram);
        return arr[c];
    }

    // returns a random character that follows the specified kgram in the text,
    // chosen with weight proportional to the number of times that character
    // follows the specified kgram in the text
    public char random(String kgram) {

        // the corner cases
        if (kgram.length() != order())
            throw new IllegalArgumentException("length is invalid");
        if (!sb2.contains(kgram))
            throw new IllegalArgumentException("doesn't have kgram");

        // returning random variable
        return (char) StdRandom.discrete(sb2.get(kgram));
    }

    // tests this class by directly calling all instance methods
    public static void main(String[] args) {
        int m = 1000000;
        double[] x = new double[3];
        String text2 = "abcabdabe";
        MarkovModel model = new MarkovModel(text2, 2);
        System.out.println(model.order());
        System.out.println(model.freq("ab"));
        System.out.println(model.freq("ab", 'c'));
        System.out.println();
        System.out.println(model);
        System.out.println();
        for (int i = 0; i < m; i++) {
            char c = model.random("ab");
            if (c == 'c') x[0] += 1.0;
            else if (c == 'd') x[1] += 1.0;
            else x[2] += 1.0;
        }

        System.out.printf("{ %3.4f, %3.4f, %3.4f }",
                          3 * x[0] / m, 3 * x[1] / m, 3 * x[2] / m);
    }
}
