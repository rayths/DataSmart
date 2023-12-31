import streamlit as st

# Fungsi menu jadwal
def search_jadwal(cursor_jadwal, keyword, username): # fungsi search
    query = "SELECT * FROM jadwal_kelas WHERE jadwal = ? AND username_db = ?"
    result = cursor_jadwal.execute(query, (keyword, username,)).fetchall()
    return result

def display_jadwal(jadwal):
    if jadwal:
        for row in jadwal:
            st.markdown(f"### __{row[3]}__")
            st.caption(f"{row[4]} - {row[5]}")
            st.text(f"{row[1]} ({row[2]}) | {row[6]}")
            
def display_search_jadwal(jadwal, jadwal_conn, username):
    sorted_jadwal = sorted(jadwal, key=lambda x: x[3])

    if sorted_jadwal:
        for row in sorted_jadwal:
            st.markdown(f"### __{row[3]}__")
            st.caption(f"{row[4]} - {row[5]}")
            st.text(f"{row[1]} ({row[2]}) | {row[6]}")
    else:
        st.warning("Tidak ada jadwal yang ditemukan, silahkan tambahkan jadwal anda.")

        # Display the sorted jadwal in case nothing is found
        jadwal_sort = jadwal_conn.execute("SELECT * FROM jadwal_kelas WHERE username_db = ? ORDER BY jadwal ASC", (username,)).fetchall()
        st.write("Jadwal Mingguan Anda:")
        display_jadwal(jadwal_sort)


def delete_jadwal(jadwal_conn, cursor_jadwal, jadwal):
    query = "DELETE FROM jadwal_kelas WHERE mata_kuliah = ?"
    cursor_jadwal.execute(query, (jadwal,))
    jadwal_conn.commit()
    st.success("Jadwal berhasil dihapus")

def update_jadwal(jadwal_conn, cursor_jadwal, new_jadwal):
    query = "UPDATE jadwal_kelas SET ? WHERE "
    cursor_jadwal.execute(query)
    jadwal_conn.commit()
    st.success("Jadwal berhasil diubah")

def display_delete_update_jadwal(jadwal_conn, cursor_jadwal, jadwal):
    if jadwal:
        for row in jadwal:
            st.markdown(f"### __{row[3]}__")
            st.caption(f"{row[4]} - {row[5]}")
            st.text(f"{row[1]} ({row[2]}) | {row[6]}")
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                if st.button("Hapus", key=f"{row[1]}"):
                    delete_jadwal(jadwal_conn, cursor_jadwal, row[1])
            with col2:
                if st.button("Ubah", key=f"{row[0]}"):
                    pass
    else:
        st.write("Tidak ada jadwal yang ditemukan, silahkan tambahkan jadwal anda.")


# Fungsi menu notes
def display_notes(note):
    if note:
        for row in note:
            judul, notes, tanggal = row
            st.markdown(f"#### __{judul}__")
            st.caption(f"{tanggal}")
            st.write(f'''<div style="text-align: justify">
                        {notes}
                        </div>''', unsafe_allow_html=True) 
            
    else:
        st.write("Belum ada data catatan. Silahkan buat catatan.")

def delete_notes(notes_conn, cursor_notes, note):
    query = "DELETE FROM notes WHERE judul = ?"
    cursor_notes.execute(query, (note,))
    notes_conn.commit()
    st.success("Catatan berhasil dihapus")

def display_delete_update_notes(notes_conn, cursor_notes, note):
    if note:
        for row in note:
            judul, notes, tanggal = row
            st.markdown(f"#### __{judul}__")
            st.caption(f"{tanggal}")
            st.write(f'''<div style="text-align: justify">
                        {notes}
                        </div>''', unsafe_allow_html=True) 
            
            col1, col2 = st.columns([0.9, 0.1])
            with col1:
                if st.button("Hapus", key=f"{judul}"):
                    delete_notes(notes_conn, cursor_notes, judul)
            with col2:
                if st.button("Ubah", key=f"{notes}"):
                    pass
    else:
        st.write("Belum ada data catatan. Silahkan buat catatan.")
