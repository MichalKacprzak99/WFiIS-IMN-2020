#include <array>
#include <cmath>
#include <cstring>
#include <iostream>
#include <utility>

// stałe
const int nx = 400;
const int ny = 90;
const int i1 = 200;
const int i2 = 210;
const int my_j1 = 50;
const double delta = 0.01;
const double sigma = 10 * delta;
const double xA = 0.45;
const double yA = 0.45;

// obliczenie x, y
double x(int i) {
    return delta * i;
}

double y(int j) {
    return delta * j;
}

void inicjalizacja_gestosci(std::array<std::array<double, ny+1>, nx+1>& u0) {
    double constant1 = 1.0 / (2 * M_PI * pow(sigma, 2));
    double constant2 = 2 * pow(sigma, 2);
    for (int i = 0; i <= nx; i++) {
        for (int j = 0; j <= ny; j++) {    
            u0[i][j] = constant1 * exp(-(pow(x(i) - xA, 2) + pow(y(j) - yA, 2)) / constant2);
        }
    }
}

void calculate_save_c_xsr(FILE* f, std::array<std::array<double, ny+1>, nx+1>& u0, 
std::array<std::array<double, ny+1>, nx+1>& u1, int it, double time_step){
    double c = 0.;
    double xsr = 0.;
    for (int i = 0; i <= nx; i++) {
        for (int j = 0; j <= ny; j++) {
            c += u0[i][j];
            xsr += x(i) * u0[i][j];
        }
    }
    c *= (delta * delta);
    xsr *= (delta * delta);
    fprintf(f, "%f %lf %lf\n", it * time_step, c, xsr);
}

void save_for_map(double D, int p, std::array<std::array<double, ny+1>, nx+1>& u0, 
std::array<std::array<double, ny+1>, nx+1>& u1){
    std::cout << ("result/zad" + std::to_string(D) + "_it=" + std::to_string(p) + ".txt") << "\n";
    FILE* file = fopen(("result/zad" + std::to_string(D) + "_it=" + std::to_string(p) + ".txt").c_str(), "wb");
    
    for (int i = 0; i < u0.size(); i++) {
        for(int j = 0; j < u0[i].size(); j++){
            fprintf(file, "%d %d %lf\n", i, j, u0[i][j]);
        }
        fprintf(file, "\n");
    }
    fclose(file);
}
void crank_nicolson_method(std::array<std::array<double, ny+1>, nx+1>& u0, std::array<std::array<double, ny+1>, nx+1>& u1, 
std::array<std::array<double, ny+1>, nx+1>& V_x, std::array<std::array<double, ny+1>, nx+1>& V_y, 
double time_step, double D, int IT_MAX) {
    FILE* file = fopen(("result/out_" + std::to_string(D)  + ".dat").c_str(), "w");
    int p = 1;
    for (int it = 1; it <= IT_MAX; it++) {
        // zaladowanie poprzedniej iteracji
        for (int i = 0; i < u0.size(); i++) {
            std::memcpy(u1[i].data(), u0[i].data(), u0[i].size() * sizeof(double));
        }
         // start iteracji Picarda
        for (int k = 1; k <= 20; k++) {
            for (int i = 0; i <= nx; i++) {
                for (int j = 1; j <= ny - 1; j++) {
                    if (i > i1 && i < i2 && j < my_j1) {
                        continue;
                    }
                    if (i == 0 ) {
                        u1[i][j] = (1.0 / (1 + (2 * D * time_step / pow(delta, 2)))) * (u0[i][j] - (time_step / 2.0) * V_x[i][j] * (((u0[i + 1][j] - u0[nx][j]) / (2.0 * delta)) + (u1[i + 1][j] - u1[nx][j]) / (2.0 * delta)) - (time_step / 2) * V_y[i][j] * ((u0[i][j + 1] - u0[i][j - 1]) / (2.0 * delta) + (u1[i][j + 1] - u1[i][j - 1]) / (2.0 * delta)) + time_step / 2.0 * D * ((u0[i + 1][j] + u0[nx][j] + u0[i][j + 1] + u0[i][j - 1] - 4 * u0[i][j]) / pow(delta, 2) + (u1[i + 1][j] + u1[nx][j] + u1[i][j + 1] + u1[i][j - 1]) / pow(delta, 2)));
                    } else if (i == nx) {
                        u1[i][j] = (1.0 / (1 + (2 * D * time_step / pow(delta, 2)))) * (u0[i][j] - (time_step / 2.0) * V_x[i][j] * (((u0[0][j] - u0[i - 1][j]) / (2.0 * delta)) + (u1[0][j] - u1[i - 1][j]) / (2.0 * delta)) - (time_step / 2) * V_y[i][j] * ((u0[i][j + 1] - u0[i][j - 1]) / (2.0 * delta) + (u1[i][j + 1] - u1[i][j - 1]) / (2.0 * delta)) + time_step / 2.0 * D * ((u0[0][j] + u0[i - 1][j] + u0[i][j + 1] + u0[i][j - 1] - 4 * u0[i][j]) / pow(delta, 2) + (u1[0][j] + u1[i - 1][j] + u1[i][j + 1] + u1[i][j - 1]) / pow(delta, 2)));
                    } else {
                        u1[i][j] = (1.0 / (1 + (2 * D * time_step / pow(delta, 2)))) * (u0[i][j] - (time_step / 2.0) * V_x[i][j] * (((u0[i + 1][j] - u0[i - 1][j]) / (2.0 * delta)) + (u1[i + 1][j] - u1[i - 1][j]) / (2.0 * delta)) - (time_step / 2) * V_y[i][j] * ((u0[i][j + 1] - u0[i][j - 1]) / (2.0 * delta) + (u1[i][j + 1] - u1[i][j - 1]) / (2.0 * delta)) + time_step / 2.0 * D * ((u0[i + 1][j] + u0[i - 1][j] + u0[i][j + 1] + u0[i][j - 1] - 4 * u0[i][j]) / pow(delta, 2) + (u1[i + 1][j] + u1[i - 1][j] + u1[i][j + 1] + u1[i][j - 1]) / pow(delta, 2)));
                    }
                }
            }
        }
        // zachowujemy rozwiązanie do następnej iteracji
        for (int i = 0; i < u0.size(); i++) {
            std::memcpy(u0[i].data(), u1[i].data(), u0[i].size() * sizeof(double));
        }

        calculate_save_c_xsr(file, u0, u1, it, time_step);

        //zapisu danych dla mapy rozkladu
        if(it * time_step >= (p * IT_MAX * time_step) / 5){
            save_for_map(D, p, u0, u1);
            p++;
        }
    }

    fclose(file);
}

