from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import get_products, add_product, toggle_product, create_order, get_orders, update_status
bp=Blueprint('main',__name__)
@bp.get('/')
def home(): return render_template('index.html', products=get_products())
@bp.post('/pedido')
def order():
    data={k:request.form.get(k,'').strip() for k in ['customer','phone','address','note']}
    raw=request.form.get('items','[]')
    import json
    items=json.loads(raw)
    if not all(data[k] for k in ['customer','phone','address']) or not items:
        flash('Preencha nome, telefone, endereço e escolha ao menos um item.','error'); return redirect(url_for('main.home'))
    oid=create_order(data,items); flash(f'Pedido #{oid} recebido! Obrigado por escolher a Pausa & Prosa.','success')
    return redirect(url_for('main.home'))
@bp.get('/admin')
def admin(): return render_template('admin.html', products=get_products(False), orders=get_orders())
@bp.post('/admin/produto')
def product():
    add_product(request.form['name'],request.form['category'],request.form['description'],float(request.form['price']),request.form.get('icon','☕')); return redirect(url_for('main.admin'))
@bp.post('/admin/produto/<int:pid>/alternar')
def toggle(pid): toggle_product(pid); return redirect(url_for('main.admin'))
@bp.post('/admin/pedido/<int:oid>')
def status(oid): update_status(oid,request.form['status']); return redirect(url_for('main.admin'))
