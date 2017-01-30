from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, Markup
from flask_login import login_user, logout_user, current_user, login_required, LoginManager
from .forms import LoginForm, EditForm, PostForm, SearchForm
from .model import User, Post
from flask.ext.babel import gettext
from datetime import datetime
from oauth import OAuthSignIn
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash,check_password_hash
from config import MAX_SEARCH_RESULTS, LANGUAGES, POSTS_PER_PAGE
from .email import follower_notification
from app import app, db, lm, babel
from guess_language import guessLanguage
from .translate import online_translate
from stock import get_nasdaq_100_data, yahoo_get_all_data
import numpy as np
import pandas as pd
import bokeh
from bokeh.plotting import figure
from bokeh.io import show
from bokeh.embed import components
bv = bokeh.__version__

app.vars={}

@lm.user_loader
def user_loader(id):
    return User.query.get(id)

@babel.localeselector
def get_locale():
    # otherwise try to guess the language from the user accept
    # header the browser transmits.  The best match wins.
    #return request.accept_languages.best_match(LANGUAGES.keys())
    return 'en'


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        g.search_form = SearchForm()
    g.locale = get_locale()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    form = PostForm()
    if form.validate_on_submit():
        language = guessLanguage(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data,
                    timestamp=datetime.utcnow(),
                    author=g.user,
                    language=language)
        db.session.add(post)
        db.session.commit()
        flash(gettext('Your post is now live!'))
        return redirect(url_for('index'))
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html',
                           title='Home',
                           form=form,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user_input = form.data['user_name']
        pwd_input = form.data['password']
        user = User.query.filter_by(email=user_input).first()
        #register new user
        if user is None:
            email_addr = form.data['user_name']
            nickname_str = email_addr.split('@')[0]
            nickname_valid = User.make_valid_nickname(nickname_str)
            nickname = User.make_unique_nickname(nickname_valid)
            pwd = User.hashed_password(pwd_input)
            user = User(nickname=nickname, email=email_addr, password=pwd)
            db.session.add(user)
            db.session.commit()
            # make the user follow him/herself
            db.session.add(user.follow(user))
            db.session.commit()
        remember_me = False
        if 'remember_me' in session:
            remember_me = session['remember_me']
            session.pop('remember_me', None)
        #log in back existing user
        if user.is_authenticated(pwd_input) is False:
            flash(gettext('Invalid login. Please try again.'))
            return redirect(url_for('index'))

        login_user(user, remember=remember_me)
        return redirect(url_for('index'))


    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext('User %(nickname)s not found.', nickname=nickname))
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
                           user=user,
                           posts=posts)

@app.route('/chart')
def chart():
    #stock_data = yahoo_get_all_data('AAPL')
    chart_type = 'bar'
    chartID = 0
    chart_height = 350
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height, }
    series = [{"name": 'Label1', "data": [1, 2, 3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'AAPL'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    return render_template('chart.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis,
                           yAxis=yAxis)


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    # Request data from Quandl and get into pandas
    # --------------------------------------------|
    req = 'https://www.quandl.com/api/v3/datasets/WIKI/'
    req = '%s%s.json?&collapse=weekly' % (req, app.vars['ticker'])
    if not app.vars['start_year'] == '':
        req = '%s&start_date=%s-01-01' % (req, app.vars['start_year'])
    r = requests.get(req)
    cols = r.json()['dataset']['column_names'][0:5]
    df = pd.DataFrame(np.array(r.json()['dataset']['data'])[:, 0:5], columns=cols)
    df.Date = pd.to_datetime(df.Date)
    df[['Open', 'High', 'Low', 'Close']] = df[['Open', 'High', 'Low', 'Close']].astype(float)
    if not app.vars['start_year'] == '':
        if df.Date.iloc[-1].year > int(app.vars['start_year']):
            app.vars['tag'] = '%s, but Quandl record begins in %s' % (app.vars['tag'], df.Date.iloc[-1].year)
    app.vars['desc'] = r.json()['dataset']['name'].split(',')[0]

    # Make Bokeh plot and insert using components
    # ------------------- ------------------------|
    p = figure(plot_width=450, plot_height=450, title=app.vars['ticker'], x_axis_type="datetime")
    if 'Range' in app.vars['select']:
        tmpx = np.array([df.Date, df.Date[::-1]]).flatten()
        tmpy = np.array([df.High, df.Low[::-1]]).flatten()
        p.patch(tmpx, tmpy, alpha=0.3, color="gray", legend='Range (High/Low)')
    if 'Open' in app.vars['select']:
        p.line(df.Date, df.Open, line_width=2, legend='Opening price')
    if 'Close' in app.vars['select']:
        p.line(df.Date, df.Close, line_width=2, line_color="#FB8072", legend='Closing price')
    p.legend.orientation = "top_left"

    # axis labels
    p.xaxis.axis_label = "Date"
    p.xaxis.axis_label_text_font_style = 'bold'
    p.xaxis.axis_label_text_font_size = '16pt'
    p.xaxis.major_label_orientation = np.pi / 4
    p.xaxis.major_label_text_font_size = '14pt'
    p.xaxis.bounds = (df.Date.iloc[-1], df.Date.iloc[0])
    p.yaxis.axis_label = "Price ($)"
    p.yaxis.axis_label_text_font_style = 'bold'
    p.yaxis.axis_label_text_font_size = '16pt'
    p.yaxis.major_label_text_font_size = '12pt'

    # render graph template
    # ------------------- ------------------------|
    script, div = components(p)
    return render_template('graph.html', bv=bv, ticker=app.vars['ticker'],
                           ttag=app.vars['desc'], yrtag=app.vars['tag'],
                           script=script, div=div)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash(gettext('Your changes have been saved.'))
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext('User %s not found.' % nickname))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t follow yourself!'))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash(gettext('Cannot follow %(nickname)s.', nickname=nickname))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You are now following %(nickname)s!', nickname=nickname))
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname=nickname))


@app.route("/stock_nasdaq_100")
def stock_nasdaq_100():
    return jsonify(get_nasdaq_100_data())

@app.route('/stock')
def stock():
    return render_template("stock.html")

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash(gettext('User %s not found.' % nickname))
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t unfollow yourself!'))
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash(gettext('Cannot unfollow %(nickname)s.', nickname=nickname))
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash(gettext('You have stopped following ' + nickname + '.'))
    return redirect(url_for('user', nickname=nickname))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash(gettext('Authentication failed.'))
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('search_results.html',
                           query=query,
                           results=results)
@app.route('/translate', methods=['POST'])
@login_required
def translate():
    return jsonify({
        'text': online_translate(
            request.form['text'],
            request.form['sourceLang'],
            request.form['destLang'])})


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post is None:
        flash('Post not found.')
        return redirect(url_for('index'))
    if post.author.id != g.user.id:
        flash('You cannot delete this post.')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
