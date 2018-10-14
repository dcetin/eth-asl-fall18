package ch.ethz.asltest;

import java.util.*;
import java.net.*;
import java.io.*;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

//import org.apache.logging.log4j.LogManager;
//import org.apache.logging.log4j.Logger;

public class MyMiddleware {

	/*
	private static final Logger logger = LogManager.getLogger("HelloWorld");
    public static void main(String[] args) {
        logger.info("Hello, World!");
    }
	*/

	public String myIp;
	public int myPort;
	public List<String> mcAddresses;
	public int numThreadsPTP;
	public boolean readSharded;
	public static boolean verbose = true;
	private	List<String> ipArray = new ArrayList<String>();
	private	List<Integer> portArray = new ArrayList<Integer>();

	public MyMiddleware(String _myip, int _myport, List<String> _myaddresses, int _numthreadsptp, boolean _readsharded) {
		this.myIp = _myip;
		this.myPort = _myport;
		this.mcAddresses = _myaddresses;
		this.numThreadsPTP = _numthreadsptp;
		this.readSharded = _readsharded;	
	}

	public void run() throws IOException {
		System.out.println("MyMiddleware is running.");

		int portNumber = this.myPort;
		int clientNumber = -1;

		for (int i = 0; i < this.mcAddresses.size(); i++)
		{
			String cur_add = mcAddresses.get(i);
			String[] split = cur_add.split(":");
			String cur_ip = split[0];
			Integer cur_port = Integer.parseInt(split[1]);
			
			ipArray.add(cur_ip);
			portArray.add(cur_port);
		}

		List<ClientData> clientDataList = Collections.synchronizedList(new ArrayList<ClientData>());
		BlockingQueue<RequestData> requestQueue = new LinkedBlockingQueue<RequestData>();

		ServerSocket welcomingSocket = new ServerSocket(portNumber);
        new clientHandler(clientDataList, requestQueue).start();

        for (int i = 0; i < this.numThreadsPTP; i++)
        {
        	new serverHandler(clientDataList, requestQueue, ipArray, portArray, readSharded, i).start();
        }

		try {
            while (true) {
            	try {
            		
	            	Socket clientConnection = welcomingSocket.accept(); //TODO: have to close these some time
					PrintWriter clientReplyStream = new PrintWriter(clientConnection.getOutputStream(), true);
					BufferedReader clientListenStream = new BufferedReader(new InputStreamReader(clientConnection.getInputStream()));
					clientNumber++;
	            	
					ClientData newClient = new ClientData(clientConnection, clientReplyStream, clientListenStream, clientNumber, false);

	            	clientDataList.add(newClient);

            	} catch (IOException e) {
					System.out.println(e.getMessage());
				}
            }
        } finally {
            welcomingSocket.close();
        }
	}

    private static class clientHandler extends Thread {
	    private List<ClientData> clientDataList;
	    private BlockingQueue<RequestData> requestQueue;
	    private int uniReqNum;

	    public clientHandler(List<ClientData> clientDataList, BlockingQueue<RequestData> requestQueue)
	    {
	    	this.clientDataList = clientDataList;
	    	this.requestQueue = requestQueue;
	    	this.uniReqNum = -1;
	    }

	    public void run() {

	    	while(true)
	    	{
	    		if(clientDataList.isEmpty() == false)
	    		{
	    			int listLen = clientDataList.size();
	    			for (int cl_i = 0; cl_i < listLen; cl_i++)
	    			{
	    				ClientData cl = clientDataList.get(cl_i);
						Socket clientConnection = cl.clientConnection;
			        	PrintWriter clientReplyStream = cl.clientReplyStream;
			        	BufferedReader clientListenStream = cl.clientListenStream;
			        	int clientNumber = cl.clientNumber;
			        	boolean sentItsRequest = cl.sentItsRequest;

						//Wait for client to send a query
						try {
							if (!sentItsRequest && clientListenStream.ready())
								{
									uniReqNum++;
									clientDataList.set(cl_i, new ClientData(clientConnection, clientReplyStream, clientListenStream, clientNumber, true));
									RequestData rq = new RequestData(cl, uniReqNum);

									try {
										requestQueue.put(rq);
										log("Job " + rq.requestNumber + " queued.");
									} catch (InterruptedException e) {
										System.out.println(e.getMessage());
									}
								}
								else
								{
									// No awaiting messages, will listen the next socket.
								}
							} catch (IOException e) {
								System.out.println(e.getMessage());
							}
	    			}
	    		}
	    		else
    			{
    				// No awaiting clients.
    			}
			}
	    }

