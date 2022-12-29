# Usage

This package provides an interface to a Reddit bot
that complies with the **kilroy** face API.

It assumes that you have a dedicated subreddit for your bot to post to.

## Prerequisites

You need to create a Reddit app and get the following credentials:
- `client_id`
- `client_secret`
- `refresh_token`
- `user_agent`

You also need to create a subreddit for your bot to post to and get its name.

You need to pass all this info to the server,
either as environment variables, command line arguments
or entries in a configuration file.

For example, you can do this:

```sh
export KILROY_FACE_REDDIT_FACE__CLIENT_ID="Paste your client id here"
export KILROY_FACE_REDDIT_FACE__CLIENT_SECRET="Paste your client secret here"
export KILROY_FACE_REDDIT_FACE__REFRESH_TOKEN="Paste your refresh token here"
export KILROY_FACE_REDDIT_FACE__USER_AGENT="Paste your user agent here"
export KILROY_FACE_REDDIT_FACE__SUBREDDIT="Paste your subreddit name here"
```

## Running the server

To run the server, install the package and run the following command:

```sh
kilroy-face-reddit
```

This will start the face server on port 10002 by default.
Then you can communicate with the server, for example by using
[this package](https://github.com/kilroybot/kilroy-face-client-py-sdk).
