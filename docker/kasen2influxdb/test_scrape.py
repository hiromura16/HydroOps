from main import load_config, get_html_tables, extract_value, convert_to_datetime
import pandas as pd

cfg = load_config('config.json')
df = pd.read_csv(cfg['csv']['path'])

for _, row in df.iterrows():
    tables = get_html_tables(row['url'])
    t_str, val = extract_value(tables, row['table_number'],
                               row['row_position'],
                               row['time_row_position'])
    dt = convert_to_datetime(t_str) if val is not None else None
    print(row['measurement'], row['location'], val, dt)
