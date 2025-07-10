
# 📜 **Opis techniczny działania skryptu generującego mnemoniki i portfele BIP44**

---

### 1️⃣ **Wybór języka interfejsu**

* Skrypt pyta użytkownika o wybór języka (`1 → English`, `2 → Polski`).
* Na podstawie wyboru `use_polish` jest ustawiany język do komunikatów.

---

### 2️⃣ **Wprowadzenie hasła (password)**

* Użytkownik wpisuje hasło złożone wyłącznie z liter A-Z lub a-z.
* Funkcja **`is_english_letters_only`** sprawdza, czy hasło zawiera tylko litery (regex `^[a-zA-Z]+$`).
* Jeśli hasło zawiera inne znaki, użytkownik jest proszony o ponowne wpisanie.

---

### 3️⃣ **Wprowadzenie liczby (decode\_number)**

* Użytkownik wpisuje liczbę całkowitą.
* Skrypt próbuje konwertować tę wartość do `int`.
* Jeśli jest błąd, użytkownik jest proszony o poprawne podanie liczby.

---

### 4️⃣ **Wybór liczby słów mnemonic (word\_count)**

* Użytkownik wybiera, czy chce mnemonic o długości 12 lub 24 słów.
* Jeśli wybór jest nieprawidłowy, skrypt kończy działanie.

---

### 5️⃣ **Wybór sieci kryptowalutowej (network\_choice)**

* Użytkownik podaje sieć (Bitcoin, Ethereum, Litecoin, Dogecoin, Cardano, Solana).
* Na podstawie wpisu wybierany jest odpowiedni typ monety BIP44 (`Bip44Coins`).
* Jeśli nic nie wpisze, wybierany jest domyślnie Bitcoin.

---

### 6️⃣ **Konwersja liczby na wzorzec binarny**

* Liczba podana przez użytkownika jest konwertowana na ciąg znaków reprezentujący liczbę binarną (np. `8` → `1000`).
* Ten binarny wzorzec steruje, czy dla danej litery hasła używany będzie klucz prywatny czy publiczny (opis poniżej).

---

### 7️⃣ **Generowanie pierwszego mnemonica - "seed 0"**

* Funkcja `text_to_mnemonic(text, word_count)`:

  * Hasło jest kodowane jako UTF-8 i poddawane funkcji SHA256 (`hashlib.sha256`).
  * Wynikowy hash (32 bajty) jest użyty jako entropia do generowania mnemonic:

    * Jeśli 24 słowa → bierzemy 32 bajty hasha,
    * Jeśli 12 słów → bierzemy 16 bajtów hasha.
  * Z entropii generowany jest standardowy mnemonic BIP39 z biblioteki `bip_utils`.

* Ten mnemonic jest **podstawowym seedem bazowym** do dalszej generacji.

---

### 8️⃣ **Tworzenie kontekstu portfela BIP44 z seedu**

* Z mnemonica generowany jest seed binarny (`Bip39SeedGenerator`).
* Seed ten jest używany do inicjalizacji root kontekstu BIP44 dla wybranej sieci (`Bip44.FromSeed(seed, coin)`).

---

### 9️⃣ **Iteracja po znakach hasła i generacja podportfeli**

* Dla każdego znaku `ch` w haśle, na pozycji `i`:

  1. **Wyznaczenie indeksu podportfela**:

     * Indeks = `letter_to_index(ch)` = pozycja litery w alfabecie (a=1, b=2, ..., z=26),
     * Litery są zamieniane na małe, więc `K` i `k` mają ten sam indeks 11.

  2. **Odczyt bitu sterującego z wzorca binarnego:**

     * Jeśli `i < długość wzorca`, to `bin_bit = 0 lub 1` (wartość bitu z pozycji `i` we wzorcu),
     * Jeśli nie ma bitu (indeks poza długością), to `bin_bit = 0`.

  3. **Wybór typu klucza wg bitu:**

     * Jeśli `bin_bit == 0` → pobierany jest **klucz prywatny** (`PrivateKey`),
     * Jeśli `bin_bit == 1` → pobierany jest **adres publiczny** (`PublicKey().ToAddress()`).

  4. **Generowanie podportfela (ścieżka BIP44):**

     * Korzystamy z root kontekstu `root_ctx`,
     * Przechodzimy po ścieżce:
       `m / purpose' / coin_type' / account' / change / address_index`,
       gdzie:

       * `purpose()` i `coin()` są stałe dla sieci,
       * `account()` jest 0,
       * `change()` to `CHAIN_EXT` (zewnętrzny łańcuch),
       * `address_index()` jest równy indeksowi litery (np. 11 dla `k`).

  5. **Generowanie nowego mnemonica z klucza prywatnego lub adresu publicznego:**

     * Jeśli `bin_bit == 0`, pobierany jest klucz prywatny, następnie hex tego klucza jest używany jako nowe "hasło" do funkcji `text_to_mnemonic`,
     * Jeśli `bin_bit == 1`, pobierany jest adres publiczny jako ciąg znaków (string), on jest nowym "hasłem" do `text_to_mnemonic`.

  6. **Aktualizacja root kontekstu:**

     * Z nowego mnemonica generowany jest seed i tworzymy nowy root kontekst BIP44, który jest podstawą do następnego kroku.

