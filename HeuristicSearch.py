import itertools
from BirdsOfAFeatherNode import BirdsOfAFeatherNode
from search import depth_first_search_no_repeats, reset_depth_first_search_no_repeats
from Card import STR_CARD_DICT
import numpy as np
from sympy import *

def heuristic_search():
    #Both odd bird unsolvable deals and separated flocks are lumped into one group
    OBUD_SFUD = []
    #Full-flock unsolvable deal are stored here
    FFUD = []
    
    avg_pair_count = 0
    avg_determinant = 0
    avg_zeros = 0
    
    start_seed = int(input('Start seed? '))
    num_seeds = int(input('How many seeds? '))
    for k in range(start_seed, start_seed + num_seeds):
        print("FOR NODE: " + str(k))
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
        zero = 0
        for i in range(16):
            for j in range(16):
                if a_square[i,j] == 0:
                    zero += 1
        print("The number of zeros is: " + str(zero))
        
        #Calculating the determinant
        a = Matrix(a)
        det = abs(a.det())
        
        print("The det = " + str(det))
        print('The number  of pairs is: ' + str(pair_count))
        print()
        
        if cofactor == 0:
            OBUD_SFUD.append(k)
            continue
            
        elif det <= 100 and pair_count < 46 and zero > 70:
            FFUD.append(k)
            
        avg_pair_count = avg_pair_count + abs(pair_count)
        avg_determinant = avg_determinant + abs(det)
        avg_zeros = avg_zeros + abs(zero)
        
    avg_pair_count = avg_pair_count / num_seeds
    avg_determinant = avg_determinant / num_seeds
    avg_zeros = avg_zeros / num_seeds
    
    print("---------------Search Completed---------------")
    print()
    print("The number of OBUDs and SFUDs is: " + str(len(OBUD_SFUD)))
    print(OBUD_SFUD)
    print("The number of FFUDs is: " + str(len(FFUD)))
    print(FFUD)
    print()
    print("The average pair count is: " + str(avg_pair_count))
    print("The average determinant is: " + str(avg_determinant))
    print("The average zeros is: " + str(avg_zeros))

if __name__ == '__main__':
    heuristic_search()
