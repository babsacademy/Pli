import requests
from flask import Flask, render_template
from datetime import datetime
import html

app = Flask(__name__)

api = ['https://senego.com/wp-json/wp/v2/posts', 'http://lequotidien.sn/wp-json/wp/v2/posts','http://lequotidien.sn/wp-json/wp/v2/posts']

@app.route('/')
def index():
    # Récupérer les données de tous les API WordPress
    posts = []
    for api_url in api:
        response = requests.get(api_url)
        posts.extend(response.json())

    # Formater les données pour les afficher correctement
    formatted_posts = []
    for post in posts:
        formatted_date = datetime.strptime(post['date'], '%Y-%m-%dT%H:%M:%S').strftime('%d/%m/%Y')
        formatted_summary = html.unescape(post['excerpt']['rendered'])
        formatted_title = html.unescape(post['title']['rendered'])

        # Récupérer l'image à partir de 'better_featured_image' pour le premier API et 'jetpack_featured_media_url' pour le deuxième API
        if 'better_featured_image' in post:
            formatted_image = post['better_featured_image']['source_url']
        elif 'jetpack_featured_media_url' in post:
            formatted_image = post['jetpack_featured_media_url']
        else:
            formatted_image = 'https://via.placeholder.com/150x150.png?text=No+Image+Available'

        formatted_post = {
            'title': formatted_title,
            'image': formatted_image,
            'summary': formatted_summary,
            'date': formatted_date
        }
        formatted_posts.append(formatted_post)

    # Afficher les données formatées dans la page web
    return render_template('index.html', posts=formatted_posts)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
 
