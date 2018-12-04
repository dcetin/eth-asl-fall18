package ch.ethz.asltest;

import java.util.*;
import java.net.*;
import java.io.*;

//import org.apache.logging.log4j.LogManager;
//import org.apache.logging.log4j.Logger;

public class RequestData {
    public ClientData clientInfo;
    public int requestNumber;
    public long ns_netThreadReceived;
    public long ns_workerThreadReceived;
    public long ns_workerThreadFinished;
    public int reqType; // set: 0, get: 1, multi-get: 2
    public int cacheMisses;
    public int serverHandlerID;
    public int sentServer;
    public int itemsToGet;

    public RequestData(ClientData clientInfo, int requestNumber, long ns_netThreadReceived) {
    	this.clientInfo = clientInfo;
    	this.requestNumber = requestNumber;
    	this.ns_netThreadReceived = ns_netThreadReceived;

    	this.ns_workerThreadReceived = 0;
    	this.ns_workerThreadFinished = 0;
    	this.reqType = -1;
    	this.cacheMisses = 0;
    	this.serverHandlerID = -1;
    	this.sentServer = -1;
    	this.itemsToGet = 0;
    }
}