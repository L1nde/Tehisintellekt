from Neurovõrk.neuronNetwork import Brain

b = Brain(5, 2)
b.train([1,2,3,4,5], [1,0,1,0,1])
print("Cool")