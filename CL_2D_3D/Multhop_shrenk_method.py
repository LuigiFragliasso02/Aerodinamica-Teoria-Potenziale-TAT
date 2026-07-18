import numpy as np
import matplotlib.pyplot as plt

def analizza_ala(forma='trapezoidale', metodo='multhopp', b=10.0, c_root_trap=1.0, c_tip_trap=0.5, alpha_deg=5.0, a0=2*np.pi):
    """
    Risolve l'aerodinamica dell'ala specificata.
    Le due ali (trapezoidale ed ellittica) sono costruite per avere la stessa area S e apertura b.
    """
    n = 31 # Numero di stazioni (dispari, più alto = curve più lisce)
    v = np.arange(1, n + 1)
    theta = v * np.pi / (n + 1)
    eta = np.cos(theta)
    y = eta * (b / 2)
    
    # Calcolo Area di riferimento (Ala Trapezoidale)
    S = (c_root_trap + c_tip_trap) * b / 2
    AR = b**2 / S
    
    # 1. COSTRUZIONE DISTRIBUZIONE DI CORDA c(eta)
    if forma == 'trapezoidale':
        c = c_root_trap - (c_root_trap - c_tip_trap) * np.abs(eta)
    elif forma == 'ellittica':
        # Per avere la stessa area S: S = (pi/4) * b * c_root_ell
        c_root_ell = (4 * S) / (np.pi * b)
        c = c_root_ell * np.sqrt(1 - eta**2)
    else:
        raise ValueError("Forma non valida.")
        
    alpha = np.deg2rad(alpha_deg)
    V_inf = 1.0 
    
    # 2. CALCOLO CIRCOLAZIONE (GAMMA)
    if metodo == 'schrenk':
        a_3d = a0 / (1 + a0 / (np.pi * AR))
        CL_stimato = a_3d * alpha
        
        # Gamma ellittica teorica (stesso CL)
        Gamma_root_ell = (2 * V_inf * S * CL_stimato) / (np.pi * b)
        gamma_ell = Gamma_root_ell * np.sin(theta)
        
        # Gamma geometrica (proporzionale alla corda locale)
        gamma_geom = 0.5 * V_inf * CL_stimato * c
        
        # Media di Schrenk
        gamma = 0.5 * (gamma_ell + gamma_geom)
        
    elif metodo == 'multhopp':
        A = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i == j:
                    b_vv = (n + 1) / (2 * np.sin(theta[i]))
                    A[i, j] = (2 * b) / (a0 * c[i]) + b_vv
                else:
                    if abs(i - j) % 2 != 0:
                        b_vj = (2 / (n + 1)) * np.sin(theta[j]) / (np.cos(theta[j]) - np.cos(theta[i]))**2
                        A[i, j] = -b_vj
                        
        gamma_adim = np.linalg.solve(A, alpha * np.ones(n))
        gamma = gamma_adim * (b * V_inf)

    # 3. CARICHI GLOBALI TRAMITE FOURIER
    k_vals = np.arange(1, n + 1)
    M = np.zeros((n, n))
    for i in range(n):
        for j, k in enumerate(k_vals):
            M[i, j] = 2 * b * V_inf * np.sin(k * theta[i])
            
    A_coeffs, _, _, _ = np.linalg.lstsq(M, gamma, rcond=None)
    
    CL = A_coeffs[0] * np.pi * AR
    CDi = np.pi * AR * np.sum(k_vals * A_coeffs**2)
    e = A_coeffs[0]**2 / np.sum(k_vals * A_coeffs**2) if CDi > 0 else 0

    # 4. CARICHI LOCALI
    cl_c = 2 * gamma / V_inf
    cl_locale = cl_c / c


    # CALCOLO FORZE FISICHE (Dimensionali)
    V_inf = 50.0  # Velocità di riferimento [m/s]
    rho = 1.225  # Densità dell'aria a livello del mare [kg/m^3]
    q_inf = 0.5 * rho * V_inf**2  # Pressione dinamica
    L_totale = CL * q_inf * S     # Portanza in Newton [N]
    D_indotta = CDi * q_inf * S   # Resistenza Indotta in Newton [N]

    print(f"\n--- RISULTATI FISICI (a {V_inf} m/s) ---")
    print(f"Portanza Totale: {L_totale:.2f} N")
    print(f"Resistenza Indotta: {D_indotta:.2f} N")
    print(f"Efficienza Aerodinamica (di sola ala): {CL/CDi if CDi>0 else 0:.2f}")
    V_inf = 1.0

    return eta, gamma, cl_c, cl_locale, c, CL, CDi, e

