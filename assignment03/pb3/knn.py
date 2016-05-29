from __future__ import division
import sys
import numpy as np

def readData(filename):
	dataFile = open(filename, 'r')
	line = dataFile.readline()
	specs = map(int, line.split())
	data = np.genfromtxt(dataFile)
	dataFile.close()
	return (data, specs)

def calcDist(rowDataVector, trainingData, row, dimensions):
	result = np.zeros([1,3])
	result[0,0] = 100
	result[0,1] = sys.maxint
	result[0,2] = 100
	xAmount=0
	for x in range(0, row):
		tmp = np.zeros((1,3))
		tmp[0,0] = x
		tmp[0,2] = trainingData[x,dimensions]
		# Euclidian Distance
		sum = 0
		for y in range(0, dimensions):
			sum += (trainingData[x,y]-rowDataVector[y])**2
		tmp[0,1] = sum**(0.5)
		counter = 0
		while(((tmp[0,1]>result[counter,1]) or ((tmp[0,1]==result[counter,1]) and tmp[0,2]>result[counter,2])) and (counter<xAmount)):
			counter = counter+1
		xAmount = xAmount+1
		result = np.insert(result, counter, tmp, 0)
	result = np.delete(result, xAmount, 0)
	return result

def findMost(lst, k):
	tmp = [0] * 10000
	for x in range(0,k):
		category = int(lst[x])
		tmp[category] = tmp[category]+1
	solution = [0] * 1000
	amountOverZero = 0
	maxNum = -1
	for x in range(0, 10000):
		if (tmp[x]>maxNum):
			maxNum = tmp[x]
			amountOverZero = 0
			solution[amountOverZero] = x
		elif(tmp[x]==maxNum):
			amountOverZero = amountOverZero+1
			solution[amountOverZero] = x
	return solution, amountOverZero

def findSmall(distanceMatrix, classifier, k):
	smallestDist = 100000
	for x in range(0,k):
		if distanceMatrix[x,2]==classifier:
			if distanceMatrix[x,1]<smallestDist:
				smallestDist = distanceMatrix[x,1]
	return smallestDist

def findIndex(array, k):
	index = 0
	smallest = 100000
	for i in range (0,k):
		if (array[i]<smallest):
			smallest = array[i]
			index = i
	return index

if __name__ == "__main__":

	# error testing
	if len(sys.argv) != 4:
		print "Received wrong number of arguments.\nUsage: \'python knn.py k train.txt test.txt\'"
		sys.exit()

	k = int(sys.argv[1])
	training_file = sys.argv[2]
	testing_file = sys.argv[3]

	training_data, training_specs = readData(training_file)
	testing_data, testing_specs = readData(testing_file)
	if (int(k)>int(training_specs[0])):
		print "Value of k is greater than training data give. Please select a lower value of k or switch a training data"
		sys.exit()

	# main program
	for x in range(0, testing_specs[0]):
		distanceMatrix = calcDist(testing_data[x], training_data, training_specs[0], training_specs[1]) # [Original Index, Distance, Class]
		print(str(x+1) + ".  "),
		for y in range(0, training_specs[1]):
			print (testing_data[x,y]),
		print("--"),
		totalK = [0] * k
		for z in range(0,k):
			totalK[z] = distanceMatrix[z,2]
		solutionArray, amountOverZero = findMost(totalK, k)
		if (amountOverZero==0):
			print int(solutionArray[0])
		else:
			smallestElements = [0] * (int(amountOverZero)+1)
			for q in range(0,amountOverZero+1):
				smallestElements[q] = findSmall(distanceMatrix,solutionArray[q],k)
			indexOfSmallest = findIndex(smallestElements, amountOverZero+1)
			print solutionArray[indexOfSmallest]
