import matplotlib.pyplot as plt
import data_download as dd
import data_plotting as dplt
from data_analysis import calculate_and_display_average_price, notify_if_strong_fluctuations, export_data_to_csv

def main():
    """
    Основная функция, управляющая процессом загрузки, обработки и визуализации данных о биржевых акциях.

    Функция выполняет следующие действия:
    1. Приветствует пользователя и предоставляет информацию о доступных тикерах и периодах.
    2. Запрашивает ввод тикера акции и периода для получения данных.
    3. Запрашивает порог для уведомления о колебаниях цен.
    4. Загружает данные о выбранной акции за указанный период.
    5. Добавляет скользящее среднее к загруженным данным.
    6. Строит и сохраняет график цен закрытия и скользящих средних.
    7. Рассчитывает и отображает среднюю цену закрытия, индекс относительной силы (RSI), MACD и сигнальную линию.
    8. Уведомляет пользователя о сильных колебаниях цен, если они превышают заданный порог.
    """
    try:
        print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
        print(
            "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")

        while True:
            try:
                ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ").strip().upper()
                if ticker == "":
                    print("Тикер не может быть пустым. Пожалуйста, введите корректный тикер.")
                elif not dd.is_valid_ticker(ticker):
                    print("Некорректный тикер. Пожалуйста, введите действительный тикер.")
                else:
                    break
            except Exception as e:
                print(f"Произошла ошибка: {e}. Пожалуйста, попробуйте снова.")

        print(
            "Общие периоды времени для данных о записях включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5л, 10л, с начала года, макс.")

        # Запрос выбора периода
        use_custom_dates = input("Хотите использовать конкретные даты начала и окончания? (да/нет): ")

        if use_custom_dates.lower() == 'да':
            start_date = input("Введите дату начала в формате YYYY-MM-DD: ")
            end_date = input("Введите дату окончания в формате YYYY-MM-DD: ")
            period = None  # Период не нужен, если используются конкретные даты
        else:
            period = input("Введите период для данных (например, '1mo' для одного месяца): ")
            start_date = None  # Параметры дат остаются пустыми
            end_date = None

        # Запрос стиля графика
        known_styles = [
            'seaborn-v0_8', 'seaborn-v0_8-whitegrid', 'ggplot',
            'fivethirtyeight', 'bmh', 'dark_background', 'fast',
            'classic', 'Solarize_Light2'
        ]

        print("Доступные стили графика:")
        available_styles = [style for style in plt.style.available if style in known_styles]

        # Вывод доступных стилей в одну строку
        print(", ".join(f"{i + 1}: {style}" for i, style in enumerate(available_styles)))

        # Запрос стиля с использованием номера
        while True:
            try:
                style_index = int(input("Выберите номер стиля графика из доступных: ")) - 1
                if 0 <= style_index < len(available_styles):
                    style = available_styles[style_index]
                    plt.style.use(style)
                    break
                else:
                    print("Недопустимый номер. Пожалуйста, выберите номер из списка.")
            except ValueError:
                plt.style.use('classic')
                print("Ошибка ввода. Установлен стиль 'classic'.")
                break

        # Запрос порога колебаний
        threshold_input = input("Введите порог для уведомления о колебаниях (в процентах): ")

        # Проверка на пустую строку
        if threshold_input.strip() == "":
            print("Вы не ввели запрашиваемый порог в процентах, уведомления не будет.")
            threshold = None  # Устанавливаем порог в None, если пользователь не ввёл значение
        else:
            threshold = float(threshold_input)  # Преобразуем введённое значение в число

        # Загружаем данные о выбранной акции
        try:
            stock_data = dd.fetch_stock_data(ticker, period, start_date, end_date)
        except Exception as e:
            print(f"Не удалось загрузить данные для тикера {ticker}: {e}")
            return  # Завершаем выполнение функции

        # Добавляем скользящее среднее к данным
        stock_data = dd.add_moving_average(stock_data)

        # Уведомляем о сильных колебаниях
        notify_if_strong_fluctuations(stock_data, threshold)

        # Рассчитываем и отображаем среднюю цену
        calculate_and_display_average_price(stock_data)

        # Экспорт данных в CSV
        export_filename = input("Введите имя файла для экспорта данных (например, 'stock_data.csv'): ")
        if export_filename.strip():
            export_data_to_csv(stock_data, export_filename)
        else:
            print("Соответствующий файл не был создан.")

        # Строим и сохраняем график
        filename = f"{ticker}_{start_date}_to_{end_date}.png" if use_custom_dates.lower() == 'да' else f"{ticker}_{period}.png"
        dplt.create_and_save_plot(stock_data, ticker, period, filename, style)

    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()