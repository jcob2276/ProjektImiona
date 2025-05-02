import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Ustawienia strony
st.set_page_config(
    page_title="Analiza popularności imion w Polsce",
    page_icon="👶",
    layout="wide",
)

# Funkcja do wczytywania danych
@st.cache_data
def load_data():
    try:
        df_chlopcy = pd.read_csv("top15_imiona_meskie.csv", encoding='cp1250')
        df_chlopcy['plec'] = 'M'  # Upewniamy się, że płeć jest poprawnie oznaczona
        
        # Próba wczytania danych dla dziewczynek (jeśli istnieją)
        try:
            df_dziewczyn = pd.read_csv("top15_imiona_zenskie.csv", encoding='cp1250')
            df_dziewczyn['plec'] = 'K'
            df = pd.concat([df_chlopcy, df_dziewczyn], ignore_index=True)
        except FileNotFoundError:
            df = df_chlopcy
            st.warning("Znaleziono tylko dane dla chłopców. Filtrowanie po płci będzie ograniczone.")
        
        return df
    except Exception as e:
        st.error(f"Błąd podczas wczytywania danych: {e}")
        return pd.DataFrame()

# Stylizacja
def set_custom_style():
    # Ustawienia dla wykresów
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 16

# Strona główna aplikacji
def main():
    set_custom_style()
    
    # Header z tytułem i opisem
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("🔎 Analiza popularności imion w Polsce")
        st.markdown("Wizualizacja zmian **pozycji w rankingu** oraz **liczby nadanych imion** na podstawie danych GUS.")
    

    st.markdown("---")
    
    # Wczytanie danych
    df = load_data()
    
    if df.empty:
        st.error("Nie udało się wczytać danych. Sprawdź czy plik CSV jest dostępny.")
        return
    
    # Filtrowanie danych
    with st.sidebar:
        st.header("🛠️ Ustawienia analizy")
        
        # Wybór płci
        plec_options = []
        if 'M' in df['plec'].unique():
            plec_options.append("Chłopcy")
        if 'K' in df['plec'].unique():
            plec_options.append("Dziewczyny")
        
        if len(plec_options) > 1:
            wybrana_plec = st.radio("👫 Wybierz płeć:", plec_options)
            plec_filter = 'M' if wybrana_plec == "Chłopcy" else 'K'
        else:
            wybrana_plec = plec_options[0] if plec_options else "Chłopcy"
            plec_filter = 'M'
            st.info(f"Dostępne dane tylko dla: {wybrana_plec}")
        
        # Filtrowanie po płci
        df_plec = df[df['plec'] == plec_filter]
        
        # Wybór przedziału czasowego
        lata = sorted(df_plec['Rok'].unique())
        min_rok, max_rok = min(lata), max(lata)
        
        st.write("📅 Wybierz przedział czasowy:")
        rok_start, rok_koniec = st.select_slider(
            "Zakres lat:",
            options=lata,
            value=(min_rok, max_rok)
        )
        
        # Filtrowanie po latach
        df_filtered_years = df_plec[(df_plec['Rok'] >= rok_start) & (df_plec['Rok'] <= rok_koniec)]
        
        # Tryb filtrowania imion
        st.write("🎛️ Jak chcesz wybrać imiona?")
        tryb = st.radio("", ["TOP z rankingu", "Własny wybór"])
        
        if tryb == "TOP z rankingu":
            top_n = st.selectbox("🎯 Wybierz TOP N:", [5, 10, 15], index=1)
            
            # Znajdź imiona, które były w TOP N w którymkolwiek roku
            top_imiona = set()
            for rok in df_filtered_years['Rok'].unique():
                rok_df = df_filtered_years[df_filtered_years['Rok'] == rok]
                top_n_w_roku = rok_df.nsmallest(top_n, 'Ranking')['Imie'].tolist()
                top_imiona.update(top_n_w_roku)
            
            # Filtrowanie tylko do imion z top N
            df_final = df_filtered_years[df_filtered_years['Imie'].isin(top_imiona)]
            st.success(f"Pokazuję dane dla TOP {top_n} imion w każdym roku.")
            
        else:  # "Własny wybór"
            imiona_dostepne = sorted(df_filtered_years['Imie'].unique())
            
            # Znajdź topowe imiona jako domyślne
            top_imiona = (df_filtered_years
                          .groupby('Imie')['Ranking']
                          .min()
                          .sort_values()
                          .head(3)
                          .index
                          .tolist())
            
            imiona_wybrane = st.multiselect(
                "👶 Wybierz imiona do porównania:",
                options=imiona_dostepne,
                default=top_imiona[:3] if top_imiona else imiona_dostepne[:3] if imiona_dostepne else []
            )
            
            if not imiona_wybrane:
                st.warning("Wybierz co najmniej jedno imię.")
                return
                
            df_final = df_filtered_years[df_filtered_years['Imie'].isin(imiona_wybrane)]
        
        # Typ analizy
        st.write("📊 Co chcesz analizować?")
        typ_wykresu = st.radio("", ["Pozycja w rankingu", "Liczba nadanych imion"])
    
    # Główny obszar wykresu
    st.subheader(f"📈 Analiza imion {'chłopięcych' if plec_filter == 'M' else 'dziewczęcych'} w latach {rok_start}–{rok_koniec}")
    
    if df_final.empty:
        st.warning("Brak danych do wyświetlenia dla wybranych kryteriów.")
        return
    
    # Tworzenie wykresu
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Paleta kolorów
    palette = sns.color_palette("husl", len(df_final['Imie'].unique()))
    
    if typ_wykresu == "Pozycja w rankingu":
        sns.lineplot(
            data=df_final, 
            x='Rok', 
            y='Ranking', 
            hue='Imie', 
            marker='o', 
            linewidth=2.5,
            markersize=8,
            palette=palette,
            ax=ax
        )
        ax.invert_yaxis()  # Odwrócenie osi Y
        ax.set_title(f"Zmiana pozycji w rankingu imion {'chłopięcych' if plec_filter == 'M' else 'dziewczęcych'} ({rok_start}–{rok_koniec})")
        ax.set_ylabel("Miejsce w rankingu (niższe = popularniejsze)")
    else:
        sns.lineplot(
            data=df_final, 
            x='Rok', 
            y='Liczba', 
            hue='Imie', 
            marker='o',
            linewidth=2.5,
            markersize=8,
            palette=palette,
            ax=ax
        )
        ax.set_title(f"Liczba nadanych imion {'chłopięcych' if plec_filter == 'M' else 'dziewczęcych'} ({rok_start}–{rok_koniec})")
        ax.set_ylabel("Liczba nadanych imion")
    
    # Formatowanie wykresu
    ax.set_xlabel("Rok")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.tick_params(axis='x', rotation=45)
    
    # Dodanie etykiet z wartościami dla ostatniego roku
    ostatni_rok = df_final['Rok'].max()
    for imie in df_final['Imie'].unique():
        ostatni_punkt = df_final[(df_final['Rok'] == ostatni_rok) & (df_final['Imie'] == imie)]
        if not ostatni_punkt.empty:
            if typ_wykresu == "Pozycja w rankingu":
                wartosc = ostatni_punkt['Ranking'].values[0]
            else:
                wartosc = ostatni_punkt['Liczba'].values[0]
            ax.annotate(
                f"{wartosc}",
                (ostatni_rok, wartosc),
                xytext=(10, 0),
                textcoords='offset points',
                fontsize=9,
                fontweight='bold'
            )
    
    # Zwiększenie marginesów dla lepszej czytelności legendy
    plt.tight_layout()
    plt.legend(title="Imię", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Wyświetlenie wykresu
    st.pyplot(fig)
    
    # Podsumowanie danych
    with st.expander("📋 Podsumowanie danych"):
        # Tabela z danymi
        st.dataframe(
            df_final.pivot_table(
                index='Rok', 
                columns='Imie', 
                values='Liczba' if typ_wykresu == "Liczba nadanych imion" else 'Ranking',
                aggfunc='first'
            ).style.highlight_max(axis=1, color='lightgreen')
        )

    # PRZENIESIONO DO WNĘTRZA FUNKCJI MAIN:
    # Statyczny ranking z komentarzem – TOP 10 imion w wybranym roku
    with st.expander("🏅 Ranking imion i analiza zmian między latami"):
        st.markdown("Zobacz szczegółowy ranking TOP 10 imion w wybranym roku oraz analizę awansów, spadków i zmian liczby nadanych imion między kolejnymi latami.")

        rok_dla_rankingu = st.slider(
            "📆 Wybierz rok do analizy:",
            min_value=rok_start + 1,
            max_value=rok_koniec,
            value=max_rok
        )

        df_biezacy = df_plec[df_plec['Rok'] == rok_dla_rankingu].copy()
        df_poprzedni = df_plec[df_plec['Rok'] == (rok_dla_rankingu - 1)].copy()

        # 🎯 Top 10 klasyczne
        top10 = df_biezacy.nsmallest(10, 'Ranking').copy()
        top10 = top10[['Imie', 'Liczba', 'Ranking']].reset_index(drop=True)

        st.markdown("#### 📌 Ranking TOP 10 imion:")
        for idx, row in top10.iterrows():
            pozycja = idx + 1
            imie = row['Imie']
            liczba = int(row['Liczba'])
            ranking = int(row['Ranking'])

            # Komentarz na podstawie poprzedniego roku
            rekord_prev = df_poprzedni[df_poprzedni['Imie'] == imie]
            if rekord_prev.empty:
                opis = "(nowe w rankingu)"
            else:
                ranking_prev = int(rekord_prev['Ranking'].values[0])
                if ranking_prev == ranking:
                    opis = f"(utrzymuje miejsce {ranking}.)"
                elif ranking_prev > ranking:
                    opis = f"(awans z {ranking_prev}. miejsca)"
                else:
                    opis = f"(spadek z {ranking_prev}. miejsca)"

            st.markdown(f"**{pozycja}. {imie}** – {liczba} {opis}")

        # 📊 Tabela analityczna: porównanie zmian
        st.markdown("#### 🔄 Zmiany pozycji i liczby między rokiem {0} a {1}".format(rok_dla_rankingu - 1, rok_dla_rankingu))

        df_join = pd.merge(
            df_biezacy[['Imie', 'Ranking', 'Liczba']],
            df_poprzedni[['Imie', 'Ranking', 'Liczba']],
            on='Imie',
            how='inner',
            suffixes=('_now', '_prev')
        )

        df_join['ΔRanking'] = df_join['Ranking_prev'] - df_join['Ranking_now']
        df_join['ΔLiczba'] = df_join['Liczba_now'] - df_join['Liczba_prev']

        def gen_komentarz(row):
            if row['ΔRanking'] > 0 and row['ΔLiczba'] > 0:
                return "📈 Awans i wzrost liczby"
            elif row['ΔRanking'] < 0 and row['ΔLiczba'] < 0:
                return "📉 Spadek i spadek liczby"
            elif row['ΔRanking'] > 0 and row['ΔLiczba'] < 0:
                return "📊 Awans mimo spadku liczby"
            elif row['ΔRanking'] < 0 and row['ΔLiczba'] > 0:
                return "📉 Spadek mimo wzrostu liczby"
            else:
                return "➖ Brak zmian / niewielka różnica"

        df_join['Komentarz'] = df_join.apply(gen_komentarz, axis=1)

        df_join = df_join.sort_values(by='ΔRanking', ascending=False).reset_index(drop=True)

        st.dataframe(df_join[['Imie', 'Ranking_prev', 'Ranking_now', 'ΔRanking', 'Liczba_prev', 'Liczba_now', 'ΔLiczba', 'Komentarz']])

        
    # Sekcja animacji - PRZENIESIONA DO WNĘTRZA FUNKCJI MAIN
    st.markdown("---")
    st.subheader("🎬 Animacja rankingu (Bar Chart Race)")

    # Wybierz plik wideo w zależności od płci - teraz plec_filter jest dostępne
    plik_video = "bar_race_imiona_meskie.mp4" if plec_filter == 'M' else "bar_race_imiona_zenskie.mp4"

    col1, col2 = st.columns([3, 1])

    with col1:
        try:
            st.video(plik_video)
        except:
            st.warning(f"Nie znaleziono pliku wideo: {plik_video}")
            st.info("Upewnij się, że plik MP4 znajduje się w katalogu aplikacji.")

    with col2:
        st.markdown("""
        **🎥 Co pokazuje animacja?**
        
        Ta animacja przedstawia **dynamiczne zmiany pozycji imion w rankingu** na przestrzeni lat. 
        Pokazuje momenty awansu, spadku i dominacji niektórych imion w danym okresie.
        To efektowny sposób wizualizacji trendów społecznych.
        """)

        # Miejsce na komentarz
        st.markdown("---")
        st.subheader("💬 Interpretacja wyników")
        
        with st.container():
            st.markdown("""
            W tym miejscu możesz dodać własną interpretację wyników analizy. Na przykład:
            
            - Jakie trendy są widoczne w popularności imion?
            - Które imiona zdobywają popularność, a które ją tracą?
            - Czy widać wpływ wydarzeń kulturowych na wybór imion?
            - Jak zmieniają się preferencje rodziców na przestrzeni lat?
            
            Możesz edytować ten tekst w kodzie aplikacji, dodając własne obserwacje i wnioski.
            """)
        
        # Stopka
        st.markdown("---")
        st.caption("© 2025 | Aplikacja do analizy popularności imion na podstawie danych GUS")

if __name__ == "__main__":
    main()