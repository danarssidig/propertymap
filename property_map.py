import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Peta Nilai Properti Kota Tangerang")
st.markdown("Sumber Data: Pusat Pembinaan Profesi Keuangan")
st.markdown("")
# Load data
df_tangcity = pd.read_csv('df_property.csv')

# Set up map
tangcity_map = folium.Map(location=[df_tangcity['Latitude'].mean(), df_tangcity['Longitude'].mean()], zoom_start=14)
                          
# Create sidebar for filtering
st.sidebar.subheader("")
st.sidebar.subheader("Filter Atribut Data Properti")
selected_subdistrict = st.sidebar.selectbox("Pilih Kecamatan", df_tangcity['Kecamatan'].unique())
filtered_subdistrict = df_tangcity[df_tangcity['Kecamatan']== selected_subdistrict]
selected_village = st.sidebar.selectbox("Pilih Desa/Kelurahan", filtered_subdistrict['Desa'].unique())
filtered_village = filtered_subdistrict[filtered_subdistrict['Desa']== selected_village]
selected_valuation_objectives = [st.sidebar.selectbox("Pilih Tujuan Penilaian", df_tangcity['Tujuan Penilaian'].unique())]
filtered_valuation_objectives = filtered_village[filtered_village['Tujuan Penilaian'].isin(selected_valuation_objectives)]
selected_property_types = st.sidebar.multiselect("Pilih Jenis Properti (Bisa >1)", df_tangcity['Jenis_Objek'].unique())
filtered_data = filtered_valuation_objectives[filtered_valuation_objectives['Jenis_Objek'].isin(selected_property_types)]
selected_display = st.sidebar.multiselect("Pilih Nilai untuk Ditampilkan (Bisa >1)", options=["Nilai Tanah/m2", "Nilai Objek", "Total Nilai"], default=[])

# Set up map
if len(filtered_data) == 0:
    tangcity_map = folium.Map(location=[df_tangcity['Latitude'].mean(), df_tangcity['Longitude'].mean()], zoom_start=14)
else:
    tangcity_map= folium.Map(location=[filtered_data['Latitude'].mean(), filtered_data['Longitude'].mean()], zoom_start=16)

# Loop over filtered data and add markers to map
for index, row in filtered_data.iterrows():
    lat = row['Latitude']
    lon = row['Longitude']
    nilai_tanah = row['Indikasi Nilai Tanah']
    nilai_objek = row['Nilai Objek']
    total_nilai = row['Total Nilai']
    tanggal_penilaian = row['Tgl Penilaian']
    
    # Construct html string based on selected values
    html = ""
    if "Nilai Tanah/m2" in selected_display:
        html += f"Nilai Tanah: {nilai_tanah}/m<sup>2</sup><br>"
    if "Nilai Objek" in selected_display:
        html += f"Nilai Objek: {nilai_objek}<br>"
    if "Total Nilai" in selected_display:
        html += f"Total Nilai: {total_nilai}<br>"
        
    # Always add Tanggal Penilaian as hover information
    html += f"Tgl. Penilaian: {tanggal_penilaian}"
    
    # Add marker to map with hover information
    folium.Marker(
        [lat, lon],
        tooltip=html
    ).add_to(tangcity_map)

# Display the map
tangcity_data = st_folium(tangcity_map, width=725, height=450)


