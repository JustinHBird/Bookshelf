import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# For Cloud Deployed App:
#cred = credentials.ApplicationDefault()
# For Locally Deployed App:
cred = credentials.Certificate('/Users/justinbird/Code/GCP_Keys/py-firestore-ebc03-local.json')
firebase_admin.initialize_app(cred, {'project': 'py-firestore-ebc03'})

def document_to_dict(doc):
    """Convert a Firestore document to dictionary"""
    if not doc.exists:
        return None
    doc_dict = doc.to_dict()
    doc_dict['id'] = doc.id
    return doc_dict

def create(data, book_id=None):
    db = firestore.client()
    book_ref = db.collection('Book').document(book_id)
    book_ref.set(data)
    # Return the book info as a dictionary to be used in the redirect to the
    # book info page. 
    return document_to_dict(book_ref.get())

update = create

def read(book_id):
    db = firestore.client()
    book_ref = db.collection('Book').document(book_id)
    doc = book_ref.get()
    return document_to_dict(doc)

def read_all():
    db = firestore.client()
    query = db.collection('Book').order_by('title')

    docs = query.stream()
    docs = list(map(document_to_dict, docs))
    return docs

PAGE_LIMIT = 10
def read_limit(limit=PAGE_LIMIT, start_after=None):
    db = firestore.client()
    books_ref = db.collection('Book')
    query =books_ref.limit(limit).order_by('title')
    
    if start_after:
        # Construct a new query starting at given document
        query = query.start_after({'title':start_after})
    
    docs = query.stream()
    docs = list(map(document_to_dict, docs))

    last_title = None
    if limit == len(docs):
        # Get the last document from the results and set as the last title.
        last_title = docs[-1]['title']
    return docs, last_title


    

def delete(book_id):
    db = firestore.client()
    book_ref = db.collection('Book').document(book_id)
    book_ref.delete()
    