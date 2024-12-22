import tkinter as tk
from tkinter import messagebox
from pkg.generate import generate_prime
from pkg.checking import trial_division_method, test_ferma
from pkg.ecdsa import create_curve, generate_keys, sign_message, verify_signature


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Главное меню")
        self.root.geometry("400x200")

        # Кнопка для работы с простыми числами
        self.prime_button = tk.Button(
            self.root, text="Работа с простыми числами", command=self.open_prime_menu
        )
        self.prime_button.pack(pady=10)

        # Кнопка для работы с ECDSA
        self.ecdsa_button = tk.Button(
            self.root, text="ECDSA: Подпись и проверка сообщений", command=self.open_ecdsa_windows
        )
        self.ecdsa_button.pack(pady=10)

    def open_prime_menu(self):
        """Открытие окна работы с простыми числами."""
        PrimeMenu(self.root)

    def open_ecdsa_windows(self):
        """Открытие окон взаимодействия двух пользователей."""
        ECDSAUserWindow(self.root, "Пользователь 1")
        ECDSAUserWindow(self.root, "Пользователь 2")


class PrimeMenu:
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

        # Заголовок
        self.label = tk.Label(self.window, text=f"Проверяемое число: {self.number}", font=("Arial", 16))
        self.label.pack(pady=10)

        # Рамка для метода пробных делений
        self.trial_frame = tk.LabelFrame(self.window, text="Метод пробных делений", padx=10, pady=10)
        self.trial_frame.pack(pady=10, fill="x", padx=20)

        self.trial_input = tk.Entry(self.trial_frame)
        self.trial_input.pack(pady=5)
        self.trial_input.insert(0, "25")  # По умолчанию 25 простых чисел

        self.trial_button = tk.Button(self.trial_frame, text="Проверить методом пробных делений", command=self.check_trial_division)
        self.trial_button.pack()

        # Рамка для теста Ферма
        self.ferma_frame = tk.LabelFrame(self.window, text="Тест Ферма", padx=10, pady=10)
        self.ferma_frame.pack(pady=10, fill="x", padx=20)

        self.ferma_inputs = []
        for _ in range(5):  # 5 полей для ввода оснований
            entry = tk.Entry(self.ferma_frame)
            entry.pack(pady=5)
            self.ferma_inputs.append(entry)

        self.ferma_button = tk.Button(self.ferma_frame, text="Проверить тестом Ферма", command=self.check_ferma)
        self.ferma_button.pack()

        # Текстовое поле для вывода результатов
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


class ECDSAUserWindow:
    def __init__(self, root, user_name):
        self.window = tk.Toplevel(root)
        self.window.title(user_name)
        self.window.geometry("500x500")

        self.curve = create_curve()
        self.private_key, self.public_key = generate_keys(self.curve)
        self.received_message = None

        # Генерация ключей
        self.label = tk.Label(self.window, text=f"{user_name}: ECDSA", font=("Arial", 16))
        self.label.pack(pady=10)

        self.keys_output = tk.Text(self.window, height=5, width=60)
        self.keys_output.pack(pady=10)
        self.keys_output.config(state=tk.DISABLED)

        self.generate_keys_button = tk.Button(
            self.window, text="Сгенерировать ключи", command=self.display_keys
        )
        self.generate_keys_button.pack(pady=5)

        # Ввод сообщения
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

        # Получение сообщения
        self.receive_label = tk.Label(self.window, text="Принятое сообщение:")
        self.receive_label.pack(pady=5)

        self.receive_output = tk.Text(self.window, height=5, width=60)
        self.receive_output.pack(pady=5)
        self.receive_output.config(state=tk.DISABLED)

        self.verify_button = tk.Button(
            self.window, text="Проверить подпись", command=self.verify_signature
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

    def sign_message(self):
        """Подписать сообщение."""
        message = self.message_input.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Ошибка", "Введите сообщение для подписи!")
            return

        r, s = sign_message(self.private_key, message, self.curve)
        self.signature_output.config(state=tk.NORMAL)
        self.signature_output.delete(1.0, tk.END)
        self.signature_output.insert(
            tk.END, f"Подпись: r={r}, s={s}"
        )
        self.signature_output.config(state=tk.DISABLED)

    def verify_signature(self):
        """Проверить подпись принятого сообщения."""
        if not self.received_message:
            messagebox.showerror("Ошибка", "Сообщение не получено!")
            return

        message, signature = self.received_message
        is_valid = verify_signature(self.public_key, message, signature, self.curve)
        messagebox.showinfo(
            "Проверка подписи",
            f"Подпись {'действительна' if is_valid else 'недействительна'}!",
        )
