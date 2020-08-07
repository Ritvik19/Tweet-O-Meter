from flask import render_template, request, url_for
from flask_admin.contrib.sqla import ModelView
from tweetometer import app, admin, db
from models import Post

admin.add_view(ModelView(Post, db.session))
posts=Post.query.order_by(Post.Id.desc()).limit(50).all()

@app.route('/')
def home():
    pnum = request.args.get('page', 1, int)
    return render_template('layout.html', data=Post.query.order_by(Post.Id.desc()).paginate(pnum, 1),
                            posts=posts, section='home')


@app.route('/national')
def national():
    pnum = request.args.get('page', 1, int)
    return render_template('layout.html', data=Post.query.filter_by(National=1).order_by(Post.Id.desc()).paginate(pnum, 1), 
                            posts=posts, section='national')


@app.route('/sports')
def sports():
    pnum = request.args.get('page', 1, int)
    return render_template('layout.html', data=Post.query.filter_by(Sports=1).order_by(Post.Id.desc()).paginate(pnum, 1), 
                            posts=posts, section='sports')


@app.route('/world')
def world():
    pnum = request.args.get('page', 1, int)
    return render_template('layout.html', data=Post.query.filter_by(World=1).order_by(Post.Id.desc()).paginate(pnum, 1),
                            posts=posts, section='world')


@app.route('/politics')
def politics():
    pnum = request.args.get('page', 1, int)
    return render_template('layout.html', data=Post.query.filter_by(Politics=1).order_by(Post.Id.desc()).paginate(pnum, 1), 
                            posts=posts, section='politics')


@app.route('/technology')
def technology():
    pnum = request.args.get('page', 1, int)
    return render_template('layout.html',data=Post.query.filter_by(Technology=1).order_by(Post.Id.desc()).paginate(pnum, 1), 
                            posts=posts, section='technology')


@app.route('/entertainment')
def entertainment():
    pnum = request.args.get('page', 1, int)
    return render_template('layout.html', data=Post.query.filter_by(Entertainment=1).order_by(Post.Id.desc()).paginate(pnum, 1), 
                            posts=posts, section='entertainment')


@app.route('/miscellaneous')
def miscellaneous():
    pnum = request.args.get('page', 1, int)
    return render_template('layout.html', data=Post.query.filter_by(Hatke=1).order_by(Post.Id.desc()).paginate(pnum, 1), 
                            posts=posts, section='miscellaneous')


@app.route('/archive')
def archive():
    q = int(request.args.get('q'))
    return render_template('layout.html', data=Post.query.filter_by(Id=q).paginate(1, 1), posts=posts)

