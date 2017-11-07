import random
from copy import deepcopy
from math import e

class Neuron:

    def __init__(self):
        self.node = 0
        self.bias = random.randrange(-100, 100)/100

    def setBias(self, bias):
        self.bias = bias

    def getBias(self):
        return self.bias

    def setNode(self, weight):
        self.node = weight

    def getNode(self):
        return self.node

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
            neuron.setNode(weight)
        for i in range(1, len(self.layers)):
            for neuron in self.layers[i]:
                weightSum = 0
                for prevNeuron, weight in zip(self.layers[i-1], self.weights[i-1]):
                    weightSum += prevNeuron.getNode() * weight
                neuron.setNode(self.sigmoid(weightSum + neuron.getBias()))

    def backpropacation(self, output):
        for i in range(-1, -len(self.layers), -1):
            for neuron in self.layers[i]:
                for prevNeuron in self.layers[i-1]:
                    newWeight = 2*(neuron.getNode() - output



    def sigmoid(self, x):
        return 1/(1+e**(-x))

