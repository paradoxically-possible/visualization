import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameter daun
PANJANG = 8.0          # Panjang daun (cm)
LEBAR_MAX = 5.0        # Lebar maksimum (cm)
KETEBALAN = 0.5        # Ketebalan maksimum (cm)
KERUTAN_TEPI = 0.15    # Amplitudo kerutan tepi
KELENGKUNGAN = 0.7     # Faktor kelengkungan
KETEBALAN_URAT = 0.15  # Ketebalan urat

# Fungsi bentuk daun
def bentuk_daun(u, v):
    # Koordinat X (panjang)
    x = PANJANG * u
    
    # Lebar daun bervariasi sepanjang u
    lebar = LEBAR_MAX * (1 - 0.5*u**2)
    
    # Koordinat Y (lebar dengan kerutan tepi)
    y = lebar * v * (1 + KERUTAN_TEPI*np.sin(4*np.pi*u))
    
    # Koordinat Z (ketebalan dan kelengkungan)
    z = KETEBALAN * (1 - (2*v)**4) * (1 - u) * np.exp(-2*u) * KELENGKUNGAN
    
    return x, y, z

# Fungsi urat daun
def tambah_urat(u, v, z):
    # Urat utama (midrib)
    z += 0.8*KETEBALAN_URAT * np.exp(-(20*v**2)) * np.exp(-2*(u-0.5)**2)
    
    # Urat sekunder
    for i in range(1,5):
        pos = i*0.2
        z += 0.3*KETEBALAN_URAT * np.exp(-50*(u - pos)**2) * np.exp(-(10*v)**2)
    
    return z

# Generate grid parametrik
u = np.linspace(0, 1, 100)
v = np.linspace(-1, 1, 100)
U, V = np.meshgrid(u, v)

# Hitung koordinat
X, Y, Z = bentuk_daun(U, V)
Z = tambah_urat(U, V, Z)

# Plot 3D
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d', proj_type='ortho')

# Plot permukaan dengan colormap sesuai ketinggian
surf = ax.plot_surface(X, Y, Z, cmap='YlGn', rstride=2, cstride=2,
                       linewidth=0.1, antialiased=True)

# Konfigurasi plot
ax.view_init(elev=25, azim=-45)
ax.set_xlim(0, PANJANG)
ax.set_ylim(-LEBAR_MAX, LEBAR_MAX)
ax.set_zlim(0, KETEBALAN*1.2)
ax.set_box_aspect((PANJANG, LEBAR_MAX*2, KETEBALAN*1.5))

ax.xaxis.pane.fill = False
ax.yaxis.pane.fill = False
ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('w')
ax.yaxis.pane.set_edgecolor('w')
ax.zaxis.pane.set_edgecolor('w')

plt.colorbar(surf, shrink=0.5, aspect=10, label='Elevasi (cm)')
plt.title('Proyeksi 3D Daun dengan Parameter Botani', pad=20)
plt.tight_layout()
plt.show()