---

### 🔟 **Zakończenie i wyświetlenie wyników**

* Po przejściu wszystkich znaków z hasła, wyświetlany jest finalny mnemonic o wybranej długości.

* Generowany jest finalny klucz prywatny i adres publiczny dla indeksu 0 w zmodyfikowanym root kontekście.

* Wszystkie dane są wyświetlane użytkownikowi.

---

### 💾 **Opcjonalne zapisanie wyniku do pliku JSON**

* Jeśli użytkownik wyrazi taką chęć, skrypt zapisuje:

  * Hasło,
  * Liczbę dekodującą,
  * Wzorzec binarny,
  * Szczegóły każdego kroku (znak, indeks, bit, typ klucza, dane entropy, mnemonic),
  * Finalny mnemonic,
  * Wybraną sieć,
  * Ostateczny adres i klucz prywatny.

---

# ✍️ **Podsumowanie ważnych zależności i mechanizmów**

| Element                | Opis                                                                                            |
| ---------------------- | ----------------------------------------------------------------------------------------------- |
| Hasło (case-sensitive) | Jest haszowane dokładnie tak, jak jest wpisane (wielkość liter wpływa na hash i seed 0).        |
| `letter_to_index`      | Indeks liter jest case-insensitive (a=1, z=26), służy do wyboru ścieżki BIP44.                  |
| Wzorzec binarny        | Steruje, czy dany krok używa klucza prywatnego (`0`), czy adresu publicznego (`1`).             |
| Nowy mnemonic          | Za każdym razem tworzony jest z entropy wygenerowanego z klucza lub adresu na poprzednim kroku. |
| Root kontekst BIP44    | Aktualizowany na każdym kroku na podstawie nowo wygenerowanego seed.                            |

---

# 🛠️ **Co musisz zrobić, by odtworzyć skrypt?**

1. Zaimportuj biblioteki `re`, `hashlib`, `json` i `bip_utils` (`Bip39MnemonicGenerator`, `Bip39SeedGenerator`, `Bip44`, `Bip44Coins`, `Bip44Changes`).
2. Zaimplementuj funkcje:

   * `is_english_letters_only` (sprawdzanie liter),
   * `letter_to_index` (pozycja litery a-z),
   * `text_to_mnemonic` (SHA256 haszowanie, generowanie mnemonic z entropii),
   * `select_coin` (wybór sieci na podstawie tekstu),
3. Napisz funkcje wczytujące hasło, liczbę, długość mnemonic i sieć,
4. Przetwarzaj podaną liczbę na binarny wzorzec,
5. Generuj podstawowy mnemonic z hasła,
6. Iteruj po literach hasła, na podstawie wzorca binarnego wybieraj klucz prywatny lub publiczny, generuj nowy mnemonic i root kontekst,
7. Na końcu wyświetl rezultaty i ewentualnie zapisz do pliku JSON.

---

Jasne! Poniżej masz **diagram przepływu** oraz szczegółowy podział skryptu na funkcje — krok po kroku, żeby odtworzyć go idealnie.

---

# 🌊 Diagram przepływu procesu skryptu

```plaintext
Start
  │
  ▼
[Wybierz język (1=EN, 2=PL)]
  │
  ▼
[Wprowadź hasło (litery A-Z/a-z)]
  │
  ├──(walidacja: tylko litery?)──┐
  │                             │
  ▼                             │
[Wprowadź liczbę całkowitą]     │
  │                             │
  ├──(walidacja: liczba?)───────┘
  │
  ▼
[Wybierz długość mnemonic (12 lub 24)]
  │
  ▼
[Wybierz sieć kryptowalutową]
  │
  ▼
[Konwersja liczby na wzorzec binarny]
  │
  ▼
[Generuj seed 0 z hasła → mnemonic]
  │
  ▼
[Ustaw root kontekst BIP44 z seedu]
  │
  ▼
[Iteruj po znakach hasła i dla każdego:]
  │
  ├─> Pobierz indeks litery (1-26)
  │
  ├─> Pobierz bit z wzorca binarnego
  │
  ├─> Jeśli bit == 0: pobierz klucz prywatny
  │     Jeśli bit == 1: pobierz adres publiczny
  │
  ├─> Wygeneruj nowy mnemonic z hex klucza/adresu
  │
  ├─> Z nowego mnemonic generuj nowy root kontekst BIP44
  │
  └─> Przejdź do następnego znaku
  │
  ▼
[Wyświetl finalny mnemonic, adres, klucz prywatny]
  │
  ▼
[Czy zapisać wynik do pliku JSON?]
  │
  ├─> Tak → Zapisz JSON
  │
  └─> Nie → Koniec
  ▼
End
```

