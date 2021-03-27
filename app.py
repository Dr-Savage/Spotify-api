from flask import Flask, render_template, request, redirect,session
import json
import main

app = Flask(__name__)
app.secret_key = 'Let the devil helps you'

obj = main.start()
topsongs = obj.fetch_songs()

@app.route('/')
def hello():
    return redirect('create')

@app.route('/top', methods=['GET','POST'])
def top_songs():
    print(request.method)
    if request.method == 'GET':
        return render_template("index.html", topsongs=topsongs, template='top')
    else:
        if 'id' in session.keys():
            uri = obj.get_uri(topsongs)
            id = session['id']
            ans = obj.add_songs_to_playlist(id, uri)
            return redirect('view')

@app.route('/view')
def view_songs():
    if 'id' in session.keys():
        list_song = obj.list_songs_in_playlist(session['id'])
        return render_template("index.html", list_song=list_song, template='view')


@app.route('/create', methods=['GET','POST'])
def create_playlist():
    print(request.method)
    if request.method =='GET':
        return render_template("index.html", template='create')
    if request.method == 'POST':
        name = request.form['name'].strip()
        desc = request.form['Description'].strip()
        session['id'] = obj.create_playlist(name,desc)
        return redirect('/top')


if __name__ == '__main__':
    app.run(debug=True)

