package ch.ethz.asltest;

import java.util.*;
import java.net.*;
import java.io.*;

//import org.apache.logging.log4j.LogManager;
//import org.apache.logging.log4j.Logger;

public class ClientData {
    public Socket clientConnection;
    public PrintWriter clientReplyStream;
    public BufferedReader clientListenStream;
    public Integer clientNumber;
    public boolean sentItsRequest;

    public ClientData(Socket clientConnection, PrintWriter clientReplyStream, 
    	BufferedReader clientListenStream, Integer clientNumber, boolean sentItsRequest) {
    	this.clientConnection = clientConnection;
    	this.clientReplyStream = clientReplyStream;
    	this.clientListenStream = clientListenStream;
    	this.clientNumber = clientNumber;
        this.sentItsRequest = sentItsRequest;
    }
}