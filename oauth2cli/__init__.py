#!/usr/bin/env python

import argparse
from urllib.parse import urlsplit, urlunsplit, parse_qsl, parse_qs, urlencode
from urllib.request import Request, urlopen
import socketserver
import json
import webbrowser
import os

schemeIndex = 0
locationIndex = 1
pathIndex = 2
queryStringIndex = 3
fragmentIndex = 4


def parse_args():
    parser = argparse.ArgumentParser(description="Generic OAuth 2.0 command line utility to retrive access tokens.")
    parser.add_argument('--scope', help='OAuth 2.0 request scope. (Required)', required=True)
    parser.add_argument('--server', help='OAuth 2.0 server endpoint. (Required)', required=True)
    parser.add_argument('--authorize_path', help="OAuth 2.0 server authorize path Default value: '/oauth/authorize'", default='/oauth/authorize')
    parser.add_argument('--token_path', help="OAuth 2.0 server token path Default value: '/oauth/token'", default='/oauth/token')
    parser.add_argument('--client_id', help='OAuth 2.0 Application Client ID')
    parser.add_argument('--client_secret', help='OAuth 2.0 Application Client Secret')
    parser.add_argument('--credentials_file', help='JSON file path with OAuth 2.0 Application Client ID & Secret')
    parser.add_argument('--redirect_uri', help="Override Redirect URI. Use it if your OAuth 2.0 Server doesn't support non-ssl/localhost URIs in the redirect URL.\nYou will be able to manually copy authorization code from the web browser and paste it on command line with this option.")
    parser.add_argument('--client_port', help="temporary port for client to receive authorization code. Default port is 62884.\nConfigure OAuth 2.0 server to use http://localhost:<client_port> as redirect uri.", default=62884)

    version = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'VERSION')).read().strip()
    parser.add_argument('--version', action='version', version='%(prog)s v{}'.format(version), help="Show oauth2cli version")

    global args
    args = parser.parse_args()

def get_client_id():
    if args.client_id:
        return args.client_id
    elif args.credentials_file:
        return json.load(open(args.credentials_file))['client_id']
    else:
        raise Exception("client_id not found")

def get_client_secret():
    if args.client_secret:
        return args.client_secret
    elif args.credentials_file:
        return json.load(open(args.credentials_file))['client_secret']
    else:
        raise Exception("client_secret not found")

def print_and_http_write(handler, message):
    print(message, end="")
    handler.write(message.encode())

def get_redirect_uri():
    if args.redirect_uri:
        print("using redirect_uri from options")
        return args.redirect_uri
    else:
        print("using redirect_uri localhost")
        return "http://localhost:{}".format(args.client_port)

class OAuthRedirectHandler(socketserver.StreamRequestHandler):
    def handle(self):
        endOfHeaders = False
        headers = []
        while not endOfHeaders:
            msg = self.rfile.readline().strip().decode("utf-8")
            headers.append(msg)
            if msg == '':
                endOfHeaders = True

        self.wfile.write("HTTP/1.1 200 OK\nContent-Type: text/plain; charset=utf-8\n\n".encode())

        params = parse_qs(urlsplit(headers[0].split()[1])[3])
        if 'code' in params:
            print_and_http_write(self.wfile, "Got code\n")
            code = params['code'][0]
            print_and_http_write(self.wfile, "code = {0}\n\n".format(code))

            print_and_http_write(self.wfile, "Retriving Access Token...\n")

            response_dict = process_code(code)

            print_and_http_write(self.wfile, "\nGot Access Token\n")

            for key in response_dict.keys():
                print_and_http_write(self.wfile, "{0} = {1}\n".format(key, response_dict[key]))
        else:
            print_and_http_write(self.wfile, "Failed!\ncode not found in the request!\n")

def process_code(code):
    token_url = create_token_url(code)
    request = Request(token_url, method='POST')
    response = urlopen(request)
    return json.loads(response.read().decode("utf-8"))

def create_authorize_url():
    print("Generating Authorize URL...")
    authorizeParams = ['scope', 'client_id', 'client_secret', 'redirect_uri', 'response_type']

    parts = list(urlsplit(args.server))
    parts[pathIndex] = args.authorize_path
    queryString = parts[queryStringIndex]
    queryStringList = parse_qsl(queryString)
    editedQueryStringList = list(filter(lambda queryStringPair: queryStringPair[0] not in authorizeParams, queryStringList))
    editedQueryStringList.append(('scope', args.scope))
    editedQueryStringList.append(('client_id', get_client_id()))
    editedQueryStringList.append(('client_secret', get_client_secret()))
    editedQueryStringList.append(('redirect_uri', get_redirect_uri()))
    editedQueryStringList.append(('response_type', 'code'))
    newQueryString = urlencode(editedQueryStringList)
    parts[queryStringIndex] = newQueryString
    authorize_url = urlunsplit(parts)
    print("Authorize URL: {}".format(authorize_url))
    print("Opening web browser...\n")
    webbrowser.open(authorize_url)
    return authorize_url

def create_token_url(code):
    createTokenParams = ['client_id', 'client_secret', 'code', 'grant_type', 'redirect_uri']

    parts = list(urlsplit(args.server))
    parts[pathIndex] = args.token_path
    queryString = parts[queryStringIndex]
    queryStringList = parse_qsl(queryString)
    editedQueryStringList = list(filter(lambda queryStringPair: queryStringPair[0] not in createTokenParams, queryStringList))
    editedQueryStringList.append(('client_id', get_client_id()))
    editedQueryStringList.append(('client_secret', get_client_secret()))
    editedQueryStringList.append(('code', code))
    editedQueryStringList.append(('grant_type', 'authorization_code'))
    editedQueryStringList.append(('redirect_uri', get_redirect_uri()))
    newQueryString = urlencode(editedQueryStringList)
    parts[queryStringIndex] = newQueryString
    token_url = urlunsplit(parts)
    print("Token URL: {}".format(token_url))
    return token_url

def run_oauth_redirect_server():
    server = socketserver.TCPServer(("127.0.0.1", args.client_port), OAuthRedirectHandler, bind_and_activate=False)
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    server.timeout = 3000
    server.handle_request()

def main():
    parse_args()
    create_authorize_url()
    if args.redirect_uri:
        code = input('Copy the Authorization Code from the web browser, paste it here and press ENTER: ')
        response_dict = process_code(code)
        for key in response_dict.keys():
            print("{0} = {1}".format(key, response_dict[key]))
    else:
        run_oauth_redirect_server()

if __name__ == "__main__":
    main()
