# GENERAL PURPOSE

git clone https://gitlab.ethz.ch/dcetin/asl-fall18-project.git
echo -e 'stats\r\nquit' | nc 0.0.0.0 11211 | grep "threads"

# BASELINE 1

./runner.sh -mtype cli -mno 1 -ipadd 10.0.0.5 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
./runner.sh -mtype cli -mno 2 -ipadd 10.0.0.5 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
./runner.sh -mtype cli -mno 3 -ipadd 10.0.0.5 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
./runner.sh -mtype svr -mno 1 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100