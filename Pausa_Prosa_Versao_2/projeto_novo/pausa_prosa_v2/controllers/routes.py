from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models.database import get_products, add_product, toggle_product, create_order, get_orders, update_status
bp=Blueprint('main',__name__)
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        if not session.get('admin'): return redirect(url_for('main.login'))
        return fn(*args,**kwargs)
    return wrapper
@bp.get('/')
def home(): return render_template('index.html', products=get_products())
@bp.post('/pedido')
def order():
    import json
    data={k:request.form.get(k,'').strip() for k in ['customer','phone','address','note']}
    try: items=json.loads(request.form.get('items','[]'))
    except Exception: items=[]
    if not all(data[k] for k in ['customer','phone','address']) or not items:
        flash('Confira seus dados e adicione pelo menos um produto ao carrinho.','error'); return redirect(url_for('main.home'))
    oid=create_order(data,items)
    order_data=next(x for x in get_orders() if x['id']==oid)
    return render_template('confirmation.html', order=order_data)
@bp.get('/login')
def login(): return render_template('login.html')
@bp.post('/login')
def login_post():
    if request.form.get('username')==bp_admin_user() and request.form.get('password')==bp_admin_password():
        session['admin']=True; return redirect(url_for('main.admin'))
    flash('Usuário ou senha incorretos.','error'); return redirect(url_for('main.login'))
def bp_admin_user():
    from flask import current_app
    return current_app.config['ADMIN_USER']
def bp_admin_password():
    from flask import current_app
    return current_app.config['ADMIN_PASSWORD']
@bp.get('/sair')
def logout(): session.clear(); return redirect(url_for('main.home'))
@bp.get('/admin')
@admin_required
def admin():
    search=request.args.get('q','').strip(); status=request.args.get('status','')
    return render_template('admin.html', products=get_products(False), orders=get_orders(search,status), search=search, selected_status=status)
@bp.post('/admin/produto')
@admin_required
def product():
    add_product(request.form['name'],request.form['category'],request.form['description'],float(request.form['price']),request.form.get('icon','☕')); return redirect(url_for('main.admin'))
@bp.post('/admin/produto/<int:pid>/alternar')
@admin_required
def toggle(pid): toggle_product(pid); return redirect(url_for('main.admin'))
@bp.post('/admin/pedido/<int:oid>')
@admin_required
def status(oid): update_status(oid,request.form['status']); return redirect(url_for('main.admin'))
