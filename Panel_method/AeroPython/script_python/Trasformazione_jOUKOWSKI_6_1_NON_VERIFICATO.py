# # Obiettivo:
# # L’idea è questa:

# # Prendere un cilindro in un flusso uniforme (come hai fatto nelle lezioni precedenti).

# # Se aggiungi una circolazione (un vortice), il cilindro sviluppa portanza.

# # Applicare la trasformazione di Joukowski:

# # 𝑧′ = 𝑧 + 𝑐^2/𝑧

# # Questa mappa trasforma un cerchio nel piano 
# # 𝑧 in un profilo alare nel piano 𝑧′→ È un trucco matematico per passare da un corpo semplice (cilindro) a uno realistico (airfoil).

# # Studiare il flusso attorno al profilo generato:

# # Plottare le streamlines nel piano trasformato, per vedere il campo di velocità attorno all’airfoil.

# # Calcolare e disegnare la distribuzione del coefficiente di pressione 𝐶𝑝 lungo il profilo.

# # (Extra) Identificare i punti di stagnazione (dove la velocità è zero) sul profilo trasformato.

# import numpy as np
# import matplotlib.pyplot as plt

# # ===============================
# # 1. Definizione parametri
# # ===============================
# U_inf = 1.0       # velocità di flusso uniforme
# R = 1.0           # raggio del cilindro
# Gamma = 4.0       # circolazione (controlla la portanza)
# c = 1.0           # parametro trasformazione di Joukowski

# # griglia nel piano z (cilindro)
# nx, ny = 200, 200
# x = np.linspace(-2.0, 2.0, nx)
# y = np.linspace(-2.0, 2.0, ny)
# X, Y = np.meshgrid(x, y)
# Z = X + 1j*Y

# # ===============================
# # 2. Potenziale complesso del cilindro
# #    (uniforme + doppietto + vortice)
# # ===============================
# def complex_potential(Z, U, R, Gamma):
#     return (U * (Z + (R**2)/Z) +
#             1j*Gamma/(2*np.pi) * np.log(Z))

# def complex_velocity(Z, U, R, Gamma):
#     return (U * (1 - (R**2)/(Z**2)) -
#             1j*Gamma/(2*np.pi*Z))

# # calcolo campo di velocità nel piano Z
# W = complex_velocity(Z, U_inf, R, Gamma)
# u, v = W.real, -W.imag

# # ===============================
# # 3. Trasformazione di Joukowski
# # ===============================
# Zp = Z + (c**2)/Z

# Xp, Yp = Zp.real, Zp.imag

# # ===============================
# # 4. Streamlines nel piano trasformato
# # ===============================
# plt.figure(figsize=(10,5))
# # plt.streamplot(Xp, Yp, u, v, density=2, linewidth=1)
# plt.streamplot(X, Y, u, v, density=2, linewidth=1) 
# # contorno del cilindro trasformato (profilo airfoil)
# theta = np.linspace(0, 2*np.pi, 400)
# z_cylinder = R*np.exp(1j*theta)
# z_airfoil = z_cylinder + (c**2)/z_cylinder
# plt.plot(z_airfoil.real, z_airfoil.imag, 'k-', linewidth=2)
# plt.gca().set_aspect('equal', adjustable='box')
# plt.title("Streamlines attorno al profilo generato da trasformazione di Joukowski")
# plt.xlabel("x'")
# plt.ylabel("y'")
# plt.show()

# ## Save the figure
# saveFlnm = 'trasformazione_joukowski_streamlines_AIRFOIL'
# savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
# plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

# # ===============================
# # 5. Coefficiente di pressione sul contorno
# # ===============================
# # velocità tangenziale sul cilindro
# W_cylinder = complex_velocity(z_cylinder, U_inf, R, Gamma)
# V_cylinder = np.abs(W_cylinder)

# # Cp sul cilindro
# Cp_cylinder = 1 - (V_cylinder/U_inf)**2

# # trasformato in coordinate del profilo
# x_airfoil = z_airfoil.real
# plt.figure(figsize=(10,5))
# plt.plot(x_airfoil, Cp_cylinder, 'b-', linewidth=2)
# plt.gca().invert_yaxis()  # in aerodinamica Cp viene disegnato verso il basso
# plt.title("Distribuzione di Cp sul profilo (da trasformazione di Joukowski)")
# plt.xlabel("x'")
# plt.ylabel("Cp")
# plt.show()

# ## Save the figure
# saveFlnm = 'trasformazione_joukowski_distribuzione_cp_airfoil'
# savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
# plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')


# # ===============================
# # 6. Confronto Cp: cilindro vs airfoil
# # ===============================
# plt.figure(figsize=(10,5))
# plt.plot(theta*180/np.pi, Cp_cylinder, 'r-', label="Cilindro")
# plt.plot(x_airfoil, Cp_cylinder, 'b-', label="Airfoil (trasformato)")
# plt.gca().invert_yaxis()
# plt.title("Confronto distribuzione Cp: cilindro vs profilo")
# plt.xlabel("Asse (θ in gradi o x' del profilo)")
# plt.ylabel("Cp")
# plt.legend()
# plt.show()

# ## Save the figure
# saveFlnm = 'trasformazione_joukowski_confronto_cilindro_airfoil_cp'
# savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
# plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

