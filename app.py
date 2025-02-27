# By Mohammad Alomar, 27 Feb 2025.
import acrm, flask


app = flask.Flask(__name__)


@app.before_request
def auth():
    ip = flask.request.remote_addr
    if not acrm.is_allowed(ip):
        return flask.render_template('401.html'), 401


@app.errorhandler(Exception)
def error_handler(error):
    return f'[Flask Error Handler] {error}'


@app.route('/')
def home():
    return flask.render_template('home.html')


@app.route('/get_crs')
def get_crs():
    return acrm.get_crs()


@app.route('/patch_group', methods=['PATCH'])
def patch_group():
    crid = flask.request.form['crid']
    value = flask.request.form['value']
    return acrm.patch_group(crid, value)


@app.route('/patch_comment', methods=['PATCH'])
def patch_comment():
    crid = flask.request.form['crid']
    value = flask.request.form['value']
    return acrm.patch_comment(crid, value)


@app.route('/s')
def settings():
    return flask.render_template('settings.html')
    

@app.route('/get_whitelist')
def get_whitelist():
    return acrm.get_whitelist()


@app.route('/whitelist_append', methods=['POST'])
def whitelist_append():
    value = flask.request.form['value']
    return acrm.whitelist_append(value)


@app.route('/whitelist_remove', methods=['DELETE'])
def whitelist_remove():
    value = flask.request.form['value']
    return acrm.whitelist_remove(value)


@app.route('/auto_group')
def auto_group():
    return acrm.auto_group()


@app.route('/export_project')
def export_project():
    file = acrm.export_project()
    return flask.send_file(file, download_name='acrm.zip', as_attachment=True, mimetype='application/zip')


@app.route('/import_crs', methods=['POST'])
def import_crs():
    file = flask.request.files['file'].read()
    return acrm.import_crs(file)
