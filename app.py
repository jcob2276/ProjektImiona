import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Wczytanie danych
df = pd.read_csv("top15_imiona_chlopcy.csv", encoding='cp1250')

# Interfejs aplikacji
st.title("🔎 Analiza popularności imion chłopięcych w Polsce (2000–2024)")
st.markdown("Wizualizacja zmian **pozycji w rankingu** oraz **liczby nadanych imion**.")

# Wybór trybu filtrowania imion
tryb = st.radio("🎛️ Jak chcesz wybrać imiona?", ["TOP z rankingu", "Własny wybór"])

if tryb == "TOP z rankingu":
    top_n = st.selectbox("🎯 Wybierz TOP N:", [5, 10, 15], index=1)

    # Filtrowanie: tylko top N w każdym roku
    df_filtered = (
        df[df['plec'] == 'M']
        .groupby('Rok')
        .apply(lambda x: x.nsmallest(top_n, 'Ranking'))
        .reset_index(drop=True)
    )
    st.success(f"Poniżej pokazano dane dla TOP {top_n} imion chłopięcych w każdym roku.")
else:
    imiona_dostepne = sorted(df['Imie'].unique())
    imiona_wybrane = st.multiselect(
        "👶 Wybierz imiona do porównania:",
        options=imiona_dostepne,
        default=["JAKUB", "ANTONI", "KACPER"]
    )
    df_filtered = df[df['Imie'].isin(imiona_wybrane) & (df['plec'] == 'M')]

# Wybór typu wykresu
typ_wykresu = st.radio("📊 Co chcesz analizować?", ["Pozycja w rankingu", "Liczba nadanych imion"])

# Tworzenie wykresu
fig, ax = plt.subplots(figsize=(10, 6))

if typ_wykresu == "Pozycja w rankingu":
    sns.lineplot(data=df_filtered, x='Rok', y='Ranking', hue='Imie', marker='o', ax=ax)
    ax.invert_yaxis()
    ax.set_title("Zmiana pozycji w rankingu (niższa = wyżej)")
    ax.set_ylabel("Miejsce w rankingu")
else:
    sns.lineplot(data=df_filtered, x='Rok', y='Liczba', hue='Imie', marker='o', ax=ax)
    ax.set_title("Liczba nadanych imion w czasie")
    ax.set_ylabel("Liczba")

ax.set_xlabel("Rok")
st.pyplot(fig)

# Animacja bar chart race
st.markdown("#### 📽️ Animacja rankingu (Bar Chart Race):")
st.image("C:/Users/jakub/Desktop/ProjektGUS/bar_race_imiona_chlopcy.gif")
