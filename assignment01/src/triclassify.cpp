#include <iostream>
#include <cassert>
#include <string>
#include <sstream>
#include <vector>
#include <fstream>
#include "MyClass.h"
#include "TestClass.h"

using namespace std;

vector<string> parseLine(string line) { // code to store input texts into arrays
  stringstream ss(line);
  vector<string> result;
  while(ss.good()) {
      string substr;
      getline(ss,substr,' ');
      result.push_back(substr);
  }
  // string* a = &result[0];
  return result;
}


int main(int argc, char **argv) {

	// Error if testing and training data aren't provided
	assert(argc==3);
	
	ifstream f(argv[1]);
	string s;
	getline(f,s);

	vector<string> firstLineTrainingData = parseLine(s);
	int dimensionality = stoi(firstLineTrainingData[0]);

	MyClass* first_training_class = new MyClass(dimensionality, stoi(firstLineTrainingData[1]));
	MyClass* second_training_class = new MyClass(dimensionality, stoi(firstLineTrainingData[2]));
	MyClass* third_training_class = new MyClass(dimensionality, stoi(firstLineTrainingData[3]));


	for(int i=0; i<first_training_class->getDataAmount(); i++) {
		getline(f,s);
		vector<string> data = parseLine(s);
		first_training_class->inputData(data);
	}
	
	for(int i=0; i<second_training_class->getDataAmount(); i++) {
		getline(f,s);
		vector<string> data = parseLine(s);
		second_training_class->inputData(data);
	}

	for(int i=0; i<third_training_class->getDataAmount(); i++) {
		getline(f,s);
		vector<string> data = parseLine(s);
		third_training_class->inputData(data);
	}
	first_training_class->averageCentroid();
	second_training_class->averageCentroid();
	third_training_class->averageCentroid();
	
	f.close(); 


	// Now running testing data
	ifstream n(argv[2]);
	getline(n,s);
	vector<string> firstLineTestingData = parseLine(s);


	TestClass* mainTestClass = new TestClass(first_training_class->orthogonalEquation(second_training_class->getCentroidData()),
		second_training_class->orthogonalEquation(third_training_class->getCentroidData()), 
		first_training_class->orthogonalEquation(third_training_class->getCentroidData()));
		
	int totalA = stoi(firstLineTestingData[1]);
	int totalB = stoi(firstLineTestingData[2]);
	int totalC = stoi(firstLineTestingData[3]);

	// Data Rows store Predicted A,B,C while Columns store Actual A,B,C
	int classA[3]={0,0,0};
	int classB[3]={0,0,0};
	int classC[3]={0,0,0};

	for(int i=0; i<totalA; i++) {
		getline(n,s);
		vector<string> data = parseLine(s);
		int classifier = mainTestClass->computation(data);
		if(classifier==1)
			classA[0]++;
		else if(classifier==2)
			classB[0]++;
		else 
			classC[0]++;
	}

	for(int i=0; i<totalB; i++) {
		getline(n,s);
		vector<string> data = parseLine(s);
		int classifier = mainTestClass->computation(data);
		if(classifier==1)
			classA[1]++;
		else if(classifier==2)
			classB[1]++;
		else 
			classC[1]++;
	}

	for(int i=0; i<totalC; i++) {
		getline(n,s);
		vector<string> data = parseLine(s);
		int classifier = mainTestClass->computation(data);
		if(classifier==1)
			classA[2]++;
		else if(classifier==2)
			classB[2]++;
		else 
			classC[2]++;
	}
	f.close();

	// computing and execution for True Positive Rate
	double tprA = (double)classA[0]/totalA;
	double tprB = (double)classB[1]/totalB;
	double tprC = (double)classC[2]/totalC;
	cout << "True Positive Rate: " << (tprA+tprB+tprC)/3 << endl;

	// computing and execution for Flase Positive Rate
	double fprA = (classB[0]+classC[0])/((double)(totalB+totalC));
	double fprB = (classA[1]+classC[1])/((double)(totalA+totalC));
	double fprC = (classA[2]+classB[2])/((double)(totalA+totalB));
	cout << "False Positive Rate: " << (fprA+fprB+fprC)/3 << endl;

	// computing error rate
	double errorRateA = (classB[0]+classC[0]+classA[1]+classA[2])/((double)(totalA+totalB+totalC));
	double errorRateB = (classA[1]+classC[1]+classB[0]+classB[2])/((double)(totalA+totalB+totalC));
	double errorRateC = (classA[2]+classB[2]+classC[0]+classC[1])/((double)(totalA+totalB+totalC));
	cout << "Error Rate: " << (errorRateA+errorRateB+errorRateC)/3 << endl;

	// computing accuracy
	double accuracyA = (classA[0]+classB[1]+classB[2]+classC[1]+classC[2])/((double)(totalA+totalB+totalC));
	double accuracyB = (classB[1]+classA[0]+classA[2]+classC[0]+classC[2])/((double)(totalA+totalB+totalC));
	double accuracyC = (classC[2]+classA[0]+classA[1]+classB[0]+classB[1])/((double)(totalA+totalB+totalC));
	cout << "Accuracy Rate: " << (accuracyA+accuracyB+accuracyC)/3 << endl;

	// computing Precision
	double precisionA = (double)classA[0]/(classA[0]+classA[1]+classA[2]);
	double precisionB = (double)classB[1]/(classB[0]+classB[1]+classB[2]);
	double precisionC = (double)classC[2]/(classC[0]+classC[1]+classC[2]);
	cout << "Precision Rate: " << (precisionA+precisionB+precisionC)/3 << endl;
}