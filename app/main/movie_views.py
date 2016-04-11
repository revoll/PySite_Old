# encoding: utf-8
import os

from flask import request, current_app, redirect, url_for, jsonify

from flask.ext.login import login_required

from movie_forms import PosterForm
from . import movie
from ..models.movie import Poster


@movie.route('/')
def index():
    form = PosterForm()
    if form.validate_on_submit():
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Poster.query().order_by(Poster.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTERS_PER_PAGE'], error_out=False)
    return jsonify(pagination)


@movie.route('/poster/<int:poster_id>')
def poster(poster_id):
    the_poster = Poster.query.filter_by(id=poster_id).first()
    return jsonify(the_poster)


@movie.route('/new', methods=['GET', 'POST'])
@login_required
def add():
    pass


@movie.route('/edit/<int:poster_id>', methods=['GET', 'POST'])
@login_required
def edit(poster_id):
    pass


@movie.route('/delete/<int:poster_id>')
@login_required
def delete(poster_id):
    pass


@movie.route('/delete-still/<int:still_id>')
@login_required
def delete_still(still_id):
    pass


@movie.route('/upload-poster', methods=['GET', 'POST'])
def upload_poster():
    """
    上传电影海报
    :param poster_id: 海报对应的数据库ID
    :param file['poster']: 海报图片
    :return: JSON格式的结果
    """
    if request.method == 'POST':
        poster_id = request.args.get('poster_id')
        f = request.files['poster']
        file_path = os.path.join(current_app.static_folder, 'img/poster/')
        try:
            assert poster_id and f
            file_ext = os.path.splitext(f.filename)[1]
            f.save(file_path + poster_id + file_ext)
            return 'success'
        except AssertionError and IOError:
            return 'failed'
    else:
        return 'GET is unsupported.'


@movie.route('/upload-still', methods=['GET', 'POST'])
def upload_still():
    """
    上传电影剧照
    :param still_id: 剧照记录对应的数据库ID
    :param file['still']: 剧照图片
    :return: JSON格式的结果
    """
    if request.method == 'POST':
        still_id = request.args.get('still_id')
        f = request.files['still']
        file_path = os.path.join(current_app.static_folder, 'img/stills/')
        try:
            assert still_id and f
            file_ext = os.path.splitext(f.filename)[1]
            f.save(file_path + still_id + file_ext)
            return 'success'
        except AssertionError and IOError:
            return 'failed'
    else:
        return 'GET is unsupported.'