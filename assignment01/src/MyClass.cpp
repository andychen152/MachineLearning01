#include "MyClass.h"

MyClass::MyClass(int dimensionality, int dataAmount) {
	this->dimensionality = dimensionality;
	this->dataAmount = dataAmount;
	this->centoidData = new double[dimensionality];
	for(int i=0; i<dimensionality; i++) 
		centoidData[i]=0.0;
}

int MyClass::getDataAmount() {
	return this->dataAmount;
}

void MyClass::inputData(vector<string> newData) {
	for(int i=0; i<dimensionality; i++) 
		centoidData[i] += stod(newData[i]);
}

double* MyClass::getCentroidData() {
	return this->centoidData;
}

double* MyClass::orthogonalEquation(double* pointBCentoidData) {
	// first find general vector
	double* mainVector = new double[dimensionality];
	for(int i=0; i<dimensionality; i++) {
		mainVector[i] = pointBCentoidData[i]-this->centoidData[i];
	}

	// complete C by first finiding midpoint
	double midpointVector[dimensionality];
	for(int i=0; i<dimensionality; i++) {
		midpointVector[i] = this->getCentroidData()[i] + mainVector[i]/2;
	} 
	double sum=0;
	for(int i=0; i<dimensionality; i++) {
		sum += (midpointVector[i]*mainVector[i]);
	}
	double constant = (-1)*sum;
	mainVector[dimensionality] = constant;
	return mainVector;
}

void MyClass::averageCentroid() {
	for(int i=0; i<dimensionality; i++) {
		centoidData[i] /= this->dataAmount;
	}
}