from web_parser_app.celery import app

from .run_parser import main


@app.task
def start_parsing_celery(parsing_group_id, user_id):
    main(parsing_group_id, user_id)
