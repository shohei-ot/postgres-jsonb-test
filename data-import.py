import psycopg2
from psycopg2.extras import RealDictCursor
import csv
import json

def main():
    # dryrun = True
    dryrun = False
    # import_stores(dryrun)
    # import_sells(dryrun)

def import_stores(dryrun):
    table_label = '店舗'
    csv_path = './csv/stores.csv'
    import_csv_data(table_label, csv_path, dryrun)

def import_sells(dryrun):
    table_label = '売上'
    csv_path = './csv/sells.csv'
    import_csv_data(table_label, csv_path, dryrun)

def import_csv_data(table_label, csv_path, dryrun=False):
    table = retrieve_table_record(table_label)
    cols = None
    try:
        cols = retrieve_col_records(table['id'])
    except Exception as e:
        print('##### An error occurred:', e)
        print('## table: ' + str(table))
        print('## cols: ' + str(cols))
        raise e
    records = make_records(table, cols, csv_path)
    conn = get_pgsql_conn()
    try:
      with conn:
          conn.autocommit = False
          with conn.cursor() as cursor:
            for record in records:
                insert_record(cursor, 'public.records', record, dryrun)
          conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

def make_records(table, cols, csv_path):
    # print('> called make_records')
    # print('> table: ' + str(table))
    # print('> cols: ' + str(cols))
    # print('> csv_path: ' + str(csv_path))

    records = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for csv_row in reader:

            record = {
                'data': None,
                'table_id': table['id'],
            }

            jsonb_data = {}

            for col in cols:
                col_label = col['label']
                # print('> col_label: ' + str(col_label))

                col_id = col['id']
                jsonb_data[str(col_id)] = {
                    'col_id': col_id,
                    'raw_val': csv_row[col_label],
                    'sys_val': cast_to_data_type(col['data_type'], csv_row[col_label])
                }

            record['data'] = jsonb_data

            records.append(record)

    return records

def cast_to_data_type(data_type, value):
    if data_type == 'string':
        return value
    if data_type == 'integer':
        return int(value)
    else:
        raise Exception(f"Unexpected data_type: {data_type}")

def retrieve_table_record(table_label):
    conn = get_pgsql_conn()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            q = """
            SELECT
              tables.id,
              tables.label
            FROM
              tables
            WHERE
              tables.label = %s;
            """

            curs.execute(q, (table_label,))
            row = curs.fetchone()

            return row

def retrieve_col_records(table_id):
    conn = get_pgsql_conn()
    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as curs:
            q = """
            SELECT
              cols.id,
              cols.label,
              cols.data_type
            FROM
              columns as cols
            LEFT JOIN
              tables
            ON
              cols.table_id = tables.id
            WHERE
              tables.id = %s
            """

            curs.execute(q, (table_id,))

            rows = curs.fetchall()
            # print(rows)

            return rows

def insert_record(cursor, table_name, record, dryrun):
    # print('> called insert_record')
    # print('> table_name: ' + str(table_name))
    # print('> record: ' + str(record))

    cols = list(record.keys())
    # print('> cols: ' + str(cols))
    # print('> len(cols): ' + str(len(cols)))
    placeholders = ", ".join(["%s"] * len(cols))
    vals = [json.dumps(value) if isinstance(value,dict) else value for value in record.values()]
    cols_str = ", ".join(cols)
    # print('> cols_str: ' + cols_str)
    # print('> vals: ' + str(vals))

    q = f"INSERT INTO {table_name} ({cols_str}) VALUES ({placeholders});"

    if dryrun:
        sql_str = cursor.mogrify(q, vals)
        print("> SQL: " + sql_str.decode("utf-8") + "\n")
    else:
        cursor.execute(q, vals)

def get_pgsql_conn():
    conn = psycopg2.connect(host="localhost",database="postgres", user="postgres", password="postgres")
    return conn

if __name__ == '__main__':
    main()