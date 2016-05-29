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

def calculateCentroid(data, specs):
	dimensions = specs[1]
	dataAmount = specs[0]
	centroidData = np.zeros((1, specs[1]))
	for x in range(0, dimensions):
		for y in range (0, dataAmount):
			centroidData[0,x] += data[y,x]
	for x in range(0, dimensions):
		centroidData[0,x] /= dataAmount
	return centroidData

def calcCov(data, specs, centroid):
	k = specs[0]
	dimensions = specs[1]
	data = np.asmatrix(data)
	for x in range(0, k):
		data[x] -= centroid
	result = data.getT() * data
	result = (1/k)*result
	return result

def calcDist(data, specs):
	result = np.ones((specs[0],1))
	for x in range(0, specs[0]):
		singleData = data[x]

if __name__ == "__main__":

	if len(sys.argv) != 3:
		print "Received wrong number of arguments.\nUsage: \'python mahadist.py train.txt test.txt\'"
		sys.exit()

	training_file = sys.argv[1]
	test_file_name = sys.argv[2]
	data, specs = readData(training_file)

	centroidData = calculateCentroid(data, specs)
	print("Centroid: ")
	for x in range(0, specs[1]):
		print(centroidData[0,x]),
	print("")

	covMatrix= calcCov(data, specs, centroidData)
	print("Covariance matrix:")
	for x in range(0, specs[1]):
		for y in range(0, specs[1]):
			print(covMatrix[x,y]),
		print("")

	data2, specs2 = readData(test_file_name)

	counter = 1
	print("Distances:")
	for x in range (0, specs2[0]):
		print (str(counter) + ".  "),
		counter = counter+1
		diff = data2[x]-centroidData
		# diff[0] is the actuall matrix difference
		diffMatrix = np.asmatrix(diff[0])
		result = diffMatrix * covMatrix.getI() * diffMatrix.getT()
		final_result = ((result.A[0,0])**(0.5))
		for y in range(0, specs2[1]):
			print(data2[x][y]),
		print ("--"),
		print (final_result)
