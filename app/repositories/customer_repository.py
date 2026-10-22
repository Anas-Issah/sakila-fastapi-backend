
def get_customer(customer_id:int,conn):
    with conn.cursor() as cur:
            cur.execute("SELECT customer_id, first_name, last_name," \
                " email " \
            " FROM customer " \
            "WHERE customer_id = %s",(customer_id,))
    
            return cur.fetchone()



def get_customers(offset:int | None,limit:int | None ,conn):

    query = "SELECT customer_id, first_name, last_name, email FROM customer " \
        "   ORDER BY customer_id ASC"
   
    params = []
    if offset:
        query += " OFFSET %s"
        params.append(offset)

    if limit:
        query += " LIMIT %s"
        params.append(limit)

    with conn.cursor() as cur:
        cur.execute(query,(params))

        return cur.fetchall()

    