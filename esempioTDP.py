#scriviamo un codice python che modelli un semplice gestionale aziendale, Dovremo prevedere la possibilità di definire entità
#che modellano i prodotti, i clienti, offrire interfacce per calcolare i prezzi, eventualmente scontati

class Prodotto: 
    aliquota_iva=0.22 #variabile di classe -- ovvero è la stessa per tutte le istanze che verranno create

    def __init__(self, name:str, price:float, quantity:int, supplier=None):
        self.name = name
        self._price = None
        self.price = price #chiamo il setter nel costruttore per il controllo
        self.quantity = quantity
        self.supplier = supplier

    def valore_netto(self):
        return self._price*self.quantity
    
    def valore_lordo(self):
        netto = self.valore_netto()
        lordo = netto*(1+self.aliquota_iva)
        return lordo
    
    @classmethod #crea metodi di classe, può essere usato ad esempio per creare più costruttori
    def costruttore_con_quantità_uno(cls, name:str, price:float, supplier:str): #i metodi di classe non prendono come input self ma cls
        cls(name, price, 1, supplier) #richiama l'init

    @staticmethod
    def applica_sconto(prezzo, percentuale): #essendo un metodo statico non passo né cls né self
        return prezzo*(1-percentuale)

    @property #decoratore che cambia il contenuto semantico di una funzione
    def price(self): #equivalente del getter in java
        return self._price #variabile non modificabile se preceduta da _: usiamo sempre questo

    @price.setter #posso farlo solo se ho definito un getter
    def price(self, valore):
        if valore<0:
            raise ValueError("Attenzione, il prezzo non può essere negativo.")
        self._price = valore

    def __str__(self):
        return f"{self.name} - disponibili {self.quantity} pezzi a {self.price} $"

    def __repr__(self):
        return f"Prodotto(nome = {self.name}, price = {self.price}, quantity = {self.quantity}, supplier = {self.supplier})"

    def __eq__(self, other:object):
        if not isinstance(other, Prodotto): #se other non è di tipo Prodotto
            return NotImplemented
        return {self.name==other.name
            and self.price==other.price
            and self.quantity==other.quantity
            and self.supplier==other.supplier}

    #rimpiazza il compareTo di java
    def __lt__(self, other:"Prodotto") -> bool: #anticipo che l'output sarà un boolean
        return self.price < other.price

    def prezzo_finale(self):
        return self.price*(1+self.aliquota_iva)

class ProdottoScontato (Prodotto): #classe figlia
    def __init__(self, name:str, price:float, quantity:int, supplier:str, sconto_percento:float): #ha tutti i metodi della classe Prodotto
        #Prodotto.__init__()
        super().__init__(name, price, quantity, supplier)
        self.sconto_percento = sconto_percento

    def prezzo_finale(self) -> float:
        return self.valore_lordo()*(1-self.sconto_percento/100)

class Servizio(Prodotto):
    def __init__(self, name:str, tariffa_oraria:float, ore:int):
        super().__init__(name = name, price = tariffa_oraria, quantity = 1, supplier = None)
        self.ore = ore

    def prezzo_finale(self) -> float:
        return self.price*self.ore

myproduct1 = Prodotto(name="Laptop", price=1200.0, quantity=12, supplier="ABC")
print(f"Nome prodotto: {myproduct1.name} - prezzo: {myproduct1.price}")
print(f"il totale lordo è: {myproduct1.valore_lordo()}")

p3= Prodotto.costruttore_con_quantità_uno(name="Auricolari", price=200.0, supplier="ABC") #modo per chiamare un metodo di classe
print(f"Prezzo scontato di myproduct1 {Prodotto.applica_sconto(myproduct1.price, 0.15)}")

myproduct2 = Prodotto(name="Mouse", price=10, quantity=25, supplier="CDE")
print(f"Nome prodotto: {myproduct2.name} - prezzo: {myproduct2.price}")

print(f"Valore lordo di prodotto 1: {myproduct1.valore_lordo()}")
Prodotto.aliquota_iva=0.24
print(f"Valore lordo di prodotto 1: {myproduct1.valore_lordo()}")

print(myproduct1)

