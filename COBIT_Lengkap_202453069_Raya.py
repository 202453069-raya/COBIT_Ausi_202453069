#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import os

# --- DATA PROSES COBIT ---

EDM_PROCESSES = {
    "EDM01": "Ensured Governance Framework Setting and Maintenance",
    "EDM02": "Ensured Benefits Delivery",
    "EDM03": "Ensured Risk Optimization",
    "EDM04": "Ensured Resource Optimization",
    "EDM05": "Ensured Stakeholder Transparency"
}

APO_PROCESSES = {
    "APO01": "Perencanaan dan Pengorganisasian Strategi TI",
    "APO02": "Manajemen Arsitektur Perusahaan",
    "APO03": "Manajemen Arah Inovasi",
    "APO04": "Manajemen Portofolio TI",
    "APO05": "Manajemen Investasi TI",
    "APO06": "Manajemen Anggaran dan Biaya TI",
    "APO07": "Manajemen SDM TI",
    "APO08": "Manajemen Hubungan",
    "APO09": "Manajemen Penyedia Layanan",
    "APO10": "Manajemen Permintaan",
    "APO11": "Manajemen Kualitas",
    "APO12": "Manajemen Risiko",
    "APO13": "Manajemen Keamanan"
}

BAI_PROCESSES = {
    "BAI01": "Manajemen Program",
    "BAI02": "Manajemen Definisi Kebutuhan",
    "BAI03": "Manajemen Identifikasi dan Pembangunan Solusi",
    "BAI04": "Manajemen Ketersediaan dan Kapasitas",
    "BAI05": "Manajemen Perubahan Organisasional",
    "BAI06": "Manajemen Perubahan TI",
    "BAI07": "Manajemen Penerimaan dan Transisi Perubahan",
    "BAI08": "Manajemen Pengetahuan",
    "BAI09": "Manajemen Aset",
    "BAI10": "Manajemen Konfigurasi",
    "BAI11": "Manajemen Proyek" # COBIT 2019 (Pemisahan dari BAI01)
}

DSS_PROCESSES = {
    "DSS01": "Manajemen Operasi",
    "DSS02": "Manajemen Permintaan Layanan dan Insiden",
    "DSS03": "Manajemen Permasalahan (Problem)",
    "DSS04": "Manajemen Kontinuitas",
    "DSS05": "Manajemen Layanan Keamanan",
    "DSS06": "Manajemen Kontrol Proses Bisnis"
}

MEA_PROCESSES = {
    "MEA01": "Manajemen Pemantauan Kinerja dan Kesesuaian",
    "MEA02": "Manajemen Sistem Kontrol Internal",
    "MEA03": "Manajemen Kepatuhan (Compliance) Eksternal",
    "MEA04": "Manajemen Jaminan (Assurance)",
    "MEA05": "Manajemen Evaluasi Tata Kelola" # COBIT 2019
}

# --- FUNGSI INTI ---

def tampilkan_skala():
    """Menampilkan skala penilaian yang digunakan."""
    print("\nSkala Penilaian (Linked Scale):")
    print("1. Sangat Buruk - Tidak ada penerapan atau dokumentasi")
    print("2. Buruk - Penerapan tidak konsisten dan tidak terdokumentasi")
    print("3. Cukup - Terdapat beberapa penerapan, namun belum menyeluruh")
    print("4. Baik - Sudah diterapkan secara konsisten dan terdokumentasi")
    print("5. Sangat Baik - Penerapan menyeluruh, terdokumentasi, dan terus dievaluasi\n")

def hitung_rata_rata(hasil):
    """Menghitung rata-rata skor."""
    if not hasil:
        return 0
    total = sum(hasil.values())
    rata = total / len(hasil)
    return rata

def kategori_kematangan(nilai):
    """Menerjemahkan skor rata-rata ke level kematangan."""
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

# --- FUNGSI EVALUASI & TAMPILAN ---

def clear_screen():
    """Membersihkan layar terminal."""
    # Untuk Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Untuk MacOS dan Linux
    else:
        _ = os.system('clear')

