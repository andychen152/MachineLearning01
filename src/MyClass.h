#ifndef __MY_CLASS__
#define __MY_CLASS__
#include <iostream>
#include <string>
#include <vector>

using namespace std;

class MyClass {
private:
	int dimensionality;
	int dataAmount;
	double* centoidData;

public: 
	MyClass(int dimensionality, int dataAmount);
	int getDataAmount();
	void inputData(vector<string> newData);
	double* getCentroidData();
	double* orthogonalEquation(double* pointBCentoidData);
	void averageCentroid();
};

#endif