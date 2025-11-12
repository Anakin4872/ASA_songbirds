# ---------- Isolation heatmap for Mic1 vs moving interferer ----------
# Hold Bird1 fixed as target for Mic1; sweep a hypothetical interferer in the room plane.
target = birds[0]
mic = mics[0]
xs = np.linspace(0.3, room["L"]-0.3, 80)
ys = np.linspace(0.3, room["W"]-0.3, 80)
Z = np.zeros((len(ys), len(xs)))
for iy, y in enumerate(ys):
    for ix, x in enumerate(xs):
        inter = np.array([x, y, bird_h])
        # isolation = target level minus interferer level (both totals) at Mic1
        Lt, _ = channel_total_dB(mic["pos"], mic["aim"], target)
        Li, _ = channel_total_dB(mic["pos"], mic["aim"], inter)
        Z[iy, ix] = Lt - Li
fig3 = plt.figure(figsize=(6,5))
plt.imshow(Z, extent=[xs[0], xs[-1], ys[0], ys[-1]], origin='lower', aspect='auto')
plt.colorbar(label="Isolation at Mic1 vs interferer (dB)")
plt.scatter([target[0]], [target[1]], marker='x')
plt.scatter([mic["pos"][0]], [mic["pos"][1]])
plt.title("Where can an interferer live? (higher dB = easier isolation)")
plt.xlabel("x (m)"); plt.ylabel("y (m)")
plt.tight_layout()
plt.show()
