import ipaddress
import socket
import argparse
import time
import threading
import sys
import math

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
def check_ip(address):# sjekker om adress er valid IPv4 address
    try:
       val = ipaddress.ip_address(address)
       print(f"The IP address {val} is valid.")
    except ValueError:
       print(f"The IP address is {address} not valid")


def handle_client(conn,addr, format):# funksjon for å behandle klienter og måle båndbredde
      
    

    start_time = time.time()# vi kaller funksjonen time.time(),for å få nåtidi sekunder
    
    antall_bytes = 0# Denne variabelen kommer vi til å bruke for telle antall bytes som blir mottatt
    bandwidth = 0
  

    while True: # løkken fortsetter å motta data intil det ikke er mer data igjen
        
        try:
            data = conn.recv(1000) # 1000 bytes av data blir mottatt fra tilkoblingen og lagres i variabelen data
        except:
            break
       
        if  data.decode() == "FINISH" : # ikke mer data

            print(data)
            break    # Avslutt løkken
           
       
        antall_bytes += len(data) # antall bytes økes med lengden av data som ble mottatt

        end_time  = time.time()# kaller igjen metode time.time() for å se tiden etter at data er mottatt
        
        duration = end_time - start_time # beregner tiden det tok å motta data, og legger den i variabelen duration
        
        try:
            conn.send("ACK".encode())# sender bekreftelsesmelding til klienten
        except:
            
            conn.close()
       

    bandwidth =( antall_bytes /duration )* 8 /1000000 
    # Dette er overskrift til 4 kolonner , innholdet i disse kommer ut av neste linje  som er info om data som er overført mellom client og server
    if format == "KB":# hvis vi ønsker å representere bW i KB/s
        antall_bytes = antall_bytes / 1000 # Dette konverterer antall byte til kilobyte siden 1KB~= 1000Byte/ 1024 byte
        
       
    elif format == "MB":# hvis vi ønsker å representere bW i MB/s
        antall_bytes = antall_bytes / 1000000#Dette konverterer antall byte til megabyte siden 1MB~= 1000000Byte/1048576byte
    elif format == "B":
        antall_bytes = antall_bytes    
    
      
    
    print("ID\t\tInterval\t\tReceived\t\tRate")        #print("{} 0.0 - {:.1f} {:.0f} {:.2f}Mbps".format(sock.getsockname()[0]+":"+str(sock.getsockname()[1]), duration, total_bytes/1000000, bandwidth))
    print("{}:{}\t0.0 - {:.1f}\t\t{:.0f} {}\t\t{:.2f} Mbps".format(addr[0], addr[1], duration, antall_bytes, format, bandwidth))# her bruker vi format-metoden for å vise tid som
                    #er brukt på overføring av data, antall bytes som overføres,bandwidth. addr variabel skal ha IP-adresse og portnummer til klienten som er tilkoblet.                                              
                                              # vi deler på 10^6 for å konvertere fra bytes per sekund (b/s) til megabit per sekund(Mbps), 1 megabit= 10^6 bits.   

   
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
        client_thread = threading.Thread(target=handle_client,args=(conn,addr,format))# Vi oppretter en tråd ved hjelp av target og args
        client_thread.start()# Starter tråden
      


