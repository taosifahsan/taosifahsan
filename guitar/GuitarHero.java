/* *****************************************************************************
 *  Name:            Taosif Ahsan
 *  NetID:           tahsan
 *  Precept:         P13
 *
 *  Partner Name:    Declan Farmer
 *  Partner NetID:   dfarmer
 *  Partner Precept: P13
 *
 *  Description:  Plays guitar strings when the user types the lowercase letters
 *                respectively in the standard drawing window.
 *
 **************************************************************************** */

public class GuitarHero {

    public static void main(String[] args) {

        String keyboard = "q2we4r5ty7u8i9op-[=zxdcfvgbnjmk,.;/' ";
        int length = keyboard.length();
        // Create 37 guitar strings, for concerts .

        GuitarString[] string = new GuitarString[length];
        for (int i = 0; i < length; i++)
            string[i] = new GuitarString(440 * Math.pow(2, (i - 24.0) / 12.0));


        // the main input loop
        while (true) {

            // check if the user has typed a key, and, if so, process it
            if (StdDraw.hasNextKeyTyped()) {

                // the user types this character
                char key = StdDraw.nextKeyTyped();
                String a = Character.toString(key);
                if (keyboard.contains(a)) {
                    int index = keyboard.indexOf(key);
                    // pluck the corresponding string
                    string[index].pluck();
                }

            }

            // compute the superposition of the samples
            double sample = 0;

            for (int i = 0; i < length; i++) sample += string[i].sample();


            // send the result to standard audio
            StdAudio.play(sample);

            // advance the simulation of each guitar string by one step
            for (int i = 0; i < length; i++) string[i].tic();
        }
    }

}
