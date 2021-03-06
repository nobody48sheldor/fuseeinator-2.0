from math import *
import numpy as np
from functools import cache
from numba import jit
import requests

token = "NzQ4MzMyNjU4MTQ0MTgyMzQz.X6chQA.JQvyyhi7toxdYrai8pnL-1i_9FY"
id = '811258320467787828'

def send_message(token, id, msg):
    message = {"content": msg, "nonce": id, "tts": False}
    header = {"authorization": token}
    url = 'https://discord.com/api/v9/channels/{}/messages'.format(id)
    requests.post(url, data = message, headers = header)

with open("type.txt", "r") as type_doc:
    type = type_doc.read()

type = int(type[0])

with open("fi.txt", "r") as fi_doc:
    FI = fi_doc.read().split("/")

if type == 1:
    Cz = float(FI[4])
    m = float(FI[0])

with open("wr.txt", "r") as wr_doc:
    WR = wr_doc.read().split("/")

if type == 2:
    Cz = float(WR[4])
    m = float(WR[0])

g = 9.8
mp = float(FI[1])
fp = float(FI[2])
tp = float(FI[3])
K = 0.5
rho = 1.293
rhoH = float(WR[3])
r = 0.025
h = 0.07
h_ = 0.4
S = (np.pi * r * np.sqrt((r*r) + (h*h)))
k = (Cz * K * rho * S)

Pr = float(WR[2])
mp_ = float(WR[1])
tpwr = (mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*np.pi*((r/2)**2))

n = 100000
dt = 1/10000
dt_ = 1/25

def vfp_(n, fp):
    i = 1
    m_ = m + mp
    v = 0.00000001
    ho = 0
    while i < n+1:
        m_ = m_ - (mp/n)
        v = v + ((fp*(tp/(n))*i)/m_) * np.log(1 + (mp/n)/m_) + (tp/n)*(-(k/m_)*(v**3/abs(v))-g)
        ho = ho + v* (tp/n)
        i = i + 1
    return(v)

@cache
def hvfp_(n, fp):
    i = 1
    m_ = m + mp
    v = 0.00000001
    ho = 0
    H = []
    while i < n+1:
        m_ = m_ - (mp/n)
        v = v + ((fp*(tp/(n))*i)/m_) * np.log(1 + (mp/n)/m_) + (tp/n)*(-(k/m_)*(v**3/abs(v))-g)
        ho = ho + v* (tp/n)
        H.append(ho)
        i = i + 1
    return(H)

@cache
def vvfp_(n, fp):
    i = 1
    m_ = m + mp
    v = 0.00000001
    ho = 0
    V = []
    while i < n+1:
        m_ = m_ - (mp/n)
        v = v + ((fp*(tp/(n))*i)/m_) * np.log(1 + (mp/n)/m_) + (tp/n)*(-(k/m_)*(v**3/abs(v))-g)
        ho = ho + v* (tp/n)
        V.append(v)
        i = i + 1
    return(V)


def vfpc(n, fp, C):
    i = 1
    m_ = m + mp
    v = 0.00000001
    ho = 0
    k = (C * K * rho * S)
    while i < n+1:
        m_ = m_ - (mp/n)
        v = v + ((fp*(tp/(n))*i)/m_) * np.log(1 + (mp/n)/m_) + (tp/n)*(-(k/m_)*(v**3/abs(v))-g)
        ho = ho + v* (tp/n)
        i = i + 1
    return(v)

def vfpcwr(n, P, C):
    i = 1
    m_ = m + mp_
    v = 0.00000001
    ho = 0
    k = (C * K * rho * S)
    while i < n+1:
        m_ = m_ - (mp_/n)
        v = v + np.sqrt(2*P/rhoH) * np.log(1 + (mp_/n)/m_) + (((mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*1.4))/n)*(-(k/m_)*(v**3/abs(v))-g)
        ho = ho + v* (((mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*np.pi*((r/2)**2)))/n)
        i = i + 1
    return(v)

@cache
def vfpwr_(n, P):
    i = 1
    m_ = m + mp_
    v = 0.00000001
    ho = 0
    while i < n+1:
        m_ = m_ - (mp_/n)
        v = v + np.sqrt(2*P/rhoH) * np.log(1 + (mp_/n)/m_) + (((mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*1.4))/n)*(-(k/m_)*(v**3/abs(v))-g)
        ho = ho + v* (((mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*np.pi*((r/2)**2)))/n)
        i = i + 1
    return(v)

@cache
def hvfpwr_(n, P):
    i = 1
    m_ = m + mp_
    v = 0.00000001
    ho = 0
    H = []
    while i < n+1:
        m_ = m_ - (mp_/n)
        v = v + np.sqrt(2*P/rhoH) * np.log(1 + (mp_/n)/m_) + (((mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*1.4))/n)*(-(k/m_)*(v**3/abs(v))-g)
        ho = ho + v* (((mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*np.pi*((r/2)**2)))/n)
        H.append(ho)
        i = i + 1
    return(H)

