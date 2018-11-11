# CONNECTION
	# SSH commands for each VM
	Client 1:		SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip1.westeurope.cloudapp.azure.com
	Client 2:		SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip2.westeurope.cloudapp.azure.com
	Client 3:		SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip3.westeurope.cloudapp.azure.com
	Middleware 1:	SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip4.westeurope.cloudapp.azure.com
	Middleware 2:	SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip5.westeurope.cloudapp.azure.com
	Server 1:		SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip6.westeurope.cloudapp.azure.com
	Server 2:		SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip7.westeurope.cloudapp.azure.com
	Server 3:		SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip8.westeurope.cloudapp.azure.com
	# SSH commancds for each set of VMs
	all:		SSH_AUTH_SOCK=0 cssh dcetin@storelrt4zinzjmismsshpublicip{1,2,3,4,5,6,7,8}.westeurope.cloudapp.azure.com
	clients:	SSH_AUTH_SOCK=0 cssh dcetin@storelrt4zinzjmismsshpublicip{1,2,3}.westeurope.cloudapp.azure.com
	mws:		SSH_AUTH_SOCK=0 cssh dcetin@storelrt4zinzjmismsshpublicip{4,5}.westeurope.cloudapp.azure.com
	servers:	SSH_AUTH_SOCK=0 cssh dcetin@storelrt4zinzjmismsshpublicip{6,7,8}.westeurope.cloudapp.azure.com
	# IP addresses for each VM
	Client 1 (1):		10.0.0.8
	Client 2 (2):		10.0.0.4
	Client 3 (3):		10.0.0.7
	Middleware 1 (4):	10.0.0.10
	Middleware 2 (5):	10.0.0.9
	Server 1 (6):		10.0.0.6
	Server 2 (7):		10.0.0.5
	Server 3 (8):		10.0.0.11

# SETTING UP THE ENVIRONMENT
	sudo apt-get install memcached git unzip ant openjdk-8-jdk
	wget https://github.com/RedisLabs/memtier_benchmark/archive/master.zip
	unzip master.zip
	cd memtier_benchmark-master
	sudo apt-get install build-essential autoconf automake libpcre3-dev libevent-dev pkg-config zlib1g-dev
	autoreconf -ivf
	./configure
	make
	sudo service memcached stop

# GENERAL PURPOSE
	# Install dstat
	sudo apt install dstat
	# Install iperf3
	sudo apt-get install iperf3
	# Clone git repo
	git clone https://gitlab.ethz.ch/dcetin/asl-fall18-project.git
	# Check the number of threads in memcached server
	echo -e 'stats\r\nquit' | nc 0.0.0.0 11211 | grep "threads"
	# Kill the background dstat processes
	pkill -f dstat
	# Populate the database
	./memtier_benchmark --server=10.0.0.X --port=11211 --clients=1 --threads=1 --test-time=15 --ratio=1:0 --expiry-range=9999-10000 --data-size=4096 --key-maximum=9900 --protocol=memcache_text --hide-histogram --key-pattern=S:S --debug

# CLIENT-SERVER BASELINE 1
	# Clients on VMs 1,2,3
	SSH_AUTH_SOCK=0 cssh dcetin@storelrt4zinzjmismsshpublicip{1,2,3,6}.westeurope.cloudapp.azure.com
	./runner.sh -mtype cli -mno 1 -ipadd 10.0.0.6 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	./runner.sh -mtype cli -mno 2 -ipadd 10.0.0.6 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	./runner.sh -mtype cli -mno 3 -ipadd 10.0.0.6 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	# dstat on VM 6
	./runner.sh -mtype dstat -dsmt svr -mno 1 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	# Servers on VM 6
	SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip6.westeurope.cloudapp.azure.com
	./runner.sh -mtype svr -mno 1 -pno 11211
	# Copy results
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip1.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client1res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip2.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client2res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip3.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client3res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip6.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/server1res
	# Merge results
	rsync -a /home/doruk/Desktop/client1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/client2res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/client3res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/server1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	# Remove temporary results
	rm -rf /home/doruk/Desktop/client1res/
	rm -rf /home/doruk/Desktop/client2res/
	rm -rf /home/doruk/Desktop/client3res/
	rm -rf /home/doruk/Desktop/server1res/

# CLIENT-SERVER BASELINE 2
	# Clients on VM 1
	SSH_AUTH_SOCK=0 cssh dcetin@storelrt4zinzjmismsshpublicip{1,1,6,7}.westeurope.cloudapp.azure.com
	./runner.sh -mtype cli -mno 1 -ipadd 10.0.0.6 -pno 11211 -nsvr 2 -ncli 1 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	./runner.sh -mtype cli -mno 2 -ipadd 10.0.0.5 -pno 11211 -nsvr 2 -ncli 1 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	# dstat on VMs 6,7
	./runner.sh -mtype dstat -dsmt svr -mno 1 -nsvr 2 -ncli 1 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	./runner.sh -mtype dstat -dsmt svr -mno 2 -nsvr 2 -ncli 1 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	# Servers on VMs 6,7
	SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip6.westeurope.cloudapp.azure.com
	./runner.sh -mtype svr -mno 1 -pno 11211
	SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip7.westeurope.cloudapp.azure.com
	./runner.sh -mtype svr -mno 2 -pno 11211
	# Copy results
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip1.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client1res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip6.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/server1res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip7.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/server2res
	# Merge results
	rsync -a /home/doruk/Desktop/client1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/server1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/server2res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	# Remove temporary results
	rm -rf /home/doruk/Desktop/client1res/
	rm -rf /home/doruk/Desktop/server1res/
	rm -rf /home/doruk/Desktop/server2res/

