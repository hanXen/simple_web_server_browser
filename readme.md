# Simple Web Server/Browser

## Usage

#### webserver.py
```bash
> python3 webserver.py
```
#### webclient.py
```bash
> python3 webclient.py
> input host:port ex) 127.0.0.1:50007 : [host:port]
```

## Implements 
 - Implement the GET method. The client only sends a HTTP request message with the GET method to acquire the target resource identified by a URL and the server responds to it with the content of the target resource.
 - Implement the status codes 200, 400, and 404 on server. 
 - Contain both the ‘Host’, ‘Content-Length’, and ‘Connection’ header fields. Each header is interpreted by server. 
 - Client and server are able to establish a HTTP keep-alive connection by the ‘Connection’ header as below:
    ```
    (Request headers)    
    GET /html/rfc2616 HTTP/1.1   
    Host: tools.ietf.org   
    Connection: keep-alive   
    …  
    ```
-  Web server is able to work with multiple clients simultaneously. It means, when one client has a keep-alive connection with the server, the server is able to handle other requests from other clients. 

## Web application scenarios

1. The client firstly reads the server’s IP address ( e.g. , 163.152.6.10) from the command line and performs the GET method to the server with root path ( i.e. , /). 
 
2. The server reads the HTTP GET request from the client ( i.e. , GET / HTTP/1.1) and responds to it with the content of ```index.html```. 
    ```
    <!--index.html--> 
    <html> 
    <head>     
        <title>Simple HTML</title>     
        <script src="app.js"></script>     
        <script src="app2.js"></script>     
        <script src="app3.js"></script>     
        <link rel="stylesheet" href="style.css"> 
    </head> 
    <body> 
    Hello, World! 
    </body> 
    </html>
    ```

3. The client, receiving the response from the server, parses the content of the index.html and requests the resources specified in the index.html file (in this scenario, there are app.js, app2.js, app3.js, and style.css). The server then responds to each request, respectively. In that moment, the client and the server maintain a keep-alive connection, so the sequence of request-responses is conducted over the same TCP connection. The resources, app1.js, app2.js, app3.js, and style.css, are given as follows: 

    ```
    //app.js 
    console.log("running app1"); 
    
    //app2.js 
    console.log("running app2"); 
    
    //app3.js 
    console.log("running app3"); 
    
    /* style.css */ 
    body {  
        margin: 20px;  
        font-family: Arial, sans-serif;  
        font-size: 40px;  
        background-color: #fff;  
        line-height: 1.3em; 
    }
    ```
