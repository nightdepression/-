import random

def create_mappings():
    rus = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    mappings = {}
    for i, char in enumerate(rus):
        variants = [
            (f"{chr(65 + i // 26)}{chr(65 + i % 26)}", "буква + буква"),
            (f"{i // 10}{i % 10}", "цифра + цифра"),
            (f"{i // 26}{chr(65 + i % 26)}", "цифра + буква"),
            (f"{chr(65 + i // 10)}{i % 10}", "буква + цифра")
        ]
        mappings[char] = variants
    return mappings, {code: char for char, variants in mappings.items() for code, _ in variants}

mappings, reverse_mapping = create_mappings()
fixed_mapping = {}

def choose_encryption_mode():
    while True:
        print("\nВыбор режима шифрования:")
        print("1. Случайный (постоянно случайный формат шифрования)")
        print("2. Постоянный (один случайно выбранный режим шифрования, с сохранением формата шифрования)")
        choice = input("Выберите режим (1/2): ")
        if choice in ('1', '2'):
            return choice
        print("Только 1 или 2!")

def init_fixed_mapping():
    for char in mappings:
        fixed_mapping[char] = random.choice(mappings[char])

def encrypt(text, mode):
    encrypted = []
    formats_used = []
    for char in text.lower().replace(' ', ''):
        if char in mappings:
            if mode == '1':
                code, fmt = random.choice(mappings[char])
            else:
                code, fmt = fixed_mapping.get(char, mappings[char][0])
            encrypted.append(code)
            formats_used.append(fmt)
    return ''.join(encrypted), formats_used

def main_loop():
    mode = choose_encryption_mode()
    if mode == '2':
        init_fixed_mapping()

    while True:
        text = input("\nВведите текст для шифрования (или 'выход' для завершения): ").strip().lower()
        if text == 'выход':
            break

        encrypted, formats = encrypt(text, mode)
        decrypted = decrypt(encrypted)

        print(f"\nЗашифрованный текст: {encrypted}")
        print("Использованные форматы:")
        for i, (char, fmt) in enumerate(zip(text.replace(' ', ''), formats)):
            print(f"{char} -> {encrypted[i * 2:i * 2 + 2]} ({fmt})")
        print(f"Расшифрованный текст: {decrypted}\n")

def decrypt(ciphertext):
    decrypted = []
    i = 0
    while i < len(ciphertext):
        for length in [2]:
            if i + length > len(ciphertext):
                continue
            pair = ciphertext[i:i + 2].upper()
            if pair in reverse_mapping:
                decrypted.append(reverse_mapping[pair])
                i += 2
                break
        else:
            i += 1
    return ''.join(decrypted)

if __name__ == "__main__":
    main_loop()