# MIDDLEWARE BASELINE 1
	# Clients on VMs 1,2,3
	SSH_AUTH_SOCK=0 cssh dcetin@storelrt4zinzjmismsshpublicip{1,2,3,4,6}.westeurope.cloudapp.azure.com
	./runner.sh -mtype cli -mno 1 -ipadd 10.0.0.10 -pno 1453 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 1 -tmw ~ -reps 3 -ttime 70
	./runner.sh -mtype cli -mno 2 -ipadd 10.0.0.10 -pno 1453 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 1 -tmw ~ -reps 3 -ttime 70
	./runner.sh -mtype cli -mno 3 -ipadd 10.0.0.10 -pno 1453 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 1 -tmw ~ -reps 3 -ttime 70
	# dstat on VMs 4,6
	./runner.sh -mtype dstat -dsmt mw -mno 1 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 1 -tmw ~ -reps 3 -ttime 70
	./runner.sh -mtype dstat -dsmt svr -mno 1 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 1 -tmw ~ -reps 3 -ttime 70
	# Middlewares on VM 4
	SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip4.westeurope.cloudapp.azure.com
	./runner.sh -mtype mw -mno 1 -ipadd 10.0.0.10 -pno 1453 -pairs 10.0.0.6:11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 1 -tmw ~ -reps 3 -ttime 70
	# Servers on VM 6
	SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip6.westeurope.cloudapp.azure.com
	./runner.sh -mtype svr -mno 1 -pno 11211
	# Copy results
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip1.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client1res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip2.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client2res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip3.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client3res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip4.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/mw1res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip6.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/server1res
	# Merge results
	rsync -a /home/doruk/Desktop/client1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/client2res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/client3res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/mw1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/server1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	# Remove temporary results
	rm -rf /home/doruk/Desktop/client1res/
	rm -rf /home/doruk/Desktop/client2res/
	rm -rf /home/doruk/Desktop/client3res/
	rm -rf /home/doruk/Desktop/mw1res/
	rm -rf /home/doruk/Desktop/server1res/

# MIDDLEWARE BASELINE 2
	# Clients on VMs 1,2,3
	SSH_AUTH_SOCK=0 cssh dcetin@storelrt4zinzjmismsshpublicip{1,1,2,2,3,3,4,5,6}.westeurope.cloudapp.azure.com
	./runner.sh -mtype cli -mno 1 -ipadd 10.0.0.10 -pno 1453 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	./runner.sh -mtype cli -mno 2 -ipadd 10.0.0.9 -pno 1453 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	./runner.sh -mtype cli -mno 3 -ipadd 10.0.0.10 -pno 1453 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	./runner.sh -mtype cli -mno 4 -ipadd 10.0.0.9 -pno 1453 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	./runner.sh -mtype cli -mno 5 -ipadd 10.0.0.10 -pno 1453 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	./runner.sh -mtype cli -mno 6 -ipadd 10.0.0.9 -pno 1453 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	# dstat on VMs 4,5,6
	./runner.sh -mtype dstat -dsmt mw -mno 1 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	./runner.sh -mtype dstat -dsmt mw -mno 2 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	./runner.sh -mtype dstat -dsmt svr -mno 1 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	# Middlewares on VMs 4,5
	SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip4.westeurope.cloudapp.azure.com
	./runner.sh -mtype mw -mno 1 -ipadd 10.0.0.10 -pno 1453 -pairs 10.0.0.6:11211 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip5.westeurope.cloudapp.azure.com
	./runner.sh -mtype mw -mno 2 -ipadd 10.0.0.9 -pno 1453 -pairs 10.0.0.6:11211 -nsvr 1 -ncli 3 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw 2 -tmw ~ -reps 3 -ttime 70
	# # Servers on VM 6
	# SSH_AUTH_SOCK=0 ssh dcetin@storelrt4zinzjmismsshpublicip6.westeurope.cloudapp.azure.com
	# ./runner.sh -mtype svr -mno 1 -pno 11211
	# # Copy results
	# SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip1.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client1res
	# SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip2.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client2res
	# SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip3.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client3res
	# SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip4.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/mw1res
	# SSH_AUTH_SOCK=0  scp -qr dcetin@storelrt4zinzjmismsshpublicip6.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/server1res
	# # Merge results
	# rsync -a /home/doruk/Desktop/client1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	# rsync -a /home/doruk/Desktop/client2res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	# rsync -a /home/doruk/Desktop/client3res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	# rsync -a /home/doruk/Desktop/mw1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	# rsync -a /home/doruk/Desktop/server1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	# # Remove temporary results
	# rm -rf /home/doruk/Desktop/client1res/
	# rm -rf /home/doruk/Desktop/client2res/
	# rm -rf /home/doruk/Desktop/client3res/
	# rm -rf /home/doruk/Desktop/mw1res/
	# rm -rf /home/doruk/Desktop/server1res/