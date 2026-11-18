import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "pausa_prosa.db"

def connect():
    DB_PATH.parent.mkdir(exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con

def init_db():
    with connect() as con:
        con.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, category TEXT NOT NULL, description TEXT NOT NULL,
            price REAL NOT NULL, icon TEXT NOT NULL DEFAULT '☕', active INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT NOT NULL, phone TEXT NOT NULL, address TEXT NOT NULL,
            note TEXT DEFAULT '', subtotal REAL NOT NULL, delivery REAL NOT NULL,
            total REAL NOT NULL, status TEXT NOT NULL DEFAULT 'Recebido',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT, order_id INTEGER NOT NULL,
            product_id INTEGER, product_name TEXT NOT NULL, unit_price REAL NOT NULL,
            quantity INTEGER NOT NULL, FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE SET NULL
        );
        """)
        if con.execute('SELECT COUNT(*) FROM products').fetchone()[0] == 0:
            products = [
              ('Latte de baunilha','Cafés','Espresso, leite vaporizado e baunilha.',14.00,'☕'),
              ('Coado da casa','Cafés','Café filtrado em pequenos lotes.',8.50,'🫖'),
              ('Chocolate quente','Bebidas','Chocolate cremoso com leite.',13.00,'🍫'),
              ('Chá de frutas vermelhas','Bebidas','Infusão aromática servida quente ou fria.',10.00,'🍓'),
              ('Pão de queijo','Salgados','Porção quentinha com queijo meia cura.',9.00,'🧀'),
              ('Tostada caprese','Salgados','Pão artesanal, tomate, queijo e manjericão.',18.00,'🥪'),
              ('Bolo de limão','Doces','Fatia de bolo macio com cobertura cítrica.',11.00,'🍰'),
              ('Cookie de chocolate','Doces','Cookie artesanal com gotas de chocolate.',8.00,'🍪')]
            con.executemany('INSERT INTO products(name,category,description,price,icon) VALUES(?,?,?,?,?)', products)

def get_products(active_only=True):
    with connect() as con:
        sql='SELECT * FROM products' + (' WHERE active=1' if active_only else '') + ' ORDER BY category,name'
        return con.execute(sql).fetchall()

def add_product(name, category, description, price, icon):
    with connect() as con:
        con.execute('INSERT INTO products(name,category,description,price,icon) VALUES(?,?,?,?,?)',(name,category,description,price,icon))

def toggle_product(pid):
    with connect() as con:
        con.execute('UPDATE products SET active=CASE active WHEN 1 THEN 0 ELSE 1 END WHERE id=?',(pid,))

def create_order(data, items):
    delivery=5.0
    subtotal=sum(float(i['price'])*int(i['quantity']) for i in items)
    with connect() as con:
        cur=con.execute('INSERT INTO orders(customer,phone,address,note,subtotal,delivery,total) VALUES(?,?,?,?,?,?,?)',
          (data['customer'],data['phone'],data['address'],data.get('note',''),subtotal,delivery,subtotal+delivery))
        oid=cur.lastrowid
        con.executemany('INSERT INTO order_items(order_id,product_id,product_name,unit_price,quantity) VALUES(?,?,?,?,?)',
          [(oid,i.get('id'),i['name'],float(i['price']),int(i['quantity'])) for i in items])
        return oid

def get_orders(search='', status=''):
    with connect() as con:
        sql='SELECT * FROM orders WHERE 1=1'; args=[]
        if search:
            sql += ' AND (customer LIKE ? OR CAST(id AS TEXT) LIKE ?)'; args += [f'%{search}%',f'%{search}%']
        if status:
            sql += ' AND status=?'; args.append(status)
        sql += ' ORDER BY id DESC'
        rows=con.execute(sql,args).fetchall()
        result=[]
        for r in rows:
            d=dict(r); d['items']=[dict(x) for x in con.execute('SELECT * FROM order_items WHERE order_id=?',(r['id'],)).fetchall()]; result.append(d)
        return result

def update_status(oid,status):
    with connect() as con:
        con.execute('UPDATE orders SET status=? WHERE id=?',(status,oid))
