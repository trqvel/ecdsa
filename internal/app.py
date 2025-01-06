import tkinter as tk
from tkinter import messagebox
from pkg.prime.generate import generate_prime
from pkg.prime.checking import trial_division_method, test_miller_rabin
from pkg.ecdsa.ecdsa import create_curve, generate_keys, sign_message, verify_signature


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Главное меню")
        self.root.geometry("400x125")

        self.prime_button = tk.Button(
            self.root, text="Тестирование простых чисел", command=self.open_prime_menu
        )
        self.prime_button.pack(pady=10)

        self.ecdsa_button = tk.Button(
            self.root, text="Подпись и проверка сообщений по протоколу ECDSA", command=self.open_ecdsa_windows
        )
        self.ecdsa_button.pack(pady=10)

    def open_prime_menu(self):
        PrimeWindow(self.root)

    def open_ecdsa_windows(self):
        alice_window = WindowECDSA(self.root, "Alice")
        bob_window = WindowECDSA(self.root, "Bob")

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
        self.last_generated_prime = generate_prime()

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(
            tk.END, f"Случайное простое число: {self.last_generated_prime}"
        )
        self.output_text.config(state=tk.DISABLED)

    def open_check_window(self):
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

        self.label = tk.Label(
            self.window, text=f"Проверяемое число: {self.number}", font=("Arial", 16)
        )
        self.label.pack(pady=10)

        self.trial_frame = tk.LabelFrame(self.window, text="Метод пробных делений", padx=10, pady=10)
        self.trial_frame.pack(pady=10, fill="x", padx=20)

        self.trial_input = tk.Entry(self.trial_frame)
        self.trial_input.pack(pady=5)
        self.trial_input.insert(0, "1")

        self.trial_button = tk.Button(
            self.trial_frame,
            text="Проверить методом пробных делений",
            command=self.check_trial_division
        )
        self.trial_button.pack()

        self.mr_frame = tk.LabelFrame(self.window, text="Тест Миллера-Рабина", padx=10, pady=10)
        self.mr_frame.pack(pady=10, fill="x", padx=20)

        self.mr_input = tk.Entry(self.mr_frame)
        self.mr_input.pack(pady=5)
        self.mr_input.insert(0, "1")

        self.mr_button = tk.Button(
            self.mr_frame,
            text="Проверить тестом Миллера-Рабина",
            command=self.check_mr
        )
        self.mr_button.pack()

        self.result_text = tk.Text(self.window, height=10, width=60)
        self.result_text.pack(pady=10)
        self.result_text.config(state=tk.DISABLED)

    def check_trial_division(self):
        try:
            max_primes = int(self.trial_input.get())
            result = trial_division_method(self.number, max_primes)
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"Метод пробных делений:\n{result}\n\n")
            self.result_text.config(state=tk.DISABLED)
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")

    def check_mr(self):
        try:
            k = int(self.mr_input.get())
            result = test_miller_rabin(self.number, k)
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"Тест Миллера-Рабина:\n{result}\n\n")
            self.result_text.config(state=tk.DISABLED)
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Ошибка: {str(e)}")


class WindowECDSA:
    def __init__(self, root, user_name):
        self.window = tk.Toplevel(root)
        self.window.title(user_name)
        self.window.geometry("700x700")

        self.curve = create_curve()
        self.private_key, self.public_key = generate_keys(self.curve)
        self.received_message = None
        self.partner_window = None

        self.label = tk.Label(self.window, text=f"{user_name}", font=("Arial", 16))
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
            self.window, text="Подписать сообщение", command=self.sign_message
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
            self.window, text="Проверить подпись", command=self.verify_message
        )
        self.verify_button.pack(pady=5)

    def display_keys(self):
        self.keys_output.config(state=tk.NORMAL)
        self.keys_output.delete(1.0, tk.END)
        self.keys_output.insert(
            tk.END, f"Приватный ключ: {self.private_key}\nПубличный ключ: {self.public_key}"
        )
        self.keys_output.config(state=tk.DISABLED)

    def sign_message(self):
        message = self.message_input.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Ошибка", "Введите сообщение для подписи!")
            return

        r, s = sign_message(self.private_key, message, self.curve)
        signature = (r, s)

        self.signature_output.config(state=tk.NORMAL)
        self.signature_output.delete(1.0, tk.END)
        self.signature_output.insert(
            tk.END, f"Подпись: r={r}, s={s}"
        )
        self.signature_output.config(state=tk.DISABLED)
        self.received_message = (message, signature)

    def send_message(self):
        if not self.partner_window:
            messagebox.showerror("Ошибка", "Получатель не подключён!")
            return

        if not self.received_message:
            messagebox.showerror("Ошибка", "Сначала подпишите сообщение!")
            return

        self.partner_window.receive_message(self.received_message, self.public_key)

    def receive_message(self, received_message, sender_public_key):
        self.received_message = received_message
        self.sender_public_key = sender_public_key
        message, signature = received_message

        self.receive_output.config(state=tk.NORMAL)
        self.receive_output.delete(1.0, tk.END)
        self.receive_output.insert(
            tk.END, f"Полученное сообщение: {message}\nПодпись: {signature}"
        )
        self.receive_output.config(state=tk.DISABLED)

    def verify_message(self):
        if not self.received_message:
            messagebox.showerror("Ошибка", "Сообщение не получено!")
            return

        if not hasattr(self, 'sender_public_key'):
            messagebox.showerror("Ошибка", "Публичный ключ отправителя отсутствует!")
            return

        message, signature = self.received_message
        r, s = signature

        is_valid = verify_signature(self.sender_public_key, message, (r, s), self.curve)

        self.receive_output.config(state=tk.NORMAL)
        self.receive_output.delete(1.0, tk.END)
        self.receive_output.insert(
            tk.END,
            f"Полученное сообщение: {message}\n"
            f"Подпись {'действительна' if is_valid else 'недействительна'}!"
        )
        self.receive_output.config(state=tk.DISABLED)