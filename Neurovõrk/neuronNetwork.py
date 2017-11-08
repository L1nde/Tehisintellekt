import random
from copy import deepcopy
from math import e

class Neuron:

    def __init__(self):
        self.activation = 0
        self.bias = random.randrange(-100, 100)/100

    def setBias(self, bias):
        self.bias = bias

    def getBias(self):
        return self.bias

    def setActivation(self, weight):
        self.activation = weight

    def getActivation(self):
        return self.activation

class Brain:
    def __init__(self,inputCount, outputCount, hiddenLayersCount=2, hiddenLayersNeurons=8):
        self.weights = []
        self.layers = []
        self.hiddenLayersCount = hiddenLayersCount
        self.hiddenLayersNeurons = hiddenLayersNeurons
        neurons = []
        # input layer neurons
        for _ in range(inputCount):
            neurons.append(Neuron())
        self.layers.append(neurons)

        # hidden layer neurons
        for _ in range(hiddenLayersCount):
            neurons = []
            for _ in range(hiddenLayersNeurons):
                neurons.append(Neuron())
            self.layers.append(neurons)

        # output layer neurons
        neurons = []
        for _ in range(outputCount):
            neurons.append(Neuron())
        self.layers.append(neurons)

        # weights between input and first hidden
        layerWeights = []
        for _ in range(inputCount*hiddenLayersNeurons):
            layerWeights.append(random.randrange(-100, 100)/100)
        self.weights.append(layerWeights)
        # weights between hidden layers

        for _ in range(hiddenLayersCount - 1):
            layerWeights  = []
            for _ in range(hiddenLayersNeurons*hiddenLayersNeurons):
                layerWeights.append(random.randrange(-100, 100)/100)
            self.weights.append(layerWeights)

        # weights between output and and last hidden
        layerWeights = []
        for _ in range(outputCount*hiddenLayersNeurons):
            layerWeights.append(random.randrange(-100, 100)/100)
        self.weights.append(layerWeights)

    def train(self, input, target):
        self.think(input)
        self.backpropacation(target)

    def think(self, input):
        for neuron, weight in zip(self.layers[0], input):
            neuron.setActivation(weight)
        for i in range(1, len(self.layers)):
            for neuron in self.layers[i]:
                weightSum = 0
                for prevNeuron, weight in zip(self.layers[i-1], self.weights[i-1]):
                   weightSum += prevNeuron.getActivation() * weight
                neuron.setActivation(self.sigmoid(weightSum + neuron.getBias()))

    def backpropacation(self, target):
        newWeights = []
        newWeights.append([])
        for _ in range(self.hiddenLayersCount):
            newWeights.append([])
        counter = 0
        for i in reversed(range(len(self.layers))):
            curLayer = self.layers[i]
            prevLayer = self.layers[i-1]
            for neuron in curLayer:
                for prevNeuron in prevLayer:
                    change = prevNeuron.getActivation()*self.totalErrorDerivative(target[i], i)*self.sigmoidDerivative(neuron.getActivation())
                    newWeights[i].append(self.weights[i][counter] - change)
            counter += 1
        return newWeights



    def totalError(self, target):
        sum = 0
        for i in range(len(self.layers[-1])):
            sum += (target[i] - self.layers[-1][i])**2 # Can be divided by 2
        return sum

    def totalErrorDerivative(self, target, index):
        return self.layers[-1][index].getActivation() - target

    def sigmoidDerivative(self, x):
        # return e**x/(e**x + 1)**2
        return x*(1-x)

    def sigmoid(self, x):
        return 1/(1+e**(-x))

