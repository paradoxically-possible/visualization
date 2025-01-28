# 🌀 Koleksi Visualisasi Matematika & Simulasi 3D/4D 🚀

Kumpulan program Python untuk visualisasi objek matematika, simulasi fisika, dan eksplorasi dimensi tinggi. Dibangun dengan berbagai library grafis seperti Turtle, Pygame, OpenGL, dan Matplotlib.

## 📂 Daftar Proyek

### 1. **Animasi Kubus Berputar (2 Versi)**
- **File**: `Cube_Rotate.py`, `Cube_Rotate_Two.py`
- **Deskripsi**:  
  Kubus 3D berputar dengan efek partikel bintang di latar belakang. Versi Two menambahkan:
  - Warna dinamis (HSV → RGB)
  - Peningkatan jumlah partikel (300 vs 100)
  - Efek kedalaman yang lebih kompleks
- **Teknologi**: `turtle`, matematika 3D

### 2. **Visualisasi 4D Klein Bottle**
- **File**: `Fourth_Dimensional_Part_1.py`, `Fourth_Dimensional_Part_2.py`
- **Deskripsi**:  
  Representasi 4D Klein Bottle menggunakan:
  - Proyeksi stereografis 4D → 3D
  - Rotasi bidang XY dan ZW
  - Pewarnaan berdasarkan koordinat W (Part 2)
  - Kontrol mouse & animasi otomatis
- **Teknologi**: `OpenGL`, `PyGame`, aljabar linear 4D

### 3. **Model Daun 3D Parametrik**
- **File**: `Leaf_Proyection.py`
- **Deskripsi**:  
  Generasi permukaan daun 3D dengan:
  - Parameter botani (panjang, lebar, ketebalan)
  - Simulasi urat daun
  - Efek kerutan tepi
- **Teknologi**: `Matplotlib`, `NumPy`

### 4. **Segitiga Pascal Interaktif**
- **File**: `Pascal_Triangle.py`
- **Deskripsi**:  
  Generator Segitiga Pascal dengan:
  - Input pengguna interaktif
  - Perhitungan kombinasi (nCr)
  - Implementasi rekursif faktorial

### 5. **Simulasi Fisika Bola Berputar**
- **File**: `Rotating_Triangle.py`
- **Deskripsi**:  
  Sistem fisika dengan:
  - Segitiga berotasi
  - Bola memantul dengan refleksi vektor
  - Deteksi tumbukan edge-based
- **Teknologi**: `PyGame`, matematika vektor

### 6. **Visualisasi Partikel & Fraktal**
- **File**: `Visualization.py`
- **Deskripsi**:  
  Sistem partikel kompleks dengan:
  - Medan gravitasi fraktal
  - Latar bintang paralaks
  - Icosahedron berotasi
- **Teknologi**: `OpenGL`, `NumPy`

### 7. **Permukaan Matematika Kompleks**
- **File**: `Calculus.py`
- **Deskripsi**:  
  Permukaan 3D menggunakan:
  - Fungsi Gamma dan integral Fresnel
  - Transformasi hiperbolik
  - Visualisasi tensor diferensial
- **Teknologi**: `Matplotlib`, `SciPy`

## 🛠️ Instalasi

1. **Prasyarat**:
   - Python 3.8+
   - PIP dependencies:
   ```bash
   pip install numpy matplotlib pygame pyopengl scipy
