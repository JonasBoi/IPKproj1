# ISA 2020: Odpovědní arch pro cvičení č. 1

## Zjišťování konfigurace

### (1.) Rozhraní enp0s3

*MAC adresa*: 08:00:27:ed:de:19

*IPv4 adresa*: 10.0.2.15

*Délka prefixu*: 24

*Adresa síťe*: 10.0.2.0

*Broadcastová adresa*: 10.0.2.255

### (2.) Výchozí brána

*MAC adresa*: 52:54:00:12:35:02

*IPv4 adresa*: 10.0.2.2

### (4.) DNS servery

*Soubor*: /etc/resolv.conf

*DNS servery*: 212.96.160.6 , 212.96.161.7

### (5.) Ping na výchozí bránu

*Soubor*: /etc/hosts

*Úprava*: pridani radku "10.0.2.2    gw"

### (6.) TCP spojení

*Záznam + popis*:

State       Recv-Q Send-Q        Local Address:Port                       Peer Address:Port 
ESTAB       0      0                 10.0.2.15:50782                       34.98.75.36:https

Vzpis aktivnich tcp spojeni, podle sloupce: stav spojeni, pocet prijatych, pocet odeslanych paketu, lokalni adresa a port a cilova adresa a port neboli unikatni ctverice specifikujici TCP spojeni

### (8.) NetworkManager události

*Příkaz*: sudo journalctl -t NetworkManager

### (9.) Chybová hláška sudo

*Příkaz*: sudo journalctl -t sudo (napriklad)

*Chybová hláška*: Oct 03 10:03:06 ... user : command not allowed ; TTY=pts/0 ; PWD=/home/user ; USER=root ; COMMAND=/bin/wireshark

## Wireshark

### (1.) Capture filter

*Capture filter*: port 80

### (2.) Zachycená HTTP komunikace

Komu patří nalezené IPv4 adresy a MAC adresy?
Vypisovali jste již některé z nich?
Proč tomu tak je?

*odpoved*:
Jedna z dovojic ipv4+mac patri memu zarizani konkretne rozhrani enp0s3 - vypsano vyse
Druha ip adresa patri serveru (147.229.177.179) a mac adresa (52:54:00:12:35:02) patri vychozi brane

#### Požadavek HTTP

Cílová MAC adresa

  - *Adresa*: 52:54:00:12:35:02
  - *Role zařízení*: vychozi brana(gateaway) - smerovac

Cílová IP adresa

  - *Adresa*: 147.229.177.179
  - *Role zařízení*: server

Zdrojová MAC adresa

  - *Adresa*: 08:00:27:ed:de:19
  - *Role zařízení*: klient

Zdrojová IP adresa

  - *Adresa*: 10.0.2.15
  - *Role zařízení*: klient


#### Odpověď HTTP

Cílová MAC adresa

  - *Adresa*: 08:00:27:ed:de:19
  - *Role zařízení*: klient

Cílová IP adresa

  - *Adresa*: 10.0.2.15
  - *Role zařízení*: klient

Zdrojová MAC adresa

  - *Adresa*: 52:54:00:12:35:02
  - *Role zařízení*: vychozi brana(gateaway) - smerovac

Zdrojová IP adresa

  - *Adresa*: 147.229.177.179
  - *Role zařízení*: server

### (3.) Zachycená ARP komunikace

*Display filter*: arp || icmp

### (6.) Follow TCP stream

Jaký je formát zobrazených dat funkcí *Follow TCP stream*, slovně popište
význam funkce *Follow TCP stream*:

Zpravy muzeme videt v takovem poradi v jakem chodi po siti a v jakem s nimi pracuje aplikacni vrstva.  
Sledujeme jedno souvisle TCP spojeni.

Pakety od klienta serveru vidime cervene, odpovedi serveru vidime modre.  
Uzitecne pro prehledne zobrazeni jedne komunikace v ramci spojeni.