	    private void log(String message) {
	        System.out.println(message);
	    }
	}

	private static class serverHandler extends Thread {
	    private List<ClientData> clientDataList;
	    private BlockingQueue<RequestData> requestQueue;
	    private int serverHandlerID;
	    private List<String> ipArray;
	    private List<Integer> portArray;
	    private Integer curGetServer;
	    private Integer serverCount;
	    private boolean readSharded;

	    private	List<Socket> serverSocketList = new ArrayList<Socket>();
	    private	List<PrintWriter> serverSendStreamList = new ArrayList<PrintWriter>();
	    private	List<BufferedReader> serverListenStreamList = new ArrayList<BufferedReader>();

	    private Socket serverSocket;
	    private PrintWriter serverSendStream;
	    private BufferedReader serverListenStream;

	    public serverHandler(List<ClientData> clientDataList, BlockingQueue<RequestData> requestQueue, 
	    	List<String> ipArray, List<Integer> portArray, boolean readSharded, int serverHandlerID)
	    {
	    	this.clientDataList = clientDataList;
	    	this.requestQueue = requestQueue;
	    	this.serverHandlerID = serverHandlerID;
	    	this.ipArray = ipArray;
			this.portArray = portArray;
			this.readSharded = readSharded;

			this.curGetServer = 0;
			this.serverCount = ipArray.size();
	    }

