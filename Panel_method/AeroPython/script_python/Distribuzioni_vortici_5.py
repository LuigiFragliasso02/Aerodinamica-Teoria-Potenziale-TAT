import numpy as np
import matplotlib.pyplot as plt

# ============================
# Parametri del problema
# ============================
Gamma = 1.0      # intensità del singolo vortice
a = 1.0          # passo (distanza) tra i vortici lungo x
M = 10           # numero di vortici a sinistra/destra dell'origine -> N = 2*M+1
                 # aumenta M per avvicinarti al caso "infinito"

# Griglia per il dominio di visualizzazione
nx, ny = 201, 201
x = np.linspace(-3.0, 3.0, nx)
y = np.linspace(-2.0, 2.0, ny)
X, Y = np.meshgrid(x, y)

# ============================
# 1) VORTICE PUNTUALE (mattoncino)
# ============================
def velocity_vortex(Gamma, xv, yv, X, Y):
    """
    Velocità (u,v) indotta da un vortice puntuale di intensità Gamma
    posto in (xv, yv), su una griglia (X,Y).
    """
    dx = X - xv
    dy = Y - yv
    r2 = dx**2 + dy**2
    # evito la singolarità al centro (facoltativo, ma utile numericamente)
    r2 = np.where(r2 == 0.0, np.finfo(float).eps, r2)

    u = + Gamma/(2*np.pi) * dy / r2
    v = - Gamma/(2*np.pi) * dx / r2
    return u, v

# ============================
# 2) RIGA FINITA DI VORTICI (sovrapposizione)
# ============================
# posizioni dei vortici: y=0, x = m*a con m=-M,...,M
xv = np.arange(-M, M+1, dtype=float) * a
yv = np.zeros_like(xv)

# campo di velocità totale per riga finita
u_fin = np.zeros_like(X)
v_fin = np.zeros_like(Y)
for xi, yi in zip(xv, yv):
    ui, vi = velocity_vortex(Gamma, xi, yi, X, Y)
    u_fin += ui
    v_fin += vi

# ============================
# 3) RIGA INFINITA (formula analitica del notebook)
#    u(x,y) =  +Gamma/(2a) * sinh(2πy/a) / (cosh(2πy/a) - cos(2πx/a))
#    v(x,y) =  -Gamma/(2a) * sin (2πx/a) / (cosh(2πy/a) - cos(2πx/a))
# ============================
twopi_over_a = 2.0*np.pi/a
den = np.cosh(twopi_over_a*Y) - np.cos (twopi_over_a*X)
# evito eventuali divisioni per 0 esattamente sui punti singolari
den = np.where(den == 0.0, np.finfo(float).eps, den)

u_inf = + (Gamma/(2*a)) * np.sinh(twopi_over_a*Y) / den
v_inf = - (Gamma/(2*a)) * np.sin (twopi_over_a*X) / den

# ============================
# 4) PLOT: distribuzione punti/vortici (cerchi rossi)
# ============================
plt.figure(figsize=(8,3))
plt.scatter(xv, yv, s=40, facecolors='none', edgecolors='red', label='Vortici (centri)')
plt.axhline(0.0, color='k', linewidth=1, alpha=0.4)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlim(x.min(), x.max())
plt.ylim(-0.5*a, 0.5*a)
plt.xlabel('x'); plt.ylabel('y'); plt.title('Riga finita di vortici: posizioni')
plt.legend()
plt.show()

## Save the figure
saveFlnm = 'riga_vortici_posizioni'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

# ============================
# 5) PLOT: streamlines riga FINITA
# ============================
plt.figure(figsize=(8,6))
speed_fin = np.hypot(u_fin, v_fin)
plt.streamplot(X, Y, u_fin, v_fin, density=2, linewidth=1)
plt.scatter(xv, yv, s=40, facecolors='none', edgecolors='red')  # cerchi rossi sui vortici
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('x'); plt.ylabel('y'); plt.title(f'Streamlines – riga finita (N={2*M+1}, a={a})')
plt.xlim(x.min(), x.max()); plt.ylim(y.min(), y.max())
plt.show()

## Save the figure
saveFlnm = 'riga_vortici_finite'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

# ============================
# 6) PLOT: streamlines riga INFINITA (analitica)
# ============================
plt.figure(figsize=(8,6))
speed_inf = np.hypot(u_inf, v_inf)
plt.streamplot(X, Y, u_inf, v_inf, density=2, linewidth=1)
# (niente marker: riga infinita non ha vortici "discreti", ma periodici infiniti)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('x'); plt.ylabel('y'); plt.title('Streamlines – riga infinita (formula analitica)')
plt.xlim(x.min(), x.max()); plt.ylim(y.min(), y.max())
plt.show()

## Save the figure
saveFlnm = 'riga_vortici_infiniti'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

# ============================
# 7) (facoltativo) Confronto qualitativo via contour della velocità
# ============================
levels = np.linspace(0, np.percentile(speed_inf, 99), 25)
fig, axs = plt.subplots(1, 2, figsize=(12,5), constrained_layout=True)
cf0 = axs[0].contourf(X, Y, speed_fin, levels=levels)
axs[0].scatter(xv, yv, s=20, facecolors='none', edgecolors='red')
axs[0].set_title('||V|| – riga finita'); axs[0].set_aspect('equal', 'box')

cf1 = axs[1].contourf(X, Y, speed_inf, levels=levels)
axs[1].set_title('||V|| – riga infinita'); axs[1].set_aspect('equal', 'box')

for ax in axs:
    ax.set_xlabel('x'); ax.set_ylabel('y')
fig.colorbar(cf1, ax=axs.ravel().tolist(), label='Velocità')
plt.show()

## Save the figure
saveFlnm = 'riga_finita_vs_riga_infinita'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')




# RISPOSTA DOMANDE: differenza dei due casi:
# 🔹 Riga finita di vortici

# È la sovrapposizione discreta di un numero limitato di vortici puntuali.

# Alle estremità (a sinistra e a destra) il flusso non è simmetrico → si creano disturbi perché la fila "termina".

# Le streamlines mostrano chiaramente dei vortici localizzati intorno ai cerchi rossi.

# L’effetto di periodicità si nota solo “al centro” della fila; ai bordi le linee di corrente si incurvano e si distorcono.

# Aumentando 𝑀 (più vortici) l’interno della riga diventa sempre più simile a una struttura periodica.


# 🔹 Riga infinita di vortici

# È il limite teorico con 𝑀 → ∞

# Non ha estremità → il flusso è perfettamente periodico in x con passo 𝑎.

# Le linee di corrente sono regolari, ripetute, senza distorsioni ai bordi.

# Esiste una soluzione analitica semplice per  𝑢(𝑥,𝑦),𝑣(𝑥,𝑦), che non richiede di sommare singolarmente i contributi di infiniti vortici.

# Rappresenta la struttura ideale di un reticolo infinito (simile al campo indotto da un "shear layer periodico").



# 🔹 In sintesi

# Finite row (numerico) → buona approssimazione ma presenta effetti di bordo; serve ad avvicinarsi al caso infinito aumentando i vortici.

# Infinite row (analitico) → campo perfettamente periodico, nessun bordo, usato per confrontare e validare la soluzione numerica.
