from flask import Flask, render_template, request
import pickle

popular_df = pickle.load(open('popular_books.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_score = pickle.load(open('similarity_score.pkl', 'rb'))
book_pivot = pickle.load(open('book_pivot.pkl', 'rb'))

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    book_name = request.form.get('user_input')
    book_index = book_pivot.index.get_loc(book_name)
    similarity_scores = list(enumerate(similarity_score[book_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:5]
    book_indices = [i[0] for i in similarity_scores]
    data = []
    for i in book_indices:
        item = []
        temp_df = books[books['Book-Title'] == book_pivot.index[i]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    print(data)

    return  render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)