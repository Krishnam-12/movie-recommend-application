from flask import Flask, request, jsonify, render_template
import pickle
import difflib

movies=pickle.load(open('model/movies_list','rb'))
similarity=pickle.load(open('model/similarity','rb'))
# movies=pickle.load(open('movies_list','rb'))
# similarity=pickle.load(open('similarity','rb'))

def recommend(movie):
    list_of_all_titles = movies['title'].tolist()
    find_close_match = difflib.get_close_matches(movie, list_of_all_titles)
    close_match = find_close_match[0]
    index=movies[movies['title']==close_match].index[0]
    distances=sorted(list(enumerate(similarity[index])),reverse=True, key=lambda x:x[1])
    recommended_movies=[]
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies
app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/recommendation", methods=['POST'])
def recommendation():
    movie1=request.form['movies']
#     movie1=request.form.values()
    recommended_movies_name=recommend(movie1)
    recommended_movies_string = ", ".join(f"'{item}'" for item in recommended_movies_name)
    recommended_movies_string= movie1+" are: "+recommended_movies_string
    print(recommended_movies_string)
    return render_template('index.html',prdiction_text='The movie recommendations for {}: '.format(recommended_movies_string))

if __name__ == '__main__':
    app.run()