import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Database Warga Desa", layout="wide")

# =========================
# SAFE LOAD DATA
# =========================
def load_data(file, columns):
    try:
        if (not os.path.exists(file)) or os.path.getsize(file) == 0:
            df = pd.DataFrame(columns=columns)
            df.to_csv(file, index=False)
            return df
        return pd.read_csv(file)
    except:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file, index=False)
        return df


# =========================
# VALIDATOR 16 DIGIT
# =========================
def validate_16digit(value):
    value = str(value).strip()
    return value.isdigit() and len(value) == 16


# =========================
# HIGHLIGHT INVALID DATA
# =========================
def highlight_kk(row):
    if len(str(row["No_KK"])) != 16:
        return ["background-color:#ffcccc"] * len(row)
    return [""] * len(row)


def highlight_nik(row):
    if len(str(row["NIK"])) != 16:
        return ["background-color:#ffcccc"] * len(row)
    return [""] * len(row)


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
# MENU
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

    no_kk = st.text_input("No KK (16 digit)")

    if no_kk:
        if not no_kk.isdigit():
            st.error("Harus angka semua")
        elif len(no_kk) != 16:
            st.warning(f"Panjang: {len(no_kk)} (harus 16)")
        else:
            st.success("Valid ✔")

    nama_kk = st.text_input("Nama Kepala Keluarga")
    rt = st.text_input("RT")
    rw = st.text_input("RW")
    dusun = st.text_input("Dusun")

    status_rumah = st.selectbox("Status Rumah", ["Milik", "Kontrak", "Menumpang"])
    kondisi_rumah = st.selectbox("Kondisi Rumah", ["Layak", "Tidak Layak"])
    bantuan = st.selectbox("Bantuan", ["Tidak Ada", "PKH", "BPNT", "BLT"])

    if st.button("Simpan KK"):
        if not validate_16digit(no_kk):
            st.error("No KK harus 16 digit angka")
        else:
            df_kk.loc[len(df_kk)] = [
                no_kk, nama_kk, rt, rw, dusun,
                status_rumah, kondisi_rumah, bantuan
            ]
            df_kk.to_csv("data_kk.csv", index=False)
            st.success("KK berhasil disimpan")


# =========================
# INPUT NIK
# =========================
elif menu == "Input NIK":
    st.title("🟨 Input Data NIK")

    if df_kk.empty:
        st.warning("Isi KK dulu")
    else:
        no_kk = st.selectbox("Pilih KK", df_kk["No_KK"].unique())

        nik = st.text_input("NIK (16 digit)")

        if nik:
            if not nik.isdigit():
                st.error("Harus angka semua")
            elif len(nik) != 16:
                st.warning(f"Panjang: {len(nik)} (harus 16)")
            else:
                st.success("Valid ✔")

        nama = st.text_input("Nama")
        jk = st.selectbox("JK", ["L", "P"])
        umur = st.number_input("Umur", 0, 120)

        hubungan = st.selectbox("Hubungan", ["Kepala Keluarga","Istri","Anak","Lainnya"])
        pendidikan = st.selectbox("Pendidikan", ["Tidak Sekolah","SD","SMP","SMA","Kuliah"])
        pekerjaan = st.text_input("Pekerjaan")

        bpjs = st.selectbox("BPJS", ["Aktif","Tidak"])
        disabilitas = st.selectbox("Disabilitas", ["Tidak","Ya"])

        if st.button("Simpan NIK"):
            if not validate_16digit(nik):
                st.error("NIK harus 16 digit angka")
            else:
                df_nik.loc[len(df_nik)] = [
                    no_kk, nik, nama, jk, umur,
                    hubungan, pendidikan, pekerjaan,
                    bpjs, disabilitas
                ]
                df_nik.to_csv("data_nik.csv", index=False)
                st.success("NIK berhasil disimpan")


# =========================
# VIEW KK + DELETE + HIGHLIGHT
# =========================
elif menu == "Data KK":
    st.title("📊 Data KK")

    st.dataframe(
        df_kk.style.apply(highlight_kk, axis=1),
        use_container_width=True
    )

    st.subheader("🗑️ Hapus KK")

    if not df_kk.empty:
        selected = st.selectbox("Pilih No KK", df_kk["No_KK"])

        if st.button("Hapus KK"):
            df_kk = df_kk[df_kk["No_KK"] != selected]
            df_kk.to_csv("data_kk.csv", index=False)
            st.success("KK dihapus")
            st.rerun()


# =========================
# VIEW NIK + DELETE + HIGHLIGHT
# =========================
elif menu == "Data NIK":
    st.title("📊 Data NIK")

    st.dataframe(
        df_nik.style.apply(highlight_nik, axis=1),
        use_container_width=True
    )

    st.subheader("🗑️ Hapus NIK")

    if not df_nik.empty:
        selected = st.selectbox("Pilih NIK", df_nik["NIK"])

        if st.button("Hapus NIK"):
            df_nik = df_nik[df_nik["NIK"] != selected]
            df_nik.to_csv("data_nik.csv", index=False)
            st.success("NIK dihapus")
            st.rerun()


# =========================
# EXPORT EXCEL
# =========================
elif menu == "Export Data":
    st.title("📦 Export Excel")

    if st.button("Generate Excel"):
        file = "database_desa.xlsx"

        with pd.ExcelWriter(file, engine="openpyxl") as writer:
            df_kk.to_excel(writer, sheet_name="KK", index=False)
            df_nik.to_excel(writer, sheet_name="NIK", index=False)

        with open(file, "rb") as f:
            st.download_button(
                "Download Excel",
                f,
                file_name=file
            )