from requests_oauthlib import OAuth1Session
from flask import Flask, jsonify, request, redirect
import urllib.parse as parse
import os

twitter_base_url = 'https://api.twitter.com'
authorization_endpoint = twitter_base_url + '/oauth/authenticate'
request_token_endpoint = twitter_base_url + '/oauth/request_token'
token_endpoint = twitter_base_url + '/oauth/access_token'

app = Flask(__name__)


@app.route("/login")
def login():
    twitter = OAuth1Session(
        os.environ["API_KEY"],
        os.environ["API_SECRET_KEY"]
    )
    oauth_callback = request.args.get('oauth_callback')
    res = twitter.post(request_token_endpoint, params={
        'oauth_callback': oauth_callback})
    request_token = dict(parse.parse_qsl(res.content.decode("utf-8")))
    oauth_token = request_token['oauth_token']

    return redirect(authorization_endpoint+'?{}'.format(parse.urlencode({
        'oauth_token': oauth_token
    })))


@app.route("/callback")
def callback():
    oauth_verifier = request.args.get('oauth_verifier')
    oauth_token = request.args.get('oauth_token')

    twitter = OAuth1Session(
        os.environ["API_KEY"],
        os.environ["API_SECRET_KEY"],
        oauth_token
    )

    res = twitter.post(
        token_endpoint,
        params={'oauth_verifier': oauth_verifier}
    )

    access_token = dict(parse.parse_qsl(res.content.decode("utf-8")))

    return jsonify(access_token)


if __name__ == "__main__":
    app.run(debug=True)
