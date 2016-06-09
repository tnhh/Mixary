import base64
import curses
import random
import requests
import urllib

"""
	Mixary v4.0.0
	(C) Luke Hutton
"""

MARKET = "GB"
CLIENT_ID = "1cc247b90dfc49d8b3c04b81e7dd7558"
CLIENT_SECRET = "3427491d67934770950f4cb315e4fba1"
random = random.SystemRandom()

auth_token = ""
auth_header = {}

def get_auth():
	global auth_token, auth_header

	auth_url = "https://accounts.spotify.com/api/token"

	auth_header = "Basic %s" % (base64.b64encode("%s:%s" % (CLIENT_ID, CLIENT_SECRET)))
	auth_params = {'grant_type': "client_credentials"}
	auth_headers = {'Authorization': auth_header}

	#print auth_header
	r = requests.post(auth_url, data=auth_params, headers=auth_headers)

	#print r.json()
	auth_token = r.json()["access_token"]
	auth_header = {'Authorization': "Bearer %s" % auth_token}
	#print auth_header
	return auth_token



def do_song_search(artist,title):
	search_url = "https://api.spotify.com/v1/search"
	search_params="limit=10&market=%s&type=track&q=artist:%s+track:%s" % (MARKET, urllib.quote(artist), urllib.quote(title))

	#search_params = {"q": "artist:%s&track=%s" % (artist, title),
	#			 "type": "track",
	#			 "market": "GB"}

	results = requests.get(search_url,params=search_params)
	j_results = results.json()

	return j_results


"""
	Queries Spotify recc API to return a random similar song to the given seed(s)
"""
def get_song_recs(seed):
	url = "https://api.spotify.com/v1/recommendations"
	params = 	{"market": MARKET,
			 "seed_tracks": seed,
			 "limit": 100}


	tuneables = ["acousticness", "danceability", "energy", "instrumentalness", "liveness",
	"loudness", "speechiness", "valence", "popularity"]

	tuned = {}

	while True:
		to_tune = random.choice(tuneables)
		if to_tune in tuned:
			break
		else:
			tune_min, tune_max = random.random(), random.random()
		if to_tune == "popularity":
			tune_min, tune_max = int(tune_min*100), int(tune_max*100)
		if tune_min > tune_max:
			continue
		else:
			tuned[to_tune] = [tune_min,tune_max]

	#print tuned
	for tune in tuned:
		params["min_%s" % tune] = tuned[tune][0]
		params["max_%s" % tune] = tuned[tune][1]

	print params

	while True:	
		r = requests.get(url, params=params, headers=auth_header)
		results = r.json()

		print "Got %s results" % len(results['tracks'])
		if(len(results['tracks']) == 0):
			while True:
				to_remove = random.choice(tuneables)
				if "min_%s" % to_remove in params:
					print "pruning %s and trying search again" % to_remove
					del params["min_%s" % to_remove]
					del params["max_%s" % to_remove]
					break
		else:
			rec = random.choice(results['tracks'])



def make_playlist(seed_id):
	print "Making your playlist now!"





if __name__ == "__main__":
	get_auth()

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
		track_no = int(raw_input("Make playlist from which track? [1]: ")) or 1

		#print songs['tracks']
		track_id = songs['tracks']['items'][track_no - 1]['id']

		playlist = [songs['tracks']['items'][track_no - 1]]
		while True:
			new_rec = get_song_recs(track_id)
			
			# check for duplicate artists
			for song in playlist:
				if new_rec['artists'][0]['id'] == song['artists'][0]['id']:
					break

			playlist.append(new_rec)
			track_id = new_rec['id']


		print "Playlist done (%s songs)" % (len(playlist))