void wczytanie_funkcji_strumienia(std::array<std::array<double, ny+1>, nx+1>& psi) {
    FILE* f = fopen("psi.dat", "r");
    int x = 0;
    int y = 0;
    double value = 0.0;
    for (int i = 0; i <= nx; i++) {
        for (int j = 0; j <= ny; j++) {
            fscanf(f, "%d %d %lf", &x, &y, &value);
            psi[x][y] = value;
        }
    }

    fclose(f);

}
void save_pola_predkosci(std::array<std::array<double, ny+1>, nx+1>& V_x, std::array<std::array<double, ny+1>, nx+1>& V_y){
    FILE* file_x = fopen(("result/V_x.dat"), "wb");
    for (int i = 0; i < V_x.size(); i++) {
        for(int j = 0; j < V_x[i].size(); j++){
            fprintf(file_x, "%f %f %lf\n", i * delta, j * delta, V_x[i][j]);
        }
        fprintf(file_x, "\n");
    }
    fclose(file_x);
    FILE* file_y = fopen(("result/V_y.dat"), "wb");
    for (int i = 0; i < V_y.size(); i++) {
        for(int j = 0; j < V_y[i].size(); j++){
            fprintf(file_y, "%f %f %lf\n", i * delta, j * delta, V_y[i][j]);
        }
        fprintf(file_y, "\n");
    }
    fclose(file_y);
}
 
void wyznaczenie_pol_predkosci(std::array<std::array<double, ny+1>, nx+1>& psi, 
std::array<std::array<double, ny+1>, nx+1>& V_x, std::array<std::array<double, ny+1>, nx+1>& V_y){
    for (int i = 1; i <= nx - 1; i++) {
        for (int j = 1; j <= ny - 1; j++) {
            V_x[i][j] = (psi[i][j + 1] - psi[i][j - 1]) / (2.0 * delta);
            V_y[i][j] = -(psi[i + 1][j] - psi[i - 1][j]) / (2.0 * delta);
        }
    }
    for (int i = i1; i <= i2; i++) {
        for (int j = 0; j <= my_j1; j++) {
            V_x[i][j] = 0.0;
            V_y[i][j] = 0.0;
        }
    }
    for (int i = 1; i <= nx - 1; i++) {
        V_x[i][0] = 0;
        V_y[i][0] = 0;
        V_x[i][ny] = 0;
        V_y[i][ny] = 0;
    }
    for (int j = 0; j <= ny; j++) {
        V_x[0][j] = V_x[1][j];
        V_x[nx][j] = V_x[nx - 1][j];
    }
    
}

double calculate_v_max(std::array<std::array<double, ny+1>, nx+1>& V_x, std::array<std::array<double, ny+1>, nx+1>& V_y){
    double v_max = 0;
    for (int i = 0; i <= nx; i++) {
        for (int j = 0; j <= ny; j++) {
            if (std::pow(V_x[i][j], 2) + pow(V_y[i][j], 2) > v_max) {
                v_max = std::pow(V_x[i][j], 2) + pow(V_y[i][j], 2);
            }
        }
    }
    v_max = std::sqrt(v_max);
    return v_max;
}

void solve_equation(double D, int IT_MAX, std::array<std::array<double, ny+1>, nx+1>& psi) {
    //inicjalizacja tablic
    std::array<std::array<double, ny+1>, nx+1> u0 = { { 0 } };
    std::array<std::array<double, ny+1>, nx+1> u1 = { { 0 } };
    std::array<std::array<double, ny+1>, nx+1> V_x = { { 0 } };
    std::array<std::array<double, ny+1>, nx+1> V_y = { { 0 } };

    inicjalizacja_gestosci(u0);

    wyznaczenie_pol_predkosci(psi, V_x, V_y);
    save_pola_predkosci(V_x, V_y);

    double v_max = calculate_v_max(V_x, V_y);
    double time_step = delta / (4 * v_max);
    
    crank_nicolson_method(u0, u1, V_x, V_y, time_step, D, IT_MAX);
}

int main() {
    std::array<std::array<double, ny+1>, nx+1> psi = { { 0 } };
    wczytanie_funkcji_strumienia(psi);
    solve_equation(0, 10000, psi);
    solve_equation(0.1, 10000, psi);
    return 0;
}