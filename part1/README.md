# a2

For Betsy, we have implemented alpha beta pruning with iterative deepening search.

Evaluation function: (number of open rows,columns,diagonals for maxplayer) -  (number of open rows,columns,diagonals for minplayer)

Successor Function: It returns all successors for current board including +- 1 to n.

The minmax_decision function returns best possible result. If there is a tie amongst multiple moves, it returns random move out of all moves having max value
