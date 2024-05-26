import mysql.connector
from neo4j import GraphDatabase
import config

# 连接 MySQL 数据库
def fetch_data_from_mysql(query):
    mysql_conn = mysql.connector.connect(**config.mysql_config)
    mysql_cursor = mysql_conn.cursor()
    mysql_cursor.execute(query)
    rows = mysql_cursor.fetchall()
    mysql_cursor.close()
    mysql_conn.close()
    return rows


# 连接 Neo4j 数据库并执行
def process_data_for_neo4j(tables):
    neo4j_driver = GraphDatabase.driver(config.neo4j_config['uri'], auth=(config.neo4j_config['user'], config.neo4j_config['password']))
    with neo4j_driver.session() as session:
        for table_name, operations in tables.items():
            query = operations["query"]
            extract_function = operations["extract_function"]
            rows = fetch_data_from_mysql(query)
            session.execute_write(extract_function, rows)
    neo4j_driver.close()


# 定义创建节点和关系的函数
def extractFromCompanyControlPerson(tx, rows):
    for row in rows:
        id, key_no, company_id, oper_key_no, oper_name, node_type, stock_percent = row

        tx.run("""
            MERGE (c:Company {key_no: $key_no})
            ON CREATE SET c.key_no = $key_no, c.company_id = $company_id
            ON MATCH SET c.company_id = COALESCE(c.company_id, $company_id)
        """, key_no=key_no, company_id=company_id)

        if node_type == 'company':
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


def extractFromEciCompany(tx, rows):
    for row in rows:
        key_no, company_id, company_name, oper_key_no, oper_name, province_code, province, address, phone_number = row

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


def extractFromEciEmployee(tx, rows):
    for row in rows:
        id, key_no, company_id, company_name, name, job, p_key_no = row

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

# 定义字典
tables = {
    "t_company_control_person": {
        "query": "SELECT id, key_no, company_id, oper_key_no, oper_name, node_type, stock_percent FROM t_company_control_person",
        "extract_function": extractFromCompanyControlPerson
    },
    "t_eci_company": {
        "query": "SELECT key_no, company_id, company_name, oper_key_no, oper_name, province_code, province, address, phone_number FROM t_eci_company",
        "extract_function": extractFromEciCompany
    },
    "t_eci_employee": {
        "query": "SELECT id, key_no, company_id, company_name, name, job, p_key_no FROM t_eci_employee",
        "extract_function": extractFromEciEmployee
    },
    "t_eci_partner":{
        "query": "SELECT id, key_no, company_id, company_name, stock_name, stock_type, stock_percent, should_capi, p_key_no FROM t_eci_partner",
        "extract_function": extractFromEciPartner
    },
}

process_data_for_neo4j(tables)

print("Nodes and relationships have been created successfully.")
