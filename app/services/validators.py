from fastapi import HTTPException


def check_table_values_size(
        table_values_rows_count: int,
        table_values_columns_count: int,
        row_count: int,
        column_count: int
) -> None:
    if table_values_rows_count > row_count:
        raise HTTPException(
            status_code=400,
            detail=(
                f'Количество добавляемых строк данных {table_values_rows_count} '
                f'больше количества строк таблицы {row_count}!'
            ),
        )
    if table_values_columns_count > column_count:
        raise HTTPException(
            status_code=400,
            detail=(
                f'Количество добавляемых столбцов данных {table_values_columns_count} '
                f'больше количества столбцов таблицы {column_count}!'
            ),
        )
