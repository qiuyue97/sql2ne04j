import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
from neo4j import GraphDatabase
import sys
import config


# 自定义进度条
def print_progress_bar(iteration, total, prefix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {iteration} / {total}')
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
def fetch_data_from_mysql(columns, table_name, batch_size=1000, fetch_size=0):
    offset = 0
    total_rows_fetched = 0
    try:
        mysql_conn = mysql.connector.connect(**config.mysql_config)
        mysql_cursor = mysql_conn.cursor()
        total_rows = get_total_rows(table_name)
        if total_rows is None:
            return
        while True:
            limit = batch_size
            if fetch_size > 0:
                remaining_rows = fetch_size - total_rows_fetched
                if remaining_rows <= 0:
                    break
                limit = min(batch_size, remaining_rows)
            query = f"SELECT {', '.join(columns)} FROM {table_name} LIMIT {limit} OFFSET {offset}"
            mysql_cursor.execute(query)
            rows = mysql_cursor.fetchall()
            if not rows:
                break
            total_rows_fetched += len(rows)
            offset += limit
            yield rows, total_rows
        mysql_cursor.close()
        mysql_conn.close()
    except Exception as e:
        print(f"MySQL connection error: {e}")
        if mysql_cursor:
            mysql_cursor.close()
        if mysql_conn:
            mysql_conn.close()


# 连接 Neo4j 数据库并执行
def process_data_for_neo4j(tables, fetch_size=0):
    neo4j_driver = GraphDatabase.driver(config.neo4j_config['uri'], auth=(config.neo4j_config['user'], config.neo4j_config['password']))
    with neo4j_driver.session() as session:
        create_indexes(session)
        for table_name, operations in tables.items():
            columns = operations["columns"]
            extract_function = operations["extract_function"]
            total_rows = get_total_rows(table_name)
            if total_rows is None:
                continue
            processed_rows = 0
            for chunk, _ in fetch_data_from_mysql(columns, table_name, batch_size=1000, fetch_size=fetch_size):
                batch = [dict(zip(columns, row)) for row in chunk]
                session.execute_write(extract_function, batch)
                processed_rows += len(batch)
                print_progress_bar(processed_rows, total_rows, prefix=f'Processing {table_name}', length=50)
        session.execute_write(createSuspectedRelatedRelationships)
    neo4j_driver.close()


# 定义创建节点和关系的函数
def extractFromCompanyControlPerson(tx, rows):
    tx.run("""
        UNWIND $rows AS row
        FOREACH (ignoreMe IN CASE WHEN row.key_no IS NOT NULL THEN [1] ELSE [] END |
            MERGE (c:Company {company_id: row.company_id})
            ON CREATE SET c.company_id = row.company_id, c.key_no = row.key_no, c.name = row.company_name, c.create_from = 't_company_control_person'
            ON MATCH SET c.key_no = COALESCE(c.key_no, row.key_no), c.name = COALESCE(c.name, row.company_name)
            FOREACH (ignoreMe2 IN CASE WHEN row.oper_key_no IS NOT NULL THEN [1] ELSE [] END |
                FOREACH (ignoreMe3 IN CASE WHEN row.node_type = 'ep' THEN [1] ELSE [] END |
                    MERGE (c1:Company {name: row.oper_name})
                    ON CREATE SET c1.name = row.oper_name, c1.key_no = row.oper_key_no, c1.create_from = 't_company_control_person'
                    ON MATCH SET c1.key_no = COALESCE(c1.key_no, row.oper_key_no)
                    MERGE (c1)-[:actual_control {stock_percent: row.stock_percent}]->(c)
                )
                FOREACH (ignoreMe3 IN CASE WHEN row.node_type = 'person' THEN [1] ELSE [] END |
                    MERGE (p:Person {key_no: row.oper_key_no})
                    ON CREATE SET p.key_no = row.oper_key_no, p.name = row.oper_name
                    ON MATCH SET p.name = COALESCE(p.name, row.oper_name)
                    MERGE (p)-[:actual_control {stock_percent: row.stock_percent}]->(c)
                )
            )
        )
    """, rows=rows)


def extractFromEciCompany(tx, rows):
    tx.run("""
        UNWIND $rows AS row
        FOREACH (ignoreMe IN CASE WHEN row.key_no IS NOT NULL THEN [1] ELSE [] END |
            MERGE (c:Company {company_id: row.company_id})
            ON CREATE SET c.company_id = row.company_id, c.key_no = row.key_no, c.name = row.company_name, c.address = row.address, c.phone_number = row.phone_number, c.province = row.province, c.create_from = 't_eci_company'
            ON MATCH SET c.key_no = COALESCE(c.key_no, row.key_no), c.name = COALESCE(c.name, row.company_name), c.address = COALESCE(c.address, row.address), c.phone_number = COALESCE(c.phone_number, row.phone_number), c.province = COALESCE(c.province, row.province)
            FOREACH (ignoreMe2 IN CASE WHEN row.oper_key_no IS NOT NULL AND row.oper_name <> "无" THEN [1] ELSE [] END |
                MERGE (p:Person {key_no: row.oper_key_no})
                ON CREATE SET p.key_no = row.oper_key_no, p.name = row.oper_name
                ON MATCH SET p.name = COALESCE(p.name, row.oper_name)
                MERGE (c)-[:legal_rep]->(p)
            )
        )
    """, rows=rows)


def extractFromEciEmployee(tx, rows):
    tx.run("""
        UNWIND $rows AS row
        FOREACH (ignoreMe IN CASE WHEN row.key_no IS NOT NULL THEN [1] ELSE [] END |
            MERGE (c:Company {company_id: row.company_id})
            ON CREATE SET c.company_id = row.company_id, c.key_no = row.key_no, c.name = row.company_name, c.create_from = 'zs_t_eci_employee'
            ON MATCH SET c.key_no = COALESCE(c.key_no, row.key_no), c.name = COALESCE(c.name, row.company_name)
            FOREACH (ignoreMe2 IN CASE WHEN row.p_key_no IS NOT NULL AND row.name <> "无" AND row.job IS NOT NULL THEN [1] ELSE [] END |
                MERGE (p:Person {key_no: row.p_key_no})
                ON CREATE SET p.key_no = row.p_key_no, p.name = row.name
                ON MATCH SET p.name = COALESCE(p.name, row.name)
                MERGE (c)-[:employee {job: row.job}]->(p)
            )
        )
    """, rows=rows)


def extractFromEciPartner(tx, rows):
    tx.run("""
        UNWIND $rows AS row
        WITH row,
            CASE WHEN row.stock_percent IS NULL THEN 'unknown' ELSE row.stock_percent END AS stock_percent,
            CASE WHEN row.should_capi IS NULL THEN 'unknown' ELSE row.should_capi END AS should_capi
        FOREACH (ignoreMe IN CASE WHEN row.key_no IS NOT NULL THEN [1] ELSE [] END |
            MERGE (c:Company {company_id: row.company_id})
            ON CREATE SET c.company_id = row.company_id, c.key_no = row.key_no, c.name = row.company_name, c.create_from = 't_eci_partner'
            ON MATCH SET c.key_no = COALESCE(c.key_no, row.key_no), c.name = COALESCE(c.name, row.company_name)
            FOREACH (ignoreMe2 IN CASE WHEN row.p_key_no IS NOT NULL THEN [1] ELSE [] END |
                FOREACH (ignoreMe3 IN CASE WHEN row.stock_type = '企业股东' THEN [1] ELSE [] END |
                    MERGE (c1:Company {name: row.stock_name})
                    ON CREATE SET c1.name = row.stock_name, c1.key_no = row.p_key_no, c1.create_from = 't_eci_partner'
                    ON MATCH SET c1.key_no = COALESCE(c1.key_no, row.p_key_no)
                    MERGE (c1)-[:has_stake {stock_percent: stock_percent, should_capi: should_capi}]->(c)
                )
                FOREACH (ignoreMe3 IN CASE WHEN row.stock_type = '自然人股东' THEN [1] ELSE [] END |
                    MERGE (p:Person {key_no: row.p_key_no})
                    ON CREATE SET p.key_no = row.p_key_no, p.name = row.stock_name
                    ON MATCH SET p.name = COALESCE(p.name, row.stock_name)
                    MERGE (p)-[:has_stake {stock_percent: stock_percent, should_capi: should_capi}]->(c)
                )
            )
        )
    """, rows=rows)


def extractFromEciBranch(tx, rows):
    tx.run("""
        UNWIND $rows AS row
        FOREACH (ignoreMe IN CASE WHEN row.key_no IS NOT NULL THEN [1] ELSE [] END |
            MERGE (c:Company {name: row.company_name})
            ON CREATE SET c.name = row.company_name, c.company_id = row.company_id, c.key_no = row.key_no, c.create_from = 't_eci_branch'
            ON MATCH SET c.key_no = COALESCE(c.key_no, row.key_no), c.company_id = COALESCE(c.company_id, row.company_id)
            FOREACH (ignoreMe2 IN CASE WHEN row.sub_key_no IS NOT NULL THEN [1] ELSE [] END |
                MERGE (c2:Company {name: row.name})
                ON CREATE SET c2.name = row.name, c2.company_id = row.sub_company_id, c2.key_no = row.sub_key_no, c2.create_from = 't_eci_branch'
                ON MATCH SET c2.key_no = COALESCE(c2.key_no, row.sub_key_no), c2.company_id = COALESCE(c2.company_id, row.sub_company_id)
                MERGE (c)-[:has_branch]->(c2)
            )
        )
    """, rows=rows)


def extractFromBiddingBaseinfo(tx, rows):
    tx.run("""
        UNWIND $rows AS row
        WITH row,
            CASE WHEN row.winBidPrice IS NULL OR row.winBidPrice = 'NaN' THEN 'unknown' ELSE row.winBidPrice END AS winBidPrice
        FOREACH (ignoreMe IN CASE WHEN row.wintendererCompanyId IS NOT NULL AND row.winTenderer IS NOT NULL AND row.tendereeCompanyId IS NOT NULL AND row.tenderee IS NOT NULL THEN [1] ELSE [] END |
            MERGE (c1:Company {name: row.winTenderer})
            ON CREATE SET c1.name = row.winTenderer, c1.company_id = row.wintendererCompanyId, c1.create_from = 't_company_bidding_attr_info'
            ON MATCH SET c1.company_id = COALESCE(c1.company_id, row.wintendererCompanyId)
            FOREACH (ignoreMe2 IN CASE WHEN row.tendereeCompanyId IS NOT NULL THEN [1] ELSE [] END |
                MERGE (c2:Company {name: row.tenderee})
                ON CREATE SET c2.name = row.tenderee, c2.company_id = row.tendereeCompanyId, c2.create_from = 't_company_bidding_attr_info'
                ON MATCH SET c2.company_id = COALESCE(c2.company_id, row.tendereeCompanyId)
                MERGE (c1)-[r:supplier]->(c2)
                ON CREATE SET r.pageTime = row.pageTime, r.winBidPrice = winBidPrice
                ON MATCH SET r.pageTime = CASE WHEN r.pageTime < row.pageTime THEN row.pageTime ELSE r.pageTime END,
                              r.winBidPrice = CASE WHEN r.pageTime < row.pageTime THEN winBidPrice ELSE r.winBidPrice END
            )
        )
    """, rows=rows)


def create_indexes(session):
    indexes = [
        "CREATE INDEX IF NOT EXISTS FOR (c:Company) ON (c.key_no)",
        "CREATE INDEX IF NOT EXISTS FOR (c:Company) ON (c.company_id)",
        "CREATE INDEX IF NOT EXISTS FOR (c:Company) ON (c.name)",
        "CREATE INDEX IF NOT EXISTS FOR (p:Person) ON (p.key_no)"
    ]
    for index in indexes:
        session.run(index)
    print("Indexes created.")


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
    "t_company_control_person": {
        "columns": ["key_no", "company_id", "company_name", "oper_key_no", "oper_name", "node_type", "stock_percent"],
        "extract_function": extractFromCompanyControlPerson
    },
    "t_eci_company": {
        "columns": ["key_no", "company_id", "company_name", "oper_key_no", "oper_name", "province", "address", "phone_number"],
        "extract_function": extractFromEciCompany
    },
    "zs_t_eci_employee": {
        "columns": ["key_no", "company_id", "company_name", "name", "job", "p_key_no"],
        "extract_function": extractFromEciEmployee
    },
    "t_eci_partner": {
        "columns": ["key_no", "company_id", "company_name", "stock_name", "stock_type", "stock_percent", "should_capi", "p_key_no"],
        "extract_function": extractFromEciPartner
    },
    "t_eci_branch": {
        "columns": ["key_no", "company_id", "company_name", "sub_key_no", "sub_company_id", "name"],
        "extract_function": extractFromEciBranch
    },
    "t_company_bidding_attr_info": {
        "columns": ["pageTime", "winBidPrice", "winTenderer", "wintendererCompanyId", "tenderee", "tendereeCompanyId"],
        "extract_function": extractFromBiddingBaseinfo
    },
}

process_data_for_neo4j(tables, fetch_size=0)

print("Nodes and relationships have been created successfully.")
