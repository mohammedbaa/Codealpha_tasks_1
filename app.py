import pickle
from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Initialize Spotipy client
Client_id = 'f21e8dc62f2e40ea923b8d67e047542c'
Client_secret = '276d6f78a925465f9849cbe168ec1142'
client_credentials_manager = SpotifyClientCredentials(client_id=Client_id, client_secret=Client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load your data and models
music = pickle.load(open('E:/My_Project/CodeAlpha/Task 1/df.pkl', 'rb'))
similarity = pickle.load(open('E:/My_Project/CodeAlpha/Task 1/similarity.pkl', 'rb'))

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type='track')

    if results and results['tracks']['items']: 
        track = results['tracks']['items'][0]
        album_cover_url = track['album']['images'][0]['url']
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommender(song):
    idx = music[music['song'] == song].index[0]
    distance = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])

    recommened_music_name = []
    recommended_music_poster = []
    for i in distance[1:6]:
        artist = music.iloc[i[0]]['artist']
        recommended_music_poster.append(get_song_album_cover_url(music.iloc[i[0]]['song'], artist))
        recommened_music_name.append(music.iloc[i[0]]['song'])
    return recommened_music_name, recommended_music_poster

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_song = request.form['song']
        recommended_music_names, recommended_music_posters = recommender(selected_song)
        
        # Pre-zip the lists
        recommendations = zip(recommended_music_names, recommended_music_posters)
        
        return render_template('index.html', 
                               songs=music['song'].values,
                               selected_song=selected_song,
                               recommendations=recommendations)
    else:
        return render_template('index.html', songs=music['song'].values)


if __name__ == '__main__':
    app.run(debug=True)
