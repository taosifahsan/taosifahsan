/* *****************************************************************************
 *  Name:              Taosif Ahsan
 *  NetID:             tahsan
 *  Precept:           P13
 *
 *  Partner Name:      Declan Farmer
 *  Partner NetID:     dfarmer
 *  Partner Precept:   P13
 **************************************************************************** */

Which partner is submitting the program files? Taosif Ahsan

Programming Assignment 7: Markov Model

Hours to complete assignment (optional): 4

/**********************************************************************
 * Describe the type parameters of your symbol table (i.e., what is   *
 * the key type and what is the value type). How did you use the      *
 * symbol table to implement the random() method.                     *
 **********************************************************************/
type parametre of the first symbol table:
String as key to store the kgrams, Integer as value to store the
frequency of tha kgram

type parametre of the second symbol table:
String as key to store the kgrams, int[] as array to store th frecuency
of each character.

We used StdRandom.discreet(int[]  frequencies) to generate a character
With the required probability. The frequency of appearance was stored
in STD<String, int[]> sb2. int letters[128] was used to hold the number
of appearance of individual letters. It was later called and used to
generate a character.

**********************************************************************
 * The main() method we provide in the checklist does not test your   *
 * random() method. Describe how you tested it.                       *
 **********************************************************************/
We created an simple string abcabdabe. So, 'c','d' and 'e' appears after
ab exactly onece. So the probablity distribution should be {0.333, 0.333,
0.333}. We created an array int x[3] to hold the number of appearences of
'c','d' and 'e'. We ran the random loop m=100000 times and incremented
x[i] by 1 when certain characters appeared. Then we printed out 3*x[i]/m
to get the average frequency of each characters. Thery came out to be
around {1, 1, 1} as expected.

/**********************************************************************
 * Paste two of your favorite, not too long, output fragments here.   *
 * In addition to the pseudo-random text, indicate the order of your  *
 * model and what text file you used.                                 *
 **********************************************************************/
The first one felt weird

 order 5, trump-clinton1.txt

 why did college at -- well prisons are them ended over to build never
 get rid of skills, you in from China, Iran, they don't every surprised.

The second one is included for its accuracy and well...it's beatles!

order 100, beatles.txt

 Sounds of laughter shades of life are ringing Through my open mind inciting and
inviting me. Limitless undying love which shines around me like a million suns,
And calls me on and on across the universe Jai guru deva om Nothing's gonna
change my world Not

/**********************************************************************
 *  Did you receive help from classmates, past COS 126 students, or
 *  anyone else? If so, please list their names.  ("A Sunday lab TA"
 *  or "Office hours on Thursday" is ok if you don't know their name.)
 **********************************************************************/

Yes or no?

No

/**********************************************************************
 *  Did you encounter any serious problems? If so, please describe.
 **********************************************************************/

Yes or no?

No



/**********************************************************************
 *  List any other comments here.                                     *
 **********************************************************************/
