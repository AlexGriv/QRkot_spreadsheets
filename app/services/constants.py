from datetime import datetime


FORMAT = '%Y/%m/%d %H:%M:%S'
NOW_DATE_TIME = datetime.now().strftime(FORMAT)
TABLE_VALUES = [
        ['Отчет от', NOW_DATE_TIME],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
MIN_LENGTH=1
MAX_LENGTH=100
ROW_COUNT = 100
COLUMN_COUNT = 11
