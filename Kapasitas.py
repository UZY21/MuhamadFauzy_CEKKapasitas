#Membuat Interface Lebih Menarik
import streamlit as st
from openpyxl.workbook import Workbook
import pandas as pd
from PIL import Image



#Sidebar Radio
Awal = st.sidebar.radio ("",['Home','Cek Kapasitas'])
#Laman AWAL
if Awal == "Home":
    st.header("TUGAS AKHIR")
    st.subheader("KAPASITAS PENAMPANG BALOK BETON BERTULANG DENGAN PYTHON")
    image = Image.open('ITENAS.png')
    st.image (image)
    st.subheader("Dibuat oleh:")
    st.write("Ir. Kamaludin, M.T., M.Kom.")
    st.write("Muhamad Fauzy")
if Awal == "Cek Kapasitas":
    st.header("ANALISIS KAPASITAS PENAMPANG BALOK BETON BERTULANG DENGAN PYTHON")
    tab2, tab3 = st.tabs(["Input Angka", "HASIL"])
    with tab2:
        st.subheader("INPUT DATA")
        image9 = Image.open('Tulangan1Lapis.png')
        st.image(image9)
        # Input Pembagian kolom
        col3, col4 = st.columns(2)
        with col3:
            h2 = st.number_input("Tinggi Penampang Balok =",value=500)
            b2 = st.number_input("Lebar Penampang Balok = ",value=250)
            D = st.number_input("Nilai Diameter Longitudinal (D) = ",value=25)
            d = st.number_input("Nilai Tinggi Efektif Balok (d) = ",value=450)
        with col4:
            fc = st.number_input("Nilai Mutu beton (Fc') = ",value=20)
            fy = st.number_input("Nilai Mutu Baja (Fy) = ",value=400)
            n = st.number_input("Jumlah Tulangan = ",value=3)
            # Asumsi
            Es = 200000
            hitung = st.button("EXECUTE")
            with tab3:
                st.header("CEK KAPASITAS")
                if hitung:
                    # Preliminary Desain
                    h = h2
                    b = b2
                    # Tulangan
                    if 17 <= fc <= 28:
                        beta_1 = 0.85
                    elif 28 <= fc < 55:
                        beta_1 = round(0.85 - (0.05 * (fc - 28) / 7), 2)
                    else:
                        beta_1 = 0.65
                    # Desain Tulangan
                    Asterpasang = round(n * (1 / 4) * 3.1416 * ((D) ** 2), 2)
                    # RasioTulangan
                    Aefektif = b * d
                    rho9 = round((Asterpasang / Aefektif), 3)
                    if rho9 < 0.025:
                        rho = "Memenuhi"
                    else:
                        rho = "TidakMemenuhi"
                    a = ((Asterpasang * fy) / (0.85 * fc * b))
                    c = ((a / beta_1))
                    ey = fy / Es
                    et1 = round((((d - c) / c) * 0.003), 5)
                    if et1 > ey:
                        et = "Under Reinfoce (Keruntuhan Tarik)"
                    elif et1 < ey:
                        et = "Over Reinforce (Keruntuhan Tekan)"
                    else:
                        et = "Balance"
                    # FaktorReduksiKekuatan
                    if et1 >= 0.005:
                        phi = 0.9
                    elif 0.002 < et1 < 0.005:
                        phi = round((0.65 + (et1 - 0.002) * (250 / 3)), 3)
                    else:
                        phi = 0.65
                    # Hitung Momen Nominal
                    Mn = round((Asterpasang * fy * (d - a / 2)) / 1000000, 3)
                    phiMn = round(phi * Mn, 3)
                    data = [h, b, d, n, Asterpasang,rho9, rho, ey, et1,et, phi, Mn,phiMn]
                    column_names=["h (mm)", "b (mm)", "d (mm)", "n(buah)",
                                                "As(mm^2)", "rho", "SyaratRasio", "ey", "et",
                                                "Jenis Keruntuhan", "phi", "Mn (kNm)", "phiMn (kNm)"]
                    df = pd.DataFrame([data],columns=column_names)
                    st.table(df)
                    excel = df.to_excel("data.xlsx", index=False)

                    with open("data.xlsx", "rb") as f:
                        excel_bytes = f.read()

                    st.download_button(
                        "Download Excel",
                        excel_bytes,
                        "Inkremental.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key='download-excel'
                    )