def evaluasi_proses(daftar_proses, nama_domain):
    """
    Fungsi utama untuk meminta input skor dari auditor
    untuk domain yang dipilih.
    """
    clear_screen()
    hasil_skor = {}
    print(f"==================================================")
    print(f"  EVALUASI DOMAIN COBIT: {nama_domain.upper()}")
    print(f"==================================================")
    tampilkan_skala()

    try:
        for kode, deskripsi in daftar_proses.items():
            print(f"\nProses: {kode} - {deskripsi}")
            while True:
                try:
                    skor_input = input("  Masukkan skor (1-5): ")
                    if not skor_input.strip():
                         print("  ⚠️ Input tidak boleh kosong. Masukkan angka antara 1-5.")
                         continue

                    skor = int(skor_input)
                    if 1 <= skor <= 5:
                        hasil_skor[kode] = skor
                        break
                    else:
                        print("  ⚠️ Skor harus antara 1 hingga 5.")
                except ValueError:
                    print("  ⚠️ Masukkan angka yang valid antara 1-5.")

        return hasil_skor

    except KeyboardInterrupt:
        print("\n\nProses evaluasi dibatalkan. Kembali ke menu utama.")
        return None # Mengembalikan None jika evaluasi dibatalkan

def tampilkan_hasil_evaluasi(hasil, nama_domain):
    """Menampilkan laporan hasil evaluasi untuk domain yang dipilih."""
    if hasil is None: # Jika evaluasi dibatalkan
        return

    rata = hitung_rata_rata(hasil)
    kategori = kategori_kematangan(rata)

    clear_screen()
    print(f"\n\n=== HASIL EVALUASI TINGKAT KEMATANGAN (MATURITY LEVEL) ===")
    print(f"Domain: {nama_domain}")
    print("---------------------------------------------------------")
    for kode, skor in hasil.items():
        print(f"  {kode}: Skor {skor}")
    print("---------------------------------------------------------")
    print(f"  Rata-rata skor: {rata:.2f}")
    print(f"  Tingkat Kematangan: {kategori}")
    print("\n\nTekan Enter untuk kembali ke menu utama...")
    try:
        input()
    except KeyboardInterrupt:
        pass # Langsung kembali ke menu jika Ctrl+C ditekan

def tampilkan_menu_utama():
    """Menampilkan menu utama program."""
    clear_screen()
    print("**************************************************")
    print("   PROGRAM AUDIT TATA KELOLA TI BERBASIS COBIT    ")
    print("**************************************************")
    print("\nPilih domain yang ingin dievaluasi:")
    print("  a. EDM (Evaluate, Direct and Monitor)")
    print("  b. APO (Align, Plan and Organize)")
    print("  c. BAI (Build, Acquire and Implement)")
    print("  d. DSS (Deliver, Service and Support)")
    print("  e. MEA (Monitor, Evaluate and Assess)")
    print("\n  q. Keluar Program")

    pilihan = input("\nMasukkan pilihan (a/b/c/d/e/q): ").lower().strip()
    return pilihan

# --- FUNGSI MAIN (PENGATUR PROGRAM) ---

def main():
    """Loop utama program."""

    # Membuat 'router' atau pemetaan untuk pilihan menu
    pilihan_menu = {
        'a': ("EDM (Evaluate, Direct and Monitor)", EDM_PROCESSES),
        'b': ("APO (Align, Plan and Organize)", APO_PROCESSES),
        'c': ("BAI (Build, Acquire and Implement)", BAI_PROCESSES),
        'd': ("DSS (Deliver, Service and Support)", DSS_PROCESSES),
        'e': ("MEA (Monitor, Evaluate and Assess)", MEA_PROCESSES)
    }

    while True:
        pilihan = tampilkan_menu_utama()

        if pilihan in pilihan_menu:
            nama_domain, daftar_proses = pilihan_menu[pilihan]
            hasil = evaluasi_proses(daftar_proses, nama_domain)
            tampilkan_hasil_evaluasi(hasil, nama_domain)

        elif pilihan == 'q':
            clear_screen()
            print("Terima kasih telah menggunakan program ini. Keluar...")
            sys.exit()

        else:
            print("\n⚠️ Pilihan tidak valid. Tekan Enter untuk coba lagi.")
            try:
                input()
            except KeyboardInterrupt:
                clear_screen()
                print("Terima kasih telah menggunakan program ini. Keluar...")
                sys.exit()

if __name__ == "__main__":
    main()


# In[ ]:




