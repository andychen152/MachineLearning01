#ifndef __TEST_CLASS__
#define __TEST_CLASS__
#include <iostream>
#include <vector>
#include <cassert>

using namespace std;

class TestClass {

private:
	double* a_bLine;
	double* b_cLine;
	double* a_cLine;
	
public:
	TestClass(double* aVb, double* bVc, double* aVc);
	int computation(vector<string> inputData);
};

#endif