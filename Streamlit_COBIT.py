#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd

# --- DATA PROSES COBIT DENGAN KONTEKS RSUD ---
# Struktur data diubah untuk menyertakan pertanyaan audit spesifik RSUD

EDM_PROCESSES = {
    "EDM01": {
        "deskripsi": "Ensured Governance Framework Setting and Maintenance",
        "pertanyaan_rsud": "Apakah RSUD memiliki komite pengarah TI formal yang melibatkan direksi untuk menyetujui strategi SIMRS/RME?"
    },
    "EDM02": {
        "deskripsi": "Ensured Benefits Delivery",
        "pertanyaan_rsud": "Apakah direksi menerima laporan terukur soal manfaat investasi TI (misal: 'Apakah sistem antrean online benar-benar mengurangi waktu tunggu pasien?')"
    },
    "EDM03": {
        "deskripsi": "Ensured Risk Optimization",
        "pertanyaan_rsud": "Apakah direksi RSUD sudah menetapkan 'risk appetite' (selera risiko) terkait data pasien (misal: 'Berapa lama downtime RME yang bisa ditolerir UGD?')"
    },
    "EDM04": {
        "deskripsi": "Ensured Resource Optimization",
        "pertanyaan_rsud": "Apakah alokasi anggaran dan SDM TI (termasuk pelatihan perawat/dokter) sudah memadai dan sejalan dengan strategi RSUD?"
    },
    "EDM05": {
        "deskripsi": "Ensured Stakeholder Transparency",
        "pertanyaan_rsud": "Apakah laporan TI ke direksi sudah transparan dan mudah dipahami (bukan hanya 'server down', tapi 'layanan pendaftaran terganggu 15 menit')?"
    }
}

APO_PROCESSES = {
    "APO01": {
        "deskripsi": "Manajemen Strategi TI",
        "pertanyaan_rsud": "Apakah Renstra (Rencana Strategis) TI sudah selaras dengan Renstra bisnis RSUD (misal: mendukung akreditasi KARS/JCI)?"
    },
    "APO07": {
        "deskripsi": "Manajemen SDM TI",
        "pertanyaan_rsud": "Apakah kompetensi tim TI RSUD memadai? Dan apakah pelatihan untuk pengguna (perawat/dokter) saat ada update RME sudah efektif?"
    },
    "APO12": {
        "deskripsi": "Manajemen Risiko",
        "pertanyaan_rsud": "Apakah ada risk register TI yang aktif dipantau (misal: risiko ransomware, kebocoran data rekam medis, kegagalan server SIMRS)?"
    },
    "APO13": {
        "deskripsi": "Manajemen Keamanan",
        "pertanyaan_rsud": "Apakah kebijakan keamanan informasi (termasuk UU PDP/Permenkes 24/2022) sudah diterapkan secara teknis?"
    }
}

BAI_PROCESSES = {
    "BAI01": {
        "deskripsi": "Manajemen Program",
        "pertanyaan_rsud": "Saat RSUD menerapkan modul RME baru, apakah proyek tersebut dikelola dengan baik (anggaran, waktu, dan ruang lingkup)?"
    },
    "BAI03": {
        "deskripsi": "Manajemen Identifikasi dan Pembangunan Solusi",
        "pertanyaan_rsud": "Apakah kebutuhan dokter dan perawat benar-benar didengarkan dan dianalisis sebelum vendor membangun/meng-custom modul baru?"
    },
    "BAI07": {
        "deskripsi": "Manajemen Penerimaan dan Transisi Perubahan",
        "pertanyaan_rsud": "Apakah ada proses User Acceptance Test (UAT) yang formal melibatkan dokter/perawat sebelum sistem baru di-'go-live'-kan?"
    },
    "BAI08": {
        "deskripsi": "Manajemen Pengetahuan",
        "pertanyaan_rsud": "Apakah ada dokumentasi (SOP) yang jelas dan mudah diakses oleh staf medis jika mereka lupa cara menggunakan fitur di RME?"
    }
}

DSS_PROCESSES = {
    "DSS01": {
        "deskripsi": "Manajemen Operasi",
        "pertanyaan_rsud": "Apakah ada prosedur operasional standar untuk memantau server SIMRS/RME setiap hari, termasuk prosedur backup data pasien?"
    },
    "DSS02": {
        "deskripsi": "Manajemen Permintaan Layanan dan Insiden",
        "pertanyaan_rsud": "Jika printer resep di farmasi rusak atau perawat tidak bisa login, apakah ada Helpdesk TI yang responsif dengan SLA yang jelas?"
    },
    "DSS04": {
        "deskripsi": "Manajemen Kontinuitas",
        "pertanyaan_rsud": "Apakah RSUD memiliki Rencana Pemulihan Bencana (DRP) yang teruji? Apa yang dilakukan UGD jika RME mati total selama 2 jam?"
    },
    "DSS05": {
        "deskripsi": "Manajemen Layanan Keamanan",
        "pertanyaan_rsud": "Bagaimana RSUD mengelola hak akses? (Misal: Apakah staf kasir bisa melihat rekam medis pasien? Bagaimana proses pencabutan hak akses staf yang resign?)"
    }
}

