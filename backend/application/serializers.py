from flask_marshmallow import Marshmallow
from .models import Task
from . import create_app

ma = Marshmallow(create_app())

class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)