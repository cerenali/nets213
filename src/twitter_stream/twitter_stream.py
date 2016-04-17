from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json

API_key= "CwwBYTbmw0tFkbItf1OvzXORs"
API_secret = "aZEAIW9XMwopvTpzU2J1gzhTltxtmdn76FpcOl6thhha369W2J"
access_token = "717091878693433344-XP7XhXspqumiWTTs1bvLnPdOew2OuOC"
access_token_secret = "DHlKirghxuw4WSsi6TECzJZrEcngfVUudcYqHNF4o3C6q"

class StdOutListener(StreamListener):
	def on_data(self, data) :
		print data
		return True

	def on_error(self, status):
		print status

if __name__ == '__main__':
	l = StdOutListener()
	auth = OAuthHandler(API_key, API_secret)
	auth.set_access_token(access_token, access_token_secret)
	stream = Stream(auth, l)
	stream.filter(locations=[-124.848974, 24.396308, -66.885444, 49.384358], languages=['en'])
