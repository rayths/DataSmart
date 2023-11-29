from datetime import datetime, timedelta
import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
import sqlite3 as sql
import yaml
from yaml.loader import SafeLoader
from st_pages import Page, show_pages, add_page_title, hide_pages
from func import search_jadwal, display_jadwal, display_delete_jadwal, delete_jadwal


logo = Image.open("Logo.png")
st.set_page_config(
    page_title="Data Smart",
    page_icon= logo,
    layout="wide",
)

# sql (database)

# database tugas
tugas_conn = sql.connect("file:tugas.db?mode=rwc", uri=True) # connect database tugas
#tugas_conn.execute("DROP TABLE tugas")
#tugas_conn.execute("CREATE TABLE IF NOT EXISTS tugas (id INTEGER PRIMARY KEY AUTOINCREMENT, nama_tugas VARCHAR(255), keterangan VARCHAR(255), mata_kuliah VARCHAR(255), tanggal_pengumpulan VARCHAR(50), waktu_pengumpulan VARCHAR(50))")

# database autentikasi
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# database jadwal dan ruang kelas
jadwal_ruangkelas_conn = sql.connect("file:jadwal.db?mode=rwc", uri=True)
#jadwal_ruangkelas_conn.execute("DROP TABLE jadwal_kelas")
#jadwal_ruangkelas_conn.execute("CREATE TABLE IF NOT EXISTS jadwal_kelas (id INTEGER PRIMARY KEY AUTOINCREMENT, mata_kuliah VARCHAR(255), kelas VARCHAR(255), jadwal VARCHAR(255), jam_mulai VARCHAR(255), jam_akhir VARCHAR(255), ruang_kelas VARCHAR(255))")

# database notes
notes_conn = sql.connect("file:notes.db?mode=rwc", uri=True)
#notes_conn.execute("DROP TABLE notes")
#notes_conn.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, judul VARCHAR(255), notes TEXT, tanggal VARCHAR(255))")

# autentikasi
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    hide_pages(["Setting"])
    st.error("Username/Password salah")

if authentication_status == None:
    hide_pages(["Setting"])
    st.warning("Masukan Username dan Password")
    st.write("Jika Anda belum memiliki akun, silahkan daftar.")   

