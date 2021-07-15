/* *****************************************************************************
 *  Name:    Taosif Ahsan
 *  NetID:   tahsan
 *  Precept: P13
 *
 *  Partner Name:    Declan Farmer
 *  Partner NetID:   dfarmer
 *  Partner Precept: P13
 *
 *  Description:  Generates seemingly meaningful but random text
 **************************************************************************** */

public class TextGenerator {
    public static void main(String[] args) {
        char c;
        // taking the inputs
        int k = Integer.parseInt(args[0]);
        int t = Integer.parseInt(args[1]);
        String text = StdIn.readAll();

        // creating the markovmodel and extracting the kgram
        MarkovModel model = new MarkovModel(text, k);
        String kgram = text.substring(0, k);

        // printing the kgram
        StdOut.print(kgram);

        // Generating texts
        for (int i = 0; i < t - k; i++) {

            // getting the random character
            c = model.random(kgram);

            // printing the character
            StdOut.print(c);

            // updating the kgram if k is not zero
            // there is no kgram if k=0, so no need to update kgram
            // sundtring(1,0) creates bug
            if (k != 0)
                kgram = kgram.substring(1, k) + Character.toString(c);
        }

        StdOut.println(); // Just for a nice formatt
    }
}
