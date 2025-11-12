# ---------- DRR–Isolation tradeoff by changing mic–target distance ----------
# Move Mic1 closer/farther on its aim line; compute DRR and isolation vs Bird2 (nearest same-zone)
nearest_interf = birds[1]
p0 = mics[0]["pos"]; aim = unit(mics[0]["aim"])
dists = np.linspace(0.25, 0.80, 30)  # mic–target distance
DRR_vals = []; ISO_vals = []
for r in dists:
    # place mic along the line from target backwards by r
    mp = target - aim*r
    Ltot_t, Ld_t = channel_total_dB(mp, target-mp, target)
    Ltot_i, _ = channel_total_dB(mp, target-mp, nearest_interf)
    DRR_vals.append(Ld_t - L_rev)
    ISO_vals.append(Ltot_t - Ltot_i)
fig4 = plt.figure(figsize=(6,5))
plt.plot(DRR_vals, ISO_vals, marker='o', linewidth=1)
plt.xlabel("Target DRR (dB)")
plt.ylabel("Isolation vs nearest same-zone bird (dB)")
plt.title("clarity vs isolation as you change mic distance")
plt.tight_layout()
plt.show()
