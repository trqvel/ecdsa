import tkinter as tk
from tkinter import messagebox
from pkg.generate import generate_prime
from pkg.checking import trial_division_method, test_ferma


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Генерация и проверка простого числа")
        self.root.geometry("500x300")

        self.last_generated_prime = None

        self.label = tk.Label(self.root, text="Генерация случайного простого числа", font=("Arial", 16))
        self.label.pack(pady=10)

        self.generate_button = tk.Button(self.root, text="Сгенерировать число", command=self.generate_prime)
        self.generate_button.pack(pady=5)

        self.check_button = tk.Button(self.root, text="Проверить число на простоту", command=self.check_prime)
        self.check_button.pack(pady=5)

        self.output_text = tk.Text(self.root, height=5, width=50)
        self.output_text.pack(pady=10)
        self.output_text.config(state=tk.DISABLED)

    def generate_prime(self):
        """Генерация случайного простого числа."""
        start, end, workers = 100000, 999999, 5
        self.last_generated_prime = generate_prime(start, end, workers)

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Случайное простое число: {self.last_generated_prime}")
        self.output_text.config(state=tk.DISABLED)

    def check_prime(self):
        """Проверка числа на простоту."""
        if not self.last_generated_prime:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Сначала сгенерируйте число!")
            self.output_text.config(state=tk.DISABLED)
            return

        self.run_check_window(self.last_generated_prime)

    def run_check_window(self, number):
        """Открывает новое окно для проверки числа."""
        check_window = tk.Toplevel(self.root)
        check_window.title(f"Проверка числа {number}")

        result_text = tk.Text(check_window, height=10, width=30)
        result_text.pack(pady=10)
        result_text.config(state=tk.DISABLED)

        def trial_check():
            try:
                max_primes = int(trial_input.get())
                result = trial_division_method(number, max_primes)
                result_text.config(state=tk.NORMAL)
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, result)
                result_text.config(state=tk.DISABLED)
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Ошибка ввода: {str(e)}")

        def ferma_check():
            try:
                bases = [int(ferma_input[i].get()) for i in range(5)]
                result = test_ferma(number, bases)
                result_text.config(state=tk.NORMAL)
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, result)
                result_text.config(state=tk.DISABLED)
            except ValueError:
                messagebox.showerror("Ошибка", "Ошибка ввода оснований. Введите положительные числа.")

        trial_label = tk.Label(check_window, text="Метод пробных делений:")
        trial_label.pack(pady=5)
        trial_input = tk.Entry(check_window)
        trial_input.pack(pady=5)
        trial_input.insert(0, "1")
        trial_button = tk.Button(check_window, text="Проверить методом пробных делений", command=trial_check)
        trial_button.pack(pady=5)

        ferma_label = tk.Label(check_window, text="Введите основания для теста Ферма (5 шт.):")
        ferma_label.pack(pady=5)

        ferma_input = []
        for i in range(5):
            entry = tk.Entry(check_window)
            entry.pack(pady=5)
            ferma_input.append(entry)

        ferma_button = tk.Button(check_window, text="Проверить тестом Ферма", command=ferma_check)
        ferma_button.pack(pady=5)