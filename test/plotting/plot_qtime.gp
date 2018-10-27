set term png
set output "qtimes.png"
set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 1.5
set style line 2 lc rgb '#ad6000' lt 1 lw 2 pt 7 ps 1.5
set style line 3 lc rgb '#60ad00' lt 1 lw 2 pt 7 ps 1.5
set title "Queue waiting times vs. Time"
set ylabel "Queue waiting times (ms)"
set xlabel "Experiment time (s)"
set datafile separator ","
plot "out.txt" using 1:($9 * 1000) with lines title "Set queue time" ls 1,\
"out.txt" using 1:($10 * 1000) with lines title "Get queue time" ls 2,\
"out.txt" using 1:($11 * 1000) with lines title "Multi-get queue time" ls 3