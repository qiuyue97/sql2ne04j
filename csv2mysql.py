import os
import pandas as pd
from sqlalchemy import create_engine
from tqdm import tqdm
import config
import chardet

# 定义 CSV 文件夹路径
folder_path = 'data20240603'


def create_engine_from_config(config):
    return create_engine(
        f"mysql+mysqlconnector://{config.mysql_config['user']}:{config.mysql_config['password']}@{config.mysql_config['host']}/{config.mysql_config['database']}?auth_plugin=mysql_native_password"
    )


def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(10000))
    return result['encoding']


# 批量插入数据
def insert_chunk_to_db(chunk, table_name, engine):
    with engine.begin() as connection:
        chunk.to_sql(table_name, connection, index=False, if_exists='append')


# 遍历文件夹中的所有 CSV 文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)

        # 检测文件编码
        detected_encoding = detect_encoding(file_path)
        print(f"Detected encoding for {filename}: {detected_encoding}")

        try:
            # 读取 CSV 文件并逐个 chunk 导入数据库
            chunk_size = 1000  # 分块大小
            table_name = os.path.splitext(filename)[0]

            # 创建 SQLAlchemy 引擎
            engine = create_engine_from_config(config)

            reader = pd.read_csv(file_path, encoding=detected_encoding, chunksize=chunk_size, iterator=True,
                                 low_memory=False, encoding_errors='ignore')
            for chunk in tqdm(reader, desc=f"Inserting chunks into {table_name}", unit="chunk"):
                try:
                    insert_chunk_to_db(chunk, table_name, engine)
                except Exception as e:
                    print(f"Error inserting chunk into {table_name}: {e}")

            print(f"CSV 文件 {filename} 数据已成功导入到 MySQL 数据库表 {table_name} 中。")
        except Exception as e:
            print(f"Error reading data from {filename}: {e}")

print("所有 CSV 文件数据已成功导入到 MySQL 数据库表中。")
