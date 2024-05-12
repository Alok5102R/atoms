import hashlib
import random
import os
from flask import Flask, request, render_template, redirect
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ========================================================
# MongoDB configuration

mongodbString=os.getenv("mongodb")
client = MongoClient(mongodbString)
db = client['Atoms-urlshortener']                                            # MongoDB database
collection = db['urls']                                                      # MongoDB collection


@app.route('/', methods=['GET','POST'])
def home():
    """
        Home page
    """
    url = ""
    if request.form:
        url = str(request.form['urllink'])

    query = {'longurl':url}
    url_exists_count = collection.count_documents(query)
    if url_exists_count==0 and len(url)>5:
        shorten_url = generate_short_code(url)
        query = {'longurl':url,'shorturl':shorten_url}
        collection.insert_one(query)
    else:
        pass

    return render_template('index.html')



def generate_short_code(long_url):
    """
        Generate hash value for the long URL
    """
    hash_value = hashlib.sha256(long_url.encode()).hexdigest()
    extra_encoding = os.getenv("extra_encoding")
    extra_encoding_list = list(extra_encoding)
    extra_encoding_string = ''.join(random.sample(extra_encoding_list, 4))

    short_code = hash_value[:4] + extra_encoding_string
    return short_code


@app.route('/<pk>', methods=['GET'])
def fetch_long_url(pk):
    url = ""
    query = {'shorturl':str(pk)}
    url = collection.find_one(query)['longurl']
    return redirect(url)
    

if __name__ == '__main__':
    app.run(debug=True)