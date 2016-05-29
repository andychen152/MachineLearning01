from __future__ import division
import sys
import numpy as np
import math

def readData(filename):
    dataFile = open(filename, 'r')
    line = dataFile.readline()
    specs = map(int, line.split())
    data = np.genfromtxt(dataFile)
    dataFile.close()
    return (data, specs)

def getEuc(rowVec1, rowVec2, dimension, sigma):
	#first get Euc distance
	sum = 0
	for x in range(0, dimension):
		diff = rowVec1[x]-rowVec2[x]
		sum += diff**2
	dist = sum**(0.5)

	# other parts
	result = dist**2
	result = result * -1
	squaredSigma = sigma**2
	result = result / (2*squaredSigma)
	return math.exp(result)

def getGram(pos_train_data, neg_train_data, pos_train_specs, neg_train_specs, sigma):
	dimension = pos_train_specs[0] + neg_train_specs[0]
	resultMatrix = np.zeros((dimension,dimension))
	fullTrainMatrix = np.concatenate((pos_train_data,neg_train_data), axis=0)
	for x in range(0,dimension):
		for y in range(0,dimension):
			resultMatrix[x,y] = getEuc(fullTrainMatrix[x], fullTrainMatrix[y], neg_train_specs[1]+1, sigma)
	return resultMatrix

if __name__ == "__main__":

	if len(sys.argv) != 6:
		print "Received wrong number of arguments.\nUsage: \'python triclassify.py train.txt test.txt\'"
		sys.exit()

	sigma = float(sys.argv[1])
	train_pos = sys.argv[2]
	train_neg = sys.argv[3]
	test_pos = sys.argv[4]
	test_neg = sys.argv[5]

	pos_train_data, pos_train_specs = readData(train_pos)
	neg_train_data, neg_train_specs = readData(train_neg)
	pos_test_data, pos_test_specs = readData(test_pos)
	neg_test_data, neg_test_specs = readData(test_neg)

	D = neg_train_specs[0] + pos_train_specs[0]

	# making homo
	onesForPos = np.ones((pos_train_specs[0],1))
	onesForNeg = np.ones((neg_train_specs[0],1))
	onesForPosTest = np.ones((pos_test_specs[0],1))
	onesForNegTest = np.ones((neg_test_specs[0],1))
	pos_train_data = np.concatenate((pos_train_data,onesForPos),axis=1)
	neg_train_data = np.concatenate((neg_train_data,onesForNeg),axis=1)
	pos_test_data = np.concatenate((pos_test_data,onesForPosTest),axis=1)
	neg_test_data = np.concatenate((neg_test_data,onesForNegTest),axis=1)

	# computing Gram Matrix
	gramMatrix = getGram(pos_train_data, neg_train_data, pos_train_specs, neg_train_specs, sigma)

	# Kernel Perceptron
	alphaSolution = np.zeros((1,D))  # all alphas stored here
	converged = False
	while(converged==False):
		converged = True
		for x in range(0,D):		# i
			yi = -1
			if (x<pos_train_specs[0]):
				yi = 1
			yj = 0
			for y in range(0,D):	# j
				if (y<pos_train_specs[0]):
					yj += (alphaSolution[0,y]*(1)*gramMatrix[x,y])
				else:
					yj += (alphaSolution[0,y]*(-1)*gramMatrix[x,y])
			if((yi*yj)<=0):
				alphaSolution[0,x] += 1
				converged = False

	# printing alpha
	print("Alphas:"),
	for x in range(0,D):
		print(int(alphaSolution[0,x])),

	fullTrainMatrix = np.concatenate((pos_train_data,neg_train_data), axis=0)

	# finding w matrix  # NOT USED IN THIS CLASS :(
	# w = np.zeros((1,pos_train_specs[1]+1))
	# for x in range(0,(pos_train_specs[1]+1)):
	# 	total = 0
	# 	for y in range(0,D):
	# 		if (y<pos_train_specs[0]):
	# 			total += (alphaSolution[0,y]*fullTrainMatrix[y,x]*1)
	# 		else:
	# 			total += (alphaSolution[0,y]*fullTrainMatrix[y,x]*-1)
	# 	w[0,x] = total

	# comparing to testing data
	# calculating false positives
	fp = 0
	for x in range(0, neg_test_specs[0]):
		total=0
		for y in range (0, D):
			if (y<pos_train_specs[0]):
				total += (alphaSolution[0,y]*1*getEuc(neg_test_data[x],fullTrainMatrix[y],neg_test_specs[1]+1,sigma))
			else:
				total += (alphaSolution[0,y]*-1*getEuc(neg_test_data[x],fullTrainMatrix[y],neg_test_specs[1]+1,sigma))	
		if(total>=0):
			fp+=1			

	# calculating false negatives
	fn = 0	
	for x in range(0, pos_test_specs[0]):
		total=0
		for y in range (0, D):
			if (y<pos_train_specs[0]):
				total += (alphaSolution[0,y]*1*getEuc(pos_test_data[x],fullTrainMatrix[y],neg_test_specs[1]+1,sigma))
			else:
				total += (alphaSolution[0,y]*-1*getEuc(pos_test_data[x],fullTrainMatrix[y],neg_test_specs[1]+1,sigma))	
		if(total<0):
			fn+=1		

	# calculating error rate
	errorRate = (fp+fn)/(neg_test_specs[0]+pos_test_specs[0])

	# printing fp and fn and error rate
	print("")
	print("False positives:"),
	print(fp)
	print("False negatives:"),
	print(fn)
	print("Error Rate:"),
	errorRate *= 100
	print("%"+str(errorRate))

