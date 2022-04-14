# oauthcli

`oauthcli` is a developer productivity tool. It's helpful when juggling across multiple tech stacks and you need an OAuth `access_token` to make an API call, but you don't have a quick way to generate the `access_token`. Moreover, `oauthcli` uses standard python library and doesn't have any external dependencies.

## Installation

You can install `oauthcli` using python `pip`.

```shell
pip install oauthcli
```

**Please Note:** `oauthcli` runs a temporary local redirect server to capture authorization `code`, to generate `access_token`. To use this feature, you will have to modify `redirect_uri` to http://localhost:62884 for your application on the OAuth 2.0 server. You are not able to make this change then please [create a issue](https://github.com/aerohstudios/oauthcli/issues).

## Screenshots

Terminal Output

![terminal.png](/assets/terminal.png)

Browser Output

![browser.png](/assets/browser.png)

## Features

Supports custom OAuth 2.0 server endpoint, custom authorize, token URL, etc. For reference commands, check the [examples](#examples) section.

## Command Line Arguments

`-h`, `--help`
show this help message and exit


`--scope SCOPE`
OAuth 2.0 request scope


`--server SERVER`
OAuth 2.0 server endpoint


`--authorize_path AUTHORIZE_PATH`
OAuth 2.0 server authorize path. Default value: '/oauth/authorize'


`--token_path TOKEN_PATH`
OAuth 2.0 server token path. Default value: '/oauth/token'


`--client_id CLIENT_ID`
OAuth 2.0 Application Client ID


`--client_secret CLIENT_SECRET`
OAuth 2.0 Application Client Secret


`--credentials_file CREDENTIALS_FILE`
JSON file path with OAuth 2.0 Application Client ID & Secret

`--client_port CLIENT_PORT`
temporary port for client to receive authorization code. Default port is 62884. Configure OAuth 2.0 server to use http://localhost:<client_port> as redirect uri.

## Examples

### Quick & Dirty

Retrieve OAuth Access Token with the Client ID and Secret over command line. (less secure)

```shell
oauthcli --scope mobile \
--server http://localhost:3000/oauth/authorize \
--client_id=xQIGh0SbhoZPVJWbRud4ZH4ExAx6dfi86UEpV6zoOi \
--client_secret=qJ8IWyzqcJ6WTlZC5B5iKIlwpKoflbcL8YbpMESWHxM
```

### Client ID & Secret from file

Retrieve Oauth Access Token with client_id and client_secret stored in JSON file.

```shell
oauthcli --scope mobile \
--server http://localhost:3000/oauth/authorize \
--credentials_file=/tmp/oauth_app_credentails.json
```

JSON file format

```json
{
  "client_id": "xQIGh0SbhoZPVJWbRud4ZH4ExAx6dfi86UEpV6zoOis",
  "client_secret": "qJ8IWyzqcJ6WTlZC5B5iKIlwpKoflbcL8YbpMESWHxM"
}
```

### Custom URL Endpoints

```shell
oauthcli --scope mobile \
--server http://localhost:3000/oauth/authorize \
--credentials_file=/tmp/oauth_app_credentails.json \
--authorize_path=/oauth2/authorize \
--token_path=/oauth2/token
```

## Contributing

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](https://github.com/aerohstudios/oauthcli/issues)

We hope this tool is helpful for the community, and we'd love to hear how it helped solve your problem! If you want to contribute to this project by adding features or updating documentation, please create a pull request.