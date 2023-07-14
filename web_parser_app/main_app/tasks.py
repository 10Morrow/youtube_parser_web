from web_parser_app.web_parser_app.celery import app


@app.task()
def start_parsing(parsing_group_id):
    pass
