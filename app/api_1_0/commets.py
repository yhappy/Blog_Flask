from flask import jsonify, request, current_app, url_for, g
from . import api
from ..models import User, Post, Comment, Permission
from .. import db
from .decorators import permission_required

@api.route('/comments/')
def get_comments():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page,
                                                                           per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
                                                                           error_out=False)
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_comments', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_comments', page=page + 1, _external=True)
    return jsonify({
        'commets': [commet.to_json() for comment in comments],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

