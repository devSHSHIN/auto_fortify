import os
import sys
import json
import pymysql
import zipfile
import argparse
import pandas as pd
from ssc_link import get_ssc_link
from archive import zip_files_in_tmp
from to_xlsx import convert_pickle_to_excel

def read_config(config_path):
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config

def read_query(query_path, config, appid):
    with open(query_path, 'r') as f:
        query = f.read()
    query = query.replace(':attrGuid', f"'{config['attrGuid']}'")
    query = query.replace(':appid', appid)
    return query

def connect_to_db(config):
    try:
        connection = pymysql.connect(
                host='localhost',
                user=config['db_id'],
                password=config['db_pw'],
                database=config['db_name'],
                cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Database connection error: {e}")
        sys.exit(1)

def fetch_data(connection, query):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
    return result

def process_data(result, appid, config):
    if not result:
        print("데이터베이스에서 가져온 데이터가 비어 있습니다.")
        sys.exit(1)

    df = pd.DataFrame(result)

    if df.empty:
        print("생성된 데이터프레임이 비어 있습니다.")
        sys.exit(1)

    df.rename(columns={'instance_ID': 'SSC_Link'}, inplace=True)
    df['SSC_Link'] = df.apply(lambda row: get_ssc_link(appid, row['SSC_Link'], config), axis=1)

    return df

def save_to_pickle(df, output_path):
    df.to_pickle(output_path)

def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--appid', required=True, help='')
    args = parser.parse_args()

    config = read_config('config.json')
    query = read_query('query.sql', config, args.appid)
    connection = connect_to_db(config)
    result = fetch_data(connection, query)
    df = process_data(result, args.appid, config)
    
    tmp_dir = '.tmp'
    os.makedirs(tmp_dir, exist_ok=True)
    
    pickle_path = os.path.join(tmp_dir, 'fortify_data.pkl')
    excel_path = os.path.join(tmp_dir, 'output.xlsx')
    fpr_path = os.path.join(tmp_dir, 'output.fpr')
    
    save_to_pickle(df, pickle_path)
    convert_pickle_to_excel(pickle_path, excel_path)
    
    # Assuming the .fpr file is generated somewhere in the process
    # For now, let's create an empty .fpr file for demonstration
    with open(fpr_path, 'w') as f:
        f.write('')

    zip_files_in_tmp('/fortify_ssc/apache-tomcat-9.0.88/webapps/ROOT/reports/report.zip')

    shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    main()