import vlc
import glob
import os
import json
import asyncio
import random
import websockets
import urllib.parse

class CanoeAmbientServer():
    def __init__(self):
        print("Starting Canoe Ambient Server")
        self.startPlayer()
        self.startServer()

    def startPlayer(self):
        # Create Player
        self.mediaListPlayer = vlc.MediaListPlayer()
        self.mediaListPlayer.set_playback_mode(vlc.PlaybackMode.loop)
        # Load Json
        self.json_file = ('.\Chart.json')
        self.json_obj = json.load(open(self.json_file))
        # Create MEdia List
        self.createMediaList()

    def getPlaylist(self):
        playlist = []
        for song in self.playlist:
            playlist += [os.path.basename(song)]
        return playlist

    def createMediaList(self):
        self.mediaListPlayer.stop()
        # Get And Shuffle Tracks
        self.playlist = glob.glob('.\\Lib\*')
        random.shuffle(self.playlist)
        # Print Trax
        for song in self.playlist:
            print (song)
        # Set Media List
        self.mediaList = vlc.MediaList(self.playlist)
        self.mediaListPlayer.set_media_list(self.mediaList)
        self.mediaListPlayer.play()

    async def serve(self,websocket, path):
        while True:
            msg = await websocket.recv()
            print(msg,websocket,path)
            ip = websocket.remote_address[0]

            currTrack = self.getCurrentMrl()
            if msg == 'next':
                self.mediaListPlayer.next()
            if msg == 'like':
                self.setLike(ip, currTrack, 1);
            if msg == 'dis':
                self.setLike(ip, currTrack, -1);
            if msg == 'play':
                self.mediaListPlayer.play()
            if msg == 'pause':
                self.mediaListPlayer.pause()
            if msg == 'previous':
                self.mediaListPlayer.previous()

            volume_delta = 25
            if msg == 'volume_up':
                self.mediaListPlayer.get_media_player().audio_set_volume(
                    self.mediaListPlayer.get_media_player().audio_get_volume() + volume_delta)
            if msg == 'volume_down':
                self.mediaListPlayer.get_media_player().audio_set_volume(
                    self.mediaListPlayer.get_media_player().audio_get_volume() - volume_delta)
            if msg == 'volume_100':
                self.mediaListPlayer.get_media_player().audio_set_volume( 100 )
            if msg.startswith("set_volume"):
                self.mediaListPlayer.get_media_player().audio_set_volume(int(msg.split(":")[1]))
            if msg == 'get_info':
                curr_track = os.path.basename(currTrack)
                curr_volume = self.mediaListPlayer.get_media_player().audio_get_volume()
                stats = self.getStats(curr_track)
                my_rate = self.getMyRate(curr_track,ip)
                playlist = self.getPlaylist()
                curr_track = urllib.parse.unquote(curr_track)
                info = json.dumps({'track':curr_track,"volume":curr_volume,"stats":stats,"my":my_rate,"playlist":playlist})
                await websocket.send(info)
            if msg == 'restart_player':
                self.createMediaList()

    def getStats(self,song_name):
        if song_name in  self.json_obj:
            if "total" in self.json_obj[song_name]:
                return  self.json_obj[song_name]["total"]
        return  {"likes":0,"dislikes":0,"score":0}

    def getMyRate(self,song_name,ip):
        if song_name in self.json_obj:
            if ip in self.json_obj[song_name]:
                return self.json_obj[song_name][ip]
        return 0

    def startServer(self):
        start_server = websockets.serve(self.serve, '192.168.0.23', 50000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    def setLike(self,ip,song,like):
        song_name = os.path.basename(song)
        #print(ip,song_name,like)

        if song_name not in  self.json_obj:
            self.json_obj[song_name] = dict()

        if ip not in self.json_obj[song_name]:
            self.json_obj[song_name][ip] = like
        self.json_obj[song_name][ip] = like

        diss = 0
        likes = 0
        score = 0
        for key in self.json_obj[song_name].keys():
            if key != "total":
                val = self.json_obj[song_name][key]
                score += val
                if val == 1: likes += 1
                if val == -1: diss += 1

        self.json_obj[song_name]['total'] = {"likes":likes,"dislikes":diss,"score":score}

        with open(self.json_file, 'w') as outfile:
            json.dump(self.json_obj, outfile, sort_keys=True, indent=4, separators=(',', ': '))
        print("updated")

    def getCurrentMrl(self):
        return self.mediaListPlayer.get_media_player().get_media().get_mrl()

CanoeAmbientServer()