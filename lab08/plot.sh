set term png 
set xlabel "t_n"

set ylabel "c(t_n)"
set out "images/c_t_n.png"
plot "result/out_0.000000.dat"  u 1:2 title "D=0.0", "result/out_0.100000.dat"  u 1:2 title "D=0.1"

set ylabel "x_{śr}(t_n)"
set out "images/x_sr_t_n.png"
plot "result/out_0.000000.dat"  u 1:3 title "D=0.0", "result/out_0.100000.dat"  u 1:3 title "D=0.1"


set xlabel "x"
set ylabel "y"

set out "images/mapa_predkosci_vx.png"
set title "Mapa prędkości Vx"
plot "result/V_x.dat" u 1:2:3 with image

set out "images/mapa_predkosci_vy.png"
set title "Mapa prędkości Vy"

plot "result/V_y.dat" u 1:2:3 with image

reset
set term png
set palette defined (-10 "blue", 0 "white", 10 "red")
set size ratio -1
set xlabel "x"
set ylabel "y"
set pm3d map

do for [i=1:5] {
  image_name = sprintf("images/mapa_rozkladu_0.0_it=%i.png",i)
  set output image_name
  file = sprintf("result/zad0.000000_it=%i.txt",i)
  splot file u 1:2:3 w pm3d  title sprintf("t=%i",i)
} 
do for [i=1:5] {
  image_name = sprintf("images/mapa_rozkladu_0.1_it=%i.png",i)
  set output image_name
  file = sprintf("result/zad0.100000_it=%i.txt",i)
  splot file u 1:2:3 w pm3d  title sprintf("t=%i",i)
} 
