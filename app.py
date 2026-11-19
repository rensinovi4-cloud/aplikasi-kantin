
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

# ==========================================
# 1. CLASS PESANAN
# ==========================================

class Pesanan:

    # Constructor dan atribut
    def __init__(self, id_pesanan, nama, menu, jumlah, harga):
        self.id_pesanan = id_pesanan
        self.nama = nama
        self.menu = menu
        self.jumlah = jumlah
        self.harga = harga
        self.status = "Menunggu"
        self.waktu = datetime.now().strftime("%d-%m-%Y %H:%M")

    # Method menghitung total harga
    def hitung_total(self):
        return self.jumlah * self.harga

    # Method mengubah status
    def ubah_status(self, status_baru):
        self.status = status_baru

    # Method mengubah data
    def ubah_data(self, nama, menu, jumlah, harga):
        self.nama = nama
        self.menu = menu
        self.jumlah = jumlah
        self.harga = harga


# ==========================================
# 2. KONFIGURASI APLIKASI
# ==========================================

st.set_page_config(
    page_title="Aplikasi Pemesanan Kantin",
    page_icon="🍜",
    layout="wide"
)

st.title("🍜 APLIKASI PEMESANAN KANTIN")
st.write("Aplikasi pengelolaan pesanan makanan dan minuman.")

# Daftar menu menggunakan dictionary
daftar_menu = {
    "Nasi Goreng": 15000,
    "Mie Goreng": 13000,
    "Ayam Geprek": 18000,
    "Bakso": 15000,
    "Soto Ayam": 16000,
    "Es Teh": 5000,
    "Es Jeruk": 7000,
    "Air Mineral": 4000
}

# ==========================================
# 3. SESSION STATE
# ==========================================

if "pesanan" not in st.session_state:
    st.session_state.pesanan = []

if "nomor" not in st.session_state:
    st.session_state.nomor = 1

# ==========================================
# 4. NAVIGASI MENU
# ==========================================

with st.sidebar:

    st.title("🍽️ MENU KANTIN")

    menu = option_menu(
        menu_title="Navigasi",
        options=[
            "Dashboard",
            "Tambah Pesanan",
            "Data Pesanan",
            "Tentang Aplikasi"
        ],
        icons=[
            "house",
            "plus-circle",
            "table",
            "info-circle"
        ],
        default_index=0
    )


# ==========================================
# 5. HALAMAN DASHBOARD
# ==========================================

