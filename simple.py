import ipaddress
import socket
import argparse
import time
import threading
import sys


def check_port(val):
    try:
        value = int(val)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')
    if not(1024 <=value <=65535 ):
        print('it is not a valid port')
        sys.exit()
    return value
def check_ip(address):# sjekker om adress er valid IPv4 address
    try:
       val = ipaddress.ip_address(address)
       print(f"The IP address {val} is valid.")
    except ValueError:
       print(f"The IP address is {address} not valid")
# definerer en funksjon for å sjekke om duration gitt er større enn 0.
def check_time(val):
    try:
        value = int(val)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer')
    if not value > 0:
        print('it is not a valid time')
        sys.exit
    return value       

def handle_client(conn,addr):
    print(f"Connected by {addr}")
    start_time = time.time()
    antall_bytes = 0
    bandwidth = 0

    while True: 
       
        try:
            data = conn.recv(1000)
        except:
            break
        #print(data) 
        if  data.decode() == "FINISH" :
            break 

        antall_bytes += len(data)
        #print(antall_bytes)
        end_time  = time.time()
        total_duration = end_time - start_time 

        #print(total_duration)

        if total_duration>0:
            if args.format == "KB":
                 antall_bytes = antall_bytes / 1000
            elif args.format == "MB":
                antall_bytes = antall_bytes / 1000000
            bandwidth = (antall_bytes / 1000000)/  total_duration
       
        try:
            conn.send("ACK".encode())
        except:
            conn.close()
    print("ID Interval Received Rate")                                             
    print("{} 0.0 - {:.1f} {:.0f} MB {:.2f} Mbps".format(addr[0]+":"+str(addr[1]), total_duration,antall_bytes/1000000,bandwidth))    
    conn.close()       
            
def server(ip,port):
     sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
     try:
       sock.bind((ip,port))
     except:
        print("Bind failed. Error : ")
           
     sock.listen(2)
     print("-" * 45)
     print("A simpleperf server is listening on port",port)
     print("-" * 45)
     while True:
            conn,addr = sock.accept()
            print("-" * 45)
            print("A simpleperf client with {}:{} is connected with {}:{}".format(addr[0],addr[1],ip,port))#
            print("-" * 45)
            client_thread = threading.Thread(target=handle_client,args=(conn,addr))# Vi oppretter en tråd ved hjelp av target og args
            client_thread.start()# Starter tråden
          
def client(serverip, port,duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((serverip, port))
    except:
        print("ConnectionError")
    
    print(" A simpleperf client Client connecting to server {}, port {}".format(serverip, port))
    start_time = time.time()
    total_bytes = 0
    while True: 
        data = "0" * 1000
        sock.send(data.encode())
        total_bytes += len(data)
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            sock.send("FINISH".encode())
            break
        sock.recv(1000).decode()
    #sock.close() # har lagt til denne sammenlignet med forrige kode
    end_time = time.time()
    total_duration = end_time - start_time
    bandwidth = (total_bytes / 1000000)/ total_duration
    print("Client connected with server {},port{}".format(serverip,port))
    print("ID Interval Transfer Bandwidth")
    print("{} 0.0 - {:.1f} {:.0f} MB {:.2f}Mbps".format(sock.getsockname()[0]+":"+str(sock.getsockname()[1]),total_duration, total_bytes/1000000, bandwidth))
if __name__ == '__main__':
            parser = argparse.ArgumentParser(description='Simple network throughput measurement tool')
            group = parser.add_mutually_exclusive_group(required=True)
            group.add_argument('-s', '--server', action='store_true', help='Run in server mode')
            
            group.add_argument('-c', '--client', action='store_true', help='Run in client mode')
            parser.add_argument('-b', '--bind', type=str, default ='0.0.0.0', help='IP address of the server\'s interface where the client should connect')
            parser.add_argument('-I', '--serverip', type=str, default='127.0.0.1', help='IP address of the server')
            parser.add_argument('-p','--port',type=check_port,default=8088,help='Port number on which the server should listen or the client should connect')
            parser.add_argument('-f','--format',type=str,default='MB',help='choose the format of the summary of results KB or MB')
            parser.add_argument('-t','--time',type=int, default=25,help='the total duration in seconds for which data should be generated and sent to the server and must be >0')
            parser.add_argument('-P','--parallel',type=int,default=1,help='creates parallel connections to cennect to the server and send data - it must be 2 and the max value should be 5-')
            parser.add_argument('-n','--num',type=str,help='transfer number of bytes specified by -n falg,it should be either in B,KB or MB')
            parser.add_argument('-i','--interval',type= check_time,help='print statistics per z second')

            args = parser.parse_args()
            port = args.port
            ip=args.bind
            serverip =args.serverip
            duration=args.time
            parallel=args.parallel
            if args.server:
                check_ip(ip)
                server (ip,port)
            elif args.client:
                 client(serverip,port,duration)
                     
                 








              
















        

