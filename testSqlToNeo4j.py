import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
from neo4j import GraphDatabase
import sys
import config


# 自定义进度条
def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}')
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()

# 获取表的总行数
def get_total_rows(table_name):
    try:
        mysql_conn = mysql.connector.connect(**config.mysql_config)
        mysql_cursor = mysql_conn.cursor()
        count_query = f"SELECT COUNT(*) FROM {table_name}"
        mysql_cursor.execute(count_query)
        total_rows = mysql_cursor.fetchone()[0]
        mysql_cursor.close()
        mysql_conn.close()
        return total_rows
    except mysql.connector.Error as e:
        print(f"Error fetching total rows for table {table_name}: {e}")
        return None

# 连接 MySQL 数据库并逐段读取数据
def fetch_data_from_mysql(query, table_name, chunksize=10000):
    while True:
        try:
            engine = create_engine(
                f"mysql+mysqlconnector://{config.mysql_config['user']}:{config.mysql_config['password']}@{config.mysql_config['host']}/{config.mysql_config['database']}?auth_plugin=mysql_native_password"
            )

            total_rows = get_total_rows(table_name)
            if total_rows is None:
                break

            for chunk in pd.read_sql_query(query, engine, chunksize=chunksize):
                yield chunk, total_rows

            break
        except Exception as e:
            print(f"MySQL connection error: {e}, retrying...")
            continue

# 连接 Neo4j 数据库并执行
def process_data_for_neo4j(tables):
    neo4j_driver = GraphDatabase.driver(config.neo4j_config['uri'], auth=(config.neo4j_config['user'], config.neo4j_config['password']))
    with neo4j_driver.session() as session:
        for table_name, operations in tables.items():
            query = operations["query"]
            extract_function = operations["extract_function"]

            total_rows = get_total_rows(table_name)
            if total_rows is None:
                continue

            processed_rows = 0
            for chunk, _ in fetch_data_from_mysql(query, table_name):
                for index, row in chunk.iterrows():
                    session.execute_write(extract_function, row)
                    processed_rows += 1
                    print_progress_bar(processed_rows, total_rows, prefix=f'Processing {table_name}', suffix='Complete', length=50)
        session.execute_write(createSuspectedRelatedRelationships)
    neo4j_driver.close()


# 定义创建节点和关系的函数
def extractFromCompanyControlPerson(tx, row):
    _, key_no, company_id, company_name, oper_key_no, oper_name, node_type, stock_percent = row
    if oper_key_no != None and oper_name != "无":
        tx.run("""
            MERGE (c:Company {key_no: $key_no})
            ON CREATE SET c.key_no = $key_no, c.company_id = $company_id, c.name = $company_name
            ON MATCH SET c.company_id = COALESCE(c.company_id, $company_id), c.name = COALESCE(c.company_name, $company_name)
        """, key_no=key_no, company_id=company_id, company_name=company_name)

        if node_type == 'ep':
            tx.run("""
                MERGE (c1:Company {key_no: $oper_key_no})
                ON CREATE SET c1.key_no = $oper_key_no, c1.name = $oper_name
                ON MATCH SET c1.name = COALESCE(c1.name, $oper_name)
                WITH c1
                MATCH (c2:Company {key_no: $key_no})
                MERGE (c1)-[:actual_control {stock_percent: $stock_percent}]->(c2)
            """, oper_key_no=oper_key_no, oper_name=oper_name, key_no=key_no, stock_percent=stock_percent)
        elif node_type == 'person':
            tx.run("""
                MERGE (p:Person {key_no: $oper_key_no})
                ON CREATE SET p.key_no = $oper_key_no, p.name = $oper_name
                ON MATCH SET p.name = COALESCE(p.name, $oper_name)
                WITH p
                MATCH (c:Company {key_no: $key_no})
                MERGE (p)-[:actual_control {stock_percent: $stock_percent}]->(c)
            """, oper_key_no=oper_key_no, oper_name=oper_name, key_no=key_no, stock_percent=stock_percent)


