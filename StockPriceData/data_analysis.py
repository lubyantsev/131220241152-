import os


def calculate_and_display_average_price(data):
    """
    Рассчитывает и отображает среднюю цену закрытия акций за указанный период.

    :param data: DataFrame с данными об акциях, должен содержать колонку 'Close'.
    """
    # Проверяем, содержит ли DataFrame данные о закрытии
    if 'Close' in data.columns:
        average_price = data['Close'].mean()
        print(f"Средняя цена закрытия за указанный период: {average_price:.2f}")
    else:
        print("Данные о закрытии отсутствуют.")


def notify_if_strong_fluctuations(data, threshold):
    """
    Проверяет, превышает ли процент колебания цен акций заданный порог, и выводит уведомление.

    :param data: DataFrame с данными об акциях, должен содержать колонку 'Close'.
    :param threshold: Пороговое значение процента колебаний для уведомления.
    """
    # Проверка на None для threshold
    if threshold is None:
        return

    # Проверяем, содержит ли DataFrame данные о закрытии
    if 'Close' in data.columns:
        max_price = data['Close'].max()  # Находим максимальную цену
        min_price = data['Close'].min()  # Находим минимальную цену

        fluctuation = ((max_price - min_price) / min_price) * 100  # Рассчитываем процент колебаний

        # Проверяем, превышает ли колебание заданный порог
        if fluctuation > threshold:
            print(f"Уведомление: Цены акций колебались более чем на {threshold}% за указанный период. "
                  f"Минимальная цена: {min_price:.2f}, Максимальная цена: {max_price:.2f}, "
                  f"Общий процент колебания: {fluctuation:.2f}%")
        else:
            print(f"Цены акций колебались менее чем на {threshold}%. Процент колебания: {fluctuation:.2f}%")
    else:
        print("Данные о закрытии отсутствуют.")


def export_data_to_csv(data, filename):
    """
    Экспортирует данные о ценах акций в CSV файл в папку csv_files.

    :param data: DataFrame с данными об акциях.
    :param filename: Имя файла для сохранения данных.
    """
    # Создаем папку, если она не существует
    os.makedirs('csv_files', exist_ok=True)

    # Полный путь к файлу
    filepath = os.path.join('csv_files', filename)

    try:
        data.to_csv(filepath, index=False)
        print(f"Данные успешно экспортированы в файл: {filepath}")
    except Exception as e:
        print(f"Произошла ошибка при экспорте данных: {e}")
