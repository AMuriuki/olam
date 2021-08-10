from flask_migrate import upgrade
from app import create_app, cli, db
from app.main.models.module import Module, ModuleCategory

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db}