def extractFromEciCompany(tx, row):
    key_no, company_id, company_name, oper_key_no, oper_name, province_code, province, address, phone_number = row
    if oper_key_no != None and oper_name != "无":
        tx.run("""
            MERGE (c:Company {key_no: $key_no})
            ON CREATE SET c.key_no = $key_no, c.company_id = $company_id, c.name = $company_name, c.address = $address, c.phone_number = $phone_number
            ON MATCH SET c.company_id = COALESCE(c.company_id, $company_id), c.name = COALESCE(c.name, $company_name), c.address = COALESCE(c.address, $address), c.phone_number = COALESCE(c.phone_number, $phone_number)
        """, key_no=key_no, company_id=company_id, company_name=company_name, address=address, phone_number=phone_number)
        tx.run("""
            MERGE (p:Person {key_no: $oper_key_no})
            ON CREATE SET p.key_no = $oper_key_no, p.name = $oper_name
            ON MATCH SET p.name = COALESCE(p.name, $oper_name)
            WITH p
            MATCH (c:Company {key_no: $key_no})
            MERGE (c)-[:legal_rep]->(p)
        """, oper_key_no=oper_key_no, oper_name=oper_name, key_no=key_no)
        tx.run("""
            MERGE (p:Province {code: $province_code})
            ON CREATE SET p.code = $province_code, p.name = $province
            ON MATCH SET p.name = COALESCE(p.name, $province)
            WITH p
            MATCH (c:Company {key_no: $key_no})
            MERGE (c)-[:located_at]->(p)
        """, province_code=province_code, province=province, key_no=key_no)


def extractFromEciEmployee(tx, row):
    id, key_no, company_id, company_name, name, job, p_key_no = row
    if p_key_no != None and name != "无" and job != None:
        tx.run("""
            MERGE (c:Company {key_no: $key_no})
            ON CREATE SET c.key_no = $key_no, c.company_id = $company_id, c.name = $company_name
            ON MATCH SET c.company_id = COALESCE(c.company_id, $company_id), c.name = COALESCE(c.name, $company_name)
        """, key_no=key_no, company_id=company_id, company_name=company_name)
        tx.run("""
            MERGE (p:Person {key_no: $p_key_no})
            ON CREATE SET p.key_no = $p_key_no, p.name = $name
            ON MATCH SET p.name = COALESCE(p.name, $name)
            WITH p
            MATCH (c:Company {key_no: $key_no})
            MERGE (c)-[:employee {job: $job}]->(p)
        """, p_key_no=p_key_no, name=name, key_no=key_no, job=job)


def extractFromEciPartner(tx, rows):
    for row in rows:
        id, key_no, company_id, company_name, stock_name, stock_type, stock_percent, should_capi, p_key_no = row

        tx.run("""
            MERGE (c:Company {key_no: $key_no})
            ON CREATE SET c.key_no = $key_no, c.company_id = $company_id, c.name = $company_name
            ON MATCH SET c.company_id = COALESCE(c.company_id, $company_id), c.name = COALESCE(c.name, $company_name)
        """, key_no=key_no, company_id=company_id, company_name=company_name)

        if stock_type == 'company':
            tx.run("""
                MERGE (c1:Company {key_no: $p_key_no})
                ON CREATE SET c1.key_no = $p_key_no, c1.name = $stock_name
                ON MATCH SET c1.name = COALESCE(c1.name, $stock_name)
                WITH c1
                MATCH (c2:Company {key_no: $key_no})
                MERGE (c1)-[:has_stake {stock_percent: $stock_percent, should_capi: $should_capi}]->(c2)
            """, p_key_no=p_key_no, stock_name=stock_name, key_no=key_no, stock_percent=stock_percent, should_capi=should_capi)
        elif stock_type == 'person':
            tx.run("""
                MERGE (p:Person {key_no: $p_key_no})
                ON CREATE SET p.key_no = $p_key_no, p.name = $stock_name
                ON MATCH SET p.name = COALESCE(p.name, $stock_name)
                WITH p
                MATCH (c:Company {key_no: $key_no})
                MERGE (p)-[:has_stake {stock_percent: $stock_percent, should_capi: $should_capi}]->(c)
            """, p_key_no=p_key_no, stock_name=stock_name, key_no=key_no, stock_percent=stock_percent, should_capi=should_capi)


