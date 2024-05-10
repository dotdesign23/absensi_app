import streamlit as st
import pandas as pd

# Cek apakah 'mahasiswa' sudah ada di session_state
if 'mahasiswa' not in st.session_state:
    st.session_state['mahasiswa'] = []

def tampilan_utama():
    st.sidebar.title('Aplikasi Absensi Mahasiswa')

    menu = ['Kelola Mahasiswa', 'Kelola Absensi']
    pilihan = st.sidebar.selectbox('Menu', menu)

    if pilihan == 'Kelola Mahasiswa':
        kelola_mahasiswa()
    elif pilihan == 'Kelola Absensi':
        kelola_absensi()

def kelola_mahasiswa():
    # Tamilan data mahasiswa
    st.subheader('Kelola Mahasiswa')

    # Mengecek apakah ada data mahasiswa
    if len(st.session_state['mahasiswa']):
        df = pd.DataFrame(st.session_state['mahasiswa'])
        st.write(df[['Nama', 'NIM']])
    else:
        st.error('Belum ada data mahasiswa')
    
    # Tambah data mahasiswa
    with st.form(key='form_tambah'):
        st.subheader('Tambah Data Mahasiswa')

        # Meminta input nama & NIM
        nama = st.text_input('Nama')
        nim = st.text_input('NIM')
        submit_tambah = st.form_submit_button('Tambah')
        
        if submit_tambah:

            # Validasi input tidak boleh kosong
            if nama == "" or nim == "":
                st.error('Nama dan NIM tidak boleh kosong')
            
            # Validasi NIM tidak boleh sama
            elif any(mhs['NIM'] == nim for mhs in st.session_state['mahasiswa']):
                st.error('NIM sudah ada')

            # Menambahkan data baru
            else:
                st.session_state['mahasiswa'].append({'Nama': nama, 'NIM': nim, 'Absen': False})
                st.rerun()

    # Hapus data mahasiswa
    with st.form(key='form_hapus'):
        st.subheader('Hapus Data Mahasiswa')

        # Meminta input NIM
        nim_hapus = st.text_input('NIM yang akan dihapus')
        submit_hapus = st.form_submit_button('Hapus')
        
        if submit_hapus:

            # Validasi input tidak boleh kosong
            if nim_hapus == "":
                st.error('NIM tidak boleh kosong')

            # Mengubah status absensi mahasiswa
            elif any(mhs['NIM'] == nim_hapus for mhs in st.session_state['mahasiswa']):
                st.session_state['mahasiswa'] = [mhs for mhs in st.session_state['mahasiswa'] if mhs['NIM'] != nim_hapus]
                st.rerun()
            
            # Validasi NIM tidak ditemukan
            else:
                st.error('NIM tidak ditemukan')

def kelola_absensi():
    st.subheader('Kelola Absensi')

    # Mengecek apakah ada data mahasiswa
    if len(st.session_state['mahasiswa']):
        df = pd.DataFrame(st.session_state['mahasiswa'])
        st.write(df)
    else:
        st.error('Belum ada data mahasiswa')
    
    with st.form(key='form_absensi'):
        nim_absen = st.text_input('NIM')
        submit_absen = st.form_submit_button('Absen')

        if submit_absen:
            # Validasi input tidak boleh kosong
            if nim_absen == "":
                st.error('NIM tidak boleh kosong')
            else:
                for mhs in st.session_state['mahasiswa']:
                    if mhs['NIM'] == nim_absen:
                        mhs['Absen'] = True
                        st.rerun()
                        
                st.error('NIM tidak ditemukan')

if __name__ == '__main__':
    tampilan_utama()
