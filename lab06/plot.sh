set term png
set palette defined (-10 "blue", 0 "white", 10 "red")
set size ratio -1
set xlabel "x"
set ylabel "y"
set pm3d map

set output "images/mapa50.png"
set title "nx=ny=50 eps1=eps2 = 1"
splot [0:5][0:5] "data/mapa50.dat" i 0 u 2:1:3

set output "images/mapa100.png"
set title "nx=ny=100 eps1=eps2 = 1"
splot [0:10][0:10] "data/mapa100.dat" i 0 u 2:1:3

set output "images/mapa200.png"
set title "nx=ny=200 eps1=eps2 = 1"
splot [0:20][0:20] "data/mapa200.dat" i 0 u 2:1:3

set output "images/mapa2a.png"
set title "2a) nx=ny=100 eps1=eps2 = 1"
splot [0:10][0:10][-0.8:0.8] "data/mapa2a.dat" i 0 u 2:1:3

set output "images/mapa2b.png"
set title "2b) nx=ny=100 eps1=1 eps2 = 2"
set cbrange [-0.8:0.8]
splot [0:10][0:10][-0.8:0.8] "data/mapa2b.dat" i 0 u 2:1:3

set output "images/mapa2c.png"
set title "2c) nx=ny=100 eps1=1 eps2 = 10"
set cbrange [-0.8:0.8]
splot [0:10][0:10][-0.8:0.8] "data/mapa2c.dat" i 0 u 2:1:3