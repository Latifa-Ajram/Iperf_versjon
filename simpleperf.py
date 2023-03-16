import socket
import argparse
import time
import threading
import sys

# Definerer en funksjon for å sjekke om en port er gyldig
def check_port(val):
    try:
        value = int(val)
    except ValueError:
        raise argparse.ArgumentTypeError('expected an integer but you entered a string')
    if not(1024 <=value <=65535 ):
        print('it is not a valid port')
        sys.exit()
    return value

def handle_client(conn,addr,format):# funksjon for å behandle klienter og måle båndbredde

    ###testprint
    print(f"Connected by {addr}")

    start_time = time.time()# vi kaller funksjonen time.time(),for å få nåtidi sekunder
    antall_bytes = 0# Denne variabelen kommer vi til å bruke for telle antall bytes som blir mottatt
    connected =True
    while connected: # løkken fortsetter å motta data intil det ikke er mer data igjen
        data = conn.recv(1000) # 1000 bytes av data blir mottatt fra tilkoblingen og lagres i variabelen data
        if not data: # ikke mer data
            break    # Avslutt løkken
       
        antall_bytes += len(data) # antall bytes økes med lengden av data som ble mottatt
        end_time  = time.time()# kaller igjen metode time.time() for å se tiden etter at data er mottatt
        duration = end_time - start_time # beregner tiden det tok å motta data, og legger den i variabelen duration

        if duration > 0:
            if format == "KB":# hvis vi ønsker å representere bW i KB/s
                antall_bytes = antall_bytes / 1000 # Dette konverterer antall byte til kilobyte siden 1KB~= 1000Byte/ 1024 byte
            elif format == "MB":# hvis vi ønsker å representere bW i MB/s
                antall_bytes = antall_bytes / 1000000#Dette konverterer antall byte til megabyte siden 1MB~= 1000000Byte/1048576byte
            bandwidth = antall_bytes /duration * 8 /1000000 # vi ganger med 8 for å konvertere bytes til bits siden 1 Byte = 8 bits     
                                                        # vi deler på 10^6 for å konvertere fra bytes per sekund (b/s) til megabit per sekund(Mbps), 1 megabit= 10^6 bits.
    
            print("ID Interval Received Rate")# Dette er overskrift til 4 kolonner , innholdet i disse kommer ut av neste linje  som er info om data som er overført mellom client og server
            print("{} 0.0 - {:.1f} {:.0f} {}bps".format(addr[0]+":"+str(addr[1]),duration,antall_bytes,bandwidth))# her bruker vi format-metoden for å vise tid som
                    #er brukt på overføring av data, antall bytes som overføres,bandwidth. addr variabel skal ha IP-adresse og portnummer til klienten som er tilkoblet.                                              
            
        
        conn.sendall(b"ACK")# sender bekreftelsesmelding til klienten
    conn.close()# lukker tilkobling med klienten

def server(ip,port,format)  : # Dette er funksjon for å kjøre serveren

    sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)# Oppretter TCP-server socket, AF-INET er brukt for IPV4 protokoller, SOCK_STREAM brukes som socket type
    sock.bind((ip,port)) # Vi binder socket til en spesifisert ip adresse og portnummer

   

    sock.listen(2) # lytt etter opptil 2 tilkoblinger(connections)samtidig

    print("-" * 45)
    print("A simpleperf server is listening on port",port)
    print("-" * 45)
    while True:
        conn,addr = sock.accept()# Sett opp ny tikobling fra client. addr:inneholder ip-adresse og portnummeret til klienten

        
        print("-" * 45)
        print("A simpleperf client with {}:{} is connected with {}:{}".format(addr[0],addr[1],ip,port))#
        print("-" * 45)
        # Oppretter ny tråd for å client connection

        client_thread = threading.Thread(target=handle_client,args=(conn,addr,format,))# Vi oppretter en tråd ved hjelp av target og args
        client_thread.start()# Starter tråden


def client(server_ip, port, duration):# Dette er funksjon for å kjøre client
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #oppretter ny socket objekt, ved brukt av IPV4-protokoll og TCP protokoll
    sock.connect((server_ip, port))# client kobles til server
    print(" A simpleperf client Client connecting to server {}, port {}".format(server_ip, port))# printer ut melding
    start_time = time.time() # variabelen inneholder nåværende tid når starter å koble seg til server
    total_bytes = 0 # antall byte sendt
    while True: # evig loop som sender datapakker på 1000 byte
        data = b"0" * 1000
        sock.sendall(data)# sender datapakker
        total_bytes += len(data) # vi oppdaterer antall byte for hver pakke som blir sendt
        elapsed_time = time.time() - start_time # variabelen inneholder tiden som har gått siden client startet og sende datapakker
        if elapsed_time >= duration:# dersom medgått tid er større enn duration
            break # Løkken avbrytes
    sock.sendall(b"FINISH")# client sender bye medling
    sock.recv(1024)# client tar imot respons fra server på opp til 1024 byte
    end_time = time.time()# tidspunkt når client er ferdig
    duration = end_time - start_time # tiden det tok for client å kjøre/ end_time= nåværende tidspunkt
    bandwidth = total_bytes / duration * 8 / 1000000# bandwidth-variabel beregner båndbredden som client har oppnådd,ved å dele antall byte på tid, vi ganger med 8 for å omgjøre til bps, og dele på 10^6 for å få Mbps
    print("Client connected with server {},port{}".format(server_ip,port))
    print("ID Interval Transfer Bandwidth")
    print("{} 0.0 - {:.1f} {:.0f} {}Mbps".format(sock.getsockname()[0]+":"+str(sock.getsockname()[1]), duration, total_bytes/1000000, bandwidth))
    #Dette er resultat av testen, 

if __name__ == '__main__':# sjekker navnet på det gjeldende programmet som kjøres, og koden inne i blokken, er det den som skal kjøres. Linjen er brukt for å kjøre koden

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
        client(args.serverip,port,args.time)
    #if not args.server and not args.client:
        #print("Error: you must run either in server or client mode")
        #sys.exit(1)
    