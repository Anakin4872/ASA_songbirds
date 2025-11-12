# ---------- Crosstalk / mixing matrix (dB) ----------
fig2 = plt.figure(figsize=(6,4))
plt.imshow(G, aspect='auto')
plt.colorbar(label="dB")
plt.yticks(range(len(mics)), [f"Mic{i+1}" for i in range(len(mics))])
plt.xticks(range(len(birds)), [f"B{j+1}" for j in range(len(birds))], rotation=0)
plt.title("Predicted level matrix G (Mic × Bird)")
plt.tight_layout()
plt.show()
