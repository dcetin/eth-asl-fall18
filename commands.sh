# CONNECTION
	# SSH commands for each VM
	Client 1:		SSH_AUTH_SOCK=0 ssh dcetin@storej3ybtf5b6wunqsshpublicip1.westeurope.cloudapp.azure.com
	Client 2:		SSH_AUTH_SOCK=0 ssh dcetin@storej3ybtf5b6wunqsshpublicip2.westeurope.cloudapp.azure.com
	Client 3:		SSH_AUTH_SOCK=0 ssh dcetin@storej3ybtf5b6wunqsshpublicip3.westeurope.cloudapp.azure.com
	Middleware 1:	SSH_AUTH_SOCK=0 ssh dcetin@storej3ybtf5b6wunqsshpublicip4.westeurope.cloudapp.azure.com
	Middleware 2:	SSH_AUTH_SOCK=0 ssh dcetin@storej3ybtf5b6wunqsshpublicip5.westeurope.cloudapp.azure.com
	Server 1:		SSH_AUTH_SOCK=0 ssh dcetin@storej3ybtf5b6wunqsshpublicip6.westeurope.cloudapp.azure.com
	Server 2:		SSH_AUTH_SOCK=0 ssh dcetin@storej3ybtf5b6wunqsshpublicip7.westeurope.cloudapp.azure.com
	Server 3:		SSH_AUTH_SOCK=0 ssh dcetin@storej3ybtf5b6wunqsshpublicip8.westeurope.cloudapp.azure.com
	# SSH commancds for each set of VMs
	clients:	SSH_AUTH_SOCK=0 cssh dcetin@storej3ybtf5b6wunqsshpublicip{1,2,3}.westeurope.cloudapp.azure.com
	mws:		SSH_AUTH_SOCK=0 cssh dcetin@storej3ybtf5b6wunqsshpublicip{4,5}.westeurope.cloudapp.azure.com
	servers:	SSH_AUTH_SOCK=0 cssh dcetin@storej3ybtf5b6wunqsshpublicip{6,7,8}.westeurope.cloudapp.azure.com
	# IP addresses for each VM
	Client 1 (1):		10.0.0.6
	Client 2 (2):		10.0.0.10
	Client 3 (3):		10.0.0.7
	Middleware 1 (4):	10.0.0.4
	Middleware 2 (5):	10.0.0.11
	Server 1 (6):		10.0.0.5
	Server 2 (7):		10.0.0.9
	Server 3 (8):		10.0.0.8

# GENERAL PURPOSE
	# Clone git repo
	git clone https://gitlab.ethz.ch/dcetin/asl-fall18-project.git
	# Check the number of threads in memcached server
	echo -e 'stats\r\nquit' | nc 0.0.0.0 11211 | grep "threads"

# BASELINE 1
	# Clients
	SSH_AUTH_SOCK=0 cssh dcetin@storej3ybtf5b6wunqsshpublicip{1,2,3}.westeurope.cloudapp.azure.com
	./runner.sh -mtype cli -mno 1 -ipadd 10.0.0.5 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	./runner.sh -mtype cli -mno 2 -ipadd 10.0.0.5 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	./runner.sh -mtype cli -mno 3 -ipadd 10.0.0.5 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	# Servers
	SSH_AUTH_SOCK=0 ssh dcetin@storej3ybtf5b6wunqsshpublicip6.westeurope.cloudapp.azure.com
	./runner.sh -mtype svr -mno 1 -pno 11211 -nsvr 1 -ncli 3 -icli 1 -tcli 2 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	# Copy results
	SSH_AUTH_SOCK=0  scp -qr dcetin@storej3ybtf5b6wunqsshpublicip1.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client1res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storej3ybtf5b6wunqsshpublicip2.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client2res
	SSH_AUTH_SOCK=0  scp -qr dcetin@storej3ybtf5b6wunqsshpublicip3.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client3res
	# Merge results
	rsync -a /home/doruk/Desktop/client1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/client2res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	rsync -a /home/doruk/Desktop/client3res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	# Remove temporary results
	rm -rf /home/doruk/Desktop/client1res/
	rm -rf /home/doruk/Desktop/client2res/
	rm -rf /home/doruk/Desktop/client3res/
	# Remove results permanently
	rm -rf /home/doruk/Desktop/asl/asl-fall18-project/res/

# BASELINE 2
	# Clients
	SSH_AUTH_SOCK=0 cssh dcetin@storej3ybtf5b6wunqsshpublicip{1,1}.westeurope.cloudapp.azure.com
	./runner.sh -mtype cli -mno 1 -ipadd 10.0.0.5 -pno 11211 -nsvr 2 -ncli 1 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	./runner.sh -mtype cli -mno 2 -ipadd 10.0.0.9 -pno 11211 -nsvr 2 -ncli 1 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	# Servers
	SSH_AUTH_SOCK=0 cssh dcetin@storej3ybtf5b6wunqsshpublicip{6,7}.westeurope.cloudapp.azure.com
	./runner.sh -mtype svr -mno 1 -pno 11211 -nsvr 2 -ncli 1 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	./runner.sh -mtype svr -mno 2 -pno 11211 -nsvr 2 -ncli 1 -icli 2 -tcli 1 -vcli ~ -wrkld ~ -mgshrd NA -mgsize NA -nmw NA -tmw NA -reps 3 -ttime 100
	# Copy results
	SSH_AUTH_SOCK=0  scp -qr dcetin@storej3ybtf5b6wunqsshpublicip1.westeurope.cloudapp.azure.com:/home/dcetin/asl-fall18-project/res /home/doruk/Desktop/client1res
	# Merge results
	rsync -a /home/doruk/Desktop/client1res/ /home/doruk/Desktop/asl/asl-fall18-project/res/
	# Remove temporary results
	rm -rf /home/doruk/Desktop/client1res/
	# Remove results permanently
	rm -rf /home/doruk/Desktop/asl/asl-fall18-project/res/
