from flask import Flask, request, jsonify, make_response, render_template, abort
import server.services.account_service as account_service
import server.services.auth_service as auth_service
import server.services.token_service as token_service
import server.configs.SERVER as SERVER_CONFIG
import server.configs.JWT as JWT_CONFIG
import server.services.data_api as data_api
import server.services.session_service as session_service
import server.utils.date_time as date_time

app = Flask(__name__, template_folder='client/', static_folder='client/')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        auth_result = auth_service.authentication(request.form.get('login'), request.form.get('password'))

        if auth_result['status'] == 'success':
            access_token, refresh_token = auth_service.authorization(
                auth_result['user_id'], request.headers.get('User-Agent')
            )

            res = make_response(jsonify({
                'status': 'success',
                'access_token': access_token
            }))

            res.set_cookie('refresh_token', refresh_token, max_age=JWT_CONFIG.REFRESH_TOKEN_EXP_SEC)

            return res

        else:
            return jsonify({
                'status': 'failure',
                'message': 'Login or password incorrect'
            })


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        user_id = account_service.create_account(request.form.get('login'), request.form.get('password'))

        access_token, refresh_token = auth_service.authorization(user_id, request.headers.get('User-Agent'))

        res = make_response(jsonify({
            'access_token': access_token
        }))

        res.set_cookie('refresh_token', refresh_token, max_age=JWT_CONFIG.REFRESH_TOKEN_EXP_SEC)

        return res


@app.route('/refresh_tokens', methods=['GET'])
def refresh_tokens():
    refresh_token = request.cookies.get('refresh_token')
    user_agent = request.headers.get('User-Agent')
    result = token_service.refresh_access_token(refresh_token, user_agent)
    if result['status'] == 'failure':
        session_service.remove_session(refresh_token)
        res = make_response(result)
        res.set_cookie('refresh_token', '', expires=0)
        return res

    return jsonify(result)


@app.route('/get_data', methods=['GET'])
def get_data():
    access_token = request.headers['Authorization']
    try:
        decoded_data = token_service.decode_access_token(access_token)
    except Exception:
        return abort(401)

    user_id = decoded_data['user_id']
    is_expired = date_time.check_expired(decoded_data['exp'])
    if is_expired:
        return abort(401)

    user_data = data_api.get_data(user_id)
    return jsonify(user_data)


if __name__ == '__main__':
    app.run(
        host=SERVER_CONFIG.HOST,
        port=SERVER_CONFIG.PORT,
        debug=SERVER_CONFIG.DEBUG
    )
