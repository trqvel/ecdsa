import tkinter as tk
from tkinter import messagebox
import math

# Проверка методом пробных делений
def trial_division_method(number, max_primes):
    if number <= 0:
        raise ValueError("Число для проверки методом пробных делений должно быть натуральным!")
    
    if max_primes <= 0:
        raise ValueError("Введите натуральное число!")
    
    if max_primes > 25:
        raise ValueError("Не могу осуществить проверку с более чем 25 простыми числами!")
    
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    if max_primes < len(primes):
        primes = primes[:max_primes]
    
    for p in primes:
        if number % p == 0:
            return f"Число {number} делится на {p}. Не является простым."
    return f"Число {number} успешно прошло тест пробных делений!"


# Тест Ферма
def test_ferma(number, bases):
    if number <= 0:
        raise ValueError("Число для проверки тестом Ферма должно быть натуральным!")

    if any(b <= 0 for b in bases):
        raise ValueError("Все основания теста Ферма должны быть натуральными!")

    fail_bases = []
    for a in bases:
        if pow(a, number - 1, number) != 1:
            fail_bases.append(a)

    if fail_bases:
        return f"Число {number} не прошло тест Ферма для оснований: {fail_bases}"
    else:
        return f"Число {number} прошло тест Ферма для всех оснований!"


def run_check_window(number):
    def check_trial():
        try:
            max_primes = int(trial_input.get())
            result = trial_division_method(number, max_primes)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result)
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Ошибка ввода: {str(e)}")

    def check_ferma():
        try:
            bases = [int(ferma_input[i].get()) for i in range(5)]
            result = test_ferma(number, bases)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result)
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Ошибка ввода: {str(e)}")

    window = tk.Tk()
    window.title("Проверка простоты числа")

    label_number = tk.Label(window, text=f"Проверяемое число: {number}", font=("Arial", 16))
    label_number.pack(pady=10)

    frame_trial = tk.LabelFrame(window, text="Метод пробных делений", padx=10, pady=10)
    frame_trial.pack(pady=10, fill="x", padx=20)

    trial_input = tk.Entry(frame_trial)
    trial_input.pack(pady=5)
    trial_input.insert(0, "25")

    trial_button = tk.Button(frame_trial, text="Проверить методом пробных делений", command=check_trial)
    trial_button.pack()

    frame_ferma = tk.LabelFrame(window, text="Тест Ферма", padx=10, pady=10)
    frame_ferma.pack(pady=10, fill="x", padx=20)

    ferma_label = tk.Label(frame_ferma, text="Впишите основания (по одному в каждое поле):")
    ferma_label.pack(pady=5)

    ferma_input = []
    for i in range(5):
        entry = tk.Entry(frame_ferma)
        entry.pack(pady=5)
        ferma_input.append(entry)

    ferma_button = tk.Button(frame_ferma, text="Проверить тестом Ферма", command=check_ferma)
    ferma_button.pack()

    result_text = tk.Text(window, height=5, width=40)
    result_text.pack(pady=20)
    result_text.config(state=tk.DISABLED)

    window.mainloop()
