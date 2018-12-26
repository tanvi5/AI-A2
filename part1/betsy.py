#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 14:09:27 2018

We have referred following website for implementing timeout functionality
https://dreamix.eu/blog/webothers/timeout-function-in-python-3
@author: tanvi
"""
#minimax with evaluation function

import sys


from threading import Thread, Event
import random
stop_event = Event()

'''
Evaluation function returns number of open rows,columns,diagonals for maxplayer -  number of open rows,columns,diagonals for minplayer 
'''
def evaluation_fun(board):
        col_count_opposite = sum([1 if (sum( [1 if board[row][col]<>MinPlayer else 0 for row in range(3,N+3) ] )) == N else 0 for col in range(N)])
        row_count_opposite = sum([1 if (sum( [1 if board[row][col]<>MinPlayer else 0 for col in range(N) ] )) == N else 0 for row in range(3,N+3)])
        diag_lr_count_opposite = sum([1 if sum( [1 if board[index+3][index]<>MinPlayer else 0 for index in range(N) ]) == N else 0])
        diag_rl_count_opposite = sum([1 if sum( [1 if board[index+3][N - index - 1]<>MinPlayer else 0 for index in range(N) ]) == N else 0])
        col_count = sum([1 if (sum( [1 if board[row][col]<>MaxPlayer else 0 for row in range(3,N+3) ] )) == N else 0 for col in range(N)])
        row_count = sum([1 if (sum( [1 if board[row][col]<>MaxPlayer else 0 for col in range(N) ] )) == N else 0 for row in range(3,N+3)])
        diag_lr_count = sum([1 if sum( [1 if board[index+3][index]<>MaxPlayer else 0 for index in range(N) ]) == N else 0])
        diag_rl_count = sum([1 if sum( [1 if board[index+3][N - index - 1]<>MaxPlayer else 0 for index in range(N) ]) == N else 0])
        
        return (row_count_opposite+col_count_opposite+diag_lr_count_opposite+diag_rl_count_opposite) - (row_count+col_count+diag_rl_count+diag_lr_count)
'''
Counts total number of pieces of player on the board
'''
def total_pieces(board,player):
    return sum([count_on_row(board, col, player) for col in range(N+3)])
    
'''
Rotates column passed in function where row demotes number of rows in that column
'''
def rotate_col(board,col,row):
    newboard = []
    for x in range(row-1):
        newboard.append(board[x][:col] + [board[x+1][col]] + board[x][col+1:] )
    newboard.append(board[row-1][:col] + [board[0][col]] + board[row-1][col+1:])
    for newRow in board[row:]:
        newboard.append(newRow)
    return newboard

'''
Count number of pieces of player in row
'''
def count_on_row(board, row,player):
    return sum( [1 if board[row][col]==player else 0 for col in range(N)] ) 

'''
Count number of pieces of player in given column
'''
def count_on_col(board, col, player):
    return sum( [1 if board[row][col]==player else 0 for row in range(3,N+3) ]) 

'''
Counts number of pieces of player in diagonal starting from top left corner
'''
def count_on_diag_lr(board, player):
    return sum([1 if sum( [1 if board[index+3][index]==player else 0 for index in range(N) ]) == N else 0])

'''
Counts number of pieces of player in diagonal starting from right left corner
'''
def count_on_diag_rl(board, player):
    return sum([1 if sum( [1 if board[index+3][N - index - 1]==player else 0 for index in range(N) ]) == N else 0])

'''
Return successors with moves
'''
def succesors2(board):
    setOfSuccessors = []
    for col in range(N):
        row = no_of_elements_in_col(col,board)
        if row < (N+3) and total_pieces(board,MaxPlayer)<(N*(N+3)/2):
            setOfSuccessors.append((board[0:row] + [board[row][0:col] + [MaxPlayer,] + board[row][col+1:]] + board[row+1:],str((col+1))))
        if row > 1:
            setOfSuccessors.append((rotate_col(board,col,row),'-'+str((col+1))))
            
    return setOfSuccessors

'''
Return successors without moves
'''
def succesors(board,Player):
    setOfSuccessors = []
    for col in range(N):
        row = no_of_elements_in_col(col,board)
        if row < (N+3) and total_pieces(board,MaxPlayer)<(N*(N+3)/2):
            setOfSuccessors.append(board[0:row] + [board[row][0:col] + [Player,] + board[row][col+1:]] + board[row+1:])
        if row > 1:
            setOfSuccessors.append(rotate_col(board,col,row))
            
    return setOfSuccessors

'''
Returns total number of elements in column
'''
def no_of_elements_in_col(col,board):
    return sum([1 if row[col]!=0 else 0 for row in board])
    
'''
Check is player given as input to funtion won
'''
def checkIfPlayerWon(Board,player):
    for r in range(3,N+3):
        if count_on_row(Board, r, player) == N:
            return True
    for c in range(N):
        if count_on_col(Board, c, player) == N:
            return True
    if count_on_diag_rl(Board,player) == N:
        return True
    if count_on_diag_lr(Board,player) == N:
        return True
    return False
    

'''
Find best move using iterative deepening search
'''
def minimax_decision(S):
    allSuccessors = succesors2(S)
    max_till_now = -10
    allSuccessorsWithCost = []
    k = 2
    max_move = allSuccessors[0][1]
    maxSuccessor = allSuccessors[0][0]
    while k<max_depth:
        
        allSuccessorsWithCost = [] 
        max_till_now = -10
        for succesor in allSuccessors:
            currentDepth=0
            current_node = min_values(succesor[0],currentDepth,-10,10,k)
            allSuccessorsWithCost.append([current_node[0],succesor[0],succesor[1]])
            if current_node[0] == 10:
                print succesor[1], printable_board(succesor[0])
                return
            if current_node[0] > max_till_now:
                max_till_now = current_node[0]
		max_move = succesor[1]
            	maxSuccessor = succesor[0]
	indices = [i for i, x in enumerate(allSuccessorsWithCost) if x[0] == max_till_now]#This list is used to store all successors having same cost
	selected_index = random.randrange(len(indices))					#To choose a random successor having max value
        print allSuccessorsWithCost[indices[selected_index]][2], printable_board(allSuccessorsWithCost[indices[selected_index]][1])
	#print max_move, printable_board(maxSuccessor)
	if stop_event.is_set():
            break
        k+=1
    

'''
Return min values
'''
def min_values(S, currentDepth,alpha,beta,k):
    currentDepth+=1
    if k <= currentDepth:
        return (evaluation_fun(S),S)
    if checkIfPlayerWon(S,MaxPlayer):
        return (10,S)
    elif checkIfPlayerWon(S,MinPlayer):
        return (-10,S)
    else:
        for succesor in succesors(S,MinPlayer):
            beta = min(beta,max_values(succesor,currentDepth,alpha,beta,k)[0])
            if alpha >= beta:
                return (beta,S) 
        return (beta,S)
    
'''
Return max values
'''
def max_values(S,currentDepth,alpha,beta,k):
    currentDepth+=1
    if k <= currentDepth:
        return (evaluation_fun(S),S)
    if checkIfPlayerWon(S,MaxPlayer):
        return (10,S)
    elif checkIfPlayerWon(S,MinPlayer):
        return (-10,S)
    else:
        for succesor in succesors(S,MaxPlayer):
            alpha = max(alpha,min_values(succesor,currentDepth,alpha,beta,k)[0])
            if alpha >= beta:
                return (alpha,S)
        return (alpha,S)
    
'''
Convert board's format from list to string
'''
def printable_board(board):
    #print "\n".join([ " ".join([ board[row][col] if board[row][col] else "." for col in range(N) ])[::-1] for row in range(N+3)])[::-1]
    return "".join([ "".join([ board[row][col] if board[row][col] else "." for col in range(N) ])[::-1] for row in range(N+3)])[::-1]
   # print 'board_to_print', board_to_print   
    
'''
Convert board's format from string to list
'''
def convertBoardToList(inputBoard):
    board = []
    c = 0
    row = []
    for char in inp:
        if c<N:
            row.append(0 if char == '.' else char)
            c+=1
        else:
            board.insert(0,row)
            c = 1
            row = [0 if char == '.' else char]
    board.insert(0,row)
    return board

N = int(sys.argv[1]) 
max_depth = 20   
MaxPlayer = sys.argv[2]
MinPlayer = {'x':'o','o':'x'}[MaxPlayer]
inp = sys.argv[3]
initial_board = convertBoardToList(inp)
p = Thread(target=minimax_decision,args=(initial_board,))
p.start()

p.join(int(sys.argv[4]))

stop_event.set()



