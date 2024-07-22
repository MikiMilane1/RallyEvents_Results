def register_bps(app, *args):
    for arg in args:
        app.register_blueprint(arg)