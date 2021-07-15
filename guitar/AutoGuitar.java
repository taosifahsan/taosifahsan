/* *****************************************************************************
 *  Name:            Taosif Ahsan
 *  NetID:           tahsan
 *  Precept:
 *
 *  Partner Name:    Declan Farmer
 *  Partner NetID:   dfarmer
 *  Partner Precept: P13javac
 *
 *  Description:  Plays a music automatically
 *
 **************************************************************************** */

public class AutoGuitar {
    public static void main(String[] args) {

        // creating the keyboard representation of keys
        String keyboard = "q2we4r5ty7u8i9op-[=zxdcfvgbnjmk,.;/' ";
        int length = keyboard.length();

        // actual music where 1 represents pause
        // We created this ourselves!
        String music = "u1i1p1u1i1p1u1i1p1u1i1p1r1u1i1p1u1i1p1u1i1p1t1u1i1p1u1i"
                + "1p1u1i1p1y1u1i1p1u1i1p1u1i1p1u1u1i1p1u1i1p1u1i1p1i1u1"
                + "i1p1u1i1p1u1i1p1o1u1i1p1u1i1p1u1i1p1p11111y1u1o1p1y1u"
                + "1o1p1y1u1o1p1u1i1p1[1u1i1p1[1y1u1o1p1y111u111o111p111"
                + "y111u111o111p111u111i111p111[111y111u111o111p1111111y"
                + "1u1o1p11111y11111u11111o11111p11111";

        // twinkle twinkle little star is saved in the comment
        // "nn//  /1..,,mmn1//..,,m1//..,,m1nn//  /1..,,mmn1";

        // speed variable
        int speed = 5000;

        // time variable
        int call = 2 * speed * music.length();

        // creating empty tones to slow down the music
        StringBuilder tone = new StringBuilder();
        for (int i = 0; i < music.length(); i++) {
            tone.append(music.charAt(i));
            for (int j = 0; j < speed; j++) {
                tone.append("1");
            }
        }
        music = tone.toString();

        // Create 37 guitar strings, for concerts
        GuitarString[] string = new GuitarString[length];
        for (int i = 0; i < length; i++)
            string[i] = new GuitarString(110 * Math.pow(2, i / 12.0));


        // the main input loop
        for (int i = 0; i < call; i++) {

            // check if the next tone in music is audible, and, if so,
            // process it
            char key = music.charAt(i % music.length());
            String a = Character.toString(key);
            if (keyboard.contains(a)) {
                int index = keyboard.indexOf(key);
                // pluck the corresponding string
                string[index].pluck();
            }

            // compute the superposition of the samples
            double sample = 0;
            for (int k = 0; k < length; k++) sample += string[k].sample();

            // send the result to standard audio
            StdAudio.play(sample);

            // advance the simulation of each guitar string by one step
            for (int k = 0; k < length; k++) string[k].tic();

        }
    }
}
