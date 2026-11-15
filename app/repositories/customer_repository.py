
async def get_customer(customer_id:int,conn):
    async with conn.cursor() as cur:
            
            await cur.execute("SELECT customer_id, first_name, last_name," \
                " email " \
            " FROM customer " \
            "WHERE customer_id = %s",(customer_id,))

            customer = await cur.fetchone()
    
            return customer

async def search_customer(first_name:str | None, last_name:str | None,conn):

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

    async with conn.cursor() as cur:
        await cur.execute(query,(params))
        customer = await cur.fetchall()

        return customer

    
async def get_customers(offset:int | None,limit:int | None ,conn):

    query = "SELECT customer_id, first_name, last_name, email FROM customer " \
        "   ORDER BY customer_id ASC"
   
    params = []
    if offset:
        query += " OFFSET %s"
        params.append(offset)

    if limit:
        query += " LIMIT %s"
        params.append(limit)

    async with conn.cursor() as cur:
        await cur.execute(query,(params))
        customers = await cur.fetchall()

        return customers


async def get_customer_rental_history(customer_id:int,conn):

    async with conn.cursor() as cur:
    
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
    
            await cur.execute(query,(customer_id,))
            customer_history = await cur.fetchall()
            
            return customer_history


async def get_customer_payment_history(customer_id:int,conn):

    query = "SELECT c.customer_id,CONCAT(c.first_name,' ',c.last_name) AS customer_name,"
    query += "r.rental_id,p.payment_id,p.amount,CAST(p.payment_date AS DATE) AS payment_date "
    query += "FROM customer c "
    query += "INNER JOIN rental r "
    query += "ON c.customer_id = r.customer_id "
    query += "INNER JOIN payment p "
    query += "ON r.rental_id = p.rental_id "
    query += "WHERE c.customer_id = %s "
    query += "ORDER BY payment_date"
     
    async with conn.cursor() as cur:
        await cur.execute(query,(customer_id,))

        customer_history = await cur.fetchall()
        return customer_history


async def get_store_ids(conn):

    async with conn.cursor() as cur:
        await cur.execute("SELECT store_id FROM store")

        store_id = await cur.fetchall()
        return store_id


async def get_address_ids(conn):

    async with conn.cursor() as cur:
        await cur.execute("SELECT address_id FROM address")

        address_id = await cur.fetchall()
        return address_id
     

async def add_customer(
        store_id:int,first_name:str,
        last_name:str,email:str,address_id:int,
        conn):

    query = "INSERT INTO customer(store_id,first_name,last_name,email,address_id) "
    query += "VALUES (%s,%s,%s,%s,%s) "
    query += "RETURNING *"

    async with conn.cursor() as cur:

        await cur.execute(query,(store_id,first_name,last_name,
                            email,address_id))
        new_customer = await cur.fetchone()

        return new_customer


async def delete_customer(customer_id:int,conn):
    
    query = "DELETE FROM customer "
    query += "WHERE customer_id = %s"

    async with conn.cursor() as cur:
        await cur.execute(query,(customer_id,))

    