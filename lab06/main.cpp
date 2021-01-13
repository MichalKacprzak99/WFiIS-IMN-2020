#include <cmath>
#include <iostream>
#include "mgmres.h"

#define DELTA 0.1

int get_j(int nx, int l){
    return (l / (nx + 1));
}

int get_i(int nx, int l){
    return l - get_j(nx,l) * (nx + 1);
}

double get_e_l(int nx, int l, int eps1, int eps2){
    if(get_i(nx,l) <= nx / 2)
        return eps1;
    else
        return eps2;
}

double gestosc1(double x, double y, double xmax, double ymax, double sig) {
	return exp(-1 * pow(x - 0.25 * xmax, 2)/pow(sig, 2) - pow(y - 0.5 * ymax, 2)/pow(sig, 2));
}

double gestosc2(double x, double y, double xmax, double ymax, double sig) {
	return -1 * exp(-1 * pow(x - 0.75 * xmax, 2)/pow(sig, 2) - pow(y - 0.5 * ymax, 2)/pow(sig, 2));
}

double gestosc(double x, double y, double xmax, double ymax, double sig) {
	return gestosc1(x, y, xmax, ymax, sig) + gestosc2(x, y, xmax, ymax, sig);
}

int warunki_dirichleta(int N, double V1, double V2, double V3, double V4, int nx, int ny, int eps1, int eps2,
	int *ja, int *ia, double *a, double *b,double xmax, double ymax) {
	FILE * macierz = fopen(("data/a_" + std::to_string(nx) + "_" + std::to_string(eps1) + ".dat").c_str(), "w");
    FILE * wektor = fopen(("data/b_" + std::to_string(nx) + "_" + std::to_string(eps1) + ".dat").c_str(), "w");
//numeruje niezerowe
	int k = -1;
//liczba niezerowych get_e_l
	int nz_num = 0;

	for(int l = 0; l < N; ++l) {
		int brzeg = 0;  //0 srodek, 1 brzeg
		double vb = 0;  //potencjal na brzegu
		if(get_i(nx, l) == 0){
			brzeg = 1;
			vb = V1;
		}
		if(get_j(nx, l) == ny){
			brzeg = 1;
			vb = V2;
		}
		if(get_i(nx, l) == nx){
			brzeg = 1;
			vb = V3;
		}

		if(get_j(nx, l) == 0){
			brzeg = 1;
			vb = V4;
		}

		b[l] = (-1) * gestosc(DELTA * get_i(nx,l), DELTA * get_j(nx, l), xmax, ymax, xmax/10);
		if(brzeg == 1)
			b[l] = vb;


		ia[l] = -1;
		// lewa skrajna przekatna 
		if(l - nx - 1 >= 0 && brzeg == 0){
			k++;
			if(ia[l] < 0)
                ia[l] = k;

			a[k] = get_e_l(nx, l, eps1, eps2) / (DELTA * DELTA);
			ja[k] = l - nx - 1;
		}
		//poddiag
		if(l-1 >= 0 && brzeg == 0) {
			k++;
			if(ia[l] < 0)
                ia[l] = k;
			a[k] = get_e_l(nx, l, eps1, eps2) / (DELTA * DELTA);
			ja[k] = l - 1;
		}
		//diag
		k++;
		if(ia[l] < 0)
            ia[l] = k;

		if(brzeg == 0)
			a[k] = -(2 * get_e_l(nx, l, eps1, eps2) + get_e_l(nx, l+1, eps1, eps2) + 
					get_e_l(nx, l+nx+1, eps1, eps2)) / (DELTA * DELTA);
		else
			a[k] = 1;

		ja[k] = l;
		//naddiag
		if(l < N && brzeg == 0){
			k++;
			a[k] = get_e_l(nx, l+1, eps1, eps2) / (DELTA * DELTA);
			ja[k] = l + 1;
		}
		//prawa skrajna przek
		if(l < N-nx-1 && brzeg == 0){
			k++;
			a[k] = get_e_l(nx, l+nx+1, eps1, eps2) / (DELTA * DELTA);
			ja[k] = l + nx + 1;
		}
        fprintf(wektor,"%d %d %d %f \n", l, get_i(nx, l), get_j(nx, l), b[l]);

    }

	nz_num = k+1;
	ia[N] = nz_num;
    for(int i = 0; i < 5 * N; i++){
		if((int)a[i]!=0.0){
			fprintf(macierz,"%d %d %d %f \n", i, get_i(nx, i), get_j(nx, i), a[i]);
		}		
	}
	fclose(macierz);
	fclose(wektor);

    return nz_num;
}

void poisson_equation(int nx, int ny, int eps1, int eps2, int V1, int V2, int V3, int V4,
	double xmax, double ymax, const std::string& numer=""){
	
	int N = (nx + 1) * (ny + 1);
    double a[5*N] ={0.0};
    int ja[5*N] = {0};
    int ia[N+1] = {0};
    double b[N] = {0.0};
    double V[N] = {0.0};

    int nz_num = warunki_dirichleta(N, V1,V2,V3,V4,nx,ny,eps1,eps2,ja,ia,a,b,xmax,ymax);

    int itr_max = 500;
    int mr = 500;
    double tol_abs = pow(10,-8);
    double tol_rel = pow(10,-8);

    pmgmres_ilu_cr(N,nz_num,ia,ja,a,V,b,itr_max, mr,tol_abs,tol_rel);

	if(numer!=""){
		FILE * mapa = fopen(("data/mapa"+numer+".dat").c_str(), "w");

		double tmp =0.;
		for(int z = 0; z < N; ++z){
			if(DELTA*get_j(nx,z) > tmp)
				fprintf(mapa,"\n");
			fprintf(mapa,"%f %f %f \n", DELTA*get_j(nx,z), DELTA*get_i(nx,z), V[z]);
			tmp = DELTA*get_j(nx,z);
		}
		fclose(mapa);
	}
	
}

int main(){
    int nx = 4;
    int ny = 4;
    int eps1 = 1;
    int eps2 = 1;
    int V1 = 10;
    int V2 = -10;
    int V3 = 10;
    int V4 = -10;
    double xmax = 0;
    double ymax = 0;

    poisson_equation
(nx,ny,eps1,eps2,V1,V2,V3,V4,xmax,ymax);

	nx = 50;
	ny = 50;
    poisson_equation
(nx,ny,eps1,eps2,V1,V2,V3,V4,xmax,ymax, "50");

	nx = 100;
	ny = 100;
    poisson_equation
(nx,ny,eps1,eps2,V1,V2,V3,V4,xmax,ymax, "100");

	nx = 200;
	ny = 200;
    poisson_equation
(nx,ny,eps1,eps2,V1,V2,V3,V4,xmax,ymax, "200");

	nx = 100;
	ny = 100;
	V1=V2=V3=V4=0;
	xmax = DELTA*nx;
	ymax = DELTA*ny;

    poisson_equation
(nx,ny,eps1,eps2,V1,V2,V3,V4,xmax,ymax, "2a");

	eps1 = 1;
	eps2 = 2;
    poisson_equation
(nx,ny,eps1,eps2,V1,V2,V3,V4,xmax,ymax, "2b");

	eps1 = 1;
	eps2 = 10;
    poisson_equation
(nx,ny,eps1,eps2,V1,V2,V3,V4,xmax,ymax, "2c");

}