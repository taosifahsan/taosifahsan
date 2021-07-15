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

Programming Assignment 8: Traveling Salesperson Problem

Hours to complete assignment (optional): 5


/**********************************************************************
 *  Explain how you implemented the nearest insertion heuristic.      *
 **********************************************************************/
At first we took care of the the null case. then we figured out the right
spot to enter the point. To do that we created a loop which traversed the
nodeand constantly calculated the distance from that point to other points.
If the distance was lower then we changed a temporary point object to
the closest point till that loop. After that we inserted the the point
after the closest point using insert function. insert function basically
works like this: it runs through the entire loop for a point and adds desired
point after that if the forst point is found.


/**********************************************************************
 *  Explain how you implemented the smallest insertion heuristic.     *
 *  It's sufficient to list only the differences between this         *
 *  heuristic and the nearest insertion heuristic.                    *
 **********************************************************************/
At first we took care of the the null case. then we figured out the right
spot to enter the point. To do that we created a loop which traversed the
nodeand constantly calculated the distance from that point to other points.
If the increase after the addition of the point was lower then we changed
a temporary point object to the closest point till that loop. After that we
inserted the the point after the closest point using insert function.
insert function basicallyworks like this: it runs through the entire loop
for a point and adds desired point after that if the firstly mentioned point
is found.

to figure out the increase of length we used this formula:
dl =  l(1,p)+l(p,2)-l(1,2)

/**********************************************************************
 *  Explain why it's better to use a circularly linked list instead   *
 *  of an array.                                                      *
 **********************************************************************/
1. Memory is minimum when node is used
2. Flexible

/**********************************************************************
 *  Fill in the lengths computed by your heuristics.                  *
 **********************************************************************/

data file      nearest neighbor     smallest increase
-----------------------------------------------------
tsp10.txt         1566.1363             1655.7462
tsp100.txt        7389.9297             4887.2190
tsp1000.txt      27868.7106            17265.6282
usa13509.txt     77449.9794            45074.7769

/**********************************************************************
 *  Do two timing analyses. Estimate the running time (in seconds)    *
 *  of each heuristic as a function of n, using expressions of the    *
 *  form: a * n^b, where b is an integer.                             *
 *                                                                    *
 *  Explain how you determined each of your answers.                  *
 *                                                                    *
 *  To get your data points, run the two heuristics for n = 1,000,    *
 *  and repeatedly double n until the execution time exceeds 60       *
 *  seconds.                                                          *
 *                                                                    *
 *  You may use TSPTimer to help do this, as per the checklist.       *
 *  If you do so, execute it with the -Xint option. This turns off    *
 *  various compiler optimizations, which helps normalize and         *
 *  stabilize the timing data that you collect.                       *
 *                                                                    *
 *  (If n = 1,000 takes over 60 seconds, your code is too slow.       *
 *  See the checklist for a suggestion on how to fix it.)             *
 **********************************************************************/

n               nearest time           smallest time
------------------------------------------------------------
 1000            0.150                   0.349
 2000            0.585                   1.377
 4000            2.419                   5.789
 8000            9.532                  22.317
16000           37.356                  87.996

Assuming the t vs n follows t=a*n^b pattern, we took log(t) =b * log(n)+log(a).
we plotted log(t) vs log(n) on geogebra and found out that it follows an linear
pattern. We calculated the slopes and y-intercept and figured out b and log(a)
(hence a). Here it should be mentioned that log is base 2.

(in both cases regression, r=0.999.., so the evidence of a*n^b is strong)

for nearest time,
 a = 1.55 e -7
 b = 1.99... = 2
 so, t=1.55e-7*n^2

for smallest time,
a = 3.56 e -7
b = 1.99... = 2
so, t= 3.56 e -7 n^2;


/**********************************************************************
 *  Did you receive help from classmates, past COS 126 students, or
 *  anyone else? If so, please list their names.  ("A Sunday lab TA"
 *  or "Office hours on Thursday" is ok if you don't know their name.)
 **********************************************************************/

Yes or no?
no


/**********************************************************************
 *  Did you encounter any serious problems? If so, please describe.
 **********************************************************************/

Yes or no?
no

/**********************************************************************
 *  List any other comments here.
 **********************************************************************/
