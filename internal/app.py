import tkinter as tk
from tkinter import messagebox
from pkg.generate import generate_prime
from pkg.checking import trial_division_method, test_ferma
from pkg.ecdsa import create_curve, generate_keys, sign_message, verify_signature
from pkg.encryption import encrypt_message_with_curve
from pkg.decryption import decrypt_message_with_curve


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Главное меню")
        self.root.geometry("400x150")

        self.prime_button = tk.Button(
            self.root, text="Тестирование простых чисел", command=self.open_prime_menu
        )
        self.prime_button.pack(pady=10)

        self.ecdsa_button = tk.Button(
            self.root, text="Подпись и проверка сообщений по протоколу ECDSA", command=self.open_ecdsa_windows
        )
        self.ecdsa_button.pack(pady=10)

    def open_prime_menu(self):
        """Открытие окна работы с простыми числами."""
        PrimeWindow(self.root)

    def open_ecdsa_windows(self):
        """Открытие окон взаимодействия двух пользователей."""
        alice_window = WindowECDSA(self.root, "Alice")
        bob_window = WindowECDSA(self.root, "Bob")

        # Устанавливаем связь между окнами
        alice_window.partner_window = bob_window
        bob_window.partner_window = alice_window


class PrimeWindow:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Работа с простыми числами")
        self.window.geometry("500x300")

        self.last_generated_prime = None

        self.label = tk.Label(
            self.window, text="Генерация случайного простого числа", font=("Arial", 16)
        )
        self.label.pack(pady=10)

        self.generate_button = tk.Button(
            self.window, text="Сгенерировать число", command=self.generate_prime
        )
        self.generate_button.pack(pady=5)

        self.check_button = tk.Button(
            self.window, text="Проверить число на простоту", command=self.open_check_window
        )
        self.check_button.pack(pady=5)

        self.output_text = tk.Text(self.window, height=5, width=60)
        self.output_text.pack(pady=10)
        self.output_text.config(state=tk.DISABLED)

    def generate_prime(self):
        """Генерация случайного простого числа."""
        start, end, workers = 100000, 999999, 5
        self.last_generated_prime = generate_prime(start, end, workers)

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(
            tk.END, f"Случайное простое число: {self.last_generated_prime}"
        )
        self.output_text.config(state=tk.DISABLED)

    def open_check_window(self):
        """Открывает новое окно для проверки простоты числа."""
        if not self.last_generated_prime:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте число!")
            return

        PrimeCheckWindow(self.window, self.last_generated_prime)


class PrimeCheckWindow:
    def __init__(self, root, number):
        self.window = tk.Toplevel(root)
        self.window.title(f"Проверка числа {number}")
        self.window.geometry("750x600")

        self.number = number

        self.label = tk.Label(self.window, text=f"Проверяемое число: {self.number}", font=("Arial", 16))
        self.label.pack(pady=10)

        self.trial_frame = tk.LabelFrame(self.window, text="Метод пробных делений", padx=10, pady=10)
        self.trial_frame.pack(pady=10, fill="x", padx=20)

        self.trial_input = tk.Entry(self.trial_frame)
        self.trial_input.pack(pady=5)
        self.trial_input.insert(0, "1")

        self.trial_button = tk.Button(self.trial_frame, text="Проверить методом пробных делений", command=self.check_trial_division)
        self.trial_button.pack()

        self.ferma_frame = tk.LabelFrame(self.window, text="Тест Ферма", padx=10, pady=10)
        self.ferma_frame.pack(pady=10, fill="x", padx=20)

        self.ferma_inputs = []
        for _ in range(5):
            entry = tk.Entry(self.ferma_frame)
            entry.pack(pady=5)
            self.ferma_inputs.append(entry)

        self.ferma_button = tk.Button(self.ferma_frame, text="Проверить тестом Ферма", command=self.check_ferma)
        self.ferma_button.pack()

        self.result_text = tk.Text(self.window, height=10, width=60)
        self.result_text.pack(pady=10)
        self.result_text.config(state=tk.DISABLED)

    def check_trial_division(self):
        """Проверка методом пробных делений."""
        try:
            max_primes = int(self.trial_input.get())
            result = trial_division_method(self.number, max_primes)
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"Метод пробных делений:\n{result}\n\n")
            self.result_text.config(state=tk.DISABLED)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число для метода пробных делений!")

    def check_ferma(self):
        """Проверка тестом Ферма."""
        try:
            bases = [int(entry.get()) for entry in self.ferma_inputs if entry.get()]
            if not bases:
                raise ValueError
            result = test_ferma(self.number, bases)
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"Тест Ферма:\n{result}\n\n")
            self.result_text.config(state=tk.DISABLED)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные основания для теста Ферма!")


