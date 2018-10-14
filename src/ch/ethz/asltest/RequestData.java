package ch.ethz.asltest;

import java.util.*;
import java.net.*;
import java.io.*;

//import org.apache.logging.log4j.LogManager;
//import org.apache.logging.log4j.Logger;

public class RequestData {
    public ClientData clientInfo;
    public int requestNumber;

    public RequestData(ClientData clientInfo, int requestNumber) {
    	this.clientInfo = clientInfo;
    	this.requestNumber = requestNumber;
    }
}