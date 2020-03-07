# 1. projekt do predmetu IPK (FIT VUT)
**Jméne:** Jonáš Sasín
**Login:** xsasin05
**Datum:** 7.3.2020
**Zvolený jazyk**: Python

"Implementace severu, který komunikuje protokolem HTTP a zajišťuje překlad doménových jmen."

## Spuštění
Program se spustí příkazem "make run PORT=*cislo_portu*"  
příkazy: GET, POST  
make run PORT=5353  
příklad GET: curl localhost:5353/resolve?name=www.fit.vutbr.cz\&type=A  
příklad POST: curl --data-binary @queries.txt -X POST http://localhost:5353/dns-query  

## Popis řešení
Program pracuje s jediným argumentem - číslo portu. Po zpracování argumentu se na tomto portu vytvoří "naslouchající" socket, který čeká v nekonečném cyklu na navázání spojení pomocí *accept()*. Jakmile je spojení navázáno, přijatá zpráva je zpracována pomocí funkce *parse_request()* a podle požadavku GET resp. POST je odpověď vytvořena funkcí *op_get()* resp *op_post()*. k odpovědi je poté přidána funkcí *add_header()* odpovídající hlavička. Zpráva je dále zakódována a odeslána komunikujícímu klientovi. Spojení je poté ukončeno a server čeká na navázání dalšího spojení.

## Návratové kódy
**0** - Spuštění serveru proběhlo vpořádku  
**1** - Spuštění serveru se nezdařilo

### Použité moduly: sys, socket, re



