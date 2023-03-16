import socket
import threading
import sys
import argparse
FORMAT="utf-8"

def check_port(val):
    try:
        value = int(val)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')
    if not(1024 <=value <=65535 ):
        print('it is not a valid port')
        sys.exit()
    return value


def handle_client(conn,addr,format):

    print(f"Connected by {addr}")#initiere ny connection

    connected=True
    while connected:# så lenge det er en connection fra en client
        msg = conn.recv(1000).decode(FORMAT)# her skal vi legge inn hvor mange bits vi kommer til å motta fra clienten, dette er blocking line of code ,som
                                            # betyr vi skal ikke kjøre this line of code før vi har mottat message fra clienten, dette er viktig
                                            # for å ikke hindre andre klienter i å ta connection
        if (msg== "exit" ):# dersom meldingen motatt er disconnect betyr at clienenten er ikke koblet lenger til porten
           
            break
        
        ########

        ######

        print(f"[{addr} {msg}]")    
# new meassage to the client
        msg = f"Msg recieived:{msg}"
        conn.send(msg.encode(FORMAT))# server sender tilbakemelding til clienten
    conn.close()    




def server(ip,port,format):

    sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)# Oppretter TCP-server socket, AF-INET er brukt for IPV4 protokoller, SOCK_STREAM brukes som socket type
    sock.bind((ip,port)) # Vi binder socket til en spesifisert ip adresse og portnummer


    sock.listen(2) # lytt etter opptil 2 tilkoblinger(connections)samtidig

    print("-" * 45)
    print("A simpleperf server is listening on port",port)
    print("-" * 45)

    while True:
        conn,addr = sock.accept()# når serveren aksepterer vil vi lagre
        #objekt laget av conn, addr forå gi respons til clienten


        client_thread = threading.Thread(target=handle_client,args=(conn,addr,format,))# Vi oppretter en tråd ved hjelp av target og args
        client_thread.start()# Starter tråden

        
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")# teller antall threads= antall klienter som er connected
        # vi lager new thread for hver ny klient, siden det er en thread som alltid kjører (def main()) skal vi trekke fra en thread 
        # for at den skal fortelle oss at det er an aktiv connection når det er 2 threads som kjører
       
        print("-" * 45)
        print("A simpleperf client with {}:{} is connected with {}:{}".format(addr[0],addr[1],ip,port))#
        print("-" * 45)
        # Oppretter ny tråd for å client connection


def client(server_ip, port):

    sock =socket.socket(socket.AF_INET,socket.SOCK_STREAM) # oppretter sokcet

    sock.connect((server_ip,port))#connect to the server
    print(" A simpleperf client Client connecting to server {}, port {}".format(server_ip, port))# printer ut melding
    
    connected = True
    while connected: # den while løkken er laget for å kunne motta alle meldingene så lenge det er data som sendes
    # tilbake fra server
        msg=input(">")
        sock.send(msg.encode())

        if msg == "exit":
            connected = False
        else:

            msg = sock.recv(1024).decode() # tar i mot response fra server
            if len(msg):
                print(f"[SERVER] {msg}")
        
    
        

    sock.close()      

if __name__ == "__main__":


     # Oppretter en argparse-parser objekt med en beskrivelse av programmet vårt
    parser = argparse.ArgumentParser(description='Simple network throughput measurement tool')

    # oppretter gruppe av argumenter hvor bare ett argument kan være aktivt om gangen, True: vil si at bruker må minst velge ett av argumentene i gruppen
    group = parser.add_mutually_exclusive_group(required=True)

    # group inneholder argumenter som utelukker hverandre(hvis du gir en verdi for ett argument, vil de andre argumentene i gruppen bli ignorert)
    group.add_argument('-s', '--server', action='store_true', help='Run in server mode')
    
    group.add_argument('-c', '--client', action='store_true', help='Run in client mode')

    parser.add_argument('-b', '--bind', type=str, default ='0.0.0.0', help='IP address of the server\'s interface where the client should connect')
    parser.add_argument('-I', '--serverip', type=str, default='127.0.0.1', help='IP address of the server')
    parser.add_argument('-p','--port',type=check_port,default=8088,help='Port number on which the server should listen or the client should connect')
    parser.add_argument('-f','--format',type=str,default='MB',help='choose the format of the summary of results KB or MB')
    parser.add_argument('-t','--time',type= int,default=50,help='the total duration in seconds for which data should be generated and sent to the server and must be >0')
    parser.add_argument('-P','--parallel',type=int,default=1,help='creates parallel connections to cennect to the server and send data - it must be 2 and the max value should be 5-')
    
    parser.add_argument('-n','--num',type=int,help='transfer number of bytes specified by -n falg,it should be either in B,KB or MB')
    #-i angir intervallet mellom h
    parser.add_argument('-i','--interval',type=int,help='print statistics per z second')
    #kjøre parseren og hente ut argumentene fra sys.argv
    args = parser.parse_args()
    port = args.port # henter portnummer fra argumentene som er sendt inn via kommandolinejen

   
    if args.server:# basert på dette kaller vi funksjon server()
        server (args.bind,port,args.format)
    elif args.client:# basert på dette kaller vi funksjon client()
        client(args.serverip,port)
    #if not args.server and not args.client:
        #print("Error: you must run either in server or client mode")
        #sys.exit(1)
    

    
           