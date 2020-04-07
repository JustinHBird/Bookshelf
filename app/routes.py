from flask import Blueprint, render_template, url_for, request, redirect, jsonify
from app.forms import BookForm
import firestore

bp = Blueprint('app', __name__)

@bp.route('/')
def index():
    start_after = request.json['start_after']
    if start_after:
        return jasonify(books)
    #books = firestore.read_all()
    books, last_title = firestore.read_limit(start_after=start_after)
    return render_template('list.html', books=books, last_title=last_title)


@bp.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new book to the firestore database

    Return user to the view page for the new book"""
    form = BookForm()

    if form.validate_on_submit():
        data = form.data

        # Processs image if there is one
        # COME BACK

        book = firestore.create(data)
        return redirect(url_for('app.view', book_id=book['id']))

    return render_template('book_form.html', form=form, header="Add Book")

@bp.route('/<book_id>/update', methods=['GET', 'POST'])
def update(book_id):
    book = firestore.read(book_id)
    form = BookForm(data=book)

    # Process form if submission request
    if form.validate_on_submit():
        data = form.data
        book = firestore.update(data, book_id)
        return redirect(url_for('app.view', book_id=book['id']))
    
    book = firestore.read(book_id)
    return render_template('book_form.html', form=form, header="Update Book")

@bp.route('/<book_id>/delete', methods=['GET'])
def delete(book_id):
    firestore.delete(book_id)
    return redirect(url_for('app.index'))


@bp.route('/<book_id>')
def view(book_id):
    book = firestore.read(book_id)
    return render_template('view.html', book=book)

@bp.route('/ajax', methods=['POST'])
def ajax():
    if request.method == "POST":
        print(request.json['start_after'])

    
    return 'response to ajax request'
