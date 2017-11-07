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

    def train(self, input, output):
        self.think(input)

    def think(self, input):
        for neuron, weight in zip(self.layers[0], input):
            neuron.setActivation(weight)
        for i in range(1, len(self.layers)):
            for neuron in self.layers[i]:
                weightSum = 0
                for prevNeuron, weight in zip(self.layers[i-1], self.weights[i-1]):
                   weightSum += prevNeuron.getActivation() * weight
                neuron.setActivation(self.sigmoid(weightSum + neuron.getBias()))

    def backpropacation(self, output):
        revLayers = reversed(self.layers)
        for layer in reversed(self.layers):
            for neuron in layer:




    def sigmoidDerivative(self, x):
        return e**x/(e**x + 1)**2

    def sigmoid(self, x):
        return 1/(1+e**(-x))

