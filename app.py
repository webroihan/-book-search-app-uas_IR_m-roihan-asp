import streamlit as st
import json

st.set_page_config(page_title="Book Search App", layout="wide")

@st.cache_data
def load_books():
    try:
        with open("data/books.json", "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Gagal memuat data buku: {e}")
        return []

books = load_books()

with st.sidebar:
    st.title("🔍 Filter Buku")
    search = st.text_input("Cari Judul")
    min_price, max_price = st.slider("Rentang Harga (£)", 0.0, 100.0, (0.0, 50.0))
    rating = st.selectbox("Rating", ["All", "One", "Two", "Three", "Four", "Five"])
    stock = st.checkbox("Hanya Tersedia", True)

filtered = [
    b for b in books
    if (search.lower() in b['title'].lower() if search else True)
    and (min_price <= float(b['price'].replace('\u00a3','').replace('£','')) <= max_price)
    and (rating == "All" or b['rating'] == rating)
    and (not stock or "In stock" in b['availability'])
]

st.title("📚 Books to Scrape - Explorer")
if not filtered:
    st.warning("Tidak ada buku ditemukan dengan filter saat ini.")
for book in filtered:
    with st.expander(book['title']):
        st.metric("💲 Harga", book['price'])
        st.write(f"⭐ Rating: {book['rating']}")
        st.write(f"📦 Ketersediaan: {book['availability']}")
