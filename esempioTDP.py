#scriviamo un codice python che modelli un semplice gestionale aziendale, Dovremo prevedere la possibilità di definire entità
#che modellano i prodotti, i clienti, offrire interfacce per calcolare i prezzi, eventualmente scontati

class Prodotto: 
    aliquota_iva=0.22 #variabile di classe -- ovvero è la stessa per tutte le istanze che verranno create

    def __init__(self, name:str, price:float, quantity:int, supplier=None):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.supplier = supplier

    def valore_netto(self):
        return self.price*self.quantity
    
    def valore_lordo(self):
        netto = self.valore_netto()
        lordo = netto*(1-self.aliquota_iva)
        return lordo
    
    @classmethod #crea metodi di classe
    #può essere usato ad esempio per creare più costruttori
    def costruttore_con_quantità_uno(cls, name, price, supplier): #i metodi di classe non prendono come input self ma cls
        cls(name, price, quantity:1, supplier) #richiama l'init

    @classmethod
    def applica_sconto(prezzo, percentuale): #essendo un metodo statico non passo né cls né self
    
myproduct1 = Prodotto(name:"Laptop", price:1200.0, quantity:12, supplier:"ABC")
print(f"Nome prodotto: {myproduct1.name} - prezzo: {myproduct1.price}")
print(f"il totale lordo è: {myproduct.valore_lordo()}")

myproduct2 = Prodotto(name:"Mouse", price:10, quantity:25, supplier:"CDE")
print(f"Nome prodotto: {myproduct2.name} - prezzo: {myproduct2.price}")

#Scrivere una classe Cliente che abbia i campi "nome", "email", "categoria" ("Gold", "Silver", "Bronze"),
#vorremmo che questa classe avesse un metodo che chiamiamo "descrizione" che deve restituire una stringa formattata 
#ad esempio "Cliente Fulvio Bianchi (Gold) - fulvio@google.com"

class Cliente:
    def __init__(self, nome, email, categoria):
        self.nome=nome
        self.email=email
        self.categoria=categoria

    def descrizione(self):
        return f"Cliente: {self.nome} ({self.categoria}) - {self.email}"

c1 = Cliente(nome:"Mario Bianchi", email:"mario.bianchi@polito.it", categoria:"Gold")
print(c1.descrizione())