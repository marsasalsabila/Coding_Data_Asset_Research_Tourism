# Coding Data Asset Research Tourism 🏖️📊

Repositori ini berisi penelitian dan analisis data tentang aset coding dan tourism research menggunakan Jupyter Notebook.

## 📋 Daftar Isi

- [Tentang Proyek](#tentang-proyek)
- [Fitur Utama](#fitur-utama)
- [Struktur Repositori](#struktur-repositori)
- [Instalasi](#instalasi)
- [Cara Penggunaan](#cara-penggunaan)
- [Dataset](#dataset)
- [Analisis](#analisis)
- [Hasil dan Temuan](#hasil-dan-temuan)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)
- [Kontak](#kontak)

## 🎯 Tentang Proyek

Proyek ini adalah inisiatif penelitian yang menggabungkan aspek coding, data science, dan tourism research. Fokus utama adalah:

- **Data Exploration**: Mengeksplorasi dan memahami karakteristik data tourism
- **Data Analysis**: Melakukan analisis mendalam terhadap tren dan pola
- **Data Visualization**: Membuat visualisasi yang informatif dan mudah dipahami
- **Research Insights**: Memberikan insights yang berguna untuk pengembangan sektor tourism

## ✨ Fitur Utama

- 📊 **Analisis Data Komprehensif**: Menggunakan pandas, numpy, dan libraries data science lainnya
- 📈 **Visualisasi Data**: Grafik dan chart interaktif dengan matplotlib, seaborn, dan plotly
- 🔍 **Exploratory Data Analysis (EDA)**: Pemahaman mendalam tentang dataset
- 🤖 **Predictive Modeling**: Model machine learning untuk forecasting (jika ada)
- 📝 **Dokumentasi Lengkap**: Setiap notebook didokumentasikan dengan baik

## 📂 Struktur Repositori

```
Coding_Data_Asset_Research_Tourism/
│
├── BERTopic.ipynb                                                              # ipynb for BERTopic Processing
├── Cultural_Preservation_Subsystem.ipynb                                       # ipynb for Cultural Prservation
├── Economic_Subsystem_of_The_Local_Community_in_the_Tourism_Sector.ipynb       # ipynb for Local Economy Community Subsystem
├── Environmental_Sanitation_Subsystem.ipynb                                    # ipynb for Sanitation Subsystem
├── Tourism_Facilitites_Availibility_Subsystem.ipynb                            # ipynb for Facilities Availibility Subsystem
├── Tourism_Revenue_Subsystem.ipynb                                             # ipynb for Revenue Subsystem
├── Tourism_Services_Subsystem.ipynb                                            # ipynb for Services Subsystem
├── Tourism_Population_Subsystem.ipynb                                          # ipynb for Tourism Population Subsystem
├── final_data_for_25_destinations_with_coordinates.zip                         # Dataset Files
```

## 🚀 Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip atau conda

### Langkah Instalasi

1. **Clone Repositori**
   ```bash
   git clone https://github.com/marsasalsabila/Coding_Data_Asset_Research_Tourism.git
   cd Coding_Data_Asset_Research_Tourism
   ```

2. **Buat Virtual Environment**
   ```bash
   # Menggunakan venv
   python -m venv env
   source env/bin/activate  # Di Windows: env\Scripts\activate
   
   # Atau menggunakan conda
   conda create --name tourism_research python=3.10
   conda activate tourism_research
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Buka Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

## 📖 Cara Penggunaan

### Menjalankan Notebook

1. Navigasikan ke folder `notebooks/`
2. Buka notebook sesuai urutan numerik (01, 02, 03, dst)
3. Jalankan setiap cell dengan Shift + Enter
4. Sesuaikan path data jika diperlukan

### Contoh Penggunaan Kode

```python
import pandas as pd
import matplotlib.pyplot as plt
from src.analysis import analyze_data
from src.visualization import create_plots

# Load data
df = pd.read_csv('data/raw/tourism_data.csv')

# Analisis
results = analyze_data(df)

# Visualisasi
create_plots(results)
```

## 📊 Dataset

Proyek ini menggunakan dataset tentang:
- **Sumber**: [Sebutkan sumber data]
- **Ukuran**: [Jumlah baris dan kolom]
- **Periode**: [Rentang waktu data]
- **Variabel Utama**: 
  - [Variabel 1]
  - [Variabel 2]
  - [Variabel 3]

**Catatan**: Dataset tersimpan di folder `data/`. Jika Anda memiliki dataset besar, gunakan `.gitignore` untuk mengecualikannya dari version control.

## 🔬 Analisis

### Pertanyaan Penelitian

1. **Pertanyaan 1**: [Sebutkan pertanyaan penelitian utama]
2. **Pertanyaan 2**: [Sebutkan pertanyaan penelitian kedua]
3. **Pertanyaan 3**: [Sebutkan pertanyaan penelitian ketiga]

### Metodologi

- **Teknik EDA**: Deskriptif statistik, distribusi data, korelasi
- **Cleaning**: Handling missing values, outliers, dan duplicates
- **Visualisasi**: Time series, heatmap, scatter plot, bar chart
- **Analisis Statistik**: Hypothesis testing, correlation analysis

## 📈 Hasil dan Temuan

### Key Findings

- **Insight 1**: [Deskripsi insight utama yang ditemukan]
- **Insight 2**: [Deskripsi insight kedua]
- **Insight 3**: [Deskripsi insight ketiga]

### Visualisasi Utama

Berikut adalah beberapa visualisasi penting dari analisis:
- Chart 1: [Deskripsi]
- Chart 2: [Deskripsi]
- Chart 3: [Deskripsi]

Lihat folder `output/figures/` untuk semua visualisasi.

## 🤝 Kontribusi

Kami menyambut kontribusi dari komunitas! Jika Anda ingin berkontribusi:

1. Fork repositori ini
2. Buat branch fitur (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan Anda (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buka Pull Request

### Guidelines Kontribusi
- Tulis kode yang bersih dan mudah dipahami
- Tambahkan dokumentasi yang jelas
- Ikuti naming conventions yang konsisten
- Sertakan unit tests jika memungkinkan

## 📝 Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE) - lihat file LICENSE untuk detail lebih lanjut.

## 👤 Kontak

**Author**: [Mara Salsabila](https://github.com/marsasalsabila)

- 📧 Email: [Masukkan email Anda]
- 🐙 GitHub: [@marsasalsabila](https://github.com/marsasalsabila)
- 💼 LinkedIn: [Masukkan profil LinkedIn Anda]

## 🙏 Ucapan Terima Kasih

Terima kasih kepada:
- Komunitas Python dan Data Science
- Contributors yang telah membantu
- [Sumber dataset/resources lainnya]

---

**Last Updated**: 20 Mei 2026

**Status**: ✅ Active Development

*Jika Anda menemukan bug atau memiliki saran, silakan buat issue di [halaman issues](https://github.com/marsasalsabila/Coding_Data_Asset_Research_Tourism/issues).*
