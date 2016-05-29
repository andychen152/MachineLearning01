#include "TestClass.h"

TestClass::TestClass(double* aVb, double* bVc, double* aVc) {
	this->a_bLine = aVb;
	this->b_cLine = bVc;
	this->a_cLine = aVc;
}

int TestClass::computation(vector<string> inputData) { 
	double sum=0;

	for(int i=0; i<inputData.size(); i++) { //AvB
		sum += (this->a_bLine[i]*stod(inputData[i]));
	}
	sum += a_bLine[inputData.size()];

	if(sum<=0) { // AvC
		sum=0;
		for(int i=0; i<inputData.size(); i++) {
			sum += (this->a_cLine[i]*stod(inputData[i]));
		}
		sum += a_cLine[inputData.size()];
		if(sum<=0)
			return 1;
		else
			return 3;
	}

	else { // BvC
		sum=0;
		for(int i=0; i<inputData.size(); i++) {
			sum += (this->b_cLine[i]*stod(inputData[i]));
		}
		sum += b_cLine[inputData.size()];
		if(sum<=0)
			return 2;
		else
			return 3;
	}
}