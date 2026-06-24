import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Database Warga Desa", layout="wide")

# =========================
# LOAD DATA (ANTI ERROR + AUTO INIT)
# =========================
def load_data(file, columns):
    try:
        if (not os.path.exists(file)) or os.path.getsize(file) == 0:
            df = pd.DataFrame(columns=columns)
            df.to_csv(file, index=False)
            return df

        return pd.read_csv(file)

    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file, index=False)
        return df


# =========================
# VALIDATOR 16 DIGIT
# =========================
def validate_16digit(value, label):
    value = str(value).strip()

    if not value.isdigit():
        return False, f"{label} harus angka semua"

    if len(value) != 16:
        return False, f"{label} harus tepat 16 digit"

    return True, value


# =========================
# INIT DATA
# =========================
df_kk = load_data("data_kk.csv", [
    "No_KK","Nama_KK","RT","RW","Dusun",
    "Status_Rumah","Kondisi_Rumah","Bantuan"
])

df_nik = load_data("data_nik.csv", [
    "No_KK","NIK","Nama","JK","Umur","Hubungan",
    "Pendidikan","Pekerjaan","BPJS","Disabilitas"
])


# =========================
# SIDEBAR MENU
# =========================
menu = st.sidebar.selectbox(
    "Menu",
    ["Input KK", "Input NIK", "Data KK", "Data NIK", "Export Data"]
)


# =========================
# INPUT KK
# =========================
if menu == "Input KK":
    st.title("🟦 Input Data KK")

    with st.form("form_kk"):
        no_kk = st.text_input("No KK (16 digit)")
        nama_kk = st.text_input("Nama Kepala Keluarga")
        rt = st.text_input("RT")
        rw = st.text_input("RW")
        dusun = st.text_input("Dusun")

        status_rumah = st.selectbox("Status Rumah", ["Milik", "Kontrak", "Menumpang"])
        kondisi_rumah = st.selectbox("Kondisi Rumah", ["Layak", "Tidak Layak"])
        bantuan = st.selectbox("Bantuan", ["Tidak Ada", "PKH", "BPNT", "BLT"])

        submit = st.form_submit_button("Simpan KK")

        if submit:
            valid, result = validate_16digit(no_kk, "No KK")

            if not valid:
                st.error(result)
            else:
                new_data = pd.DataFrame([{
                    "No_KK": result,
                    "Nama_KK": nama_kk,
                    "RT": rt,
                    "RW": rw,
                    "Dusun": dusun,
                    "Status_Rumah": status_rumah,
                    "Kondisi_Rumah": kondisi_rumah,
                    "Bantuan": bantuan
                }])

                df_kk = pd.concat([df_kk, new_data], ignore_index=True)
                df_kk.to_csv("data_kk.csv", index=False)
                st.success("Data KK berhasil disimpan!")


# =========================
# INPUT NIK
# =========================
elif menu == "Input NIK":
    st.title("🟨 Input Data Anggota (NIK)")

    if df_kk.empty:
        st.warning("Isi data KK dulu!")
    else:
        with st.form("form_nik"):
            no_kk = st.selectbox("Pilih No KK", df_kk["No_KK"].unique())

            nik = st.text_input("NIK (16 digit)")
            nama = st.text_input("Nama")

            jk = st.selectbox("Jenis Kelamin", ["L", "P"])
            umur = st.number_input("Umur", 0, 120)

            hubungan = st.selectbox("Hubungan", [
                "Kepala Keluarga", "Istri", "Anak", "Lainnya"
            ])

            pendidikan = st.selectbox("Pendidikan", [
                "Tidak Sekolah", "SD", "SMP", "SMA", "Kuliah"
            ])

            pekerjaan = st.text_input("Pekerjaan")

            bpjs = st.selectbox("BPJS", ["Aktif", "Tidak"])
            disabilitas = st.selectbox("Disabilitas", ["Tidak", "Ya"])

            submit = st.form_submit_button("Simpan NIK")

            if submit:
                valid, result = validate_16digit(nik, "NIK")

                if not valid:
                    st.error(result)
                else:
                    new_data = pd.DataFrame([{
                        "No_KK": no_kk,
                        "NIK": result,
                        "Nama": nama,
                        "JK": jk,
                        "Umur": umur,
                        "Hubungan": hubungan,
                        "Pendidikan": pendidikan,
                        "Pekerjaan": pekerjaan,
                        "BPJS": bpjs,
                        "Disabilitas": disabilitas
                    }])

                    df_nik = pd.concat([df_nik, new_data], ignore_index=True)
                    df_nik.to_csv("data_nik.csv", index=False)
                    st.success("Data NIK berhasil disimpan!")


# =========================
# VIEW DATA KK
# =========================
elif menu == "Data KK":
    st.title("📊 Data KK")
    st.dataframe(df_kk, use_container_width=True)


# =========================
# VIEW DATA NIK
# =========================
elif menu == "Data NIK":
    st.title("📊 Data NIK")
    st.dataframe(df_nik, use_container_width=True)


# =========================
# EXPORT EXCEL
# =========================
elif menu == "Export Data":
    st.title("📦 Export Data")

    if st.button("Generate Excel"):
        file_name = "database_desa.xlsx"

        with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
            df_kk.to_excel(writer, sheet_name="KK", index=False)
            df_nik.to_excel(writer, sheet_name="NIK", index=False)

        with open(file_name, "rb") as f:
            st.download_button(
                "Download Excel",
                f,
                file_name=file_name
            )