# # ===============================
# # 7. Punti di stagnazione
# # ===============================
# # condizione di stagnazione: V = 0
# stagnation_indices = np.where(np.isclose(V_cylinder, 0, atol=1e-2))[0]

# plt.figure(figsize=(10,5))
# plt.plot(z_airfoil.real, z_airfoil.imag, 'k-', linewidth=2, label="Airfoil")
# plt.scatter(z_airfoil.real[stagnation_indices], 
#             z_airfoil.imag[stagnation_indices], 
#             color='red', s=80, label="Punti di stagnazione")
# plt.gca().set_aspect('equal', adjustable='box')
# plt.title("Punti di stagnazione sul profilo di Joukowski")
# plt.xlabel("x'")
# plt.ylabel("y'")
# plt.legend()
# plt.show()

# ## Save the figure
# saveFlnm = 'trasformazione_joukowski_punti_ristagno'
# savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
# plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

import numpy as np
import matplotlib.pyplot as plt

# ============================
# PARAMETRI
# ============================
U_inf = 1.0       # velocità libera
R = 1.0           # raggio cilindro
Gamma = 4.0       # circolazione
c = 1.0           # parametro della trasformazione di Joukowski

# griglia nel piano cilindro
N = 200
x_start, x_end = -2.0, 2.0
y_start, y_end = -2.0, 2.0
x = np.linspace(x_start, x_end, N)
y = np.linspace(y_start, y_end, N)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# ============================
# POTENZIALE COMPLESSO
# ============================
def W(z):
    return (U_inf*(z + R**2/z) + 
            1j*Gamma/(2*np.pi) * np.log(z))

# velocità (derivata del potenziale)
def dW_dz(z):
    return (U_inf*(1 - R**2/z**2) + 
            1j*Gamma/(2*np.pi* z))

# campo velocità nel piano cilindro
vel = dW_dz(Z)
u, v = vel.real, -vel.imag   # attenzione al segno per v

# streamfunction (parte immaginaria del potenziale)
psi = W(Z).imag

# ============================
# PLOT 1: streamlines cilindro
# ============================
plt.figure(figsize=(8,8))
plt.contour(X, Y, psi, levels=np.linspace(-3,3,50), colors='b')
circle = plt.Circle((0,0), R, color='k', fill=False, linewidth=2)
plt.gca().add_patch(circle)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Linee di corrente attorno al cilindro con circolazione")
plt.gca().set_aspect('equal')
plt.show()

# Save the figure
saveFlnm = 'trasformazione_joukowski_streamlines_cilindro'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

# ============================
# TRASFORMAZIONE DI JOUKOWSKI
# ============================
def joukowski(z):
    return z + c**2/z

# contorno cilindro → profilo
theta = np.linspace(0, 2*np.pi, 500)
z_cyl = R*np.exp(1j*theta)
z_airfoil = joukowski(z_cyl)

# trasformazione della griglia
Zp = joukowski(Z)
Xp, Yp = Zp.real, Zp.imag

# streamfunction nel piano trasformato
psi_p = psi   # la streamfunction resta la stessa

# ============================
# PLOT 2: streamlines airfoil
# ============================
plt.figure(figsize=(10,5))
plt.contour(Xp, Yp, psi_p, levels=np.linspace(-3,3,50), colors='b')
plt.plot(z_airfoil.real, z_airfoil.imag, 'k-', linewidth=2)
plt.xlabel("x'")
plt.ylabel("y'")
plt.title("Linee di corrente attorno al profilo (trasformazione di Joukowski)")
plt.gca().set_aspect('equal', adjustable='box')
plt.show()

# Save the figure
saveFlnm = 'trasformazione_joukowski_streamlines_airfoil'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

# ============================
# COEFFICIENTE DI PRESSIONE
# ============================
# velocità tangenziale sul cilindro
V_theta = 2*U_inf*np.sin(theta) + Gamma/(2*np.pi*R)
Cp_cyl = 1 - (V_theta/U_inf)**2

# Cp sul profilo: stesso Cp riportato in coordinate trasformate
Cp_airfoil = Cp_cyl

# ============================
# PLOT 3: Cp sul cilindro
# ============================
plt.figure(figsize=(8,5))
plt.plot(theta*180/np.pi, Cp_cyl, 'r-', linewidth=2)
plt.xlabel("θ (gradi)")
plt.ylabel("Cp")
plt.title("Distribuzione di Cp sul cilindro")
plt.gca().invert_yaxis()
plt.grid()
plt.show()

# Save the figure
saveFlnm = 'trasformazione_joukowski_distribuzione_cp_cilindro'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

# ============================
# PLOT 4: Cp sul profilo alare
# ============================
plt.figure(figsize=(10,5))
plt.plot(z_airfoil.real, Cp_airfoil, 'b-', linewidth=2)
plt.xlabel("x'")
plt.ylabel("Cp")
plt.title("Distribuzione di Cp sul profilo trasformato")
plt.gca().invert_yaxis()
plt.grid()
plt.show()

# Save the figure
saveFlnm = 'trasformazione_joukowski_distribuzione_cp_airfoil'
savePth = '/home/luigi/Progetti_Aerodiamica_git/Panel_method_1/AeroPython/script_python/plot/' + saveFlnm + '.JPG'
plt.savefig(savePth,bbox_inches='tight',facecolor='w',edgecolor='w')

 
