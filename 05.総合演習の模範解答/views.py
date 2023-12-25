from flask import render_template,request,session,abort,redirect,flash
from flask.json import JSONEncoder
from flask_login import login_required,login_user, logout_user

from config import app, login_manager
from models import Product,User,Category, UserManager, ProductManager, CategoryManager
from forms import ProductForm,CategoryForm,LoginForm, SearchForm

user_manager = UserManager(app.config['DATABASE_URI'])
product_manager = ProductManager(app.config['DATABASE_URI'])
category_manager = CategoryManager(app.config['DATABASE_URI'])

#ログイン用のユーザ取得
@login_manager.user_loader
def load_user(user_id):
    if user_id != "None":
        user_data = user_manager.get_user_one(user_id)
        user = User(user_data[1],user_data[2],user_data[3],user_data[4])
        return user

class MyJSONEncoder(JSONEncoder):
    """
    JSON Encoder
    """
    def default(self, obj):
        if isinstance(obj, Product):
            return {
                'id':obj.id,
                'name': obj.name,
                'price': obj.price,
                'category_id': obj.category_id,
            }
        elif isinstance(obj, Category):
            return {
                'id':obj.id,
                'name': obj.name,
            }
        return super(MyJSONEncoder, self).default(obj)

app.json_encoder = MyJSONEncoder

#メインメニュー
@app.route('/')
@login_required
def index():
    return render_template('index.html')

#ログイン判定
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_data = user_manager.get_user_one(form.id.data)
        user = User(user_data[1],user_data[2],user_data[3],user_data[4])
        user.id = user_data[0]
        if user is not None:
            if user.password == form.password.data:
                login_user(user, False)
                next = request.args.get('next')
                return redirect(next or "/")
        flash('ユーザ、パスワードが間違っています')
    return render_template('auth/login.html',form=form, login=False)

#ログアウト処理
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/product/list',methods=['GET','POST'])
@login_required
def product_list():
    '''
    商品一覧
    '''
    form = SearchForm()

    if request.method == 'POST':
        if form.name.data != "":
            # 商品名が指定されて絞り込みボタンが押された場合
            search_str = form.name.data
            session['last_search'] = search_str    # 絞り込み文字列をsessionへ
            # products = Product.query.filter(Product.name.like('%' + search_str + '%')).all()
            products = product_manager.get_product_all(" product.name LIKE '%" + form.name.data + "%'")
        else:
            # Price 昇順/降順が押された場合
            # または商品名がクリアされて絞り込みボタンが押された場合
            search_str = session.get('last_search', None) # 前回の絞り込み文字があれば取り出す
            if 'asc' in request.form:
                if search_str:
                    # 前回の絞り込みあり、Price昇順
                    products = product_manager.get_product_all(" product.name LIKE '%" + search_str + "%'",
                                                                 " product.price ASC")
                    form.name.data = search_str
                else:
                    # 前回の絞り込みなし、Price昇順
                    products = product_manager.get_product_all(None, " product.price ASC")
            elif 'desc' in request.form:
                if search_str:
                    # 前回の絞り込みあり、Price降順
                    products = product_manager.get_product_all(" product.name LIKE '%" + search_str + "%'",
                                                                 " product.price DESC")
                    form.name.data = search_str
                else:
                    # 前回の絞り込みなし、Price降順
                    products = product_manager.get_product_all(None, " product.price DESC")
            else:
                # 商品名クリア
                search_str = session.pop('last_search', None) # session['last_search'] 削除
                products = product_manager.get_product_all()
    else:  # 'GET'
        session.pop('last_search', None) # last_search が session に残っていたら消す
        products = product_manager.get_product_all()

    return render_template('product_list.html',form=form, products=products)

@app.route('/product/add',methods=['GET','POST'])
@login_required
def product_add():
    '''
    商品登録処理
    '''
    form = ProductForm()
    categories = category_manager.get_category_all()
    form.category.choices = [(cat[0], cat[1]) for cat in categories]

    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            price = form.price.data
            category_id = form.category.data

            category = category_manager.get_category_one(category_id)

            product = Product(name, price, category_id)
            session['product'] = product
            return render_template('product_add_confirm.html', product=product, category_name=category[1])
             
    # 'GET' or validate error
    return render_template('product_add.html', form=form)

@app.route('/product_add_done')
@login_required
def product_add_done():
    '''
    商品登録終了
    '''
    product_dict = session.get('product')
    if not product_dict:
        abort(400)
    product =Product(product_dict.get('name'),
                     product_dict.get('price'),
                     product_dict.get('category_id'))
    product_manager.add_product(product)
    category = category_manager.get_category_one(product.category_id)
    product.category_name = category[1]

    session.pop('product',None) #セッションクリア
    return render_template('product_add_done.html',product=product)

