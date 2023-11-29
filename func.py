import streamlit as st

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
            
def display_search_jadwal(jadwal, jadwal_conn, username): # fungsi display
    if jadwal:
        for row in jadwal:
            st.markdown(f"### __{row[3]}__")
            st.caption(f"{row[4]} - {row[5]}")
            st.text(f"{row[1]} ({row[2]}) | {row[6]}")
    else:
        st.warning("Tidak ada jadwal yang ditemukan, silahkan tambahkan jadwal anda.")

        jadwal_sort = jadwal_conn.execute("SELECT * FROM jadwal_kelas WHERE username_db = ? ORDER BY jadwal ASC", (username,)).fetchall() # inisalisi jadwal sort

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
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                if st.button("Hapus"):
                    delete_jadwal(jadwal_conn, cursor_jadwal, row[1])
            with col2:
                if st.button("Ubah"):
                    pass
    else:
        st.write("Tidak ada jadwal yang ditemukan, silahkan tambahkan jadwal anda.")
