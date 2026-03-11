from gestionale.prodotti import Prodotto, crea_prodotto_standard, ProdottoScontato, Servizio #importo la classe Prodotto dall'altro file

#scriviamo un codice python che modelli un semplice gestionale aziendale, Dovremo prevedere la possibilità di definire entità
#che modellano i prodotti, i clienti, offrire interfacce per calcolare i prezzi, eventualmente scontati


print("------------------------------------------------------------")

#Definire una classe Abbonamento che abbia come attributi "nome, prezzo_mensile, mesi". Abbonamento dovrà avere un metodo
#per calcolare il prezzo finale, ottenuto come prezzo_mensile*mesi)

class Abbonamento:
    def __init__(self, name:str, prezzo_mensile:float, mesi:int):
        self.name=name
        self.prezzo_mensile=prezzo_mensile
        self.mesi = mesi

    def prezzo_finale(self) -> float:
        return self.prezzo_mensile*self.mesi



def calcola_totale(elementi):
    tot = 0
    for e in elementi:
        tot+=e.prezzo_finale() #ducktyping
    return tot

from typing import Protocol

class HaPrezzoFinale(Protocol): #protocollo per check classi in metodo calcola_totale
    def prezzo_finale(self) -> float: #firma del metodo implementato da TUTTE le classi che utilizzano il protocollo
        ...

def calcola_totale(elementi:list(HaPrezzoFinale)) -> float:
    return sum(e.prezzo_finale() for e in elementi)


print("============================================================")

p1=Prodotto(name="Ebook reader", price=120.0, quantity=1, supplier="AAA")
p2=crea_prodotto_standard("Tablet", 750)

print(p1)
print(p2)

#MODI PER IMPORTARE
#1)
from gestionale.prodotti import ProdottoScontato
p21=ProdottoScontato("Auricolari", 230, 1, "ABC", 10)

#2)
from gestionale.prodotti import ProdottoScontato as ps #per rinominare l'oggetto importato
p3=ps("Auricolari", 230, 1, "ABC", 10)

#3)
import gestionale.prodotti #importa l'intero file e stampa i print al suo interno

#4)
import gestionale.prodotti as p

print(dir(p)) #stampa i nomi (classi e funzioni) definiti nel modulo prodotti importato
print(dir()) #stampa i nomi dei moduli importati nella classe corrente

p5=p.ProdottoScontato("Auricolari", 230, 1, "ABC", 10)

print("============================================================")

print("------------------------------------------------------------")

from gestionale.clienti import ClienteRecord

cliente1 = ClienteRecord("Mario Rossi", "mariorossi@example.com", "Gold")

from gestionale.prodotti import ProdottoRecord

p1 = ProdottoRecord("Laptop", 1200.0)
p2 = ProdottoRecord("Mouse", 20)

from gestionale.ordini import Ordine, RigaOrdine, OrdineConSconto

ordine = Ordine([RigaOrdine(p1, 2), RigaOrdine(p2, 10)], cliente1)
ordine_scontato = OrdineConSconto([RigaOrdine(p1, 2), RigaOrdine(p2, 10)], cliente1, 0.10)

print(ordine) #stampa come __repr__ anche se non definito PERCHé DATACLASS
print("Numero di righe nell'ordine: ", ordine.numero_righe())
print("Totale netto: ", ordine.totale_netto())
print("Totale lordo (IVA 22%): ", ordine.totale_lordo(0.22))

print(ordine_scontato)
print("Totale netto sconto: ", ordine_scontato.totale_netto())
print("Totale lordo scontato: ", ordine_scontato.totale_lordo(0.22)) #il metodo totale_lordo non esiste in OrdineConSconto quindi richiama quello della superclasse

print("------------------------------------------------------------")

#Scrivere una classe Cliente che abbia i campi "nome", "email", "categoria" ("Gold", "Silver", "Bronze"),
#vorremmo che questa classe avesse un metodo che chiamiamo "descrizione" che deve restituire una stringa formattata 
#ad esempio "Cliente Fulvio Bianchi (Gold) - fulvio@google.com"

#Si modifichi la classe "Cliente" in modo che la proprietà categoria sia "protetta"
# e accetti solo ("Gold", "Silver", "Bronze")

from gestionale.clienti import Cliente
c1=Cliente("Mario Rossi", "mail@mail.com", "Gold")

#Nel package gestionale scriviamo un modulo fatture.py che contenga:
# - una classe fattura che contiene un Ordine, un numero fattura e una data
# - un metodo genera_fattura() che restituisce una stringa formattata con tutte le info della fattura
