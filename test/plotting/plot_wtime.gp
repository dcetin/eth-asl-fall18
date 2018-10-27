set term png
set output "wtimes.png"
set style line 1 lc rgb '#0060ad' lt 1 lw 2 pt 7 ps 1.5
set style line 2 lc rgb '#ad6000' lt 1 lw 2 pt 7 ps 1.5
set style line 3 lc rgb '#60ad00' lt 1 lw 2 pt 7 ps 1.5
set title "Server service times vs. Time"
set ylabel "Server service times (ms)"
set xlabel "Experiment time (s)"
set datafile separator ","
plot "out.txt" using 1:($12 * 1000) with lines title "Set service time" ls 1,\
"out.txt" using 1:($13 * 1000) with lines title "Get service time" ls 2,\
"out.txt" using 1:($14 * 1000) with lines title "Multi-get service time" ls 3