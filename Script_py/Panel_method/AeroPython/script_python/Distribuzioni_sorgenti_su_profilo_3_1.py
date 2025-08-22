import numpy as np
import matplotlib.pyplot as plt
import math

# ======================
# FUNZIONI ELEMENTARI
# ======================

def get_velocity_source(strength, xs, ys, X, Y):
    """
    Velocità indotta da una sorgente/sink.
    """
    u = strength / (2 * np.pi) * (X - xs) / ((X - xs)**2 + (Y - ys)**2)
    v = strength / (2 * np.pi) * (Y - ys) / ((X - xs)**2 + (Y - ys)**2)
    return u, v

def get_stream_function_source(strength, xs, ys, X, Y):
    """
    Funzione di corrente di una sorgente/sink.
    """
    psi = strength / (2 * np.pi) * np.arctan2((Y - ys), (X - xs))
    return psi

def get_velocity_doublet(strength, xd, yd, X, Y):
    """
    Velocità indotta da un doublet.
    """
    u = (- strength / (2 * math.pi) *
         ((X - xd)**2 - (Y - yd)**2) /
         ((X - xd)**2 + (Y - yd)**2)**2)
    v = (- strength / (2 * math.pi) *
         2 * (X - xd) * (Y - yd) /
         ((X - xd)**2 + (Y - yd)**2)**2)
    return u, v

def get_stream_function_doublet(strength, xd, yd, X, Y):
    """
    Funzione di corrente di un doublet.
    """
    psi = - strength / (2 * math.pi) * (Y - yd) / ((X - xd)**2 + (Y - yd)**2)
    return psi

# ======================
# FUNZIONI UTILI
# ======================

def get_velocity_distribution(x_sources, y_sources, strengths, X, Y, U_inf=1.0):
    """
    Calcola il campo di velocità dovuto a una distribuzione di sorgenti + flusso uniforme.
    """
    # flusso uniforme
    u = U_inf * np.ones_like(X)
    v = np.zeros_like(X)

    # aggiungo contributo di tutte le sorgenti
    for (xs, ys, s) in zip(x_sources, y_sources, strengths):
        us, vs = get_velocity_source(s, xs, ys, X, Y)
        u += us
        v += vs
    
    return u, v

def get_pressure_coefficient(u, v, U_inf=1.0):
    """
    Calcola Cp = 1 - (u^2+v^2)/U_inf^2
    """
    return 1.0 - (u**2 + v**2) / U_inf**2

# ======================
# MAIN SCRIPT
# ======================

# Carico i dati del NACA0012
x_s = np.loadtxt('../lessons/resources/NACA0012_x.txt')
y_s = np.loadtxt('../lessons/resources/NACA0012_y.txt')
sigma = np.loadtxt('../lessons/resources/NACA0012_sigma.txt')

# ======================
# PLOT DISTRIBUZIONE SORGENTI
# ======================
plt.figure(figsize=(10,5))
plt.plot(x_s, y_s, 'k-', linewidth=2, label="Profilo NACA0012")   # contorno del profilo
plt.scatter(x_s, y_s, c='red', s=40, marker='o', label="Sorgenti") # punti sorgente

plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel("x")
plt.ylabel("y")
plt.title("Distribuzione dei punti e sorgenti sul profilo NACA0012")
plt.legend()
plt.show()

## Save the figure
saveFlnm = 'NACA0012_visualizzazione_distribuzione_sorgenti'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

# Definisco la griglia
nx, ny = 51, 51
x = np.linspace(-1.0, 2.0, nx)
y = np.linspace(-0.5, 0.5, ny)
X, Y = np.meshgrid(x, y)

# Calcolo velocità totale
U_inf = 1.0
u, v = get_velocity_distribution(x_s, y_s, sigma, X, Y, U_inf)

# Calcolo Cp
Cp = get_pressure_coefficient(u, v, U_inf)

# Trovo massimo di Cp e indici
idx_flat = np.argmax(Cp)
i_max, j_max = np.unravel_index(idx_flat, Cp.shape)
Cp_max = Cp[i_max, j_max]

print(f"Valore massimo Cp: {Cp_max:.4f}")
print(f"Indici del massimo Cp: i={i_max}, j={j_max}")

# ======================
# PLOT STREAMLINES
# ======================
plt.figure(figsize=(10,5))
plt.streamplot(X, Y, u, v, density=2, linewidth=1)
plt.plot(x_s, y_s, 'k-', linewidth=2)
plt.title("Streamlines attorno al NACA0012")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("scaled")
plt.show()

## Save the figure
saveFlnm = 'NACA0012_streamlines'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

# ======================
# PLOT Cp
# ======================
plt.figure(figsize=(10,5))
contf = plt.contourf(X, Y, Cp, levels=50, cmap='coolwarm')
plt.colorbar(contf, label="Cp")
plt.plot(X[i_max, j_max], Y[i_max, j_max], 'mo', markersize=8, label="Max Cp")
plt.plot(x_s, y_s, 'k-', linewidth=2)
plt.legend()
plt.title("Distribuzione Cp attorno al NACA0012")
plt.xlabel("x")
plt.ylabel("y")
plt.axis("scaled")
plt.show()

## Save the figure
saveFlnm = 'NACA0012_Cp'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')