# ==========================================
# ESECUZIONE DELLE 4 CONFIGURAZIONI
# ==========================================
risultati = {}
configurazioni = [
    ('trapezoidale', 'multhopp', 'b', '-'),   # Blu continuo
    ('trapezoidale', 'schrenk',  'b', '--'),  # Blu tratteggiato
    ('ellittica',    'multhopp', 'r', '-'),   # Rosso continuo
    ('ellittica',    'schrenk',  'r', '--')   # Rosso tratteggiato
]

for forma, met, col, style in configurazioni:
    eta, gamma, cl_c, cl_loc, c, CL, CDi, e = analizza_ala(forma=forma, metodo=met)
    risultati[f"{forma}_{met}"] = {
        'eta': eta, 'gamma': gamma, 'cl_c': cl_c, 'cl_loc': cl_loc, 'c': c, 
        'CL': CL, 'CDi': CDi, 'e': e, 'col': col, 'style': style,
        'label': f"{forma.capitalize()} - {met.capitalize()}"
    }

# ==========================================
# STAMPA TABELLA DI CONFRONTO
# ==========================================
print("\n" + "="*80)
print(f"{'FORMA ALA':<15} | {'METODO':<12} | {'C_L':<10} | {'C_Di':<12} | {'OSWALD (e)':<10}")
print("-" * 80)
for k, v in risultati.items():
    forma, met = k.split('_')
    print(f"{forma.capitalize():<15} | {met.capitalize():<12} | {v['CL']:<10.4f} | {v['CDi']:<12.6f} | {v['e']:<10.3f}")
print("="*80 + "\n")

# ==========================================
# PLOTTING SISTEMATICO
# ==========================================
fig, axs = plt.subplots(2, 2, figsize=(15, 11))

# --- Plot 1: Distribuzione Geometrica della Corda ---
axs[0, 0].plot(risultati['trapezoidale_multhopp']['eta'], risultati['trapezoidale_multhopp']['c'], 'b-', linewidth=2, label='Ala Trapezoidale')
axs[0, 0].plot(risultati['ellittica_multhopp']['eta'], risultati['ellittica_multhopp']['c'], 'r-', linewidth=2, label='Ala Ellittica (Stessa Area)')
axs[0, 0].fill_between(risultati['trapezoidale_multhopp']['eta'], 0, risultati['trapezoidale_multhopp']['c'], color='blue', alpha=0.1)
axs[0, 0].fill_between(risultati['ellittica_multhopp']['eta'], 0, risultati['ellittica_multhopp']['c'], color='red', alpha=0.1)
axs[0, 0].set_title('Confronto Forme in Pianta $c(\eta)$', fontsize=12, fontweight='bold')
axs[0, 0].set_xlabel('$\eta = 2y/b$')
axs[0, 0].set_ylabel('Corda [m]')
axs[0, 0].legend()
axs[0, 0].grid(True, linestyle=':')

# --- Plot 2: Distribuzione di Circolazione Gamma ---
for key, v in risultati.items():
    axs[0, 1].plot(v['eta'], v['gamma'], color=v['col'], linestyle=v['style'], linewidth=2, label=v['label'])
axs[0, 1].set_title('Distribuzione della Circolazione $\Gamma(\eta)$', fontsize=12, fontweight='bold')
axs[0, 1].set_xlabel('$\eta$')
axs[0, 1].set_ylabel('$\Gamma$')
axs[0, 1].legend()
axs[0, 1].grid(True, linestyle=':')

# --- Plot 3: Carico Alare Locale (cl * c) ---
for key, v in risultati.items():
    axs[1, 0].plot(v['eta'], v['cl_c'], color=v['col'], linestyle=v['style'], linewidth=2, label=v['label'])
axs[1, 0].set_title('Distribuzione Carico Alare $C_l \cdot c$', fontsize=12, fontweight='bold')
axs[1, 0].set_xlabel('$\eta$')
axs[1, 0].set_ylabel('$C_l \cdot c$ [m]')
axs[1, 0].legend()
axs[1, 0].grid(True, linestyle=':')

# --- Plot 4: Coefficiente di Portanza Locale (cl) ---
for key, v in risultati.items():
    axs[1, 1].plot(v['eta'], v['cl_loc'], color=v['col'], linestyle=v['style'], linewidth=2, label=v['label'])
axs[1, 1].set_title('Coefficiente di Portanza Locale $C_l$', fontsize=12, fontweight='bold')
axs[1, 1].set_xlabel('$\eta$')
axs[1, 1].set_ylabel('$C_l$')
axs[1, 1].legend()
axs[1, 1].grid(True, linestyle=':')

plt.tight_layout(pad=3.0)
plt.show()