def vvfpwr_(n, P):
    i = 1
    m_ = m + mp_
    v = 0.00000001
    ho = 0
    V = []
    while i < n+1:
        m_ = m_ - (mp_/n)
        v = v + np.sqrt(2*P/rhoH) * np.log(1 + (mp_/n)/m_) + (((mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*1.4))/n)*(-(k/m_)*(v**3/abs(v))-g)
        ho = ho + v* (((mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*np.pi*((r/2)**2)))/n)
        V.append(v)
        i = i + 1
    return(V)

def ho_(n):
    i = 1
    m_ = m + mp
    v = 0.00000001
    ho = 0
    while i < n+1:
        m_ = m_ - (mp/n)
        v = v + ((fp*(tp/(n))*i)/m_) * np.log(1 + (mp/n)/m_) + (tp/n)*(-(k/m_)*(v**3/abs(v))-g)
        ho = ho + v* (tp/n)
        i = i + 1
    return(ho)

def howr_(n):
    i = 1
    m_ = m + mp_
    v = 0.00000001
    ho = 0
    while i < n+1:
        m_ = m_ - (mp_/n)
        v = v + np.sqrt(2*Pr/rhoH) * np.log(1 + (mp_/n)/m_) + (((mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*1.4))/n)*(-(k/m_)*(v**3/abs(v))-g)
        ho = ho + v* (((mp_/rhoH)/(np.sqrt(2*Pr/rhoH)*np.pi*((r/2)**2)))/n)
        i = i + 1
    return(ho)

ho = ho_(n)
howr = howr_(n)

@cache
def high(vfp, dt):
    t = tp
    h = ho
    H = []
    while h >= 0:
        vfp = vfp + dt*(-(k/m)*(vfp**3/abs(vfp))-g)
        h = h + vfp*dt
        H.append(h)
        t = t + dt
    return(H)

@cache
def highwr(vfp, dt):
    t = tpwr
    h = howr
    H = []
    while h >= 0:
        vfp = vfp + dt*(-(k/m)*(vfp**3/abs(vfp))-g)
        h = h + vfp*dt
        H.append(h)
        t = t + dt
    return(H)

def highmax(vfp, dt):
    t = 0
    h = 0
    while vfp >= 0:
        vfp = vfp + dt*(-(k/m)*(vfp**3/abs(vfp))-g)
        h = h + vfp*dt
        t = t + dt
    return(h)

def highmaxC(vfp, dt, C):
    t = 0
    h = 0
    k = (C * K * rho * S)
    while vfp >= 0:
        vfp = vfp + dt*(-(k/m)*(vfp**3/abs(vfp))-g)
        h = h + vfp*dt
        t = t + dt
    return(h)

def speed(vfp, dt):
    t = tp
    h = ho
    V = []
    while h >= 0:
        vfp = vfp + dt*(-(k/m)*(vfp**3/abs(vfp))-g)
        h = h + vfp*dt
        V.append(vfp)
        t = t + dt
    return(V)

def speedwr(vfp, dt):
    t = tpwr
    h = howr
    V = []
    while h >= 0:
        vfp = vfp + dt*(-(k/m)*(vfp**3/abs(vfp))-g)
        h = h + vfp*dt
        V.append(vfp)
        t = t + dt
    return(V)

@cache
def hmax():
    H = []
    VFP = []
    FP = []
    fp = 10
    while fp < 1000:
        v = vfp_(n, fp)
        H.append(highmax(v, dt_))
        VFP.append(v)
        FP.append(fp)
        fp = fp + 5
        if fp%(10) == 0:
            print(fp/(10), "%")
    R = []
    R.append(FP)
    R.append(VFP)
    R.append(H)
    return(R)

@cache
def hmaxwr():
    H = []
    VFP = []
    P = []
    p = 100000
    while p < 2000000:
        v = vfpwr_(n, p)
        H.append(highmax(v, dt_))
        VFP.append(v)
        P.append(p)
        p = p + 20000
        if p%(20000) == 0:
            print(p/(20000), "%")
    R = []
    R.append(P)
    R.append(VFP)
    R.append(H)
    return(R)

def highC(n):
    dt = 1/n
    c = np.linspace(0, 1.5, n)
    R = []
    H = []
    i = 0
    while i < n:
        C = c[i]
        vfp = vfpc(n, fp, C)
        h = highmaxC(vfp, dt, C)
        H.append(h)
        i = i + 1
    R.append(c)
    R.append(H)
    return(R)

def highCwr(n):
    dt = 1/n
    c = np.linspace(0, 1.5, n)
    R = []
    H = []
    i = 0
    while i < n:
        C = c[i]
        vfp = vfpcwr(n, Pr, C)
        h = highmaxC(vfp, dt, C)
        H.append(h)
        i = i + 1
    R.append(c)
    R.append(H)
    return(R)
