#################################################################################################
#                                                                                               #
#                   Utroligt tung og rodet kode, som kunne optimeres gevaldigt.                 #
#                   Jeg kunne derudover gøre flere af metoderne dynamiske, så jeg               #
#                   kunne genbruge dem i checkpoint-opgaverne.                                  #
#                                                                                               #
#                   Men det virker! Og til sidst ville jeg bare gerne blive færdig              #
#                   og aflevere.                                                                #
#                                                                                               #
#                                           God weekend!                                        #
#                                                                                               #
#################################################################################################


############################# Opgave 1-2 #############################

# Her udleveres kode til løsning af opgave 1

def pace2velocity(p):
    return (1000/60)/p

assert pace2velocity(10) == 1.666666666666666666

def v2p(v):
    return (1000/60)/v

assert v2p(1.666666666666666666) == 10

# Her udleveres kode til at løse opgave 2
# virker med stien når du har mappen `projektopgave` aktiv`

def indlaes_fra_fit(fname = "projektopgave/data/hok_klubmesterskab_2022/CA8D1347.FIT"):
    from fit_file import read
    points = read.read_points(fname)
    return points

punkter = indlaes_fra_fit()

print(f"Der er indlæst {len(punkter)} punkter fra filen")
print(punkter[300])

############################# Opgave 3-5 #############################

from geopy.distance import distance 

run = list()
runSeconds = list ()
runPercent = float()
runMeters = list()
walk = list()
walkSeconds = list()
walkPercent = float()
walkMeters = list()
idle = list()
idleSeconds = list()
idlePercent = float()
idleMeters = list()

# Funktion, der itererer gennem vores liste af hastighed(m/s)
# og konkluderer så om der bliver løbet/gået/stået
def tempoZones(msList, seconds, distance):

    for i, ms in enumerate(msList):
        if ms > pace2velocity(10):
            run.append(ms)
            runSeconds.append(seconds[i])
            runMeters.append(distance[i])
        elif ms < pace2velocity(10) and ms > pace2velocity(50):
            walk.append(ms)
            walkSeconds.append(seconds[i])
            walkMeters.append(distance[i])
        elif ms < pace2velocity(50):
            idle.append(ms)
            idleSeconds.append(seconds[i])
            idleMeters.append(distance[i])
    
    global runPercent
    global walkPercent
    global idlePercent

    runPercent = round(sum(runSeconds) / sum(runTime) * 100, 1)
    walkPercent = round(sum(walkSeconds) / sum(runTime) * 100, 1)
    idlePercent = round(sum(idleSeconds) / sum(runTime) * 100, 1)

 # Funktion, der printer et table med relevant data ud i konsollen
def printTable():
    d = {"Run": [round(sum(runMeters), 1), sum(runSeconds), str(runPercent) + "%"],
    "Walk": [round(sum(walkMeters), 1), sum(walkSeconds), str(walkPercent) + "%"],
    "Idle": [round(sum(idleMeters), 1), sum(idleSeconds), str(idlePercent) + "%"],
    "Total": [round(sum(ddList), 1), sum(runTime), str(round(runPercent + walkPercent + idlePercent)) + "%"],
    }

    print ("{:<15} {:<15} {:<10} {:<10}".format('Entire Run','Meters','Seconds','Percent'))
    for k, v in d.items():
        Meters, Seconds, Percent = v
        print ("{:<15} {:<15} {:<10} {:<10}".format(k, Meters, Seconds, Percent))
    print("-------------------------------------------------------------")

runTime = list()
vList = list()
ddList = list()
for i, p in enumerate(punkter[1:]):
    # previus point
    pp = punkter[i]

    dt = (p['timestamp'] - pp['timestamp']).seconds
    dd = distance( (pp['latitude'], pp['longitude']), (p['latitude'], p['longitude'])).meters
    v = dd/dt
    vList.append(v)
    ddList.append(dd)
    runTime.append(dt)

tempoZones(vList, runTime, ddList)
printTable()

############################# Opgave 6 #############################

import csv
import datetime

