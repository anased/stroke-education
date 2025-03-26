# app/cli.py
import click
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from .extensions import db
from .models.admin import Admin

def register_commands(app):
    app.cli.add_command(create_admin)

@click.command('create-admin')
@click.argument('username')
@click.argument('password')
@with_appcontext
def create_admin(username, password):
    """Create a new admin user."""
    admin = Admin.query.filter_by(username=username).first()
    
    if admin:
        click.echo(f'Admin user {username} already exists. Use a different username.')
        return
    
    new_admin = Admin(
        username=username,
        password=generate_password_hash(password)
    )
    
    db.session.add(new_admin)
    db.session.commit()
    
    click.echo(f'Admin user {username} created successfully!')