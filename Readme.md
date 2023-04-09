# simpleperf
Dette programmet er en enkel Python-basert server-client applikasjon som kan brukes til å måle bandwidth mellom to enheter.

Kjøring av Simpleperf:

For å kjøre programmet, må serveren startes først og deretter starte klienten. serveren startes ved å kjøre følgende kommando:
python3 simpleperf.py -s <ip-adresse> -p <portnummer> -f <format>
'ip-adresse' er IP-adressen til enheten der serverev kjører,'portnummer ' er portnummeret som skal brukes for kommunikasjon 
'format' er formatet som man ønsker å få båndbredden i (B,KB eller MB)

For å starte klienten, kan man kjøre dette:
python3 simpleperf.py -c <ip-adresse> -p < portnummer> -t <varighet> -f <format>
'ip-adresse' er IP-adressen til enheten der serveren kjører,'portnummer ' er portnummeret som skal brukes for kommunikasjon.
'varighet' er hvor lenge man ønsker å sende data(måles i sekunder)
'format' er formatet som man ønsker å få båndbredden i (B,KB eller MB)
ved å kjøre dette: python3 simpleperf.py -c <ip-adresse> -p < portnummer> -t  vil det skrives ut statistikk per t sekunder spesifisert etter -i- flagget.
ved å kjøre dette: python3 simpleperf -c -I <server_ip> -p <server_port> -P 2   vil det åpnes to TCP-tilkoblinger parallelt for å koble til serveren


Hvordan fungerer programmet?

Når klienten kobler seg til serveren, vil serveren starte en ny tråd for å håndtere klienten. Tråden vil motta data fra klienten og beregne båndbredden mellom klienten og serveren.
For å beregne båndbredden, vil tråden telle antall bytes som blir mottatt og beregne tiden det tok å motta data. deretter vil den dele bytes på tiden det tok å motta data, og konvertere resultatet til ønsket format(B;KB;MB)

Krav:

programmet krever at pyhton er installert på datamaskinen der du ønsker å kjøre programmet.