import os
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
from waitress import serve
from flask_migrate import Migrate
from services import *
from AI_Services import *

load_dotenv()

app = Flask(__name__)
CORS(app) 

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').strip()

from models import db, Complaint, Comment, ComplaintStats
# migrate = Migrate(app, db)

# Initialize the app with SQLAlchemy
db.init_app(app)

# Initialize database
with app.app_context():
    db.create_all()

# Create a test route
@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Server is running'})

# Get Complaint Statistics
@app.route('/api/grievance/stats', methods=['GET'])
def get_complaint_stats():
    return get_complaint_stats_service()

# Create a complaint
@app.route('/api/grievance/new_complaint', methods=['POST'])
def create_complaint_route():
    return create_complaint_service()

# Upvote a complaint
@app.route('/api/grievance/upvote/<int:c_id>', methods=['PUT'])
def upvote_complaint_route(c_id):
    return upvote_complaint_service(c_id)

# Get number of upvotes for a complaint
@app.route('/api/grievance/get_upvotes/<int:c_id>', methods=['GET'])
def get_upvotes_route(c_id):
    return get_upvotes_service(c_id)

# Add a resolver to a complaint
@app.route('/api/grievance/add_resolver/<int:c_id>', methods=['PUT'])
def add_resolver_route(c_id):
    return add_resolver_service(c_id)

# Add Comment to a complaint
@app.route('/api/grievance/add_comment/<int:c_id>', methods=['POST'])
def add_comment_route(c_id):
    return add_comment_service(c_id)

# Get all comments for a complaint
@app.route('/api/grievance/get_comments/<int:c_id>', methods=['GET'])
def get_comments_route(c_id):   
    return get_comments_service(c_id)

# Delete a comment from a complaint
@app.route('/api/grievance/delete_comment/<int:c_id>/<int:comment_id>', methods=['DELETE'])
def delete_comment_route(c_id, comment_id):
    return delete_comment_service(c_id, comment_id)

# Delete a complaint
@app.route('/api/grievance/delete_complaint/<int:c_id>', methods=['DELETE'])
def delete_complaint_route(c_id):
    return delete_complaint_service(c_id)

# -------- AI Services APIs --------

@app.route("/api/grievance/ai/embed_store", methods=["POST"])
def embed_store():
    return embed_service()

@app.route("/api/grievance/ai/query", methods=["POST"])
def query():
    return query_service()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=4000)