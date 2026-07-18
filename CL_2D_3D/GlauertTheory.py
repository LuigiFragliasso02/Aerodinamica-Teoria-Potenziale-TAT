import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad, trapezoid

# =========================================================
# 1. FUNZIONI GEOMETRICHE (NACA 4-DIGIT) E DERIVATE (dy/dx)
# =========================================================
def dy_dx_thickness(x, t):
    x = max(x, 1e-8)
    return 5 * t * (0.2969 / (2 * np.sqrt(x)) - 0.1260 - 0.7032 * x + 0.8529 * x**2 - 0.4060 * x**3)

def dy_dx_camber(x, m, p):
    if x < p:
        return (2 * m / p**2) * (p - x)
    else:
        return (2 * m / (1 - p)**2) * (p - x)

# =========================================================
# 2. I TRE PROBLEMI SEPARATI DI GLAUERT
# =========================================================
def u_lastra_piana(theta, alpha_deg):
    alpha = np.deg2rad(alpha_deg)
    return alpha * (1 + np.cos(theta)) / np.sin(theta)

def u_linea_curva(theta_array, m, p):
    def integrand_A0(th):
        xi = 0.5 * (1 - np.cos(th))
        return dy_dx_camber(xi, m, p)
    A0 = - (1 / np.pi) * quad(integrand_A0, 0, np.pi, limit=200)[0]
    
    A_coeffs = np.zeros(10)
    for n in range(1, 10):
        def integrand_An(th, n_val):
            xi = 0.5 * (1 - np.cos(th))
            return dy_dx_camber(xi, m, p) * np.cos(n_val * th)
        A_coeffs[n] = (2 / np.pi) * quad(integrand_An, 0, np.pi, args=(n,), limit=200)[0]
        
    u_camber = np.zeros_like(theta_array)
    for i, th in enumerate(theta_array):
        val = A0 * (1 + np.cos(th)) / np.sin(th)
        for n in range(1, 10):
            val += A_coeffs[n] * np.sin(n * th)
        u_camber[i] = val
    return u_camber

def u_profilo_simmetrico(x_array, t):
    u_thick = np.zeros_like(x_array)
    for i, x_val in enumerate(x_array):
        def integrand_ut(xi, x_v):
            if abs(xi - x_v) < 1e-7: return 0.0
            return (dy_dx_thickness(xi, t) - dy_dx_thickness(x_v, t)) / (x_v - xi)
        
        val, _ = quad(integrand_ut, 1e-6, 1.0, args=(x_val,), limit=200)
        val += dy_dx_thickness(x_val, t) * np.log(x_val / (1.0 - x_val))
        u_thick[i] = val / np.pi
    return u_thick

# =========================================================
# 3. ESECUZIONE E SOVRAPPOSIZIONE DEGLI EFFETTI
# =========================================================
N = 150
theta = np.linspace(np.pi/(2*N), np.pi - np.pi/(2*N), N)
x = 0.5 * (1 - np.cos(theta))

# Dati NACA 2405 e Assetto
m_val, p_val, t_val = 0.02, 0.40, 0.05
alpha_target = 3.0

u_alpha = u_lastra_piana(theta, alpha_target)
u_camber = u_linea_curva(theta, m_val, p_val)
u_thick = u_profilo_simmetrico(x, t_val)

u_dorso  = u_thick + u_camber + u_alpha
u_ventre = u_thick - u_camber - u_alpha

dy_dx_upper = np.array([dy_dx_camber(xi, m_val, p_val) + dy_dx_thickness(xi, t_val) for xi in x])
dy_dx_lower = np.array([dy_dx_camber(xi, m_val, p_val) - dy_dx_thickness(xi, t_val) for xi in x])

V_upper = (1.0 + u_dorso) / np.sqrt(1.0 + dy_dx_upper**2)
V_lower = (1.0 + u_ventre) / np.sqrt(1.0 + dy_dx_lower**2)

Cp_upper = 1.0 - V_upper**2
Cp_lower = 1.0 - V_lower**2

# =========================================================
# 4. CALCOLO COEFFICIENTI (STILE XFOIL)
# =========================================================
# Integrazione numerica delle curve (come nei codici a pannelli)
# Cl = int (Cp_lower - Cp_upper) dx
Cl_calc = trapezoid(Cp_lower - Cp_upper, x)

# Cd in teoria potenziale pura (2D) è zero (Paradosso di D'Alembert)
Cd_calc = 0.00000

# Momento a picchiare (Nose-down) rispetto al Leading Edge (x=0)
Cm_le = trapezoid((Cp_upper - Cp_lower) * x, x)

# Trasporto del momento al quarto di corda (c/4 = 0.25)
Cm_c4 = Cm_le + 0.25 * Cl_calc

# =========================================================
# 5. PLOTTING PROFESSIONALE (XFOIL STYLE)
# =========================================================
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Teoria Analitica di Glauert - Scomposizione e Sovrapposizione NACA 2405', fontsize=16, fontweight='bold')

axs[0, 0].plot(x, u_alpha, 'm-', lw=2)
axs[0, 0].set_title(f'1. Lastra Piana ($\\alpha={alpha_target}^\\circ$)')
axs[0, 0].grid(True, linestyle=':')

axs[0, 1].plot(x, u_camber, 'g-', lw=2)
axs[0, 1].set_title('2. Linea Curva (Incurvamento)')
axs[0, 1].grid(True, linestyle=':')

axs[1, 0].plot(x, u_thick, 'c-', lw=2)
axs[1, 0].set_title('3. Profilo Simmetrico (Spessore)')
axs[1, 0].grid(True, linestyle=':')

# --- PLOT 4: STILE XFOIL CON DATI INTEGRATI ---
axs[1, 1].plot(x, Cp_upper, 'b-', lw=2, label='Upper')
axs[1, 1].plot(x, Cp_lower, 'r-', lw=2, label='Lower')
axs[1, 1].invert_yaxis()
axs[1, 1].set_title('4. Distribuzione $C_p$ e Coefficienti Globali')
axs[1, 1].set_xlabel('x/c')
axs[1, 1].set_ylabel('$C_p$')
axs[1, 1].legend(loc='lower left')
axs[1, 1].grid(True, linestyle=':')

# Creazione del riquadro testuale stile XFOIL
textstr = '\n'.join((
    r'$\bf{NACA\ 2405}$',
    r'Teoria Inviscida Lineare',
    r'-------------------------',
    r'$\alpha = %.3f^\circ$' % (alpha_target, ),
    r'$C_l = %.4f$' % (Cl_calc, ),
    r'$C_d = %.5f$' % (Cd_calc, ),
    r'$C_{m,c/4} = %.4f$' % (Cm_c4, )))

# Posizionamento del testo sul grafico
props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='black')
axs[1, 1].text(0.65, 0.95, textstr, transform=axs[1, 1].transAxes, fontsize=12,
        verticalalignment='top', bbox=props, family='monospace')

plt.tight_layout()
plt.show()