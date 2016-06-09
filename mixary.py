import curses
import requests
import urllib

"""
	Mixary v4.0.0
	(C) Luke Hutton
"""

MARKET = "GB"

def do_song_search(artist,title):
	search_url = "https://api.spotify.com/v1/search"
	search_params="limit=10&market=%s&type=track&q=artist:%s+track:%s" % (MARKET, urllib.quote(artist), urllib.quote(title))

	#search_params = {"q": "artist:%s&track=%s" % (artist, title),
	#			 "type": "track",
	#			 "market": "GB"}

	results = requests.get(search_url,params=search_params)
	j_results = results.json()

	return j_results

def make_playlist(seed_id):
	print "Making your playlist now!"





if __name__ == "__main__":
	print "Mixary"
	print "====\n"

	artist = raw_input("Enter an artist (or Spotify track id beginning 'spotify:track:'): ")
	if "spotify:track:" not in artist:
		title = raw_input("Enter a song name by %s: " % artist)

		songs = do_song_search(artist,title)

		print "\nSEARCH RESULTS"
		print "--------------"
		track_count = 1
		for track in songs['tracks']['items']:
			print "[%s] %s - %s" % (track_count, track['artists'][0]['name'], track['name'])
			track_count += 1

		print ""
		track_no = raw_input("Make playlist from which track? [1]: ") or 1

		track_id = songs['tracks'][track_no - 1]['id']



