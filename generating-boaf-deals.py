#Generating deals in BOAF and recording their properties in a spreadsheet
import itertools
from BirdsOfAFeatherNode import BirdsOfAFeatherNode
from search import depth_first_search_no_repeats, reset_depth_first_search_no_repeats
from Card import STR_CARD_DICT
import numpy as np
from sympy import *


def generatedeals():
    big_array = np.zeros(shape=(100000,5)) #initialize 100k by 5 matrix
    
    #Note: the first deal is randomized.
    start_seed = int(input('Start seed? '))
    num_seeds = int(input('How many seeds? '))
    for k in range(start_seed, start_seed + num_seeds):
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
        
		#Finding NW2 - i.e. the number of zeros in A^2
        a_square = np.matmul(a,a)
        
        zeros = 0
        for i in range(16):
            for j in range(16):
                if a_square[i,j] == 0 and i < j:
                    zeros += 1
        big_array[k][0] = k
        big_array[k][1] = pair_count
        big_array[k][2] = zeros
        big_array[k][3] = cofactor
        
        if cofactor <= 1: #for some reason Python sometimes has the cofactor as a very small value rather than just outputting 0.
            cofactor = 0
        if cofactor == 0:
            big_array[k][4] = 1
        else:
            big_array[k][4] = 0

    np.savetxt("100k-boaf-deals.csv", big_array, delimiter=",")

if __name__ == '__main__':
    generatedeals()
