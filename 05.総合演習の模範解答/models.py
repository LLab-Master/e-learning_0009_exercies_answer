from flask.json import JSONEncoder
from flask_login import UserMixin
import sqlite3

#ユーザクラス
class User(UserMixin):
    id = None
    name = None
    password = None
    age = None
    address = None

    def __init__(self, name=None, password=None, age=None, address=None):
        self.name = name
        self.password = password
        self.age = age
        self.address = address


class Product():

    id = None
    name = None
    price = None
    category_id = None

    def __init__(self, name, price, category_id):
        self.name = name
        self.price = price
        self.category_id = category_id

class Category():
    id = None
    name = None
    products = None

    def __init__(self, name):
        self.name = name

#DBにアクセスしユーザデータを取得するクラス
class UserManager:

    def __init__(self,dbfilename):
        self.dbfilename = dbfilename

    '''
    ユーザ1件取得
    '''
    def get_user_one(self, id):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        sql = "select * from user WHERE id = " + str(id)
        cur.execute(sql)
        
        user = cur.fetchone()
        con.close()

        return user


#DBにアクセスし商品データを取得、追加、更新、削除するクラス
class ProductManager:

    def __init__(self,dbfilename):
        self.dbfilename = dbfilename

    '''
    商品全件取得(条件つけ、ソートも可能)
    '''
    def get_product_all(self, where=None, order_by=None):
        product_list = []

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        # カテゴリ名も取得する
        sql = "select product.id, product.name, product.price, product.category_id, category.name  from product INNER JOIN category ON product.category_id = category.id";

        if where is not None:
            sql += " WHERE " + where

        if order_by is not None:
            sql += " ORDER BY " + order_by

        cur.execute(sql)
        
        product_list = cur.fetchall()

        con.close()

        return product_list

    '''
    商品1件取得
    '''
    def get_product_one(self, id):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        sql = "select * from product WHERE id = " + str(id)
        cur.execute(sql)
        
        product = cur.fetchone()
        con.close()

        return product

    '''
    商品追加
    '''
    def add_product(self, Product):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        result = True

        sql = ("insert into product('name', 'price', 'category_id') values('"
         + str(Product.name) + "'," + str(Product.price) + "," + str(Product.category_id) + ")")

        try:

            cur.execute(sql)

        except sqlite3.Error as e:
            print(e)
            print(sql)
            result = False

        con.commit()
        con.close()

        return result

    '''
    商品更新
    '''
    def update_product(self, Product):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        result = True

        sql = "UPDATE product SET name = '" + str(Product.name) + "'"
        sql += ", price = '" + str(Product.price) + "'"
        sql += ", category_id = " + str(Product.category_id)
        sql += " WHERE id = " + str(Product.id)
        print(sql)
        try:

            cur.execute(sql)

        except sqlite3.Error as e:
            print(e)
            result = False

        con.commit()
        con.close()

        return result
    '''
    商品削除
    '''
    def delete_product(self, id):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        result = True

        sql = "DELETE FROM product WHERE id = "+str(id)

        try:

            cur.execute(sql)

        except sqlite3.Error as e:
            print(e)
            result = False

        con.commit()
        con.close()

        return result

#DBにアクセスしカテゴリデータを取得、追加、更新、削除するクラス
class CategoryManager:

    def __init__(self,dbfilename):
        self.dbfilename = dbfilename

    '''
    カテゴリ全件取得
    '''
    def get_category_all(self):
        category_list = []

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        sql = "select * from category";
        cur.execute(sql)
        
        category_list = cur.fetchall()

        con.close()

        return category_list

    '''
    カテゴリ1件取得
    '''
    def get_category_one(self, id):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        sql = "select * from category WHERE id = " + str(id)
        cur.execute(sql)
        
        category = cur.fetchone()
        con.close()

        return category

    '''
    カテゴリ追加
    '''
    def add_category(self, Category):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        result = True

        sql = "insert into category('name') values('" + Category.name + "')"

        try:

            cur.execute(sql)

        except sqlite3.Error as e:
            print(e)
            print(sql)
            result = False

        con.commit()
        con.close()

        return result

    '''
    カテゴリ更新
    '''
    def update_category(self, Category):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        result = True

        sql = "UPDATE category SET name = '" + str(Category.name) + "'"
        sql += " WHERE id = " + str(Category.id)
        print(sql)
        try:

            cur.execute(sql)

        except sqlite3.Error as e:
            print(e)
            result = False

        con.commit()
        con.close()

        return result
    '''
    カテゴリ削除
    '''
    def delete_category(self, id):

        con = sqlite3.connect(self.dbfilename)
        cur = con.cursor()

        result = True

        sql = "DELETE FROM category WHERE id = "+str(id)

        try:

            cur.execute(sql)

        except sqlite3.Error as e:
            print(e)
            result = False

        con.commit()
        con.close()

        return result