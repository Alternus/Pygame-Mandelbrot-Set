#include "program.h"
#include <iostream>
#include <complex>
#include <cmath>
#include <list>
#include <tuple>

using namespace std;

int Calc::calcMandelbrotPoint(double x, double y, int precision) {
	complex<double> current_Result(0.0,0.0);
	complex<double> c(x,y);

	int times_Looped = 0;
		for (int i = 0; i < precision; i++ , times_Looped++) {
			if ((pow(real(current_Result),2) + pow(imag(current_Result),2)) > 4)
			{
				return times_Looped;
			}
			current_Result = pow(current_Result,2) + c;
		}
	return times_Looped;
}
