from model.model import Model

model = Model()

model.creaGrafo('vacuole')

nodi, archi = model.getInfo()
print(f'Creato grafo con {nodi} nodi e {archi} archi')

print()
archiMagg = model.getArchiMagg()
for a, b, data in archiMagg:
    print(f'{a} <-> {b}: peso {data['weight']}')

print()
compConn = model.getCompConn()
print('Le componenti connesse sono:')
for c in compConn:
    if len(c) > 1:
        stringa=''
        for n in c:
            stringa += f'{n.GeneID}, '

        print(f'{stringa} | dimensione componente = {len(c)}')

print()
cammino, punteggio = model.getCamminoOttimo()#eventualmente ci possono essere dei parametri
print(f'Il cammino ottimo ha un punteggio di {punteggio} ed è composto da {len(cammino)} nodi')
for s in cammino:
    print(f'{s}')