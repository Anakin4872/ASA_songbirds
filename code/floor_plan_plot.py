# ---------- Floor plan with mics, birds, and rough cardioid lobes ----------
fig = plt.figure(figsize=(6,6))
# Room rectangle
plt.plot([0, room["L"], room["L"], 0, 0], [0, 0, room["W"], room["W"], 0])
# Birds
for j, b in enumerate(birds):
    plt.scatter([b[0]], [b[1]], marker='o')
    plt.text(b[0]+0.03, b[1]+0.03, f"B{j+1}")
# Mics and aim
for i, m in enumerate(mics):
    p = m["pos"]; a = unit(m["aim"])
    plt.scatter([p[0]], [p[1]])
    plt.text(p[0]+0.03, p[1]-0.06, f"M{i+1}")
    # draw aim ray
    ray_len = 0.5
    plt.plot([p[0], p[0]+a[0]*ray_len], [p[1], p[1]+a[1]*ray_len])
    # crude cardioid outline in 2D (plan view only)
    phis = np.linspace(0, 2*np.pi, 100)
    r = 0.4*(1+np.cos(phis))/2.0  # scaled
    # rotate so 0 rad aligns with aim
    ang = math.atan2(a[1], a[0])
    xx = p[0] + r*np.cos(phis+ang)
    yy = p[1] + r*np.sin(phis+ang)
    plt.plot(xx, yy, linewidth=1)
plt.axis('equal')
plt.xlim(0, room["L"]); plt.ylim(0, room["W"])
plt.title("Floor plan: mics, birds, and approximate cardioid lobes")
plt.xlabel("x (m)"); plt.ylabel("y (m)")
plt.tight_layout()

plt.show()
