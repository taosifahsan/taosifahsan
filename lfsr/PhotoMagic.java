/* *****************************************************************************
 *  Name:    Taosif Ahsan
 *  NetID:   tahsan
 *  Precept: P13
 *
 *  Description:  decodes and encodes pictures using lfsr method
 *
 **************************************************************************** */

import java.awt.Color;

public class PhotoMagic {

    /* returns a transformed copy of the specified picture,using the specified
       lfsr.                                                                  */
    public static Picture transform(Picture picture, LFSR lfsr) {

        // measuring height and width of the picture
        int height = picture.height();
        int width = picture.width();

        // declaring variables
        int red, green, blue, rednew, greennew, bluenew, key;

        // creating a copy of the picture with same height and width
        Picture target = new Picture(width, height);

        // creating new picture using nested loop
        for (int col = 0; col < width; col++)
            for (int row = 0; row < height; row++) {

                // getting the color value of the pixel
                Color color = picture.get(col, row);

                // getting the value of red, green and blue from color value
                red = color.getRed();
                green = color.getGreen();
                blue = color.getBlue();
                // creating the key and changing the color of the pixel
                key = lfsr.generate(8);
                rednew = red ^ key;
                key = lfsr.generate(8);
                greennew = green ^ key;
                key = lfsr.generate(8);
                bluenew = blue ^ key;

                // creating new  color
                Color colornew = new Color(rednew, greennew, bluenew);

                // assigning the color to the pixel of the new picture
                target.set(col, row, colornew);
            }

        //
        return target;
    }

    /* takes the name of an image file and a description of an lfsr a
       command-line arguments;                                                */

    // displays a copy of the image that is "encrypted" using the LFSR.
    public static void main(String[] args) {

        // taking the inputs
        Picture picture = new Picture(args[0]);
        String seed = args[1];
        int tap = Integer.parseInt(args[2]);

        // creating the lfsr
        LFSR lfsr = new LFSR(seed, tap);

        // creating a new copy of the picture and transforming it
        Picture transformed = transform(picture, lfsr);

        // showing the picture
        transformed.show();
    }
}
