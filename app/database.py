from uuid import uuid4
import uuid
import psycopg2

from app import create_app

# app = create_app()

def establish_connection():
    try:
        connection = psycopg2.connect(
            user="deed", password="deed", host="127.0.0.1", port="5432", database="deed")
        cursor = connection.cursor()
    except (Exception, psycopg2.Error) as error:
        print("Failed to connect to the database", error)

    return cursor, connection


def close_connection(cursor, connection):
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")


def get_page_id_seq():
    cursor = establish_connection()[0]
    query = """SELECT last_value, log_cnt from wagtailcore_page_id_seq"""
    cursor.execute(query)
    result = cursor.fetchone()
    return int(list(result)[0])


def get_content_type(name):
    cursor = establish_connection()[0]
    query = """SELECT id from django_content_type WHERE app_label = %s"""
    values = (name,)
    cursor.execute(query, values)
    result = cursor.fetchone()
    return int(list(result)[0])


def slugify(name):
    return name.lower().replace(" ", "-")



def insert_product(name, model, price, sku, category):
    cursor = establish_connection()[0]
    connection = establish_connection()[1]
    
    id = get_page_id_seq() + 1
    slug = slugify(name)
    content_type = get_content_type("product")
    url_path = "/home/"+category+"/"+ slugify(name)
    path = uuid.uuid4().int & (1<<64)-1
    depth = 4
    numchild = 0
    search_description = 0
    locale_id = 1
    
    query1 = "INSERT INTO wagtailcore_page (id, title, draft_title, slug, content_type_id, live, has_unpublished_changes, owner_id, url_path, path, depth, numchild, seo_title, show_in_menus, search_description, expired, locked, translation_key, locale_id) VALUES ({}, '{}', '{}', '{}', {}, {}, {}, {}, '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(id, name, name, slug, content_type, True, False, 1, url_path, path, depth, numchild, slug, False, search_description, False, False, uuid.uuid4(), locale_id)

    print(cursor.execute(query1))
    cursor.execute(query1)
    connection.commit()

    query = """INSERT INTO product_product (page_ptr_id, name, model, price, sku) VALUES (%s,%s,%s,%s,%s)"""
    values = (get_page_id_seq() + 1, name, model, price, sku)
    
    cursor.execute(query, tuple(values))
    connection.commit()
    close_connection(cursor, connection)
