from http.client import responses

from config import NASA_API_KEY

import requests
import streamlit as st

from datetime import datetime

from streamlit import date_input

st.set_page_config(page_title="🛰️ NASA APOD Doğum Günü", layout="wide")
st.title(" 🪐 NASA - Doğum Gününde Nasa Ne Paylaştı?")


dogum_tarihi = st.date_input("🎂 Doğum Tarihi Seç",min_value=datetime(1995,6,16),max_value=datetime.today())
tarih_str = dogum_tarihi.strftime("%Y-%m-%d")

if st.button("🖼️ Göster"):

    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={tarih_str}"



    params={
        "api_key": NASA_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        st.subheader(data["title"])

        # Görsel varsa göster
        if data["media_type"] == "image":
            st.image(data["url"], use_container_width=True)
        else:
            st.video(data["url"])

        st.markdown(f"Tarih: **{data['date']}**")
        st.write("📰")
        st.write(data["explanation"])
    else:
        st.error("API'den veri alınamadı. Lütfen geçerli bir tarih giriniz.")



st.write("☄️ Doğum Gününde Yaklaşan Astreoidler ")
url2 = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={tarih_str}&end_date={tarih_str}&api_key={NASA_API_KEY}"

response2 = requests.get(url2)

if response2.status_code ==200:
    data2 = response2.json()
    astreoid_list = data2["near_earth_objects"][tarih_str]

    if astreoid_list:
        for a in astreoid_list:
            st.subheader(a["name"])
            st.write(f"🌍 Dünya'ya en yakın mesafe: **{a['close_approach_data'][0]['miss_distance']['kilometers']} km**")
            st.write(f"🚀 Hızı: **{a['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']} km/h**")
            st.write(f"⚠️ Tehlikeli mi?: **{'Evet' if a['is_potentially_hazardous_asteroid'] else 'Hayır'}**")

            st.markdown("****")
    else:
        st.info("Bu tarihte Dünyaya yaklaşan Asteroid bulunmadı")
else:
    st.error("Veri Bulunumadı Tekrar Deneyiniz!!!")






