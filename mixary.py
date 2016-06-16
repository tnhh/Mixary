import base64
import ConfigParser
import random
import requests
import subprocess
import urllib
import os

"""
	Mixary v4.0.0
	(C) 2014 - 2016 Luke Hutton
"""

MARKET = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
random = random.SystemRandom()

auth_token = ""
auth_header = {}

def get_auth():
	global auth_token, auth_header

	auth_url = "https://accounts.spotify.com/api/token"

	auth_header = "Basic %s" % (base64.b64encode("%s:%s" % (CLIENT_ID, CLIENT_SECRET)))
	auth_params = {'grant_type': "client_credentials"}
	auth_headers = {'Authorization': auth_header}

	r = requests.post(auth_url, data=auth_params, headers=auth_headers)
        if (r.status_code == requests.codes.ok):
            auth_token = r.json()["access_token"]
            auth_header = {'Authorization': "Bearer %s" % auth_token}
            return auth_token
        else:
            r.raise_for_status()

def do_song_search(artist,title):
	search_url = "https://api.spotify.com/v1/search"
	search_params="limit=10&market=%s&type=track&q=artist:%s+track:%s" % (MARKET, urllib.quote(artist), urllib.quote(title))

	results = requests.get(search_url,params=search_params)
        if (results.status_code == requests.codes.ok):
	    j_results = results.json()

	    return j_results
        else:
            results.raise_for_status()


"""
	Queries Spotify recc API to return a random similar song to the given seed(s)
"""
def get_song_recs(seed,last_song):
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

	for tune in tuned:
		params["min_%s" % tune] = tuned[tune][0]
		params["max_%s" % tune] = tuned[tune][1]

	while True:	
		r = requests.get(url, params=params, headers=auth_header)
		results = r.json()
                if (r.status_code == requests.codes.ok):

                    if(len(results['tracks']) == 0):
                            while True:
                                    to_remove = random.choice(tuneables)
                                    if "min_%s" % to_remove in params:
                                            del params["min_%s" % to_remove]
                                            del params["max_%s" % to_remove]
                                            break
                    else:
                            rec = random.choice(results['tracks'])
                            if rec['artists'][0]['id'] == last_song['artists'][0]['id']:
                                    return None
                            return rec
                else:
                    r.raise_for_status()

def set_paste_data(data):
        p = None

        try:
	    # macs use pbcopy
            p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        except OSError as err:
            if err.errno == os.errno.ENOENT:
                # no pbcopy? let's look for xclip
                p = subprocess.Popen(['xclip', '-sel', 'clip'], stdin=subprocess.PIPE)

        if p is not None:
            p.stdin.write(data)
            p.stdin.close()
            wait = p.wait()

def read_config():
	global MARKET, CLIENT_SECRET, CLIENT_ID
	config = ConfigParser.ConfigParser()

	config.read("config")
	MARKET = config.get("mixary","market")
	CLIENT_SECRET = config.get("mixary","spotify_secret")
	CLIENT_ID = config.get("mixary","spotify_id")

if __name__ == "__main__":
	read_config()
	get_auth()
	

	print "Mixary"
	print "=====\n"

	while True:

		artist = raw_input("Enter an artist: ")

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

		if(len(songs['tracks']['items']) == 0):
			print "No search results"
			continue

		while True:
			track_no = int(raw_input("Make playlist from which track? [1]: ") or 1)
			if track_no not in range(1,(len(songs['tracks']['items'])+1)):
				print "Invalid track number"
				continue
			else:
				break




		#print songs['tracks']
		seed = songs['tracks']['items'][track_no - 1]
		track_id = seed['id']

		playlist = [seed]
		break_play = False
		last_song = seed

		print "\n ----- \n Getting playlist. Hold tight! \n -----"
		print "[1] %s - %s" % (seed['artists'][0]['name'], seed['name'])
		while True:
			new_rec = get_song_recs(track_id,last_song)
			if new_rec == None:
				continue
			
			# check for duplicate artists
			for song in playlist:
				if new_rec['artists'][0]['id'] == song['artists'][0]['id']:
					break_play = True
					break
			
			if break_play:
				break
			playlist.append(new_rec)
			last_song = new_rec
			track_id = new_rec['id']
			print "[%s] %s - %s" % (len(playlist), new_rec['artists'][0]['name'], new_rec['name']) 


		print "Playlist done (%s songs)" % (len(playlist))

		# build playlist url
		trackset = ""
		for song in playlist:
			if trackset == "":
				trackset = song['id']	
			else:
				trackset = "%s,%s" % (trackset, song['id'])

		build_url = "http://open.spotify.com/trackset/Mixed by Mixary/%s?autoplay=1" % trackset
		print "\n ==== \n Playlist in clipboard: %s \n ====" % build_url

		set_paste_data(build_url)
		break