@app.route('/product/delete/<int:id>')
@login_required
def product_delete(id=None):
    '''
    商品削除
    '''
    if not id:
        abort(400)

    product = list(product_manager.get_product_one(id))
    category = category_manager.get_category_one(product[3])
    product.append(category[1])

    return render_template('product_delete_confirm.html',product=product)

@app.route('/product/delete_done/<int:id>')
@login_required
def product_delete_done(id=None):
    '''
    商品削除完了
    '''
    if not id:
        abort(400)

    product_manager.delete_product(id)

    return render_template('product_delete_done.html')

@app.route('/product/update/<int:id>',methods=['GET','POST'])
@login_required
def product_update(id=None):
    '''
    商品更新
    '''
    if not id:
        abort(400)

    form = ProductForm()
    categories = category_manager.get_category_all()

    form.category.choices = [(cat[0], cat[1]) for cat in categories]
    
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            price = form.price.data
            category_id = form.category.data

            category = category_manager.get_category_one(category_id)
            category_name = category[1]

            product = Product(name, price, category_id)
            session['product'] = product
            return render_template('product_update_confirm.html', product=product, category_name=category_name)

    # 'GET' or vaildate error
    product = product_manager.get_product_one(id)
    form.name.data = product[1]
    form.price.data = product[2]
    session['product_id'] = product[0]

    return render_template('product_update.html' , form=form)

@app.route('/product/update_done')
@login_required
def product_update_done():
    '''
    商品更新完了
    '''
    product_dict = session.get('product')
    id = session.get('product_id')
    if not product_dict:
        abort(400)

    product = Product(product_dict.get('name'),
                product_dict.get('price'),
                product_dict.get('category_id'))
    product.id = id

    product_manager.update_product(product)

    category = category_manager.get_category_one(product_dict.get('category_id'))
    product.category_name = category[1]

    session.pop('product',None) #セッションクリア
    session.pop('product_id',None)

    return render_template('product_update_done.html',product=product)


@app.route('/category/list',methods=['GET','POST'])
@login_required
def category_list():
    '''
    カテゴリー一覧
    '''
    categorys = category_manager.get_category_all()

    return render_template('category_list.html',categorys=categorys)

@app.route('/category/add',methods=['GET','POST'])
@login_required
def category_add():
    '''
    カテゴリー登録処理
    '''
    form = CategoryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data

            category = Category(name)
            session['category'] = category
            return render_template('category_add_confirm.html', category=category)

    return render_template('category_add.html', form=form)

@app.route('/category_add_done')
@login_required
def category_add_done():
    '''
    カテゴリー登録終了
    '''
    category_dict = session.get('category')
    if not category_dict:
        abort(400)
    category =Category(category_dict.get('name'))

    category_manager.add_category(category)

    session.pop('category',None) #セッションクリア
    return render_template('category_add_done.html',category=category)

@app.route('/category/delete/<int:id>')
@login_required
def category_delete(id=None):
    '''
    カテゴリー削除
    '''
    if not id:
        abort(400)

    category = category_manager.get_category_one(id)

    return render_template('category_delete_confirm.html',category=category)

@app.route('/category/delete_done/<int:id>')
@login_required
def category_delete_done(id=None):
    '''
    カテゴリー削除完了
    '''
    if not id:
        abort(400)

    category_manager.delete_category(id)

    return render_template('category_delete_done.html')

@app.route('/category/update/<int:id>',methods=['GET','POST'])
@login_required
def category_update(id=None):
    '''
    カテゴリー更新
    '''
    if not id:
        abort(400)

    form = CategoryForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            category = Category(name)
            session['category'] = category
            return render_template('category_update_confirm.html', category=category)

    # 'GET' or validation error
    category = category_manager.get_category_one(id)
    form.name.data = category[1]
    session['category_id'] = category[0]
    return render_template('category_update.html' , form=form)

@app.route('/category/update_done')
@login_required
def category_update_done():
    '''
    カテゴリー更新完了
    '''
    category_dict = session.get('category')
    id = session.get('category_id')
    if not category_dict:
        abort(400)

    category =Category(category_dict.get('name'))
    category.id = id
    category_manager.update_category(category)

    session.pop('category',None) #セッションクリア
    session.pop('category_id',None)

    return render_template('category_update_done.html',category=category)