class WindowECDSA:
    def __init__(self, root, user_name):
        self.window = tk.Toplevel(root)
        self.window.title(user_name)
        self.window.geometry("700x700")

        self.curve = create_curve()
        self.private_key, self.public_key = generate_keys(self.curve)
        self.received_message = None

        # Ссылки на другие окна (используются для пересылки)
        self.partner_window = None

        self.label = tk.Label(self.window, text=f"{user_name}: ECDSA", font=("Arial", 16))
        self.label.pack(pady=10)

        self.keys_output = tk.Text(self.window, height=5, width=60)
        self.keys_output.pack(pady=10)
        self.keys_output.config(state=tk.DISABLED)

        self.generate_keys_button = tk.Button(
            self.window, text="Сгенерировать ключи", command=self.display_keys
        )
        self.generate_keys_button.pack(pady=5)

        self.message_label = tk.Label(self.window, text="Сообщение:")
        self.message_label.pack(pady=5)

        self.message_input = tk.Text(self.window, height=3, width=40)
        self.message_input.pack(pady=5)

        self.sign_message_button = tk.Button(
            self.window, text="Подписать и зашифровать сообщение", command=self.sign_and_encrypt_message
        )
        self.sign_message_button.pack(pady=5)

        self.signature_output = tk.Text(self.window, height=3, width=60)
        self.signature_output.pack(pady=10)
        self.signature_output.config(state=tk.DISABLED)

        self.send_button = tk.Button(
            self.window, text="Отправить сообщение", command=self.send_message
        )
        self.send_button.pack(pady=5)

        self.receive_label = tk.Label(self.window, text="Принятое сообщение:")
        self.receive_label.pack(pady=5)

        self.receive_output = tk.Text(self.window, height=5, width=60)
        self.receive_output.pack(pady=5)
        self.receive_output.config(state=tk.DISABLED)

        self.verify_button = tk.Button(
            self.window, text="Проверить подпись и расшифровать", command=self.verify_and_decrypt_message
        )
        self.verify_button.pack(pady=5)

    def display_keys(self):
        """Отображение ключей."""
        self.keys_output.config(state=tk.NORMAL)
        self.keys_output.delete(1.0, tk.END)
        self.keys_output.insert(
            tk.END, f"Приватный ключ: {self.private_key}\nПубличный ключ: {self.public_key}"
        )
        self.keys_output.config(state=tk.DISABLED)

    def sign_and_encrypt_message(self):
        """Подписать и зашифровать сообщение."""
        message = self.message_input.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Ошибка", "Введите сообщение для подписи!")
            return

        # Подпись сообщения
        r, s = sign_message(self.private_key, message, self.curve)
        signature = (r, s)

        # Шифрование сообщения
        encrypted_message = encrypt_message_with_curve(message, self.private_key, self.public_key, self.curve)

        # Отображение зашифрованного сообщения и подписи
        self.signature_output.config(state=tk.NORMAL)
        self.signature_output.delete(1.0, tk.END)
        self.signature_output.insert(
            tk.END, f"Зашифрованное сообщение: {encrypted_message}\nПодпись: r={r}, s={s}"
        )
        self.signature_output.config(state=tk.DISABLED)

        # Сохранение для передачи
        self.received_message = (encrypted_message, signature)

    def send_message(self):
        """Отправить сообщение другому пользователю."""
        if self.partner_window is None:
            messagebox.showerror("Ошибка", "Получатель не подключён!")
            return

        if not self.received_message:
            messagebox.showerror("Ошибка", "Сначала подпишите и зашифруйте сообщение!")
            return

        # Передаём сообщение, подпись и публичный ключ Alice
        self.partner_window.receive_message(self.received_message, self.public_key)

    def receive_message(self, received_message, sender_public_key):
        """Принять сообщение от другого пользователя."""
        self.received_message = received_message
        self.sender_public_key = sender_public_key  # Сохраняем публичный ключ отправителя
        encrypted_message, signature = received_message

        # Отобразить принятое сообщение
        self.receive_output.config(state=tk.NORMAL)
        self.receive_output.delete(1.0, tk.END)
        self.receive_output.insert(
            tk.END, f"Зашифрованное сообщение: {encrypted_message}\nПодпись: {signature}"
        )
        self.receive_output.config(state=tk.DISABLED)

    def verify_and_decrypt_message(self):
        """Проверить подпись и расшифровать сообщение."""
        if not self.received_message:
            messagebox.showerror("Ошибка", "Сообщение не получено!")
            return

        if not hasattr(self, 'sender_public_key'):
            messagebox.showerror("Ошибка", "Публичный ключ отправителя отсутствует!")
            return

        encrypted_message, signature = self.received_message

        # Расшифровка сообщения с использованием приватного ключа Bob
        decrypted_message = decrypt_message_with_curve(
            encrypted_message, self.private_key, self.sender_public_key, self.curve
        )

        # Проверка подписи с использованием публичного ключа Alice
        is_valid = verify_signature(self.sender_public_key, decrypted_message, signature, self.curve)

        # Отображение результата
        self.receive_output.config(state=tk.NORMAL)
        self.receive_output.delete(1.0, tk.END)
        self.receive_output.insert(
            tk.END,
            f"Расшифрованное сообщение: {decrypted_message}\n"
            f"Подпись {'действительна' if is_valid else 'недействительна'}!",
        )
        self.receive_output.config(state=tk.DISABLED)