p_a = Prodotto(name="Laptop", price =1200.0, quantity=12, supplier="ABC")
p_b = Prodotto(name="Mouse", price=10, quantity=14, supplier="CDE")

print("myproduct1 == p_a?", myproduct1 == p_a) #va a chiamare il metodo __eq__ appena implementatao, mi aspetto TRUE

print ("p_a == p_b", p_a==p_b) #mi aspetto FAlSE

mylist = [p_a, p_b, myproduct1]
mylist.sort()
print("lista prodotti ordinata:")
for p in mylist:
    print(f"- {p}")

my_product_scontato = ProdottoScontato(name = "Auricolari", price = 120, quantity = 1, supplier = "ABC", sconto_percento = 10)
my_service = Servizio (name = "Consulenza", tariffa_oraria = 100, ore = 3)

mylist.append(my_product_scontato)
mylist.append(my_service)

mylist.sort(reverse = "True")

for element in mylist:
    print (element.name, "->", element.prezzo_finale())

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

abb = Abbonamento(name = "Software gestionale",prezzo_mensile= 30,mesi= 24)
mylist.append(abb)
for elem in mylist:
    print(elem.name, "->", elem.prezzo_finale())

def calcola_totale(elementi):
    tot = 0
    for e in elementi:
        tot+=e.prezzo_finale() #ducktyping
    return tot

print(f"Il totale è: ",calcola_totale(mylist))

from typing import Protocol

class HaPrezzoFinale(Protocol): #protocollo per check classi in metodo calcola_totale
    def prezzo_finale(self) -> float: #firma del metodo implementato da TUTTE le classi che utilizzano il protocollo
        ...

def calcola_totale(elementi:list(HaPrezzoFinale)) -> float:
    return sum(e.prezzo_finale() for e in elementi)

print(f"Il totale è: ",calcola_totale(mylist))

print("------------------------------------------------------------")
print("Sperimentiamo con dataclass")

from dataclasses import dataclass

@dataclass #grazie alla dataclass la classe acquisisce automaticamente il costruttore e tutti i dunder methods
class ProdottoRecord:
    name:str
    prezzo_unitario:float

@dataclass
class ClienteRecord:
    name:str
    email:str
    categoria:str

@dataclass
class RigaOrdine:
    prodotto: ProdottoRecord
    quantità: int

    def totale_riga(self) -> float:
        return self.prodotto.prezzo_unitario*self.quantità

@dataclass
class Ordine:
    righe: list[RigaOrdine]
    cliente: ClienteRecord

    def totale_netto(self):
        return sum(r.totale_riga() for r in self.righe)

    def totale_lordo(self, aliquota_iva):
        return self.totale_netto()*(1+aliquota_iva)

    def numero_righe(self):
        return len(self.righe)


@dataclass
class OrdineConSconto(Ordine):
    sconto_percentuale:float

    def totale_scontato(self):
        return self.totale_lordo*(1-sconto_percentuale)

    def totale_netto(self): #metodo della classe padre ridefinito
        netto_base = super().totale_netto()
        return netto_base*(1-self.sconto_percentuale)


cliente1 = ClienteRecord("Mario Rossi", "mariorossi@example.com", "Gold")
p1 = ProdottoRecord("Laptop", 1200.0)
p2 = ProdottoRecord("Mouse", 20)

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

class Cliente:
    def __init__(self, nome, email, categoria):
        self.nome=nome
        self.email=email
        self._categoria=None
        self.categoria=categoria

    def descrizione(self):
        return f"Cliente: {self.nome} ({self.categoria}) - {self.email}"

    @property
    def categoria(self):
        return self._categoria

    @categoria.setter
    def categoria(self, valore: str):
        categorie_valide={"Gold", "Silver", "Bronze"}
        if valore not in categorie_valide:
            raise ValueError("Attenzione, la categoria deve essere una tra le seguenti: 'Gold', 'Silver', 'Bronze'")
        self._categoria=valore

    def descrizione(self):
        return f"Cliente: {self.nome} ({self.categoria}) - {self.email}"

c1 = Cliente(nome="Mario Bianchi", email="mario.bianchi@polito.it", categoria="Gold")
#c2=Cliente("Carlo Masone", "carlo.masone@polito.it", "Platinum")
print(c1.descrizione())