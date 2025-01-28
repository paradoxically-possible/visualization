import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.special import gamma, fresnel

# Fungsi permukaan parametrik kompleks berbasis integral Fresnel dan Gamma function
def complex_surface(u, v):
    # Transformasi koordinat hiperbolik
    α = np.arctanh(0.9*np.sin(2*np.pi*v))
    β = np.arcsinh(3*u)
    
    # Integral Fresnel
    S, C = fresnel(3*β)
    
    # Komponen tensor diferensial
    x = gamma(1+α) * (C * np.cos(4*np.pi*u) - S * np.sin(4*np.pi*v))
    y = gamma(1+α) * (S * np.cos(4*np.pi*u) + C * np.sin(4*np.pi*v))
    z = gamma(0.5+β) * np.sqrt(np.abs(np.tan(α + β))) * np.exp(-α**2 - β**2)
    
    return x, y, z

# Parameter grid dengan presisi tinggi
u = np.linspace(-1, 1, 300)
v = np.linspace(0, 1, 300)
U, V = np.meshgrid(u, v)

# Hitung koordinat permukaan
X, Y, Z = complex_surface(U, V)

# Visualisasi 3D dengan presisi
fig = plt.figure(figsize=(16, 12))
ax = fig.add_subplot(111, projection='3d', proj_type='ortho')

# Plot permukaan dengan colormap kompleks
surf = ax.plot_surface(X, Y, Z, cmap='plasma',
                      rstride=2, cstride=2,
                      linewidth=0.1,
                      antialiased=True,
                      edgecolor='#1f1f1f')

# Konfigurasi sumbu dan perspektif
ax.view_init(elev=35, azim=-45)
ax.set_xlim(X.min(), X.max())
ax.set_ylim(Y.min(), Y.max())
ax.set_zlim(Z.min(), Z.max())

# Format sumbu saintifik
ax.xaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
ax.zaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))

# Parameter tampilan
ax.grid(False)
ax.xaxis.pane.set_edgecolor('black')
ax.yaxis.pane.set_edgecolor('black')
ax.zaxis.pane.set_edgecolor('black')
ax.xaxis.pane.set_alpha(0.8)
ax.yaxis.pane.set_alpha(0.8)
ax.zaxis.pane.set_alpha(0.8)

plt.colorbar(surf, shrink=0.6, aspect=20, label='Kompleksitas Tensor')
plt.title('Permukaan Diferensial Kompleks: Integrasi Fresnel-Gamma dengan Transformasi Hiperbolik', pad=25)
plt.tight_layout()
plt.show()