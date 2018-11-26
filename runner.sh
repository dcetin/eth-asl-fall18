#!/bin/bash

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
	# Machine specific parameters
	-mtype|--machinetype) MTYPE="$2"
	shift 2 ;; # Machine type
	-mno|--machineno) MNO="$2"
	shift 2 ;; # Machine number

	# Network parameters
	-ipadd|--ipaddress) IPADD=$2
	shift 2;; # IP address
	-pno|--portnumber) PNO=$2
	shift 2 ;; # Port number
	-pairs|--addresspairs) PAIRS=$2
	shift 2 ;; # Address pairs

	# Experiment parameters
	-nsvr|--servernumber) NSVR=$2
	shift 2 ;; # Number of servers
	-ncli|--clientnumber) NLCI=$2
	shift 2 ;; # Number of client machines
	-icli|--clientinstance) ICLI=$2
	shift 2 ;; # Instances of memtier per machine
	-tcli|--clientthread) TCLI=$2
	shift 2 ;; # Threads per memtier instance
	-vcli|--clientvirtual) VCLI=$2
	shift 2 ;; # Virtual clients per thread
	-wrkld|--workload) WRKLD=$2
	shift 2 ;; # Workload - Set:Get Ratio
	-mgshrd|--mgetsharded) MGSHRD=$2
	shift 2 ;; # Multi-get behaviour
	-mgsize|--mgetsize) MGSIZE=$2
	shift 2 ;; # Multi-get size
	-nmw|--middlewarenumber) NMW=$2
	shift 2 ;; # Number of middlewares
	-tmw|--middlewarethread) TMW=$2
	shift 2 ;; # Worker threads per middleware
	-reps|--repeats) REPS=$2
	shift 2 ;; # Repetitions
	-ttime|--testtime) TTIME=$2
	shift 2 ;; # Test time

	# dstat parameter
	-dsmt|--dstatmachinetype) DSMT=$2
	shift 2 ;; # mw or svr
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

# template: -nsvr ~ -ncli ~ -icli ~ -tcli ~ -vcli ~ -wrkld ~ -mgshrd ~ -mgsize ~ -nmw ~ -tmw ~ -reps ~ -ttime ~
# csb1: -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100 
# csb2: -nsvr 2 -ncli 1 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
# mwb1: -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 1 -tmw ~ -reps 3 -ttime 70
# mwb2: -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
# tpfw: -nsvr 3 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld 1:0 -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
# mgs: 
# mgns: 
# 2k: 

# Local paths
MLOC="/home/doruk/Desktop/asl/memtier_benchmark-master/memtier_benchmark"
JAR="/home/doruk/Desktop/asl/asl-fall18-project/dist/middleware-dcetin.jar"
RESBASE="/home/doruk/Desktop/asl/asl-fall18-project/res/test/"

# Remote paths
MLOC="/home/dcetin/memtier_benchmark-master/memtier_benchmark"
JAR="/home/dcetin/asl-fall18-project/dist/middleware-dcetin.jar"
RESBASE="/home/dcetin/asl-fall18-project/res/"

RES="${RESBASE}nsvr=${NSVR}/ncli=${NLCI}/icli=${ICLI}/tcli=${TCLI}/vcli=${VCLI}/wrkld=${WRKLD}/mgshrd=${MGSHRD}/mgsize=${MGSIZE}/nmw=${NMW}/tmw=${TMW}/ttime=${TTIME}/"

# Test paths
# RES="${RESBASE}csb1wo/"

if [ $MTYPE == "svr" ]
then
	sudo service memcached stop
	memcached -t 1 -p $PNO
else
	mkdir -p $RES
	for REP in $(seq 1 $REPS);
	do
		MWOUT="${RES}mwout${MNO}rep${REP}.out"
		CLOUT="${RES}cliout${MNO}rep${REP}.out"
		CLSTT="${RES}cli${MNO}rep${REP}"

		case $MTYPE in
			"dstat")
				DSTATOUT="${RES}dstatout-${DSMT}${MNO}rep${REP}.out"
				dstat -cdngy 1 $TTIME > $DSTATOUT
				sleep 10
				;;
			"cli") # TODO: not tested with multiget
				DSTATOUT="${RES}dstatout-${MTYPE}${MNO}rep${REP}.out"
				if [ $MGSIZE == "NA" ]; then
					(dstat -cdngy 1 $TTIME > $DSTATOUT &) ; $MLOC --server=$IPADD --port=$PNO  --out-file=$CLOUT --client-stats=$CLSTT --clients=$VCLI --threads=$TCLI --test-time=$TTIME --ratio=$WRKLD --expiry-range=9999-10000 --data-size=4096 --key-maximum=10000 --protocol=memcache_text #--hide-histogram
				else
					(dstat -cdngy 1 $TTIME > $DSTATOUT &) ; $MLOC --server=$IPADD --port=$PNO  --out-file=$CLOUT --client-stats=$CLSTT --clients=$VCLI --threads=$TCLI --test-time=$TTIME --ratio=$WRKLD --expiry-range=9999-10000 --data-size=4096 --key-maximum=10000 --protocol=memcache_text --multi-key-get=$MGSIZE #--hide-histogram 
				fi
				sleep 10
				;;
			"mw")
				java -jar $JAR -l $IPADD -p $PNO -t $TMW -s $MGSHRD -m $PAIRS > $MWOUT
				sleep 1
				;;
		esac
	done
fi