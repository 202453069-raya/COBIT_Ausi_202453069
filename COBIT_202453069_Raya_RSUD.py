#!/usr/bin/env python
# coding: utf-8

# In[4]:


def tampilkan_skala():
    """Menampilkan skala penilaian yang digunakan (berdasarkan file .ipynb)."""
    print("\nSkala Penilaian (Linked Scale):")
    print("1. Sangat Buruk - Tidak ada penerapan atau dokumentasi")
    print("2. Buruk - Penerapan tidak konsisten dan tidak terdokumentasi")
    print("3. Cukup - Terdapat beberapa penerapan, namun belum menyeluruh")
    print("4. Baik - Sudah diterapkan secara konsisten dan terdokumentasi")
    print("5. Sangat Baik - Penerapan menyeluruh, terdokumentasi, dan terus dievaluasi\n")


# In[5]:


def evaluasi_proses(daftar_proses):
    """
    Fungsi untuk meminta input skor dari auditor untuk setiap proses
    (berdasarkan logika 'evaluasi_apos' dari file .ipynb).
    """
    hasil_skor = {}
    print("=== EVALUASI DOMAIN COBIT: EDM (Evaluate, Direct, Monitor) ===")
    print("=== STUDI KASUS: RSUD SUNAN KALIJAGA ===")
    tampilkan_skala()

    for kode, deskripsi in daftar_proses.items():
        print(f"\nProses: {kode} - {deskripsi}")
        while True:
            try:
                skor_input = input("Masukkan skor (1-5): ")
                # Memeriksa apakah input kosong, jika iya, ulangi
                if not skor_input.strip():
                     print("⚠️ Input tidak boleh kosong. Masukkan angka antara 1-5.")
                     continue

                skor = int(skor_input)
                if 1 <= skor <= 5:
                    hasil_skor[kode] = skor
                    break
                else:
                    print("⚠️ Skor harus antara 1 hingga 5.")
            except ValueError:
                print("⚠️ Masukkan angka yang valid antara 1-5.")
            except KeyboardInterrupt:
                print("\nProses evaluasi dibatalkan.")
                sys.exit()

    return hasil_skor


# In[6]:


def hitung_rata_rata(hasil):
    """Menghitung rata-rata skor (berdasarkan file .ipynb)."""
    if not hasil:
        return 0
    total = sum(hasil.values())
    rata = total / len(hasil)
    return rata


# In[7]:


def kategori_kematangan(nilai):
    """Menerjemahkan skor rata-rata ke level kematangan (berdasarkan file .ipynb)."""
    if nilai < 1.5:
        return "Level 1 - Initial (Tidak Teratur)"
    elif nilai < 2.5:
        return "Level 2 - Repeatable (Dapat Diulang)"
    elif nilai < 3.5:
        return "Level 3 - Defined (Terdefinisi)"
    elif nilai < 4.5:
        return "Level 4 - Managed (Terkelola dengan Baik)"
    else:
        return "Level 5 - Optimized (Teroptimasi)"


# In[8]:


def main():
    """
    Fungsi utama untuk menjalankan program.
    Daftar proses diambil dari domain EDM yang dibahas di dokumen PDF.
    """
    # Daftar proses ini diambil dari dokumen 'Sistem Informasi-4-13.pdf'
    # di Bab I Bagian D (Ruang Lingkup) [cite: 25]
    edmlist = {
        "EDM01": "Ensured Governance Framework Setting and Maintenance", # [cite: 26]
        "EDM02": "Ensured Benefits Delivery", # [cite: 26]
        "EDM03": "Ensured Risk Optimization", # [cite: 27]
        "EDM04": "Ensured Resource Optimization", # [cite: 28]
        "EDM05": "Ensured Stakeholder Transparency" # [cite: 29]
    }

    # 1. Jalankan evaluasi
    hasil = evaluasi_proses(edmlist)

    # 2. Hitung rata-rata
    rata = hitung_rata_rata(hasil)

    # 3. Tentukan kategori
    kategori = kategori_kematangan(rata)

    # 4. Tampilkan hasil
    print("\n\n=== HASIL EVALUASI TINGKAT KEMATANGAN (MATURITY LEVEL) ===")
    print("Domain: EDM (Evaluate, Direct, Monitor)")
    print("---------------------------------------------------------")
    for kode, skor in hasil.items():
        print(f"{kode}: Skor {skor}")
    print("---------------------------------------------------------")
    print(f"Rata-rata skor: {rata:.2f}")
    print(f"Tingkat Kematangan: {kategori}")

if __name__ == "__main__":
    main()


# In[ ]:




