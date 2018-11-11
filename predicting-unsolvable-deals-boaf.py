#Predicting unsolvable deals in BoaF

import itertools
from BirdsOfAFeatherNode import BirdsOfAFeatherNode
from search import depth_first_search_no_repeats, reset_depth_first_search_no_repeats
from Card import STR_CARD_DICT
import numpy as np
from sympy import *


def test():
	#Both odd bird unsolvable deals and separated flocks are lumped into one group
	#These deals have a spanning tree count of zero and are therefore unsolvable.
    OBUD_SFUD = []
    #Full-flock unsolvable deal are stored here. FFUDs are deals that have a 
    #connected graph but are nonetheless unsolvable.
    FFUD = []
    
    start_seed = int(input('Start seed? '))
    num_seeds = int(input('How many seeds? '))
    for k in range(start_seed, start_seed + num_seeds):
        print("On node: " + str(k))
        node = BirdsOfAFeatherNode.create_initial(k)
        
        grid_cards = list(itertools.chain(*node.grid))
        card_list = list(filter(None.__ne__, grid_cards))
    
        #Create the 16x16 adjacency matrix
        a = np.zeros((16,16)); #
        num_cards = len(card_list)
        found_pair = False
        pair_count = 0;

		#Fill the 16x16 adjacency matrix
        for i in range(num_cards - 1):
            for j in range(i + 1, num_cards):
                card1 = card_list[i]
               
                card2 = card_list[j]
               
                if ((card1.get_suit() is card2.get_suit())
                        or (abs(card1.get_rank() - card2.get_rank()) <= 1)):
                    found_pair = True
                    pair_count = pair_count + 1
                    a[i,j] = 1
                    a[j,i] = 1
 
        
        #Contruct the degree matrix
        d = np.zeros((16,16))
        sum_ = a.sum(axis=1)
        for i in range(16):
            d[i,i] = sum_[i]
        
        #The laplacian matrix is equal to the adjacency matrix subtracted
        #from the degree matrix
        laplace = d - a
        #Use Kirchoff's tree theorem to find the number of spanning trees 
        #First eliminate the first row and column
        reduced_laplace = laplace[1:,1:]
        reduced_laplace = Matrix(reduced_laplace)
        #The number of spanning trees is just the cofactor, which is the 
        #determinant of the reduced laplacian matrix
        cofactor = reduced_laplace.det()
   
		#Finding number of zeros in the squared adjacency matrix
        a_square = np.matmul(a,a)
        nw_2 = 0
        for i in range(16):
            for j in range(16):
                if a_square[i,j] == 0:
                    nw_2 += 1
        
        nw_1 = 120 - pair_count
        
        #the sympy matrix determinant method sometimes outputs a small 
        #positive value when it should output 0
        if cofactor < 1: 
            cofactor = 0
        
        if cofactor == 0:
            OBUD_SFUD.append(k)
            continue
            
        elif nw_1 >= 76 and nw_2 >= 74:
            FFUD.append(k)

    print()
    print("--------------Prediction Results--------------")
    print()
    solvable_deals = num_seeds - len(OBUD_SFUD)- len(FFUD)
    print("The predicted number of solvable deals is: " + str(solvable_deals))
    print()
    print("Found " + str(len(OBUD_SFUD)) + " OBUDs and SFUDs: ")
    print("The OBUDs or SFUDs in the searched set are:")
    print(OBUD_SFUD)
    print()
    print("Found " + str(len(FFUD)) + " FFUDs: ")
    print("The predicted FFUDs in the searched set are:")
    print(FFUD)
    print()


if __name__ == '__main__':
    test()
