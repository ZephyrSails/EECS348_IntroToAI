After we step into a room:

TRUTH:
1.  4 * 4
2.  square  =>  Map
3.  ? DFS


1.  Possible action:
  1.  Move:
    1.  up
    2.  down
    3.  left
    4.  right
  2.  Shot: Scream or Not?
    1.  up
    2.  down
    3.  left
    4.  right
2.  Possible situation:
  1.  Smell?    at least 1 Dangerous in at most 3 direction
    1.  Counter:  # Mark the potential Wumpus
                  Mark no pits
  2.  Breeze?   at least 1 Dangerous in at most 3 direction
    1.  Counter:  # Mark the potential pit
                  Mark no Wumpus
  3.  Smell + Breeze? at least 2 Dangerous in at most 3 direction
    1.  Counter:  No mark, don't be stupid
  4.  Nothing
    1.  Counter:  # Mark the safe area
                  Mark no Wumpus
                  Mark no Pits
2.  Mark:
  <!-- 0.  Safe
  1.  Possible Wumpus
  2.  Possible Pit
  3.  Possible Both (only happen when both Breeze and Smell) -->
  4.  No Wumpus
  5.  No Pit

A => B, ~B        ~A
