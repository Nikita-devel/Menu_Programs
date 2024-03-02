import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pandas as pd
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def analyze_gps_data(file_path, average_speed):
    try:
        # Зчитування CSV-файлу
        df = pd.read_csv(file_path, delimiter=';')

        # Розрахунок відстані загального пройденого шляху
        total_distance = df['Distance (m)'].sum()

        # Розрахунок підйому та спуску
        positive_elevation = max(0, df['Altitude (m)'].diff().clip(lower=0).sum())
        negative_elevation = max(0, -df['Altitude (m)'].diff().clip(upper=0).sum())

        # Знайдення максимальної висоти
        max_altitude = df['Altitude (m)'].max()

        # Розрахунок часу подорожі відносно середньої швидкості
        time_of_travel = total_distance / average_speed

        # Розрахунок приблизного витрати калорій
        calories_burned = total_distance * 0.05  # Прикладовий коефіцієнт

        # Виведення результатів
        result_text = f"Distance totale parcourue: {total_distance} m\n"
        result_text += f"Dénivelé positif: {positive_elevation} m\n"
        result_text += f"Dénivelé négatif: {negative_elevation} m\n"
        result_text += f"Altitude maximum: {max_altitude} m\n"
        result_text += f"Temps de parcours à {average_speed} m/s: {time_of_travel} s\n"
        result_text += f"Dépense de calories: {calories_burned} cal"
        
        # Очищення та виведення результатів у текстове поле
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result_text)

        # Виведення графіка висоти
        plot_altitude(df)

    except Exception as e:
        messagebox.showerror("Помилка", f"Помилка при аналізі даних: {str(e)}")

def plot_altitude(df):
    # Створення нового вікна для графіка
    graph_window = tk.Toplevel(root)
    graph_window.title("Графік висоти")

    # Створення графіка висоти
    fig, ax = plt.subplots()
    ax.plot(df['<ваше ім'я стовпця для вісі x>'], df['Altitude (m)'], label='Altitude (m)')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Altitude (m)')
    ax.set_title('Altitude over Time')
    ax.legend()

    # Відображення графіка у GUI
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Функція, яка викликається при натисканні кнопки "Старт"
def start_button_clicked():
    file_path = filedialog.askopenfilename(title="Оберіть файл CSV", filetypes=[("CSV files", "*.csv")])
    if file_path:
        # Вибір швидкості
        speed_window = tk.Toplevel(root)
        speed_window.title("Введіть середню швидкість")

        speed_label = tk.Label(speed_window, text="Введіть середню швидкість (м/с):")
        speed_label.pack(pady=10)

        speed_entry = ttk.Entry(speed_window)
        speed_entry.pack(pady=10)

        def analyze_with_speed():
            speed = float(speed_entry.get())
            analyze_gps_data(file_path, speed)
            speed_window.destroy()

        speed_button = tk.Button(speed_window, text="Аналіз з введеною швидкістю", command=analyze_with_speed)
        speed_button.pack(pady=10)

# Створення головного вікна
root = tk.Tk()
root.title("Аналіз GPS-даних")

# Створення кнопки "Старт"
start_button = tk.Button(root, text="Старт", command=start_button_clicked)
start_button.pack(pady=20)

# Створення текстового поля для виведення результатів
output_text = scrolledtext.ScrolledText(root, width=40, height=15)
output_text.pack(padx=20, pady=20)

# Запуск головного циклу GUI
root.mainloop()
