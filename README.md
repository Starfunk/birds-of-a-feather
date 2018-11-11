# birds-of-a-feather
An algorithm predicting unsolvable deals in the Birds of a Feather solitaire game. 

This algorithm was the main research result of the paper: Predicting Unsolvable Deals in the Birds of a Feather Solitaire Game, which can be found at: http://maximiliankahn.com/Documents/Predicting%20Unsolvable%20Deals%20in%20the%20Birds%20of%20a%20Feather%20Solitaire%20Game.pdf

In order to run the prediction algorithm download the repo and then run predicting-unsolvable-deals-boaf.py.

You can generate new boaf data by running generating-boaf-deals.py which records the nw_1, nw_2, and spanning tree values of each deal for as many deals as you specify. The program saves the results in a CSV file.

You can confirm our results by running the decision tree algorithm: finding-boaf-weights.py, on trainingdata.csv (70000 deals). You can test the algorithm on testingdata.csv (30000 deals).

The BoaF program was originally created by Todd Neller and can be found at: http://cs.gettysburg.edu/~tneller/puzzles/boaf/index.html.
