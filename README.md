# Mixary

Mixary is a CLI tool for generating Spotify playlists based on a given seed song.

## Requirements

Python 2.6+. Run `pip install -r requirements.txt` to install any external requirements.

## Configuration

Write a file called `config` using `example_config` as a guide:

* `market`: an ISO 3166-1 alpha-2 country code, such as "GB" or "US", to ensure only songs available
in your locale are returned.

* `spotify_id`: Go to <https://developer.spotify.com/my-applications/#!/applications> and create
an app, or using an existing app, get the Client ID

* `spotify_secret`: Go to <https://developer.spotify.com/my-applications/#!/applications> and create
an app, or using an existing app, get the Client Secret

## Usage

Run `python mixary.py` and enter an artist/song title when prompted. Mixary will search for matching
songs, and let you choose which of the results to use as the seed.

Mixary will then generate a playlist based on this seed ID. Playlists are generative, meaning that as songs
are added, they influence the direction of the playlist rather than the seed song alone. Unlike some other
playlist generators, more obscure/left-field songs are also surfaced to promote discovery.

A URL to the generated playlist is given (on macOS this copied to the clipboard). Pasting this in a browser
will launch the playlist in Spotify.

## Notes

This is based on previous work with [Spotipath](https://github.com/barneyboo/spotipath) and Mixary.
This was hastily rewritten following the closure of the Echo Nest API. The playlist generation is less
sophisticated because the Spotify API just isn't as good as Echo Nest for this, but at least it does something. This is also super barebones/ugly just to experiment with the playlist logic. I'll probably stick this behind a prettier website soon to make it more accessible...