# Her åbner vi en forbindelse til CSV-filen og gemmer dataen i postkontroller-variablen
with open('projektopgave/data/hok_klubmesterskab_2022/kontroltider.csv', 'r', 
          encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    postkontroller = [{ 'nr':row['nr'], 
            'timestamp': datetime.datetime.fromisoformat(row['timestamp']) } 
          for row in reader]
    

checkpointList = []
actualDistanceList = list()
straightLineList = list()

for i, pk in enumerate(postkontroller[1:]):
    # Definerer en variabel, der indholder alle punkter med timestamps inden for det aktulle og det næste index i postkontroller
    st = [p for p in punkter if p['timestamp'].astimezone() < postkontroller[i+1]['timestamp']
                             if  p['timestamp'].astimezone() > postkontroller[i]['timestamp']]

    checkpointList.append(st)
    
    # Beregner afstanden mellem det første og det sidste målepunkt (fugleflugt)
    straightLine = distance( (st[0]['latitude'], st[0]['longitude']), (st[-1]['latitude'], st[-1]['longitude'])).meters
    straightLineList.append(straightLine)

    ddList = list()
    # Beregner afstanden mellem hvert enkelt punkt
    for j, px in enumerate(st[1:]):
        ppx = st[j]
        
        dd = distance( (ppx['latitude'], ppx['longitude']), (px['latitude'], px['longitude'])).meters
        ddList.append(dd)
    actualDistanceList.append(sum(ddList))
    
############################# Opgave 7 #############################

# Funktion, der itererer gennem vores liste af hastighed(m/s)
# og konkluderer så om der bliver løbet/gået/stået
def checkpointTempoZones(msList, seconds, distance):
    checkpointRun = list()
    checkpointRunSeconds = list ()
    checkpointRunPercent = float()
    checkpointRunMeters = list()
    checkpointWalk = list()
    checkpointWalkSeconds = list()
    checkpointWalkPercent = float()
    checkpointWalkMeters = list()
    checkpointIdle = list()
    checkpointIdleSeconds = list()
    checkpointIdlePercent = float()
    checkpointIdleMeters = list()

    for i, ms in enumerate(msList):
        if ms > pace2velocity(10):
            checkpointRun.append(ms)
            checkpointRunSeconds.append(seconds[i])
            checkpointRunMeters.append(distance[i])
        elif ms < pace2velocity(10) and ms > pace2velocity(50):
            checkpointWalk.append(ms)
            checkpointWalkSeconds.append(seconds[i])
            checkpointWalkMeters.append(distance[i])
        elif ms < pace2velocity(50):
            checkpointIdle.append(ms)
            checkpointIdleSeconds.append(seconds[i])
            checkpointIdleMeters.append(distance[i])

    checkpointRunPercent = round(sum(checkpointRunSeconds) / sum(seconds) * 100, 1)
    checkpointWalkPercent = round(sum(checkpointWalkSeconds) / sum(seconds) * 100, 1)
    checkpointIdlePercent = round(sum(checkpointIdleSeconds) / sum(seconds) * 100, 1)
    
    # Denne her gang har jeg valgt at bruge lokale variabler og kalde på vores print-funktion herfra
    # Det gjorde det også meget nemmere for mig bare at kalde på tempo-metoden gennem checkpoints
    # og derved iterere igennem dem
    printCheckpointTable(checkpointRunMeters, checkpointRunSeconds, checkpointRunPercent,
                         checkpointWalkMeters, checkpointWalkSeconds, checkpointWalkPercent,
                         checkpointIdleMeters, checkpointIdleSeconds, checkpointIdlePercent,
                         distance, seconds)
    
checkpointIndex = int()
def printCheckpointTable(*variables):
    global checkpointIndex
    checkpointIndex += 1
    d = {"Run": [round(sum(variables[0]), 1), sum(variables[1]), str(variables[2]) + "%"],
    "Walk": [round(sum(variables[3]), 1), sum(variables[4]), str(variables[5]) + "%"],
    "Idle": [round(sum(variables[6]), 1), sum(variables[7]), str(variables[8]) + "%"],
    "Total": [round(sum(variables[9]), 1), sum(variables[10]), str(round(variables[2] + variables[5] + variables[8])) + "%"],
    }

    print ("{:<15} {:<10} {:<10} {:<10}".format(f'Checkpoint {checkpointIndex}','Meters','Seconds','Percent'))
    for k, v in d.items():
        Meters, Seconds, Percent = v
        print ("{:<15} {:<10} {:<10} {:<10}".format(k, Meters, Seconds, Percent))
    print("")

# Her itererer jeg gennem vores nye liste af målpunkter, som er sepereret af checkpoints
# og gør derefter egentligt bare det samme mht. distance, m/s og tid som første gang
for checkpoint in checkpointList:

    checkpointMsList = list()
    checkpointRuntimeList = list()
    checkpointDistanceList = list()

    for i, p in enumerate(checkpoint[1:]):
        pp = checkpoint[i]

        dt = (p['timestamp'] - pp['timestamp']).seconds
        dd = distance( (pp['latitude'], pp['longitude']), (p['latitude'], p['longitude'])).meters
        v = dd/dt
        checkpointMsList.append(v)
        checkpointDistanceList.append(dd)
        checkpointRuntimeList.append(dt)
    
    checkpointTempoZones(checkpointMsList, checkpointRuntimeList, checkpointDistanceList)

##############################################################
    