	    public void run() {
	    	try
	    	{
	    		for (int i = 0; i < serverCount; i++)
		    	{
		    		serverSocket = new Socket(ipArray.get(i), portArray.get(i));
					serverSendStream = new PrintWriter(serverSocket.getOutputStream(), true);
					serverListenStream = new BufferedReader(new InputStreamReader(serverSocket.getInputStream()));

					serverSocketList.add(serverSocket);
					serverSendStreamList.add(serverSendStream);
					serverListenStreamList.add(serverListenStream);
	    		}

		    	while(true)
		    	{
					try
					{
			    		RequestData rq = requestQueue.take();
			    		ClientData cl = rq.clientInfo;
						Socket clientConnection = cl.clientConnection;
			        	PrintWriter clientReplyStream = cl.clientReplyStream;
			        	BufferedReader clientListenStream = cl.clientListenStream;
			        	int clientNumber = cl.clientNumber;
			        	boolean sentItsRequest = cl.sentItsRequest;
						
						String inputLine;
						String answerLine1 = "";
						String answerLine2;
						String answerLine3;
						String data;
						String replyLine;

						inputLine = clientListenStream.readLine();
						if (inputLine != null)
						{
				        	//TODO: if you open the socket at the very beginning it fucks up the throughput, which currently is fucked up indeed

							if(verbose)
							{
								log("Thread #" + String.valueOf(serverHandlerID));
								log("C" + clientNumber + ": ->|   " + inputLine);
							}
							String[] queryArr = inputLine.split(" ");
							//SET Request
							
							if(queryArr[0].equals("set"))
							{
								data = clientListenStream.readLine();
								if(verbose) 
									log("C" + clientNumber + ": ->|   " + data);

								for(int i = 0; i< serverCount; i++) {
									serverSocket = serverSocketList.get(i);
									serverSendStream = serverSendStreamList.get(i);
									serverListenStream = serverListenStreamList.get(i);

									//Relay the query to server
									serverSendStream.println(inputLine + "\r");
									if(verbose) 
										log("S" + i + ":   |-> " + inputLine);
									serverSendStream.println(data + "\r");
									if(verbose) 
										log("S" + i + ":   |-> " + data);
									serverSendStream.flush();
									//Wait for server to send a reply
									answerLine1 = serverListenStream.readLine();
									if(verbose) 
										log("S" + i + ":   |<- " + answerLine1);

									if (!answerLine1.equals("STORED"))
										break;
								}

								//Relay the reply to the client
								if (answerLine1.equals("STORED"))
									replyLine = "STORED";
								else
									replyLine = answerLine1;
								clientReplyStream.println(replyLine + "\r");
								if(verbose) 
									log("C" + clientNumber + ": <-|   " + replyLine);
							}
							
							//GET Request
							else if(queryArr[0].equals("get"))
							{
								Integer itemsToGet = queryArr.length - 1;
								if(itemsToGet == 1 || (readSharded && serverCount == 1) || !readSharded)
								{
									serverSocket = serverSocketList.get(curGetServer);
									serverSendStream = serverSendStreamList.get(curGetServer);
									serverListenStream = serverListenStreamList.get(curGetServer);

									//Relay the query to server
									serverSendStream.println(inputLine);
									if(verbose) 
										log("S" + curGetServer + ":   |-> " + inputLine + "\r");
									serverSendStream.flush();

									//Wait for server to send a reply
									answerLine1 = serverListenStream.readLine();
									if(verbose) 
										log("S" + curGetServer + ":   |<- " + answerLine1);
									//If the answer is just END
									if(answerLine1.equals("END")) {
										clientReplyStream.println(answerLine1 + "\r");
										if(verbose) 
											log("C" + clientNumber + ": <-|   " + answerLine1);
									}
									else {
										answerLine2 = serverListenStream.readLine();
										if(verbose) 
											log("S" + curGetServer + ":   |<- " + answerLine2);
										answerLine3 = serverListenStream.readLine();
										if(verbose) 
											log("S" + curGetServer + ":   |<- " + answerLine3);
										clientReplyStream.println(answerLine1 + "\r");
										if(verbose) 
											log("C" + clientNumber + ": <-|   " + answerLine1);
										clientReplyStream.println(answerLine2 + "\r");
										if(verbose) 
											log("C" + clientNumber + ": <-|   " + answerLine2);
										clientReplyStream.println(answerLine3 + "\r");
										if(verbose) 
											log("C" + clientNumber + ": <-|   " + answerLine3);
									}
									//Proceed with the round robin
									curGetServer = (curGetServer == serverCount - 1) ? 0 : curGetServer+1;
								}
								else
								{
									//Sharded GET request with multiple servers
									Integer remainingItems = itemsToGet;
									List<Integer> itemSplit = new ArrayList<Integer>();
									for (int i = 0; i < serverCount; i++) {
										Integer newItems = remainingItems / (serverCount - i);
										itemSplit.add(newItems);
										remainingItems -= newItems;
									}
									Integer baseIdx = 1;
									List<String> getArray = new ArrayList<String>();
									for (int i = 0; i < serverCount; i++) {
										Integer thisBatch = itemSplit.get(i);
										String req = "get";
										for (int k = baseIdx; k < baseIdx + thisBatch; k++) {
											req = req + " " + queryArr[k];
										}
										getArray.add(req);
										baseIdx += thisBatch;
									}

									for (int i = 0; i < serverCount; i++) {
										inputLine = getArray.get(i);
										log(inputLine);

										serverSocket = serverSocketList.get(curGetServer);
										serverSendStream = serverSendStreamList.get(curGetServer);
										serverListenStream = serverListenStreamList.get(curGetServer);

										//Relay the query to server
										serverSendStream.println(inputLine);
										if(verbose) 
											log("S" + curGetServer + ":   |-> " + inputLine + "\r");
										serverSendStream.flush();

										//Wait for server to send a reply
										while (true) {
											answerLine1 = serverListenStream.readLine();
											if(answerLine1.equals("END"))
												break;
											if(verbose) 
												log("S" + curGetServer + ":   |<- " + answerLine1);
											clientReplyStream.println(answerLine1 + "\r");
											if(verbose) 
												log("C" + clientNumber + ": <-|   " + answerLine1);
										}
										//Proceed with the round robin
										curGetServer = (curGetServer == serverCount - 1) ? 0 : curGetServer+1;
									}
									clientReplyStream.println("END" + "\r");
									if(verbose) 
										log("C" + clientNumber + ": <-|   " + "END");
								}
							}
							else
							{
								log("Received " + queryArr[0]);
							}
							clientDataList.set(clientNumber, new ClientData(clientConnection, clientReplyStream, clientListenStream, clientNumber, false));
						}
						else
						{
							log(clientNumber + ": Received EOL");
						}
					} catch (InterruptedException e) {
						System.out.println(e.getMessage());
					}
		    	}
	    	} catch (IOException e) {
				System.out.println(e.getMessage());
			}
	    }

	    private void log(String message) {
	        System.out.println(message);
	    }
	}
}