from flask import Flask, render_template, request, redirect, url_for
from database import db, app, create_db
from models import Item, Transaction

# Ensure the database is created when the app starts
create_db()

@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        quantity = request.form['quantity']
        
        item = Item(name=name, price=price, description=description, quantity=quantity)
        db.session.add(item)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.price = request.form['price']
        item.description = request.form['description']
        item.quantity = request.form['quantity']
        
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('edit_item.html', item=item)

@app.route('/delete_item/<int:item_id>')
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/transactions', methods=['GET', 'POST'])
def transactions():
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = request.form['quantity']
        company_name = request.form['company_name']
        
        transaction = Transaction(item_id=item_id, quantity=quantity, company_name=company_name)
        db.session.add(transaction)
        db.session.commit()
        
        item = Item.query.get(item_id)
        item.quantity -= int(quantity)
        db.session.commit()
        
        return redirect(url_for('transactions'))
    
    items = Item.query.all()
    transactions = Transaction.query.all()
    return render_template('transactions.html', items=items, transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)
