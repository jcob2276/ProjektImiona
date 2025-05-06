import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt

# Włączmy tryb interaktywny matplotlib
plt.ion()

# Wczytanie danych
df = pd.read_csv(r"C:\Users\jakub\Documents\top15_imiona_meskie.csv", encoding='cp1250')

# Sprawdźmy jakie dane mamy (zakładając że to imiona dziewczynek)
df_female = df[df['plec'] == 'M']

# Pivot – Rok jako index, imiona jako kolumny, Liczba jako wartości
df_pivot = df_female.pivot(index='Rok', columns='Imie', values='Liczba')

# Upewniamy się, że Rok to liczba i sortujemy
df_pivot.index = df_pivot.index.astype(int)
df_pivot = df_pivot.sort_index()

# Uzupełnij brakujące wartości zerami (ważne dla bar_chart_race)
df_pivot = df_pivot.fillna(0)

# Spróbujmy zapisać w różnych formatach i z różnymi ustawieniami
try:
    # Format MP4
    bcr.bar_chart_race(
        df=df_pivot,
        filename='C:/Users/jakub/Desktop/bar_race_imiona_meskie.mp4',
        orientation='h',
        sort='desc',
        n_bars=10,
        steps_per_period=30,
        period_length=2000,
        period_fmt='Rok {x:.0f}',
        title='TOP 10 imion męskich w Polsce',
        bar_size=.95,
        cmap='dark12',
        dpi=200,
        figsize=(10, 7),
        filter_column_colors=True
    )
    print("Zapisano w formacie MP4")
except Exception as e:
    print(f"Błąd przy zapisie MP4: {e}")

try:
    # Format GIF z obniżoną jakością
    bcr.bar_chart_race(
        df=df_pivot,
        filename='C:/Users/jakub/Desktop/bar_race_imiona_dziewczynki_low.gif',
        orientation='h',
        sort='desc',
        n_bars=10,
        steps_per_period=20,  # mniej kroków
        period_length=1500,   # krótszy czas
        period_fmt='Rok {x:.0f}',
        title='TOP 10 imion dziewczęcych w Polsce',
        bar_size=.95,
        cmap='dark12',
        dpi=150,  # niższa rozdzielczość
        figsize=(8, 6),  # mniejszy rozmiar
        filter_column_colors=True
    )
    print("Zapisano GIF w niższej jakości")
except Exception as e:
    print(f"Błąd przy zapisie GIF niskiej jakości: {e}")

try:
    # Spróbujmy użyć HTML jako alternatywy
    bcr.bar_chart_race(
        df=df_pivot,
        filename='C:/Users/jakub/Desktop/bar_race_imiona_meskie.html',
        orientation='h',
        sort='desc',
        n_bars=10,
        steps_per_period=30,
        period_length=2000,
        period_fmt='Rok {x:.0f}',
        title='TOP 10 imion męskich w Polsce',
        bar_size=.95,
        cmap='dark12',
        dpi=200,
        figsize=(10, 7),
        filter_column_colors=True
    )
    print("Zapisano w formacie HTML")
except Exception as e:
    print(f"Błąd przy zapisie HTML: {e}")