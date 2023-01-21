from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from forms_class import MovieForms, AddMovie
from api_class import SearchMovie

app = Flask(__name__)
app.config["SECRET_KEY"] = "TommyShelby"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myMovies.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


# CREATE SQLALCHEMY DATABASE WITH Movies TABLE
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True)
    year = db.Column(db.Integer)
    description = db.Column(db.String)
    rating = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    review = db.Column(db.String)
    img_uri = db.Column(db.String)


@app.route("/")
def home_page():
    movie_data = db.session.query(Movies).order_by(Movies.rating.desc()).all()
    for i in range(len(movie_data)):
        movie_data[i].ranking = i + 1
    return render_template("index.html", movie_list=movie_data)


@app.route("/select")
def select_page():
    movie_api_id = request.args.get("id")
    movie_tool = SearchMovie()
    movie_info = movie_tool.current_movie(movie_id=movie_api_id)
    # add new movie into database:
    new_movie = Movies(
        title=movie_info["title"],
        year=movie_info["year"],
        description=movie_info["description"],
        img_uri=movie_info["img_uri"]
    )
    db.session.add(new_movie)
    db.session.commit()
    # update id
    return redirect(url_for("edit_page", id=new_movie.id))


@app.route("/edit", methods=["GET", "POST"])
def edit_page():
    form = MovieForms()
    update_id = request.args.get("id")
    update_record = Movies.query.get(update_id)
    # come back from edit page into home page:
    if form.validate_on_submit():
        update_record.rating = float(form.rating.data)
        update_record.review = form.review.data
        db.session.commit()
        return redirect(url_for("home_page"))
    return render_template("edit.html", form=form, movie=update_record)


@app.route("/add", methods=["GET", "POST"])
def add_page():
    add_form = AddMovie()
    # come back from add page into select page:
    if add_form.validate_on_submit():
        movie_name = add_form.title.data
        search_tool = SearchMovie()
        search_data = search_tool.get_movies(movie_name=movie_name)
        return render_template("select.html", movie_list=search_data)
    return render_template("add.html", form=add_form)


@app.route("/delete")
def delete_page():
    delete_id = request.args.get("id")
    delete_record = Movies.query.get(delete_id)
    db.session.delete(delete_record)
    db.session.commit()
    db.session.close()
    return redirect(url_for("home_page"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
