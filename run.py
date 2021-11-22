from flask import Flask, request, jsonify, make_response, render_template
import server.services.account_service as account_service
import server.services.auth_service as auth_service
import server.services.token_service as token_service
import server.config as config

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
                'access_token': access_token
            }))

            res.set_cookie('refresh_token', refresh_token)

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

        res.set_cookie('refresh_token', refresh_token)

        return res


@app.route('/refresh_tokens', methods=['GET'])
def refresh_tokens():
    result = token_service.refresh_access_token(
        request.cookies.get('refresh_token'), request.headers.get('User-Agent')
    )
    return jsonify(result)


if __name__ == '__main__':
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
