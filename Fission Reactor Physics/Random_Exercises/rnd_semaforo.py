## che minchia faccio al semaforo

def chedevofa(velocita,colore,distsem):

    limite = 50 

    if colore == 'verde':
        azione = 'VAI ZIOCANE'
    elif colore == 'giallo' and distsem < 10 :
        azione = 'PUOI COMUNQUE ANDARE MARPIONE'
    else :
        azione = 'FERMATI CAZZONE'
    if velocita > limite :
        suggerimento = 'E STAI SCANNANDO TROPPO MONGOLOIDE'
    elif velocita < 10 :
        suggerimento = 'E SEI UNA MERDA DI LUMACA'
    else :
        suggerimento = 'E LA VELOCITA E NEI LIMITI BOMBER'

    return azione, suggerimento

az, sug = chedevofa(40,'giallo',7)

print(f'Viste le condizioni, {az} {sug}')