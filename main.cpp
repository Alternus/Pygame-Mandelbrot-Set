#include <iostream>
#include <SDL2/SDL.h>
#include <complex>
#include <cmath>
#include <chrono>
#include <future>
#include <thread>

using namespace std;

const int screen_Width = 850;
const int screen_Height = 850;
const int precision = 1000;


float calcMandelbrotPoint(float x, float y) {
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


void calculate_Quad1(int screenArray[screen_Height][screen_Width][3]) {
	for (double y = 0; y < screen_Height/2; y++) {
		for (double x = screen_Width/2; x < screen_Width; x++) {
			if (calcMandelbrotPoint(((x - (screen_Width/2))/screen_Width) * 3,((y - (screen_Height/2))/screen_Height) * 3) == precision)
			{
				screenArray[y][x] = (0,0,0);
			}
			else{
				screenArray[y][x] = (0,0,0);
			}
		}
	}
}

void calculate_Quad2(int*** screenArray) {
	for (double y = 0; y < screen_Height/2; y++) {
		for (double x = 0; x < screen_Width/2; x++) {
			if (calcMandelbrotPoint(((x - (screen_Width/2))/screen_Width) * 3,((y - (screen_Height/2))/screen_Height) * 3) == precision)
			{
				screenArray[(int)y][(int)x][0] = 0;
				screenArray[(int)y][(int)x][1] = 0;
				screenArray[(int)y][(int)x][2] = 0;
			}
			else{
				screenArray[(int)y][(int)x][0] = 255;
				screenArray[(int)y][(int)x][1] = 0;
				screenArray[(int)y][(int)x][2] = 0;
			}
		}
	}
}

void calculate_Quad3(int*** screenArray) {
	for (double y = screen_Height/2; y < screen_Height; y++) {
		for (double x = 0; x < screen_Width/2; x++) {
			if (calcMandelbrotPoint(((x - (screen_Width/2))/screen_Width) * 3,((y - (screen_Height/2))/screen_Height) * 3) == precision)
			{
				screenArray[(int)y][(int)x][0] = 0;
				screenArray[(int)y][(int)x][1] = 0;
				screenArray[(int)y][(int)x][2] = 0;
			}
			else{
				screenArray[(int)y][(int)x][0] = 255;
				screenArray[(int)y][(int)x][1] = 0;
				screenArray[(int)y][(int)x][2] = 0;
			}
		}
	}
}

void calculate_Quad4(int*** screenArray) {
	for (double y = screen_Height/2; y < screen_Height; y++) {
		for (double x = screen_Width/2; x < screen_Width; x++) {
			if (calcMandelbrotPoint(((x - (screen_Width/2))/screen_Width) * 3,((y - (screen_Height/2))/screen_Height) * 3) == precision)
			{
				screenArray[(int)y][(int)x][0] = 0;
				screenArray[(int)y][(int)x][1] = 0;
				screenArray[(int)y][(int)x][2] = 0;
			}
			else{
				screenArray[(int)y][(int)x][0] = 255;
				screenArray[(int)y][(int)x][1] = 0;
				screenArray[(int)y][(int)x][2] = 0;
			}
		}
	}
}


int main( int argc, char** argv ) {
	SDL_Init( SDL_INIT_VIDEO );

	SDL_Window* window = SDL_CreateWindow("Mandelbrot Set | Mitchell Wills 2020", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, screen_Width, screen_Height, 0);

	SDL_Renderer* renderer = SDL_CreateRenderer( window, -1, 0 );

	SDL_Event event;
	bool runRender = true;
	SDL_RenderClear(renderer);
	int (*screenArray)[screen_Height][screen_Width][3] = (int(*)[screen_Height][screen_Width][3])malloc(sizeof *screenArray);
	while( true ) {
		SDL_PumpEvents();
		if (SDL_PollEvent(&event) && event.type == SDL_QUIT)
			break;

		SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
		if (runRender) {
			auto start = chrono::steady_clock::now();

			//async(calculate_Quad1(screenArray));

			//thread thread1(calculate_Quad1);
			//thread thread2(calculate_Quad2,ref(screenArray));
	//		thread thread3(calculate_Quad3,ref(screenArray));
	//		thread thread4(calculate_Quad4,ref(screenArray));

		//	thread1.join();
		//	thread2.join();
		//	thread3.join();
		//	thread4.join();
			SDL_RenderClear(renderer);
			cout << "finish thread";
			for (int y = 0; y < screen_Height; y++){
				for (int x = 0; y < screen_Width; x++){
					SDL_SetRenderDrawColor(renderer, screenArray[screen_Height][screen_Width][0], screenArray[screen_Height][screen_Width][1], screenArray[screen_Height][screen_Width][2], 255);
					SDL_RenderDrawPoint(renderer, x, y);
				}
			}
			SDL_RenderPresent(renderer);
			cout << chrono::duration <double, milli> (chrono::steady_clock::now() - start).count() / 1000 << " seconds" << endl;
			runRender = false;
		}

	}

	SDL_DestroyRenderer( renderer );
	SDL_DestroyWindow( window );
	SDL_Quit();

	return 0;
}
