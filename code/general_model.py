#################################################
### General acoustic setup model for the room ###

import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---------- Room & global params ----------
room = dict(L=3.94, W=3.224, H=2.58)  # meters
T60 = 0.15                             # assumed RT60 (change to 0.10–0.25 if you want)
Q = 3.0                                # cardioid
Dc = 0.057 * math.sqrt(Q * (room["L"]*room["W"]*room["H"]) / T60)  # critical distance (m)
L0 = 70.0                              # SPL at 1 m (arbitrary ref; differences matter)

# ---------- Helpers (cardioid directivity + simple room model) ----------
def unit(v):
    v = np.array(v, dtype=float)
    n = np.linalg.norm(v)
    return v / (n + 1e-12)

def cardioid_mag(theta_rad):
    return max((1 + math.cos(theta_rad)) / 2.0, 1e-6)

def direct_level_dB(mic_pos, mic_aim_vec, src_pos):
    r_vec = np.array(src_pos) - np.array(mic_pos)
    r = np.linalg.norm(r_vec)
    if r < 1e-6: r = 1e-6
    aim = unit(mic_aim_vec)
    theta = math.acos(np.clip(np.dot(aim, unit(r_vec)), -1.0, 1.0))
    patt = cardioid_mag(theta)
    Ld = L0 - 20.0*math.log10(r) + 20.0*math.log10(patt)
    return Ld, r, theta

L_rev = L0 - 20.0*math.log10(max(Dc, 1e-6))  # set so DRR=0 at r=Dc

def channel_total_dB(mic_pos, mic_aim_vec, src_pos):
    Ld, r, theta = direct_level_dB(mic_pos, mic_aim_vec, src_pos)
    L_lin = 10**(Ld/10.0) + 10**(L_rev/10.0)
    return 10*math.log10(L_lin), Ld

def mix_matrix(mics, birds):
    """
    mics: list of dicts with keys posit (x,y,z), aim (dx,dy,dz)
    birds: list of 3D positions
    Returns: MxB matrix of total levels (dB), plus DRR matrix (dB, using direct only)
    """
    M, B = len(mics), len(birds)
    G = np.zeros((M,B))
    DRR = np.zeros((M,B))
    for i, m in enumerate(mics):
        for j, b in enumerate(birds):
            Ltot, Ld = channel_total_dB(m["pos"], m["aim"], b)
            G[i,j] = Ltot
            DRR[i,j] = Ld - L_rev
    return G, DRR

def isolation_for_assignment(G, assign):
    """
    assign: list of target bird index (len=mics), or -1 if unused.
    Returns per-mic isolation: target minus summed others (energy sum).
    """
    M, B = G.shape
    iso = []
    for i in range(M):
        t = assign[i]
        if t < 0: 
            iso.append(np.nan)
            continue
        Lt = G[i, t]
        inter_lin = 0.0
        for b in range(B):
            if b == t: continue
            inter_lin += 10**(G[i,b]/10.0)
        Li = 10*math.log10(inter_lin) if inter_lin>0 else -np.inf
        iso.append(Lt - Li)
    return np.array(iso)

# ---------- Layout (scales to 6 birds, 3 mics) ----------
# Coordinates: (x along 3.94 m wall, y along 3.224 m wall, z height)
bird_h = 1.30
# Six potential cage positions (two per "zone(mic)"); comment out some if you have fewer birds
birds = [
    np.array([0.80, 0.80, bird_h]),  # zone 1
    np.array([0.80, 1.30, bird_h]),
    np.array([3.14, 0.80, bird_h]),  # zone 2
    np.array([3.14, 1.30, bird_h]),
    np.array([0.80, 2.00, bird_h]),  # zone 3
    np.array([0.80, 2.50, bird_h]),
]

# Three mics around the room, staggered heights, aimed inward
mics = [
    dict(pos=np.array([0.45, 0.45, 1.60]), aim=np.array([0.80, 0.80, bird_h])-np.array([0.45,0.45,1.60])),
    dict(pos=np.array([3.49, 0.45, 1.40]), aim=np.array([3.14, 0.80, bird_h])-np.array([3.49,0.45,1.40])),
    dict(pos=np.array([0.45, 2.77, 1.20]), aim=np.array([0.80, 2.50, bird_h])-np.array([0.45,2.77,1.20])),
]

G, DRR = mix_matrix(mics, birds)
