from prototype import app, db
from prototype.models import User, Grocery

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Grocery': Grocery}
