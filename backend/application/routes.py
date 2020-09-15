"""Application routes."""
from datetime import datetime as dt
from flask import request, render_template, make_response, redirect, url_for, jsonify, send_from_directory
from flask import current_app as app
from .models import db, Task
from .serializers import task_schema, tasks_schema
from sqlalchemy import desc, asc

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('../../frontend/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('../../frontend/public', path)


@app.route('/task', methods=['POST'])
def save_task():
    req_data = request.get_json()

    try:
        description = req_data['description']
        if description:
            existing_task = Task.query.filter(Task.description == description).first()

            if existing_task:
                return make_response(jsonify(description="You already added this task!"), 400)   
            
            new_task = Task(description=description, created=dt.now(), active=True)
            db.session.add(new_task)
            db.session.commit()

            return task_schema.jsonify(new_task)

    except (ValueError, KeyError, TypeError):
        return make_response(jsonify(description="That is a wrong request!"), 400)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.order_by(Task.created.desc(), Task.active).all()
    return jsonify(tasks_schema.dump(all_tasks))


@app.route('/task/change/<int:id>', methods=['PATCH'])
def finished_task(id):
    state = request.args.get('state')
    task = Task.query.filter_by(id=id).first_or_404()
    
    if state == "false":
        task.active = False
        db.session.commit()
    
    elif state == "true":
        task.active = True
        db.session.commit()
    
    return jsonify(task_schema.dump(task))


@app.route('/task/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.filter_by(id=id).first_or_404()
    return jsonify(task_schema.dump(task))


@app.route('/task/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.filter_by(id=id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return "Success"
