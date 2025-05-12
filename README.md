# 📊 Analiza popularności imion w Polsce (2000–2024)

Celem projektu była analiza zmian w rankingach imion męskich i żeńskich nadawanych dzieciom w Polsce w latach **2000–2024**. Dane pochodzą z Głównego Urzędu Statystycznego (GUS) i zostały przetworzone do formy pozwalającej na porównania rok do roku.

Zbudowaliśmy interaktywną aplikację w Streamlit, która umożliwia:

- analizę **pozycji w rankingu** oraz **liczby nadań imion** w czasie,
- porównania między latami: awanse, spadki, stabilność imion,
- dynamiczne przeglądanie imion TOP 5/10/15 lub własny wybór,
- prezentację danych w postaci wykresów i tabel,
- interpretację wyników z uwzględnieniem kontekstu kulturowego,
- wizualizację trendów w formie **animacji Bar Chart Race** dla imion chłopięcych i dziewczęcych.

Dodatkowo dodaliśmy sekcję z automatycznie generowanymi wnioskami, które pokazują różnice między rankingiem a realną zmianą popularności (liczby).

Projekt zawiera pełną obsługę filtrowania, analizę różnic (`ΔRanking`, `ΔLiczba`) oraz komentarze opisujące zmiany dla każdego imienia.

