
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
        self.startServer()

    async def serve(self,websocket, path):
        while True:
            msg = await websocket.recv()
            print(msg,websocket,path)
            ip = websocket.remote_address[0]

            if msg == 'like':
                self.setLike(ip, currTrack, 1);


    def startServer(self):
        start_server = websockets.serve(self.serve, "localhost", 8000)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


CanoeAmbientServer()