if menu == "Dashboard":

    st.header("📊 Dashboard")

    total_pesanan = len(st.session_state.pesanan)

    pendapatan = sum(
        p.hitung_total()
        for p in st.session_state.pesanan
    )

    menunggu = sum(
        1 for p in st.session_state.pesanan
        if p.status == "Menunggu"
    )

    selesai = sum(
        1 for p in st.session_state.pesanan
        if p.status == "Selesai"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Pesanan", total_pesanan)

    col2.metric(
        "Total Pendapatan",
        f"Rp {pendapatan:,.0f}"
    )

    col3.metric("Pesanan Selesai", selesai)

    st.subheader("Informasi Pesanan")

    st.write("Pesanan Menunggu:", menunggu)

    if st.session_state.pesanan:

        data = []

        for p in st.session_state.pesanan:
            data.append({
                "ID": p.id_pesanan,
                "Nama": p.nama,
                "Menu": p.menu,
                "Jumlah": p.jumlah,
                "Total": p.hitung_total(),
                "Status": p.status
            })

        st.dataframe(
            pd.DataFrame(data),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("Belum ada data pesanan.")


# ==========================================
# 6. HALAMAN TAMBAH PESANAN
# ==========================================

elif menu == "Tambah Pesanan":

    st.header("➕ Tambah Pesanan")

    with st.form("form_pesanan"):

        nama = st.text_input("Nama Pelanggan")

        pilihan_menu = st.selectbox(
            "Pilih Menu",
            list(daftar_menu.keys())
        )

        harga = daftar_menu[pilihan_menu]

        st.write("Harga: Rp", harga)

        jumlah = st.number_input(
            "Jumlah Pesanan",
            min_value=1,
            max_value=100,
            value=1
        )

        total = harga * jumlah

        st.success(f"Total Harga: Rp {total:,}")

        simpan = st.form_submit_button(
            "Simpan Pesanan"
        )

        if simpan:

            if nama.strip() == "":
                st.error("Nama pelanggan harus diisi!")

            else:

                id_baru = (
                    f"PSN-{st.session_state.nomor:03d}"
                )

                objek = Pesanan(
                    id_baru,
                    nama,
                    pilihan_menu,
                    jumlah,
                    harga
                )

                st.session_state.pesanan.append(objek)

                st.session_state.nomor += 1

                st.success("Pesanan berhasil ditambahkan!")

                st.rerun()


# ==========================================
# 7. HALAMAN DATA PESANAN
# ==========================================

elif menu == "Data Pesanan":

    st.header("📋 Data Pesanan")

    if len(st.session_state.pesanan) == 0:

        st.warning("Data pesanan masih kosong.")

    else:

        data = []

        for p in st.session_state.pesanan:

            data.append({
                "ID Pesanan": p.id_pesanan,
                "Nama": p.nama,
                "Menu": p.menu,
                "Jumlah": p.jumlah,
                "Harga": p.harga,
                "Total": p.hitung_total(),
                "Status": p.status
            })

        st.dataframe(
            pd.DataFrame(data),
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("Kelola Data Pesanan")

        daftar_id = [
            p.id_pesanan
            for p in st.session_state.pesanan
        ]

        pilih_id = st.selectbox(
            "Pilih ID Pesanan",
            daftar_id
        )

        # Mencari object pesanan
        objek_pilih = next(
            p for p in st.session_state.pesanan
            if p.id_pesanan == pilih_id
        )

        # ==================================
        # EDIT DATA
        # ==================================

        st.subheader("✏️ Edit Pesanan")

        with st.form("form_edit"):

            edit_nama = st.text_input(
                "Nama Pelanggan",
                value=objek_pilih.nama
            )

            edit_menu = st.selectbox(
                "Menu",
                list(daftar_menu.keys()),
                index=list(daftar_menu.keys()).index(
                    objek_pilih.menu
                )
            )

            edit_jumlah = st.number_input(
                "Jumlah",
                min_value=1,
                value=int(objek_pilih.jumlah)
            )

            edit_harga = daftar_menu[edit_menu]

            simpan_edit = st.form_submit_button(
                "Simpan Perubahan"
            )

            if simpan_edit:

                if edit_nama.strip() == "":
                    st.error("Nama tidak boleh kosong!")

                else:

                    objek_pilih.ubah_data(
                        edit_nama,
                        edit_menu,
                        edit_jumlah,
                        edit_harga
                    )

                    st.success("Data berhasil diubah!")

                    st.rerun()

        # ==================================
        # UBAH STATUS
        # ==================================

        st.subheader("🔄 Ubah Status Pesanan")

        status = st.selectbox(
            "Status Pesanan",
            ["Menunggu", "Diproses", "Selesai"],
            index=[
                "Menunggu",
                "Diproses",
                "Selesai"
            ].index(objek_pilih.status)
        )

        if st.button("Update Status"):

            objek_pilih.ubah_status(status)

            st.success("Status berhasil diperbarui!")

            st.rerun()

        # ==================================
        # HAPUS DATA
        # ==================================

        st.subheader("🗑️ Hapus Pesanan")

        konfirmasi = st.checkbox(
            "Saya yakin ingin menghapus pesanan ini."
        )

        if st.button(
            "Hapus Pesanan",
            disabled=not konfirmasi
        ):

            st.session_state.pesanan = [
                p for p in st.session_state.pesanan
                if p.id_pesanan != pilih_id
            ]

            st.success("Pesanan berhasil dihapus!")

            st.rerun()

# ==========================================
# 8. HALAMAN TENTANG APLIKASI
# ==========================================

elif menu == "Tentang Aplikasi":

    st.header("ℹ️ Tentang Aplikasi")

    st.write("""
    Aplikasi Pemesanan Kantin merupakan aplikasi
    berbasis web yang dibuat menggunakan Python
    dan Streamlit.

    Aplikasi ini digunakan untuk mengelola pesanan
    makanan dan minuman di kantin.
    """)

    st.subheader("Konsep Pemrograman")

    st.write("""
    1. Class: Pesanan
    2. Object: Objek pesanan pelanggan
    3. Atribut: ID, nama, menu, jumlah, harga, status
    4. Method: hitung_total(), ubah_status(), ubah_data()
    5. List: Menyimpan kumpulan pesanan
    6. Percabangan: if, elif, else
    7. Navigasi: option_menu
    8. Session State: Menyimpan data selama sesi aplikasi
    """)

    st.success("Terima kasih telah menggunakan aplikasi ini!")

