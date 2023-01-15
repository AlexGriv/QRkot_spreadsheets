from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from .validators import check_table_values_size
from .constants import NOW_DATE_TIME, ROW_COUNT, COLUMN_COUNT, TABLE_VALUES


SPREADSHEETS_BODY = dict(
        properties=dict(
            title=f'Отчет от', # noqa
            locale='ru_RU',
        ),
        sheets=[dict(properties=dict(
            sheetType='GRID',
            sheetId=0,
            title='Лист1',
            gridProperties=dict(
                rowCount=ROW_COUNT,
                columnCount=COLUMN_COUNT,
            )
        ))]
    )


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADSHEETS_BODY
    spreadsheet_body['properties']['title'] += NOW_DATE_TIME
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spread_sheet_id = response['spreadsheetId']
    return spread_sheet_id


async def set_user_permissions(
        spread_sheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spread_sheet_id,
            json=permissions_body,
            fields='id'
        ))


async def spreadsheets_update_value(
        spread_sheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover('sheets', 'v4')
    table_values =[
    *[TABLE_VALUES],
    *[list(map(str, project)) for project in projects]
    ]

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    table_values_rows_count = len(table_values)
    table_values_columns_count = len(max(table_values, key=len))
    check_table_values_size(
        table_values_rows_count,
        table_values_columns_count,
        100,
        11
    )
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spread_sheet_id,
            range=(
                f'R1C1:R{table_values_rows_count}'
                f'C{table_values_columns_count}'
            ),
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
