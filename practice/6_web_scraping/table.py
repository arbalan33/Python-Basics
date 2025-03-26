# %%
from prettytable import PrettyTable, TableStyle

def draw_table(fields, data: list[list[any]], title="Title") -> str:
    table = PrettyTable()
    table.field_names = fields
    table.add_rows(data)

    table.junction_char = '-'
    table.align = 'l'

    table_str = str(table)

    # Strip the top border from table
    table_str = table_str[table_str.find('\n')+1:]
    # Strip the bottom border from table
    table_str = table_str[:table_str.rfind('\n')]

    ## Add title bar
    width = table_str.find('\n')
    title_bar = title.center(width, '=')
    table_str = title_bar + '\n' + table_str

    return table_str
