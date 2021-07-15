/* *****************************************************************************
 *  Name:    Taosif Ahsan
 *  NetID:   tahsan
 *  Precept: P13
 *
 *  Partner Name:    Declan Farmer
 *  Partner NetID:   dfarmer
 *  Partner Precept: P13
 *
 *  Description:  Same as GuiterHero but this one uses just intonation. So it
 *                sounds better.
 **************************************************************************** */

public class EnrichedGuitarHero {
    public static void main(String[] args) {
        String keyboard = "q2we4r5ty7u8i9op-[=zxdcfvgbnjmk,.;/' ";
        int length = keyboard.length();
        // Create 37 guitar strings, for concerts .

        // creates array to hold the harmonious ratios
        double[] harmony = {
                1.0 / 1.0, 16.0 / 15.0, 9.0 / 8.0, 6.0 / 5.0,
                5.0 / 4.0, 4.0 / 3.0, 7.0 / 5.0, 3.0 / 2.0,
                8.0 / 5.0, 5.0 / 3.0, 16.0 / 9.0, 15.0 / 8.0
        };

        // creating GuitarString
        GuitarString[] string = new GuitarString[length];

        // the first 12 guitarstrings will have harmonious ratios
        for (int i = 0; i < length; i++) {
            // correcting the ratio
            double correctedRatio =
                    harmony[i % 12] * Math.pow(2, Math.floor((i + 0.0) / 12.0));

            // creating guitarstring using corrected ratio
            string[i] = new GuitarString(110.0 * (correctedRatio));
        }
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
