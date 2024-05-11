import streamlit as st
import pandas as pd

# Cek apakah 'siswa' sudah ada di session_state
if 'siswa' not in st.session_state:
    st.session_state['siswa'] = []

def tampilan_utama():
    st.sidebar.title('Aplikasi Absensi Siswa')

    menu = ['Kelola Siswa', 'Kelola Absensi']
    pilihan = st.sidebar.selectbox('Menu', menu)

    if pilihan == 'Kelola Siswa':
        kelola_siswa()
    elif pilihan == 'Kelola Absensi':
        kelola_absensi()

def kelola_siswa():
    # Tamilan data siswa
    st.subheader('Kelola Siswa')

    # Mengecek apakah ada data siswa
    if len(st.session_state['siswa']):
        df = pd.DataFrame(st.session_state['siswa'])
        st.write(df[['Nama', 'NIS']])
    else:
        st.error('Belum ada data siswa')
    
    # Tambah data siswa
    with st.form(key='form_tambah'):
        st.subheader('Tambah Data Siswa')

        # Meminta input nama & NIS
        nama = st.text_input('Nama')
        nis = st.text_input('NIS')
        submit_tambah = st.form_submit_button('Tambah')
        
        if submit_tambah:

            # Validasi input tidak boleh kosong
            if nama == "" or nis == "":
                st.error('Nama dan NIS tidak boleh kosong')
            
            # Validasi NIS tidak boleh sama
            elif any(mhs['NIS'] == nis for mhs in st.session_state['siswa']):
                st.error('NIS sudah ada')

            # Menambahkan data baru
            else:
                st.session_state['siswa'].append({'Nama': nama, 'NIS': nis, 'Absen': False})
                st.rerun()

    # Hapus data siswa
    with st.form(key='form_hapus'):
        st.subheader('Hapus Data Siswa')

        # Meminta input NIS
        nis_hapus = st.text_input('NIS yang akan dihapus')
        submit_hapus = st.form_submit_button('Hapus')
        
        if submit_hapus:

            # Validasi input tidak boleh kosong
            if nis_hapus == "":
                st.error('NIS tidak boleh kosong')

            # Mengubah status absensi siswa
            elif any(mhs['NIS'] == nis_hapus for mhs in st.session_state['siswa']):
                st.session_state['siswa'] = [mhs for mhs in st.session_state['siswa'] if mhs['NIS'] != nis_hapus]
                st.rerun()
            
            # Validasi NIS tidak ditemukan
            else:
                st.error('NIS tidak ditemukan')

def kelola_absensi():
    st.subheader('Kelola Absensi')

    # Mengecek apakah ada data siswa
    if len(st.session_state['siswa']):
        df = pd.DataFrame(st.session_state['siswa'])
        st.write(df)
    else:
        st.error('Belum ada data siswa')
    
    with st.form(key='form_absensi'):
        nis_absen = st.text_input('NIS')
        submit_absen = st.form_submit_button('Absen')

        if submit_absen:
            # Validasi input tidak boleh kosong
            if nis_absen == "":
                st.error('NIS tidak boleh kosong')
            else:
                for mhs in st.session_state['siswa']:
                    if mhs['NIS'] == nis_absen:
                        mhs['Absen'] = True
                        st.rerun()

                st.error('NIS tidak ditemukan')

if __name__ == '__main__':
    tampilan_utama()