def extractFromEciBranch(tx, rows):
    for row in rows:
        id, key_no, company_id, company_name, sub_key_no, sub_company_id, name = row

        tx.run("""
            MERGE (c:Company {key_no: $key_no})
            ON CREATE SET c.key_no = $key_no, c.company_id = $company_id, c.name = $company_name
            ON MATCH SET c.company_id = COALESCE(c.company_id, $company_id), c.name = COALESCE(c.name, $company_name)
        """, key_no=key_no, company_id=company_id, company_name=company_name)

        tx.run("""
            MERGE (c:Company {key_no: $sub_key_no})
            ON CREATE SET c.key_no = $sub_key_no, c.company_id = $sub_company_id, c.name = $name
            ON MATCH SET c.company_id = COALESCE(c.company_id, $sub_company_id), c.name = COALESCE(c.name, $name)
            WITH c
            MATCH (c2:Company {key_no: $key_no})
            MERGE (c2)-[:has_branch]->(c)
        """, sub_key_no=sub_key_no, sub_company_id=sub_company_id, name=name, key_no=key_no)


def extractFromBiddingBaseinfo(tx, rows):
    for row in rows:
        pageTime, winBidPrice, winTenderer, tenderee = row

        tx.run("""
            MERGE (c1:Company {name: $winTenderer})
            WITH c1
            MATCH (c2:Company {name: $tenderee})
            MERGE (c1)-[:supplier {pageTime: $pageTime, winBidPrice: $winBidPrice}]->(c2)
        """, winTenderer=winTenderer, tenderee=tenderee, pageTime=pageTime, winBidPrice=winBidPrice)


def createSuspectedRelatedRelationships(tx):
    tx.run("""
        // 建立相同地址的关系
        MATCH (c1:Company), (c2:Company)
        WHERE c1.address IS NOT NULL AND c1.address = c2.address AND id(c1) < id(c2)
        MERGE (c1)-[r:suspected_related {reason: 'same_address'}]->(c2)
    """)
    tx.run("""
        // 建立相同电话号码的关系
        MATCH (c1:Company), (c2:Company)
        WHERE c1.phone_number IS NOT NULL AND c1.phone_number = c2.phone_number AND id(c1) < id(c2)
        MERGE (c1)-[r:suspected_related {reason: 'same_phone_number'}]->(c2)
    """)


# 定义字典
tables = {
    # "t_company_control_person": {
    #     "query": "SELECT id, key_no, company_id, company_name, oper_key_no, oper_name, node_type, stock_percent FROM t_company_control_person",
    #     "extract_function": extractFromCompanyControlPerson
    # },
    # "t_eci_company": {
    #     "query": "SELECT key_no, company_id, company_name, oper_key_no, oper_name, province_code, province, address, phone_number FROM t_eci_company",
    #     "extract_function": extractFromEciCompany
    # },
    "zs_t_eci_employee": {
        "query": "SELECT id, key_no, company_id, company_name, name, job, p_key_no FROM zs_t_eci_employee",
        "extract_function": extractFromEciEmployee
    },
    # "t_eci_partner":{
    #     "query": "SELECT id, key_no, company_id, company_name, stock_name, stock_type, stock_percent, should_capi, p_key_no FROM t_eci_partner",
    #     "extract_function": extractFromEciPartner
    # },
    # "t_eci_branch": {
    #     "query": "SELECT id, key_no, company_id, company_name, sub_key_no, sub_company_id, name FROM t_eci_branch",
    #     "extract_function": extractFromEciBranch
    # },
    # "t_bidding_baseinfo": {
    #     "query": "SELECT pageTime, winBidPrice, winTenderer, tenderee FROM t_bidding_baseinfo",
    #     "extract_function": extractFromBiddingBaseinfo
    # }
}

process_data_for_neo4j(tables)

print("Nodes and relationships have been created successfully.")
