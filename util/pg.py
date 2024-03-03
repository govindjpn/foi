import psycopg2 

DSN = 'database = "foi", user = "foi", host = "localhost", password = "foi", port = 5432'
conn = psycopg2.connect(DSN)


def sql_add_file (row) : 
    with conn:
        cur = conn.cursor(buffered=True)
        cur.execute("select max(doc_id) from foi_docs")
        row = cur.fetchone()
        cur.close()
        if row is None or row[0] is None:
            file_num = 1
        else:
            file_num = row[0] + 1
        insert_str = "insert into foi_docs (doc_id, doc_name, page_count, category, summary) values (" \
            + str(file_num) + ', "' + row[0] + '" , ' + str(row[1]), + ', "' + row[2] + '" , "'  + row[3] + '"' \
            + ");"
        cur.execute(insert_str)
        conn.commit()


def sql_get_file (name, user_name) : 
    with conn:
        cur = conn.cursor(buffered=True)
        cur.execute('select doc_id, page_count, category, summary from foi_docs where doc_name = "' \
                    + name + '" and user_name = "' + user_name + '";' )
        row = cur.fetchone()
        if row is None or row[0] is None:
            return None 
        return row
    

def sql_get_all_files (user_name) : 
    with conn:
        cur = conn.cursor(buffered=True)
        cur.execute('select doc_id, page_count, category, summary from foi_docs where user_name = "' + user_name + '";' )
        rows = cur.fetchall()
        if rows is None or rows[0] is None:
            return None 
        return rows
