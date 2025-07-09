#!/usr/bin/env python3

import re
import hashlib
import json
from bip_utils import (
    Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39Languages,
    Bip44, Bip44Coins, Bip44Changes
)

def is_english_letters_only(s):
    return re.match("^[a-zA-Z]+$", s) is not None

def letter_to_index(ch):
    return ord(ch.lower()) - ord('a') + 1

def text_to_mnemonic(text, word_count=24):
    hash_bytes = hashlib.sha256(text.encode()).digest()
    entropy = hash_bytes[:32] if word_count == 24 else hash_bytes[:16]
    return Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromEntropy(entropy)

def select_coin(network_choice):
    network_choice = network_choice.strip().lower()
    if network_choice == "bitcoin":
        return Bip44Coins.BITCOIN
    elif network_choice == "ethereum":
        return Bip44Coins.ETHEREUM
    elif network_choice == "litecoin":
        return Bip44Coins.LITECOIN
    elif network_choice == "dogecoin":
        return Bip44Coins.DOGECOIN
    elif network_choice == "cardano":
        return Bip44Coins.CARDANO_ICARUS
    elif network_choice == "solana":
        return Bip44Coins.SOLANA
    else:
        return Bip44Coins.BITCOIN  # Default universal BIP44

def input_password(use_polish):
    while True:
        password = input("🔑 Podaj hasło (tylko litery a-z, A-Z): " if use_polish else "🔑 Enter password (letters only a-z, A-Z): ").strip()
        if is_english_letters_only(password):
            return password
        else:
            print("❌ Hasło może zawierać tylko litery a-z, A-Z!" if use_polish else "❌ Password can contain only letters a-z, A-Z!")

def input_decode_number(use_polish):
    while True:
        try:
            return int(input("🔢 Podaj liczbę do zamiany na binarkę: " if use_polish else "🔢 Enter number to convert to binary: ").strip())
        except ValueError:
            print("❌ Niepoprawna liczba!" if use_polish else "❌ Invalid number!")

def input_network(use_polish):
    msg = (
        "🌐 Na jaką sieć chcesz portfel? (Bitcoin, Ethereum, Solana, Dogecoin, Litecoin, Cardano). ENTER = uniwersalny BIP44 (Bitcoin)"
        if use_polish else
        "🌐 Which network? (Bitcoin, Ethereum, Solana, Dogecoin, Litecoin, Cardano). Press ENTER = universal BIP44 (Bitcoin)"
    )
    return input(msg + ": ").strip()

def main():
    print("🌐 Wybierz język interfejsu / Choose interface language:")
    print("1 → English")
    print("2 → Polski")
    lang_choice = input("✏️ Your choice: / Twój wybór:").strip()

    use_polish = (lang_choice == "2")

    password = input_password(use_polish)
    decode_number = input_decode_number(use_polish)

    try:
        word_count = int(input("📜 Ile słów chcesz? [12/24]: " if use_polish else "📜 How many words? [12/24]: ").strip())
        if word_count not in [12, 24]:
            raise ValueError
    except ValueError:
        print("❌ Dozwolone tylko 12 lub 24." if use_polish else "❌ Allowed only 12 or 24.")
        return

    network_choice = input_network(use_polish)
    coin = select_coin(network_choice)

    save_to_file = input("📁 Zapisać wynik do JSON? [t/N]: " if use_polish else "📁 Save result to JSON? [y/N]: ").strip().lower() in ["t", "y"]

    bin_decode = bin(decode_number)[2:]
    print(f"\n🔢 Binarny wzorzec: {bin_decode}\n" if use_polish else f"\n🔢 Binary pattern: {bin_decode}\n")

    all_data = []
    mnemonic = text_to_mnemonic(password, word_count)
    print(f"[Seed 0] {'Z hasła' if use_polish else 'From password'}: {mnemonic}")

    seed = Bip39SeedGenerator(mnemonic).Generate()
    root_ctx = Bip44.FromSeed(seed, coin)

    for i, ch in enumerate(password):
        index = letter_to_index(ch)
        bin_bit = int(bin_decode[i]) if i < len(bin_decode) else 0

        acc_ctx = root_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(index)

        if bin_bit == 1:
            data = acc_ctx.PublicKey().ToAddress()
            print(f"[{i+1}] '{ch}' → index {index}, bit=1 → {'Adres publiczny' if use_polish else 'Public address'}: {data}")
            source_type = "publiczny" if use_polish else "public"
        else:
            data = acc_ctx.PrivateKey().Raw().ToHex()
            print(f"[{i+1}] '{ch}' → index {index}, bit=0 → {'Klucz prywatny' if use_polish else 'Private key'}: {data}")
            source_type = "prywatny" if use_polish else "private"

        mnemonic = text_to_mnemonic(data, word_count)
        print(f"[Seed {i+1}] {'Z' if use_polish else 'From'} {source_type} {'klucza' if use_polish else 'key'}: {mnemonic}\n")

        seed = Bip39SeedGenerator(mnemonic).Generate()
        root_ctx = Bip44.FromSeed(seed, coin)

        all_data.append({
            "step": i + 1,
            "char": ch,
            "index": index,
            "bit": bin_bit,
            "source_type": source_type,
            "data_used_as_entropy": data,
            "mnemonic": str(mnemonic)
        })

    print(f"✅ {'Ostateczne słowa kluczowe' if use_polish else 'Final mnemonic words'} ({word_count}):")
    print(mnemonic)

    final_ctx = root_ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
    address = final_ctx.PublicKey().ToAddress()
    private_key = final_ctx.PrivateKey().Raw().ToHex()

    print(f"\n🌐 {'Sieć' if use_polish else 'Network'}: {network_choice.capitalize() if network_choice else 'Universal BIP44'}")
    print(f"📬 {'Adres publiczny' if use_polish else 'Public address'}: {address}")
    print(f"🔑 {'Klucz prywatny' if use_polish else 'Private key'}: {private_key}")

    if save_to_file:
        filename = f"wallet_output_{password}_{decode_number}.json"
        with open(filename, "w") as f:
            json.dump({
                "input_password": password,
                "decode_number": decode_number,
                "binary_decode": bin_decode,
                "steps": all_data,
                "final_mnemonic": str(mnemonic),
                "network": network_choice if network_choice else "Universal BIP44",
                "address": address,
                "private_key": private_key
            }, f, indent=4)
        print(f"\n📁 {'Zapisano do' if use_polish else 'Saved to'}: {filename}")

if __name__ == "__main__":
    main()
