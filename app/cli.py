import os
import click
from flask_migrate import upgrade
from app.fetch import get_access_groups, get_access_rights, get_models, set_admin_groups
from app.tasks import dummy_data


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @app.cli.command()
    def dummy():
        """Import dummy data"""
        dummy_data()
    
    @app.cli.command()
    def fetch():
        """Fetch from Olam API"""
        get_access_groups()
        set_admin_groups()
        get_models()
        get_access_rights()


    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')
