import random

class Domanda:
    """Classe che rappresenta una singola domanda del Trivia."""
    def __init__(self, testo, livello, corretta, errate):
        self.testo = testo
        self.livello = int(livello)
        self.corretta = corretta
        self.errate = errate

    def ottieni_opzioni_mischiate(self):
        """Restituisce una lista di opzioni mischiate casualmente."""
        opzioni = [self.corretta] + self.errate
        random.shuffle(opzioni)
        return opzioni


class TriviaGame:
    """Classe che gestisce la logica di gioco, il caricamento e il salvataggio."""
    def __init__(self, file_domande="domande.txt", file_punti="punti.txt"):
        self.file_domande = file_domande
        self.file_punti = file_punti
        self.domande = []
        self.carica_domande()

    def carica_domande(self):
        """Legge il file domande.txt e popola la lista degli oggetti Domanda."""
        try:
            with open(self.file_domande, 'r', encoding='utf-8') as f:
                # Filtriamo le righe vuote per semplificare la lettura a blocchi di 6
                righe = [riga.strip() for riga in f if riga.strip()]
            
            for i in range(0, len(righe), 6):
                if i + 5 < len(righe):
                    testo = righe[i]
                    livello = righe[i+1]
                    corretta = righe[i+2]
                    errate = [righe[i+3], righe[i+4], righe[i+5]]
                    
                    nuova_domanda = Domanda(testo, livello, corretta, errate)
                    self.domande.append(nuova_domanda)
        except FileNotFoundError:
            print(f"Errore: Il file '{self.file_domande}' non è stato trovato.")
            exit(1)

    def salva_punteggio(self, nickname, punteggio):
        """Salva il nuovo punteggio aggiornando il file e ordinandolo in modo decrescente."""
        lista_punteggi = []
        
        # 1. Lettura dei punteggi esistenti 
        try:
            with open(self.file_punti, 'r', encoding='utf-8') as f:
                for riga in f:
                    if riga.strip():
                        parti = riga.strip().split()
                        nome = " ".join(parti[:-1])
                        punti = int(parti[-1])
                        lista_punteggi.append((nome, punti))
        except FileNotFoundError:
            # Se il file non esiste ancora, non facciamo nulla. 
            # La lista_punteggi rimarrà vuota e ci aggiungeremo solo il giocatore attuale.
            pass
        
        # 2. Aggiunta del nuovo punteggio e ordinamento decrescente
        lista_punteggi.append((nickname, punteggio))
        lista_punteggi.sort(key=lambda x: x[1], reverse=True)
        
        # 3. Scrittura sul file
        with open(self.file_punti, 'w', encoding='utf-8') as f:
            for nome, punti in lista_punteggi:
                f.write(f"{nome} {punti}\n")
    

    def gioca(self):
        """Gestisce il loop principale della partita."""
        livello_corrente = 0
        punti = 0

        while True:
            # Filtra solo le domande del livello attuale
            domande_livello = [d for d in self.domande if d.livello == livello_corrente]
            
            # Condizione di vittoria: se non ci sono più domande per il livello corrente
            if not domande_livello:
                print("\nHai completato con successo tutti i livelli di difficoltà disponibili! 🎉")
                break
            
            # Seleziona una domanda casuale
            domanda_scelta = random.choice(domande_livello)
            opzioni = domanda_scelta.ottieni_opzioni_mischiate()
            
            # Stampa la domanda e le opzioni
            print(f"\nLivello {livello_corrente}) {domanda_scelta.testo}")
            for idx, opzione in enumerate(opzioni, 1):
                print(f"\t{idx}. {opzione}")
            
            # Input dell'utente con controllo degli errori
            while True:
                try:
                    scelta_utente = int(input("Inserisci la risposta: "))
                    if 1 <= scelta_utente <= 4:
                        break
                    else:
                        print("Per favore, inserisci un numero tra 1 e 4.")
                except ValueError:
                    print("Valore non valido. Inserisci un numero tra 1 e 4.")
            
            # Valutazione della risposta
            risposta_utente = opzioni[scelta_utente - 1]
            
            if risposta_utente == domanda_scelta.corretta:
                print("Risposta corretta!")
                punti += 1
                livello_corrente += 1
            else:
                # Trova l'indice corretto per mostrarlo nel messaggio di errore
                indice_corretto = opzioni.index(domanda_scelta.corretta) + 1
                print(f"Risposta sbagliata! La risposta corretta era: {indice_corretto}")
                break

        # Fine partita: salvataggio
        print(f"\nHai totalizzato {punti} punti!")
        nickname = input("Inserisci il tuo nickname: ")
        self.salva_punteggio(nickname, punti)
        print("Punteggio salvato con successo!")

# --- Punto di ingresso del programma ---
if __name__ == "__main__":
    gioco = TriviaGame()
    gioco.gioca()