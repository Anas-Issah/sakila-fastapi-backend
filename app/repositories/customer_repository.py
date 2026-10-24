
def get_customer(customer_id:int,conn):
    with conn.cursor() as cur:
            cur.execute("SELECT customer_id, first_name, last_name," \
                " email " \
            " FROM customer " \
            "WHERE customer_id = %s",(customer_id,))
    
            return cur.fetchone()

def search_customer(first_name:str | None, last_name:str | None,conn):

    query = "SELECT customer_id, first_name, last_name, email " 
    query += "FROM customer "
    query += "WHERE "

    params = []

    if first_name:
        params.append(first_name)
        query += "first_name = %s "

    if last_name:
        params.append(last_name)

        if first_name:
            query += "AND last_name = %s" 
        else:
            query += "last_name = %s"

    with conn.cursor() as cur:
        cur.execute(query,(params))

        return cur.fetchall()

    
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


def get_customer_rental_history(customer_id:int,conn):

    with conn.cursor() as cur:
    
            query = "SELECT c.customer_id, CONCAT(c.first_name,' ',c.last_name) AS customer_name, "
            query += "r.rental_id,f.title,CAST(r.rental_date AS DATE) AS rental_date "
            query += "FROM customer c "
            query += "INNER JOIN rental r "
            query += "ON c.customer_id = r.customer_id "
            query += "INNER JOIN inventory i "
            query += "ON r.inventory_id = i.inventory_id "
            query += "INNER JOIN film f "
            query += "ON i.film_id = f.film_id "
            query += "WHERE c.customer_id = %s "
            query += "ORDER BY rental_date"
    
            cur.execute(query,(customer_id,))
    
            return cur.fetchall()


def get_customer_payment_history(customer_id:int,conn):

    query = "SELECT c.customer_id,CONCAT(c.first_name,' ',c.last_name) AS customer_name,"
    query += "r.rental_id,p.payment_id,p.amount,CAST(p.payment_date AS DATE) AS payment_date "
    query += "FROM customer c "
    query += "INNER JOIN rental r "
    query += "ON c.customer_id = r.customer_id "
    query += "INNER JOIN payment p "
    query += "ON r.rental_id = p.rental_id "
    query += "WHERE c.customer_id = %s "
    query += "ORDER BY payment_date"
     
    with conn.cursor() as cur:
        cur.execute(query,(customer_id,))

        return cur.fetchall()

def get_store_ids(conn):

     with conn.cursor() as cur:
        cur.execute("SELECT store_id FROM store")
        
        return cur.fetchall()

def get_address_ids(conn):

     with conn.cursor() as cur:
        cur.execute("SELECT address_id FROM address")
        
        return cur.fetchall()
     

def add_customer(
        store_id,first_name,
        last_name,email,address_id,
        conn):

    query = "INSERT INTO customer(store_id,first_name,last_name,email,address_id) "
    query += "VALUES (%s,%s,%s,%s,%s) "
    query += "RETURNING *"

    with conn.cursor() as cur:

        cur.execute(query,(store_id,first_name,last_name,
                            email,address_id))

        return cur.fetchone()