---

# 🧩 Szczegółowy podział na funkcje i ich zadania

---

### 1. `choose_language() -> bool`

* Pobiera wybór języka od użytkownika (`1` lub `2`),
* Zwraca `True` jeśli polski, `False` jeśli angielski,
* Wypisuje komunikaty w odpowiednim języku.

---

### 2. `input_password() -> str`

* Pobiera hasło od użytkownika,
* Waliduje, czy zawiera tylko litery angielskie (`is_english_letters_only`),
* Jeśli nie, prosi o powtórne wpisanie,
* Zwraca poprawne hasło.

---

### 3. `input_number() -> int`

* Pobiera liczbę od użytkownika,
* Próbuje konwersji do `int`,
* Jeśli błąd, prosi o poprawę,
* Zwraca poprawną liczbę całkowitą.

---

### 4. `choose_word_count() -> int`

* Pyta o liczbę słów w mnemonic (12 lub 24),
* Jeśli inna wartość, kończy program z komunikatem,
* Zwraca 12 lub 24.

---

### 5. `choose_network() -> Bip44Coins`

* Pyta użytkownika o nazwę sieci (bitcoin, ethereum, itp.),
* Mapuje wpis na odpowiedni enum `Bip44Coins`,
* Jeśli pusty input, domyślnie Bitcoin.

---

### 6. `number_to_binary_pattern(num: int) -> str`

* Konwertuje podaną liczbę do binarnego ciągu znaków (np. 8 → "1000"),
* Zwraca łańcuch znaków binarnych.

---

### 7. `text_to_mnemonic(text: str, word_count: int) -> str`

* Tworzy SHA256 hasz z tekstu,
* Bierze 16 bajtów (dla 12 słów) lub 32 bajty (dla 24 słów) z hash,
* Generuje mnemonic BIP39 z entropii,
* Zwraca mnemonic.

---

### 8. `generate_root_context(mnemonic: str, coin: Bip44Coins) -> Bip44`

* Generuje seed z mnemonic (`Bip39SeedGenerator`),
* Tworzy root kontekst BIP44 z seedu i wybranego coin,
* Zwraca kontekst.

---

### 9. `letter_to_index(ch: str) -> int`

* Zamienia literę na indeks 1-26 (niezależnie od wielkości liter),
* `a` lub `A` → 1, `z` lub `Z` → 26,
* Zwraca indeks.

---

### 10. `process_password_letters(password: str, binary_pattern: str, root_ctx: Bip44, word_count: int) -> (str, Bip44)`

* Dla każdego znaku w haśle:

  * Pobiera indeks litery,
  * Pobiera bit sterujący z wzorca binarnego (0 lub 1),
  * Jeśli bit == 0, generuje mnemonic z klucza prywatnego podportfela,
  * Jeśli bit == 1, generuje mnemonic z adresu publicznego podportfela,
  * Aktualizuje root\_ctx do nowego kontekstu z wygenerowanego mnemonic,

* Zwraca finalny mnemonic i root\_ctx.

---

### 11. `display_results(final_mnemonic: str, root_ctx: Bip44)`

* Generuje klucz prywatny i adres publiczny z root\_ctx (indeks 0),
* Wyświetla mnemonic, adres i klucz prywatny.

---

### 12. `save_to_json(filename: str, data: dict)`

* Zapisuje dane do pliku JSON,
* Dane mogą zawierać: hasło, liczby, wzorce, mnemoniki, adresy, klucze, parametry sieci.

---

# 🔗 **Łączenie funkcji w główny przepływ**

```python
def main():
    use_polish = choose_language()
    password = input_password()
    decode_number = input_number()
    word_count = choose_word_count()
    coin = choose_network()

    binary_pattern = number_to_binary_pattern(decode_number)
    mnemonic0 = text_to_mnemonic(password, word_count)
    root_ctx = generate_root_context(mnemonic0, coin)

    final_mnemonic, final_ctx = process_password_letters(password, binary_pattern, root_ctx, word_count)

    display_results(final_mnemonic, final_ctx)

    if ask_user_save():
        data = collect_all_data(...)  # dane do JSON
        save_to_json("result.json", data)
```
