
# 🔑 Deterministic Wallet Decoder

**Ten projekt to interaktywny dekoder/generator słów kluczowych (seedów BIP-39) oparty na haśle i liczbie.**
🧠 Pozwala na łatwe zapamiętanie backupu portfela 🔑

---

## ⚙️ Jak to działa?

1️⃣ **Podajesz hasło** – tylko litery a-z/A-Z  
2️⃣ **Podajesz liczbę** – jest konwertowana na wzorzec binarny  
3️⃣ **Skrypt deterministycznie generuje słowa kluczowe (12/24)** – kompatybilne ze standardem [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)  
4️⃣ **Standard BIP-44** – umożliwia użycie w wielu sieciach: Bitcoin, Ethereum, Cardano, Solana, Litecoin, Dogecoin i inne

📌 **Wystarczy zapamiętać hasło i liczbę** → w dowolnym momencie możesz odtworzyć te same seedy!  
📌 **UWAGA**: Jeśli ktoś pozna Twoje hasło i liczbę – ma pełny dostęp do seedów! 
⚠️ Generator jest deterministyczny – nie ma możliwości zmiany słów kluczowych bez zmiany hasła/liczby.

---

## 🧩 Szczegółowy opis działania

### 1️⃣ Wybór języka interfejsu
- Polski lub angielski interfejs.

### 2️⃣ Wprowadzenie hasła
- Hasło to tylko litery a-z/A-Z.
- Każda litera zamieniana jest na numer 1–26.

### 3️⃣ Podanie liczby
- Liczba całkowita konwertowana jest na wzorzec binarny.

### 4️⃣ Liczba słów mnemonic
- Wybierasz 12 lub 24 słowa.

### 5️⃣ Wybór sieci blockchain
- Bitcoin, Ethereum, Solana, Litecoin, Dogecoin, Cardano.
- Domyślnie Bitcoin.

### 6️⃣ Zapis do pliku
- Możesz zapisać wynik do pliku JSON.

### 🔗 Techniczne flow:
1. Hasło → SHA-256 → entropia → mnemonic BIP39.
2. Mnemonic → seed → drzewo BIP44.
3. Każda litera i bit wzorca binarnego wybiera klucz prywatny/publiczny, który jest znowu hashowany i generuje nowy mnemonic.
4. Proces zapętla się – powstaje wielowarstwowy chain.
5. Wynik: finalny mnemonic, seed, klucz prywatny/publiczny.

✅ Deterministyczny – zawsze daje te same wyniki dla tych samych danych wejściowych.  
✅ Kompatybilny z BIP39/BIP44.  
✅ Obsługuje wiele sieci.

---

## 🚨 Bezpieczeństwo

- 🔒 **Nigdy nie udostępniaj swojego hasła i liczby nikomu!**
- 🔑 Seedy są tak bezpieczne, jak Twoje hasło i liczba.
- 📚 Działa z portfelami Ledger, MetaMask, TrustWallet itd.

---

## 🚀 Jak uruchomić?

### 1️⃣ Sklonuj repozytorium

```bash
git clone https://github.com/hattimon/wallet-decoder.git
cd wallet-decoder
```

### 2️⃣ Nadaj prawa wykonywania i zainstaluj zależności

```bash
chmod +x install.sh
./install.sh
```

### 3️⃣ Uruchom generator

```bash
./wallet_generator.py
```

---

## ✨ Autor

Projekt open-source stworzony przez [hattimon](https://github.com/hattimon) 🚀