MEA_PROCESSES = {
    "MEA01": {
        "deskripsi": "Manajemen Pemantauan Kinerja dan Kesesuaian",
        "pertanyaan_rsud": "Apakah kinerja TI diukur? (Misal: Berapa % uptime server SIMRS? Berapa lama waktu rata-rata penanganan tiket insiden?)"
    },
    "MEA03": {
        "deskripsi": "Manajemen Kepatuhan (Compliance) Eksternal",
        "pertanyaan_rsud": "Apakah ada audit internal rutin untuk memastikan RME sudah patuh pada regulasi eksternal (Permenkes 24/2022, UU PDP, integrasi SATUSEHAT)?"
    },
    "MEA04": {
        "deskripsi": "Manajemen Jaminan (Assurance)",
        "pertanyaan_rsud": "Apakah RSUD secara proaktif melakukan audit jaminan (misal: tes penetrasi/vulnerability assessment) pada aplikasi web RME?"
    }
}

# Daftar semua domain untuk navigasi
ALL_DOMAINS = {
    "EDM (Evaluate, Direct and Monitor)": EDM_PROCESSES,
    "APO (Align, Plan and Organize)": APO_PROCESSES,
    "BAI (Build, Acquire and Implement)": BAI_PROCESSES,
    "DSS (Deliver, Service and Support)": DSS_PROCESSES,
    "MEA (Monitor, Evaluate and Assess)": MEA_PROCESSES
}

# --- FUNGSI HELPER (DARI KODE .ipynb ANDA) ---

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

# --- TATA LETAK APLIKASI STREAMLIT ---

def main():
    st.set_page_config(page_title="Audit COBIT RSUD", layout="wide")

    # --- SIDEBAR (NAVIGASI MENU) ---
    st.sidebar.title("Navigasi Domain COBIT")
    st.sidebar.info("Aplikasi ini membantu auditor menghitung tingkat kematangan (maturity) tata kelola TI di RSUD.")

    domain_names = list(ALL_DOMAINS.keys())
    pilihan_domain_str = st.sidebar.radio(
        "Pilih domain yang ingin dievaluasi:",
        domain_names
    )

    # Ambil data proses berdasarkan pilihan di sidebar
    domain_processes = ALL_DOMAINS[pilihan_domain_str]

    # --- HALAMAN UTAMA (MAIN PAGE) ---
    st.title("Program Audit Tata Kelola TI (COBIT)")
    st.header(f"Studi Kasus: Rumah Sakit Umum Daerah (RSUD)")
    st.markdown(f"### Domain yang Dievaluasi: **{pilihan_domain_str}**")

    # Tampilkan skala penilaian dalam expander
    with st.expander("Klik untuk melihat Skala Penilaian (1-5)"):
        st.markdown("""
        * **1. Sangat Buruk (Initial):** Tidak ada penerapan atau dokumentasi. Proses kacau dan reaktif.
        * **2. Buruk (Repeatable):** Penerapan tidak konsisten, bergantung pada individu. Tidak ada SOP tertulis.
        * **3. Cukup (Defined):** Sudah ada SOP tertulis dan distandarisasi. Sudah ada pelatihan, tapi kepatuhan bervariasi.
        * **4. Baik (Managed):** Proses dikelola, diukur kinerjanya (ada KPI), dan dipantau secara konsisten.
        * **5. Sangat Baik (Optimized):** Proses terus-menerus dievaluasi, disempurnakan, dan diinovasi (best practice).
        """)

    st.markdown("---")
    st.info("Silakan berikan skor (1-5) untuk setiap proses di bawah ini berdasarkan temuan audit di RSUD.")

    hasil_skor = {}

    # --- FORM INPUT PENILAIAN ---
    # Menggunakan form agar aplikasi tidak me-reload setiap kali slider digeser
    with st.form(key="audit_form"):
        for kode, data in domain_processes.items():
            st.markdown(f"#### **{kode}: {data['deskripsi']}**")
            st.caption(f"**Pertanyaan Audit Kunci RSUD:** *{data['pertanyaan_rsud']}*")

            # Slider untuk input skor 1-5
            hasil_skor[kode] = st.slider(
                f"Skor untuk {kode}", 
                min_value=1, 
                max_value=5, 
                value=3,  # Nilai default
                key=kode,
                label_visibility="collapsed" # Sembunyikan label slider karena sudah ada di markdown
            )
            st.markdown("---") # Garis pemisah antar proses

        # Tombol submit
        submitted = st.form_submit_button("Hitung Tingkat Kematangan")

    # --- HASIL EVALUASI ---
    if submitted:
        # Hitung rata-rata dan kategori
        rata_rata = hitung_rata_rata(hasil_skor)
        kategori = kategori_kematangan(rata_rata)

        st.subheader(f"Hasil Evaluasi Domain: {pilihan_domain_str}")

        # Tampilkan hasil dalam 2 kolom
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="Rata-rata Skor Kematangan", value=f"{rata_rata:.2f}")
        with col2:
            st.success(f"**Tingkat Kematangan (Maturity Level):**\n\n### {kategori}")

        st.subheader("Rincian Skor yang Diberikan:")

        # Ubah dictionary hasil_skor menjadi DataFrame untuk tampilan yang lebih baik
        df_hasil = pd.DataFrame(list(hasil_skor.items()), columns=['Proses', 'Skor'])
        st.dataframe(df_hasil.set_index('Proses'), use_container_width=True)

if __name__ == "__main__":
    main()