if authentication_status:
    def main():
        hide_pages(["Register"])
        # side bar customization
        st.sidebar.write('''<div style="text-align:center">
                         <img src="http://drive.google.com/uc?export=view&id=1vsVDyaQ1N3AMoysnDvEjBAeIZwWV9l92" width="125">
                         <br><br></div>''', unsafe_allow_html=True)
        st.sidebar.write(f":blue[**Selamat Datang di Data Smart, <br> {name} !!**]", unsafe_allow_html=True)

        st.header(":blue[Data Smart]", divider="orange")
        selected_tab = option_menu(menu_title=None, options=["Home", "Data Remind", "Data Search", "Data Notes"], icons=["house", "bell", "search", "bookmarks"], 
                                    key="nav", orientation="horizontal",)

        if selected_tab == "Home":
            st.header(":blue[Welcome to Data Smart!]", divider="grey")
            st.write('''<div style="text-align: justify">
                     <h3>Apa Itu Data Smart?</h3>
                     Data smart merupakan aplikasi di bidang pendidikan yang berbasis teknologi.
                     Sederhananya pengertian Data Smart merupakan kerangka management untuk memudahkan pengguna dalam mengelola waktu dan tanggung jawab mereka.
                     </div>''', unsafe_allow_html=True)
            
            st.write("<hr>", unsafe_allow_html=True)
            st.write('''<div style="text-align: justify">
                     <h3>Latar Belakang</h3>
                     Aktivitas yang padat sering kali membuat seseorang sulit untuk mengingat beberapa hal yang ada dalam rutinitas sehari-harinya. 
                     Apalagi sebagai seorang mahasiswa hal tersebut merupakan hal yang sering terjadi, misalnya dalam hal jadwal harian, ruangan kelas, maupun tenggat tugas yang mereka miliki. 
                     Dengan adanya aplikasi data smart dapat membantu pengguna mengelola waktu dan tanggung jawab dengan memberikan notifikasi yang dapat disesuaikan.
                     </div>''', unsafe_allow_html=True)
            
            st.write("<hr>", unsafe_allow_html=True)
            st.write('''<div style="text-align: justify">
                     <h3>Data Remind</h3>
                     Fitur ini membantu pengguna untuk mengingat aktivitas yang seharusnya dilakukan, seperti untuk mengingat tugas yang harus dikerjakan, 
                     berserta batas waktu pengumpulannya.
                     </div>''', unsafe_allow_html=True)
            
            st.write("<hr>", unsafe_allow_html=True)
            st.write('''<div style="text-align: justify">
                     <h3>Data Search</h3>
                     Fitur ini membantu pengguna untuk menemukan informasi yang diinginkan, seperti ruangan kelas, dan jadwal harian.
                     </div>''', unsafe_allow_html=True)
            
            st.write("<hr>", unsafe_allow_html=True)
            st.write('''<div style="text-align: justify">
                     <h3>Data Notes</h3>
                     Fitur ini membantu pengguna untuk membuat catatan perkuliahan serta mengupload file yang mereka inginkan.
                     </div>''', unsafe_allow_html=True)


        elif selected_tab == "Data Remind":
            st.header(":blue[Data Remind]", divider="grey")
            fitur = st.selectbox("Pilih Menu:", ["Tugas", "Tambah Tugas"])
            if fitur == "Tugas":
                st.subheader("Tugas")

                tugas_conn = sql.connect("file:tugas.db?mode=rwc", uri=True)
                tugas = tugas_conn.execute("SELECT nama_tugas, keterangan, mata_kuliah, tanggal_pengumpulan, waktu_pengumpulan FROM tugas").fetchall()

                if tugas:
                    for row in tugas:
                        nama_tugas, keterangan, mata_kuliah, tanggal_pengumpulan, waktu_pengumpulan = row
                        st.markdown(f"### __{nama_tugas}__ - *{mata_kuliah}*")
                        st.caption(f"{tanggal_pengumpulan} | {waktu_pengumpulan}")
                        with st.expander("Keterangan: "):
                            st.write(f"{keterangan}")

                        if st.button("Done"):
                            with tugas_conn:
                                tugas_conn.execute("DELETE FROM tugas WHERE nama_tugas = ?", (nama_tugas,))
                            st.success("Selamat Tugas Anda Sudah Selesai, Silahkan Kerjakan Tugas Lainnyaa!")
            
                        #if datetime.now() > datetugas:
                        #    st.error("Waktu Pengumpulan Sudah Melewati Tenggat")
                else:
                    st.write("Belum ada tugas dalam waktu dekat. Anda dapat menambahkan tugas apabila terdapat tugas dalam waktu dekat.")

            elif fitur == "Tambah Tugas":
                st.subheader("Tambah Tugas")
                nama_tugas = st.text_input("Nama Tugas:")
                keterangan = st.text_area("Keterangan:")
                matkul = st.text_input("Mata Kuliah:")
                tanggal = st.date_input("Tanggal Pengumpulan:")
                waktu = st.time_input("Waktu Pengumpulan:", None)
                tugas_conn = sql.connect("file:tugas.db?mode=rwc", uri=True)

                #datetugas = datetime.combine(tanggal, waktu)
                tanggalstr = str(tanggal)
                waktustr = str(waktu)

                if st.button("Tambah Tugas"):
                    with tugas_conn:
                        tugas_conn.execute("INSERT INTO tugas(nama_tugas, keterangan, mata_kuliah, tanggal_pengumpulan, waktu_pengumpulan) VALUES (?, ?, ?, ?, ?)",
                            (nama_tugas, keterangan, matkul, tanggalstr, waktustr)
                        )
                        st.success("Tugas berhasil ditambahkan")

        elif selected_tab == "Data Search":
            st.header(":blue[Data Search]", divider="grey")
            fitur = st.selectbox("Pilih Menu:", options=["Jadwal dan Ruang Kelas", "Tambah Jadwal dan Ruang Kelas"])
            
            if fitur == "Jadwal dan Ruang Kelas":
                st.subheader("Jadwal dan Ruang Kelas")

                menu_datasearch = st.selectbox("Pilih Menu:",["Cari Jadwal", "Hapus & Ubah Jadwal"])
                
                if menu_datasearch == "Cari Jadwal":

                    cursor_jadwal = jadwal_ruangkelas_conn.cursor()
                    keyword = st.text_input("Masukkan hari:")

                    cari = st.button("Cari")
                    if cari == True:
                        # Memanggil fungsi pencarian
                        search_result = search_jadwal(cursor_jadwal, keyword)

                        # Menampilkan hasil pencarian
                        st.write("Hasil Pencarian:")
                        display_jadwal(search_result)

            
                    elif cari == False:

                        jadwal_sort = jadwal_ruangkelas_conn.execute("SELECT * FROM jadwal_kelas ORDER BY jadwal ASC").fetchall()

                        st.write("<h4>Jadwal Mingguan Anda:</h4>", unsafe_allow_html = True)
                        display_jadwal(jadwal_sort)

                elif menu_datasearch == "Hapus & Ubah Jadwal":

                    jadwal_sort = jadwal_ruangkelas_conn.execute("SELECT * FROM jadwal_kelas ORDER BY jadwal ASC").fetchall()
                    cursor_jadwal = jadwal_ruangkelas_conn.cursor()

                    st.write("<h4>Pilih Jadwal Untuk Di Hapus:</h4>", unsafe_allow_html = True)
                    display_delete_jadwal(jadwal_ruangkelas_conn, cursor_jadwal, jadwal_sort)

            elif fitur == "Tambah Jadwal dan Ruang Kelas":
                st.subheader("Tambah Data")
                matkul = st.text_input("Mata Kuliah:")
                hari = str(st.selectbox("Pilih Hari:", ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu"]))
                jam_mulai = str(st.time_input("Waktu Mulai:"))
                jam_akhir = str(st.time_input("Waktu Selesai:"))
                kelas = st.text_input("Kelas:")
                ruangkelas = st.text_input("Ruang Kelas:")

                if st.button("Tambah"):
                    with jadwal_ruangkelas_conn:
                        jadwal_ruangkelas_conn.execute("INSERT INTO jadwal_kelas(mata_kuliah, kelas, jadwal, jam_mulai, jam_akhir, ruang_kelas) VALUES (?, ?, ?, ?, ?, ?)",
                                                       (matkul, kelas, hari, jam_mulai, jam_akhir, ruangkelas)
                                                       )
                        st.success("Jadwal berhasil ditambahkan")

        elif selected_tab == "Data Notes":
            st.header(":blue[Data Notes]", divider="grey")
            fitur = st.selectbox("Pilih Menu:", options=["Notes", "Tambah Notes"])

            if fitur == "Notes":
                st.subheader("Notes")
                note = notes_conn.execute("SELECT judul, notes, tanggal FROM notes").fetchall()

                if note:
                    for row in note:
                        judul, notes, tanggal = row
                        st.markdown(f"#### __{judul}__")
                        st.caption(f"{tanggal}")
                        st.write(f'''<div style="text-align: justify">
                                 {notes}
                                 </div>''', unsafe_allow_html=True) 

            elif fitur == "Tambah Notes":
                st.subheader("Tambah Notes")
                judul = st.text_input("Judul:")
                tanggal_notes = st.date_input("Tanggal:")
                notes = st.text_area("Masukkan teks anda disini:")

                if st.button("Tambah"):
                    with notes_conn:
                        notes_conn.execute("INSERT INTO notes (judul, notes, tanggal) VALUES (?, ?, ?)", (judul, notes, tanggal_notes ))
                        st.success("Notes berhasil ditambahkan")

    if __name__ == "__main__":
        main()

    authenticator.logout("Logout","sidebar")