def client(serverip, port, format,duration,parallel):# Dette er funksjon for å kjøre client
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #oppretter ny socket objekt, ved brukt av IPV4-protokoll og TCP protokoll
    sock.settimeout(1)# Setter timeout til 1 sekund
    sock.connect((serverip, port))# client kobles til server
    print("-" * 45)
    print(" A simpleperf client Client connecting to server {}, port {}".format(serverip, port))# printer ut melding
    print("-" * 45)
    last_print_time = time.time()
    start_time = time.time() # variabelen inneholder nåværende tid når starter å koble seg til server
    total_bytes = 0 # antall byte sendt

    while True: # evig loop som sender datapakker på 1000 byte
        data = "0" * 1000
        sock.send(data.encode())# sender datapakker
        total_bytes += len(data) # vi oppdaterer antall byte for hver pakke som blir sendt
        
        now = time.time()
        elapsed_time = now - start_time # variabelen inneholder tiden som har gått siden client startet og sende datapakker
        
       
        if interval:    
            #if math.floor(elapsed_time) % interval == 0:
                bandwidth = total_bytes / duration * 8 / 1000000
                
                if now - last_print_time >= interval:
                    print("Client connected with server {},port{}".format(serverip,port))
                    print("ID Interval Transfer Bandwidth")
                    print("{} {:.1f} - {:.1f} {:.0f} {:.2f}Mbps".format(sock.getsockname()[0]+":"+str(sock.getsockname()[1]),  math.floor(elapsed_time) - interval,math.floor(elapsed_time) , total_bytes/1000000, bandwidth))
                    last_print_time = time.time()
                
                
        if elapsed_time >= duration:# dersom medgått tid er større enn duration
            if data =="FINISH":
                sock.send(data.encode())# client sender bye medling
            break # Løkken avbrytes
    
        msg= sock.recv(1000).decode()# client tar imot respons (Acknowlegement) fra server på opp til 10 byte
    print ("data received", msg)
    end_time = time.time()# tidspunkt når client er ferdig
    
    duration = end_time - start_time # tiden det tok for client å kjøre/ end_time= nåværende tidspunkt
    
    
    #prøv å telle antallbyte her og se forskjellen
    #bandwidth = (total_bytes / 1000000)/ duration # bandwidth-variabel beregner båndbredden som client har oppnådd,ved å dele antall byte på tid, vi ganger med 8 for å omgjøre til bps, og dele på 10^6 for å få Mbps
    bandwidth = (total_bytes / duration )* 8 / 1000000
    if format == "KB":# hvis vi ønsker å representere bW i KB/s
        total_bytes = total_bytes / 1000 # Dette konverterer antall byte til kilobyte siden 1KB~= 1000Byte/ 1024 byte
       
                #print(antall_bytes)
    elif format == "MB":# hvis vi ønsker å representere bW i MB/s
        total_bytes = total_bytes / 1000000#Dette konverterer antall byte til megabyte siden 1MB~= 1000000Byte/1048576byte
    elif format == "B":
        total_bytes= total_bytes    
   
    print("Client connected with server {},port{}".format(serverip,port))
    print("ID\t\tInterval\t\tTransfer\tBandwidth")
    print("{}:{}\t0.0 - {:.1f}\t\t{:.0f} {}\t\t{:.2f} Mbps".format(sock.getsockname()[0], sock.getsockname()[1], duration, total_bytes,format, bandwidth))
        

if __name__ == '__main__':# sjekker navnet på det gjeldende programmet som kjøres, og koden inne i blokken, er det den som skal kjøres. Linjen er brukt for å kjøre koden

    # Oppretter en argparse-parser objekt med en beskrivelse av programmet vårt
    parser = argparse.ArgumentParser(description='Simple network throughput measurement tool')

    # oppretter gruppe av argumenter hvor bare ett argument kan være aktivt om gangen, True: vil si at bruker må minst velge ett av argumentene i gruppen
    #group = parser.add_mutually_exclusive_group(required=True)

    # group inneholder argumenter som utelukker hverandre(hvis du gir en verdi for ett argument, vil de andre argumentene i gruppen bli ignorert)
    #group.add_argument('-s', '--server', action='store_true', help='Run in server mode')
    
    #group.add_argument('-c', '--client', action='store_true', help='Run in client mode')

    parser.add_argument('-s','--server', action='store_true', help='Run in server mode')
    parser.add_argument('-c', '--client', action='store_true', help='Run in client mode')

    parser.add_argument('-b', '--bind', type=str, default ='0.0.0.0', help='IP address of the server\'s interface where the client should connect')
    parser.add_argument('-I', '--serverip', type=str, default='127.0.0.1', help='IP address of the server')
    parser.add_argument('-p','--port',type=check_port,default=8088,help='Port number on which the server should listen or the client should connect')
    parser.add_argument('-f','--format',type=str,default='MB',help='choose the format of the summary of results KB or MB')
    parser.add_argument('-t','--time',type=int, default=25,help='the total duration in seconds for which data should be generated and sent to the server and must be >0')
    parser.add_argument('-P','--parallel',type=int,default=1,help='creates parallel connections to cennect to the server and send data - it must be 2 and the max value should be 5-')
    #parser.add_argument('-P','--parallel',type=check_parallel, default = 1,help='creates parallel connections to cennect to the server and send data - it must be 2 and the max value should be 5-')
    
    parser.add_argument('-n','--num',type=str,help='transfer number of bytes specified by -n falg,it should be either in B,KB or MB')
    #-i angir intervallet mellom h
    parser.add_argument('-i','--interval',type= check_time,help='print statistics per z second')
    #kjøre parseren og hente ut argumentene fra sys.argv
    args = parser.parse_args()
    
    
    port = args.port # henter portnummer fra argumentene som er sendt inn via kommandolinejen
    ip=args.bind
    serverip =args.serverip
    duration=args.time
    parallel=args.parallel
    interval=args.interval
    format=args.format
    if args.server and args.client:        
         print("Error: Cannot run both server and client mode")         
    elif args.server:# basert på dette kaller vi funksjon server()
        check_ip(ip)
        
        server (ip,port,format)
    elif args.client:# basert på dette kaller vi funksjon client()
       
            if parallel in range(2, 6):
                for i in range(0, parallel):
                    client_thread = threading.Thread(target=client, args=(args.serverip, port,format, duration, i,))# Vi oppretter en tråd ved hjelp av target og args
                    client_thread.start()# Starter tråden
            else:
                client(serverip,port,format,duration,parallel)
    

             