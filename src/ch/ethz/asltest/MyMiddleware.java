package ch.ethz.asltest;

import java.util.*;
import java.net.*;
import java.io.*;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import static java.util.concurrent.TimeUnit.*;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledFuture;

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
	// if true, will print the messages received and sent
	public static boolean verboseLogs = false;
	// if true, will print the info about finished requests
	public static boolean verboseAggr = true;
	// lists that store the addresses of the servers
	private	List<String> ipArray = new ArrayList<String>();
	private	List<Integer> portArray = new ArrayList<Integer>();
	// set the timeout limit for how long should the middleware wait before finishing
	private int timeoutSecs = 3;
	// inital delay and the period for the scheduled aggregator
	public static int initDelaySecs = 1;
	public static int periodSecs = 1;
	// separator for the output
	public static String sep = ",";

	public MyMiddleware(String _myip, int _myport, List<String> _myaddresses, int _numthreadsptp, boolean _readsharded) {
		this.myIp = _myip;
		this.myPort = _myport;
		this.mcAddresses = _myaddresses;
		this.numThreadsPTP = _numthreadsptp;
		this.readSharded = _readsharded;	
	}

	public void run() throws IOException {
		if(verboseLogs)
			System.out.println("MyMiddleware is running.");

		int portNumber = this.myPort;
		int clientNumber = -1;

		// parse the server addresses
		for (int i = 0; i < this.mcAddresses.size(); i++)
		{
			String cur_add = mcAddresses.get(i);
			String[] split = cur_add.split(":");
			String cur_ip = split[0];
			Integer cur_port = Integer.parseInt(split[1]);
			
			ipArray.add(cur_ip);
			portArray.add(cur_port);
		}

		// initialize the lists
		List<ClientData> clientDataList = Collections.synchronizedList(new ArrayList<ClientData>());
		BlockingQueue<RequestData> requestQueue = new LinkedBlockingQueue<RequestData>();
		BlockingQueue<RequestData> finishedQueue = new LinkedBlockingQueue<RequestData>();
		List<Integer> responseHistogram = Collections.synchronizedList(new ArrayList<Integer>());

		// initalize the server socket and the net thread
		ServerSocket welcomingSocket = new ServerSocket(portNumber);
		new clientHandler(clientDataList, requestQueue, finishedQueue, timeoutSecs, responseHistogram).start();

		// initialize the worker threads
		for (int i = 0; i < this.numThreadsPTP; i++)
		{
			new serverHandler(clientDataList, requestQueue, ipArray, portArray, readSharded, finishedQueue, i).start();
		}

		try {
			while (true) {
				try {
					// listen for incoming connections, create a new client object when a connection is established
					Socket clientConnection = welcomingSocket.accept(); // TODO: is System.exit() good enough?
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

	// given the timestamps, calculates the time interval for the specified factor, e.g. -9 for nanoseconds
	public static double interval(long ns_begin, long ns_end, int factor) {
		long elapsedTime = ns_end - ns_begin;
		return (double) elapsedTime / (Math.pow(10, 9 + factor) * 1.0);
	}

	// simple functions to log messages easier
	public static void log(String message) {
		System.out.println(message);
	}
	public static void log_double(double message) {
		System.out.println( String.valueOf(message) );
	}
	public static void log_int(int message) {
		System.out.println( String.valueOf(message) );
	}
	public static String itos(int message) {
		return String.valueOf(message);
	}
	public static String dtos(double message) {
		return String.valueOf(message);
	}
	public static String dtos2(double message) {
		//return String.format("%5.2e", message);
		return String.format("%.12f", message);
	}
	public static String reqtypestr(int message) {
		if(message == 0)
			return "S";
		else if(message == 1)
			return "G";
		else if(message == 2)
			return "M";
		else
			return "_";
	}

	// net thread. iterates over clients and pushes their requests to request queue
	private static class clientHandler extends Thread {
		private List<ClientData> clientDataList;
		private BlockingQueue<RequestData> requestQueue;
		private BlockingQueue<RequestData> finishedQueue;
		private int uniReqNum;
		private int timeoutSecs;
		private List<Integer> responseHistogram;

		public clientHandler(List<ClientData> clientDataList, BlockingQueue<RequestData> requestQueue, BlockingQueue<RequestData> finishedQueue, int timeoutSecs, List<Integer> responseHistogram)
		{
			this.finishedQueue = finishedQueue;
			this.clientDataList = clientDataList;
			this.requestQueue = requestQueue;
			this.uniReqNum = -1;
			this.timeoutSecs = timeoutSecs;
			this.responseHistogram = responseHistogram;
		}

		public void run() {

			long lastReqTime = 0;
			boolean firstReq = true;

			while(true)
			{
				// if at least one client has arrived
				if(clientDataList.isEmpty() == false)
				{
					if(firstReq)
					{
						if(verboseAggr)
						{
							log("STAT START");
							log("secs" + sep + "qlen" + sep + "thru" + sep + "msrt" + sep + "items" + sep + "nset" + sep + "nget" + sep + "nmget" + sep + "sqt" + sep + "gqt" + sep + "mqt" + sep + "swt" + sep + "gwt" + sep + "mwt");
						}
						new ScheduledControl(clientDataList, requestQueue, finishedQueue, initDelaySecs, periodSecs, responseHistogram).runCheck();
						firstReq = false;
					}

					int listLen = clientDataList.size();
					long curTime = System.nanoTime();
					double seconds = interval(lastReqTime, curTime, 0);

					// check to see if any query has been recently made
					if (lastReqTime != 0 && seconds >= timeoutSecs)
					{
						// no requests have been made for quite some time, prepare to shut the system
						try {
							if(verboseLogs)
								log("Haven't received new requests for " + String.valueOf(seconds) + " seconds, shutting down...");
							for (int cl_i = 0; cl_i < listLen; cl_i++)
							{
								ClientData cl = clientDataList.get(cl_i);
								Socket clientConnection = cl.clientConnection;
								PrintWriter clientReplyStream = cl.clientReplyStream;
								BufferedReader clientListenStream = cl.clientListenStream;
								clientConnection.close();
								clientReplyStream.close();
								clientListenStream.close();
							}
						} catch (IOException e) {
							System.out.println(e.getMessage());
						}
						break;
					}

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
									// record the time net thread receives the request, it also comes in handy for the timeout case
									lastReqTime = System.nanoTime();
									uniReqNum++;
									clientDataList.set(cl_i, new ClientData(clientConnection, clientReplyStream, clientListenStream, clientNumber, true));
									RequestData rq = new RequestData(cl, uniReqNum, lastReqTime);

									try {
										requestQueue.put(rq);
										if(verboseLogs)
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

			// out of the while loop, net thread will finish soon enough
			if(verboseAggr)
			{
				log("STAT END");
				log("HIST START");
				int nbins = responseHistogram.size();
				//log("Latency (<= 100mirosec),Count");
				log_int(nbins);
				for (int i = 0; i < nbins; i++) {
					log("   " + String.valueOf(i) + " " + String.valueOf(responseHistogram.get(i)));
				}
				log("HIST END");
			}	
			// finish process, killing all the other threads
			if(verboseLogs)
				log("Killing all threads...");
			System.exit(0);
		}
	}

	// worker threads. pop requests from the queue and execute the queries
	private static class serverHandler extends Thread {
		private List<ClientData> clientDataList;
		private BlockingQueue<RequestData> requestQueue;
		private BlockingQueue<RequestData> finishedQueue;
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
			List<String> ipArray, List<Integer> portArray, boolean readSharded, BlockingQueue<RequestData> finishedQueue, int serverHandlerID)
		{
			this.clientDataList = clientDataList;
			this.requestQueue = requestQueue;
			this.serverHandlerID = serverHandlerID;
			this.ipArray = ipArray;
			this.portArray = portArray;
			this.readSharded = readSharded;
			this.finishedQueue = finishedQueue;

			this.curGetServer = 0;
			this.serverCount = ipArray.size();
		}

		public void run() {
			try
			{
				// establish dedicated connections for each server
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
						// pop a request from the queue
						RequestData rq = requestQueue.take();
						// record the time worker thread receives the request
						long ns_workerThreadReceived = System.nanoTime();
						rq.ns_workerThreadReceived = ns_workerThreadReceived;
						ClientData cl = rq.clientInfo;
						Socket clientConnection = cl.clientConnection;
						PrintWriter clientReplyStream = cl.clientReplyStream;
						BufferedReader clientListenStream = cl.clientListenStream;
						int clientNumber = cl.clientNumber;
						boolean sentItsRequest = cl.sentItsRequest;
						rq.serverHandlerID = serverHandlerID;

						String inputLine;
						String answerLine1 = "";
						String data;
						String replyLine = "STORED";
						int curCacheMisses = 0;

						inputLine = clientListenStream.readLine();
						if (inputLine != null)
						{
							if(verboseLogs)
							{
								log("Thread #" + String.valueOf(serverHandlerID));
								log("C" + clientNumber + ": ->|   " + inputLine);
							}
							// parse the request
							String[] queryArr = inputLine.split(" ");
							// it's a SET Request
							if(queryArr[0].equals("set"))
							{
								// mark the request type as SET
								rq.reqType = 0;
								rq.sentServer = -1;
								data = clientListenStream.readLine();
								if(verboseLogs) 
									log("C" + clientNumber + ": ->|   " + data);
								// send the query to each server
								for(int i = 0; i< serverCount; i++) {
									serverSocket = serverSocketList.get(i);
									serverSendStream = serverSendStreamList.get(i);
									serverListenStream = serverListenStreamList.get(i);
									//Relay the query to server
									serverSendStream.println(inputLine + "\r");
									if(verboseLogs) 
										log("S" + i + ":   |-> " + inputLine);
									serverSendStream.println(data + "\r");
									if(verboseLogs) 
										log("S" + i + ":   |-> " + data);
									serverSendStream.flush();
									//Wait for server to send a reply
									answerLine1 = serverListenStream.readLine();
									if(verboseLogs) 
										log("S" + i + ":   |<- " + answerLine1);
									// if it is non successful, we will reply with the most recent error message
									if (!answerLine1.equals("STORED"))
										replyLine = answerLine1;
								}
								// eelay the reply to the client, it's either and error message or it is STORED
								clientReplyStream.println(replyLine + "\r");
								if(verboseLogs) 
									log("C" + clientNumber + ": <-|   " + replyLine);
								clientReplyStream.flush();
							}
							// it's a GET Request
							else if(queryArr[0].equals("get"))
							{
								// count how many items are queired
								Integer itemsToGet = queryArr.length - 1;
								rq.itemsToGet = itemsToGet;
								// mark the request type as GET or MULTI-GET
								rq.reqType = (itemsToGet == 1) ? 1 : 2;
								// this will be useful when counting cache misses
								int nonEndLinesReceived = 0;
								// if it's a simple GET request OR mode is sharded read but there's only one server
								// OR mode is non-sharded read proceed to send the request to one server only
								if(itemsToGet == 1 || (readSharded && serverCount == 1) || !readSharded)
								{
									rq.sentServer = curGetServer;
									serverSocket = serverSocketList.get(curGetServer);
									serverSendStream = serverSendStreamList.get(curGetServer);
									serverListenStream = serverListenStreamList.get(curGetServer);
									// relay the query to server
									serverSendStream.println(inputLine);
									if(verboseLogs) 
										log("S" + curGetServer + ":   |-> " + inputLine + "\r");
									serverSendStream.flush();
									// wait for server to send a reply
									while (true) {
										answerLine1 = serverListenStream.readLine();
										// if it is an END message, server does not have any more to say
										if(answerLine1.equals("END"))
											break;
										// count the number of non-END lines
										nonEndLinesReceived++;
										if(verboseLogs)
											log("S" + curGetServer + ":   |<- " + answerLine1);
										clientReplyStream.println(answerLine1 + "\r");
										if(verboseLogs)
											log("C" + clientNumber + ": <-|   " + answerLine1);
									}
									clientReplyStream.flush();
									//Proceed with the round robin
									curGetServer = (curGetServer == serverCount - 1) ? 0 : curGetServer+1;
									// calculate the cache misses for this query
									curCacheMisses = itemsToGet - nonEndLinesReceived / 2;
									rq.cacheMisses += curCacheMisses;
									clientReplyStream.println("END" + "\r");
									if(verboseLogs) 
										log("C" + clientNumber + ": <-|   " + "END");
									if(verboseLogs) 
										log(String.valueOf(curCacheMisses) + " cache misses.");
									clientReplyStream.flush();
								}
								else
								{
									rq.sentServer = -1;
									//Sharded GET request with multiple servers
									Integer remainingItems = itemsToGet;
									// parse the query keys
									List<Integer> itemSplit = new ArrayList<Integer>();
									for (int i = 0; i < serverCount; i++) {
										Integer newItems = remainingItems / (serverCount - i);
										itemSplit.add(newItems);
										remainingItems -= newItems;
									}
									Integer baseIdx = 1;
									List<String> getArray = new ArrayList<String>();
									// create new multi get requests
									for (int i = 0; i < serverCount; i++) {
										Integer thisBatch = itemSplit.get(i);
										String req = "get";
										for (int k = baseIdx; k < baseIdx + thisBatch; k++) {
											req = req + " " + queryArr[k];
										}
										getArray.add(req);
										baseIdx += thisBatch;
									}
									// send the newly created requests to each server, continuing the round robin
									for (int i = 0; i < serverCount; i++) {
										inputLine = getArray.get(i);
										serverSocket = serverSocketList.get(curGetServer);
										serverSendStream = serverSendStreamList.get(curGetServer);
										serverListenStream = serverListenStreamList.get(curGetServer);
										//Relay the query to server
										serverSendStream.println(inputLine);
										if(verboseLogs) 
											log("S" + curGetServer + ":   |-> " + inputLine + "\r");
										serverSendStream.flush();
										//Wait for server to send a reply
										while (true) {
											answerLine1 = serverListenStream.readLine();
											// if it is an END message, server does not have any more to say
											if(answerLine1.equals("END"))
												break;
											// count the number of non-END lines
											nonEndLinesReceived++;
											if(verboseLogs)
												log("S" + curGetServer + ":   |<- " + answerLine1);
											clientReplyStream.println(answerLine1 + "\r");
											if(verboseLogs)
												log("C" + clientNumber + ": <-|   " + answerLine1);
										}
										clientReplyStream.flush();
										//Proceed with the round robin
										curGetServer = (curGetServer == serverCount - 1) ? 0 : curGetServer+1;
									}
									// calculate the cache misses for this query
									curCacheMisses = itemsToGet - nonEndLinesReceived / 2;
									rq.cacheMisses += curCacheMisses;
									clientReplyStream.println("END" + "\r");
									if(verboseLogs) 
										log("C" + clientNumber + ": <-|   " + "END");
									if(verboseLogs)
										log(String.valueOf(curCacheMisses) + " cache misses.");
									clientReplyStream.flush();
								}
							}
							// erroneous request for this middleware
							else
							{
								log("Received " + queryArr[0]);
							}
							// unmark the client, so that it can send other requests through net thread
							clientDataList.set(clientNumber, new ClientData(clientConnection, clientReplyStream, clientListenStream, clientNumber, false));
						}
						else
						{
							log(clientNumber + ": Received EOL");
						}
						// record the time when the execution finished
						long ns_workerThreadFinished = System.nanoTime();
						rq.ns_workerThreadFinished = ns_workerThreadFinished;
						finishedQueue.put(rq);

					} catch (InterruptedException e) {
						System.out.println(e.getMessage());
					}
				}

			} catch (IOException e) {
				System.out.println(e.getMessage());
			}
		}
	}

	// scheduled thread that iterates over the finished requests and aggregates them
	private static class ScheduledControl {
		// TODO: currently calculates misses for every get inside multigets
		// TODO: currently calculates throghput not for gets inside multigets
		private List<ClientData> clientDataList;
		private BlockingQueue<RequestData> requestQueue;
		private BlockingQueue<RequestData> finishedQueue;
		private int initDelaySecs;
		private int periodSecs;
		private int newItems;
		private int totalTime;
		private List<Integer> responseHistogram;

		public ScheduledControl(List<ClientData> clientDataList, BlockingQueue<RequestData> requestQueue, BlockingQueue<RequestData> finishedQueue, int initDelaySecs, int periodSecs, List<Integer> responseHistogram)
		{
			this.finishedQueue = finishedQueue;
			this.clientDataList = clientDataList;
			this.requestQueue = requestQueue;
			this.initDelaySecs = initDelaySecs;
			this.periodSecs = periodSecs;
			this.newItems = 0;
			this.totalTime = initDelaySecs;
			this.responseHistogram = responseHistogram;
		}

	    private final ScheduledExecutorService scheduler =
	       Executors.newScheduledThreadPool(1);

	    public void runCheck() {
	        final Runnable aggregator = new Runnable() {
	                public void run()
	                {
	                	// TODO: run dstat, iperf or such
						// iterate over the finished requests
						newItems = finishedQueue.size();
						// iterate over finished requests
						int n_set = 0;
						int n_get = 0;
						int n_mget = 0;
						int n_miss = 0;
						int n_item = 0;
						double set_queuetime = 0;
						double set_worktime = 0;
						double get_queuetime = 0;
						double get_worktime = 0;
						double mget_queuetime = 0;
						double mget_worktime = 0;

						try
						{
							for (int i = 0; i < newItems; i++) {
								RequestData rq = finishedQueue.take();
								double queuetime = interval(rq.ns_netThreadReceived, rq.ns_workerThreadReceived, 0);
								double worktime = interval(rq.ns_workerThreadReceived, rq.ns_workerThreadFinished, 0);

								double responseTime = (queuetime + worktime); // in seconds
								responseTime = responseTime * Math.pow(10, 6); // in microseconds
								int newIdx = (int)responseTime / 100;
								while(responseHistogram.size() < newIdx + 1)
									responseHistogram.add(0);
								responseHistogram.set(newIdx, responseHistogram.get(newIdx)+1);

								//if (verboseAggr)
								//	log(itos(rq.requestNumber) + sep + itos(rq.serverHandlerID) + sep + itos(rq.sentServer));

								n_miss += rq.cacheMisses;
								n_item += rq.itemsToGet;
								if (rq.reqType == 0)
								{
									n_set++;
									set_worktime += worktime;
									set_queuetime += queuetime;
								}
								else if (rq.reqType == 1)
								{
									n_get++;
									get_worktime += worktime;
									get_queuetime += queuetime;
								}
								else if (rq.reqType == 2)
								{
									n_mget++;
									mget_worktime += worktime;
									mget_queuetime += queuetime;
								}
							}
						} catch (InterruptedException e) {
							System.out.println(e.getMessage());
						}
						// average the values
						if(!(n_set == 0 && n_get == 0 && n_mget == 0))
						{
							double avg_set_queuetime = set_queuetime / n_set;
							double avg_set_worktime = set_worktime / n_set;
							double avg_get_queuetime = get_queuetime / n_get;
							double avg_get_worktime = get_worktime / n_get;
							double avg_mget_queuetime = mget_queuetime / n_mget;
							double avg_mget_worktime = mget_worktime / n_mget;
							double miss_ratio = (1.0 * n_miss) / n_item;

							double throughput = (newItems * 1.0) / periodSecs; // ops/sec
							if(verboseAggr)
								log(itos(totalTime) + sep + itos(requestQueue.size()) + sep + dtos2(throughput) + sep + dtos2(miss_ratio) + sep + n_item + sep + itos(n_set) + sep + itos(n_get) + sep + itos(n_mget) + sep + dtos2(avg_set_queuetime) + sep + dtos2(avg_get_queuetime) + sep + dtos2(avg_mget_queuetime) + sep + dtos2(avg_set_worktime) + sep + dtos2(avg_get_worktime) + sep + dtos2(avg_mget_worktime));
						}

						// for the next aggregation
						newItems = 0;
	                }
	            };

	        final ScheduledFuture<?> aggregatorHandle =
	            scheduler.scheduleAtFixedRate(aggregator, initDelaySecs, periodSecs, SECONDS); // initial delay, period, time unit
	        scheduler.schedule(new Runnable() {
	                public void run() { aggregatorHandle.cancel(true); }
	            }, 60 * 60, SECONDS);
	    }
 	}

}