import pandas as pd
import matplotlib.pyplot  as plt
from matplotlib.ticker import MultipleLocator

#obliczenie wykładniczej średniej kroczącej o n elementach z df zaczynajac od m
def EMA(m,n,df):
    a=2/(n+1)
    temp=1
    EMAu=0
    EMAd=0
    for i in range(m,m+n):
        EMAu += df[i] * temp
        EMAd += temp
        temp *= (1-a)
    return EMAu/EMAd
ILOSC=1000
df = pd.read_csv("pieniedze/kasa.csv")
Value=df.Zamkniecie
Date=df.Data
MACDv=[]
SIGNAL=[]
#obliczenie wartosci MACD zaczynajac od 27 elementu
for i in range(27,ILOSC):
    EMA26=EMA(i-27,26,df.Zamkniecie)
    EMA12=EMA(i-27,12,df.Zamkniecie)
    MACDv.insert(i-27,EMA12-EMA26)
#obliczenie wartosci Signal zaczyanajac od 36 elementu(27+9)
for i in range(36,ILOSC):
    EMA9=EMA(i-36,9,MACDv)
    SIGNAL.insert(i-36,EMA9)

#Wykres
#wrownanie wartosci na osiach
MACDv=MACDv[8:-1]
Date=Date[36:ILOSC]
Value=Value[36:ILOSC]

fig, ax = plt.subplots()
#ustawienie na osi x odstepu wartosci od siebie
ax.xaxis.set_major_locator(MultipleLocator(ILOSC/10))
ax.xaxis.set_minor_locator(MultipleLocator(ILOSC/100))
#dodanie lini MACD Signal oraz wartosci akcji
plt.plot(Date,MACDv)
plt.plot(Date,SIGNAL)
plt.plot(Date,Value)
#dodanie legendy
plt.legend(['MACD','Signal','Value'])
#ustawienie dat pod ukosem
fig.autofmt_xdate()
plt.show()

#algorytm kupujący i sprzedający akcje
money=10000
actions=0
newSingal=0
newMACD=0
oldSignal=SIGNAL[0]
oldMACD=MACDv[0]
for i in range(1,ILOSC-36):
    newMACD=MACDv[i]
    newSingal=SIGNAL[i]
    #MACD przzecina od dolu
    #wyznaczenie przeciecia na podstawie wartosci MACD i Signal z dnia wczesniejszego
    if newMACD>newSingal and oldMACD<oldSignal:
        #kupienie tylu akcji na ile nas stac
        while df.Zamkniecie[i]<money:
            actions=actions+1
            money=money-df.Zamkniecie[i]
    #MACD przecina od gory
    #wyznaczenie przeciecia na podstawie wartosci MACD i Signal z dnia wczesniejszego
    if newMACD < newSingal and oldMACD > oldSignal:
        #sprzedanie wszystkich akcji
        while actions>0:
            actions = actions - 1
            money = money + df.Zamkniecie[i]
    #zapisanie starnych wartosci
    oldMACD=newMACD
    oldSignal=newSingal
print("pieniadze: ",money)
print("akcje: ",actions)
print ("wartość zasobów: ",Value.iloc[-1]*actions+money)


