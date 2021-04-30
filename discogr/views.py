from datetime import datetime
from flask import render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from discogr import app
#import sqlite3
#import mariadb
import mysql.connector as mariadb
import os

UPLOAD_FOLDER = '/Users/kirillskorobogatov/Desktop/FlaskGromov/FlaskGromov/covers'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg'])

#def get_db_connection():
#    cur = sqlite3.connect('database.db')
#    cur.row_factory = sqlite3.Row
#    return cur

def get_db_connection():
    cnx = mariadb.connect(
         host='127.0.0.1',
         port= 3306,
         user='root',
         passwd='passwd',
         database='discogr')
    cur = cnx.cursor()
    return cur

def get_post(post_id):
    cur = get_db_connection()
    post = cur.execute('SELECT * FROM posts WHERE id = ?',(post_id,)).fetchone()
    cur.close()
    if post is None:
        abort(404)
    return post

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/insert_to_db', methods=('GET', 'POST'))
def insert_to_db():
    if request.method == 'POST':
        artist = request.form['artist']
        song = request.form['song']
        duration = request.form['duration']
        album = request.form['album']
        year = request.form['year']
        label = request.form['label']
        genre = request.form['genre']

        file = request.files['file']

        #if file and allowed_file(file.filename):
        #    filename = secure_filename(file.filename)
        #    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            

        if not artist:
            flash('Artist must be!')
            
        else:
            cur = get_db_connection()
            cur.execute('INSERT INTO posts (artist, song, duration, album, year, label, genre) VALUES (?, ?, ?, ?, ?, ?, ?)',
                         (artist, song, duration, album, year, label, genre))
            cur.commit()
            cur.close()
            flash('Successful!')
            return redirect(url_for('insert_to_db'))
   
    return render_template(
        'insert_to_db.html',
        title='Add row to DB',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
   
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/')
@app.route('/show_records', methods=['GET', 'POST'])
def show_records():
  
    title='View row DB'
    ex_string = 'SELECT * FROM posts'
    search_string = []
    search_applied = False
    sort_asc = False
    sort_dec = False


    if request.method == 'POST': 
        check_list = request.form.getlist('sort_by_date')
        search_string = request.form.getlist('search_string')
        
        # flash(f'{search_string}')


        if (search_string != [''] and search_string != []):  
            search_applied = True
            ex_string += ' WHERE artist LIKE \'%{}%\''.format(search_string[0])

            if '1' in check_list:
                ex_string += ' ORDER BY year DESC'
                sort_dec = True
            elif '2' in check_list:
                ex_string += ' ORDER BY year ASC'
                sort_asc = True

        else:
            if '1' in check_list:
                ex_string += ' ORDER BY year DESC'
                sort_dec = True
            elif '2' in check_list:
                ex_string += ' ORDER BY year ASC'
                sort_asc = True

        
        # search_string = request.form.getlist('search_string')

        # flash(f'{search_string}')

        # if (search_string != [''] and search_string != []):  
        #     search_applied = True
        #     ex_string += f' WHERE artist LIKE \'%{search_string[0]}%\''

           

    cur = get_db_connection()
    print(ex_string)
    posts = cur.execute(ex_string).fetchall()
    cur.close()
    

    return render_template(
        'show_records.html',
        title=title,
        year=datetime.now().year,
        posts=posts,
        sort_asc = sort_asc,
        sort_dec = sort_dec,
        search_applied=search_applied,
        search_string=search_string,
        num_of_records=len(posts),
        message='Your application description page.'
    )



@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)



@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        artist = request.form['artist']
        song = request.form['song']

        if not artist:
            flash('Artist is required!')
        else:
            cur = get_db_connection()
            cur.execute('UPDATE posts SET artist = ?, song = ?'
                         ' WHERE id = ?',
                         (artist, song, id))
            cur.commit()
            cur.close()
            return redirect(url_for('show_records'))

    return render_template('edit.html', post=post, title='Edit row')


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    cur = get_db_connection()
    cur.execute('DELETE FROM posts WHERE id = ?', (id,))
    cur.commit()
    cur.close()
    flash('Successful added!')
    return redirect(url_for('show_records'))
