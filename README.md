
# 🔑 Deterministic Wallet Decoder

**Ten projekt to prosty dekoder/generator słów kluczowych (seedów BIP-39) oparty na haśle i liczbie binarnej.**

---

## ⚙️ Jak to działa?

1️⃣ **Podajesz hasło** – tylko litery a-z/A-Z  
2️⃣ **Podajesz liczbę** – jest konwertowana na wzorzec binarny  
3️⃣ **Skrypt deterministycznie generuje słowa kluczowe (12/24)** – kompatybilne ze standardem [BIP-39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)  
4️⃣ **Standard BIP-44** – umożliwia użycie w wielu sieciach: Bitcoin, Ethereum, Cardano, Solana i inne

📌 **Wystarczy zapamiętać hasło i liczbę** → w dowolnym momencie możesz odtworzyć te same seedy!  
📌 **UWAGA**: Jeśli ktoś pozna Twoje hasło i liczbę – ma pełny dostęp do seedów! Generator jest deterministyczny – nie ma możliwości zmiany słów kluczowych bez zmiany hasła/liczby.

---

## 🚨 Bezpieczeństwo

- 🔒 **Nigdy nie udostępniaj swojego hasła i liczby nikomu!**
- 🔑 Twoje seedy są tak bezpieczne, jak Twoje hasło i liczba!
- 📚 Skrypt zgodny z BIP-39/BIP-44 – możesz używać seedów w portfelach takich jak Ledger, MetaMask, TrustWallet itp.

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
