import os
import tweepy
from dotenv import load_dotenv

load_dotenv()

def publicar_tweet(texto: str) -> bool:
    """Publica un tweet usando la API v2 de Twitter."""
    try:
        client = tweepy.Client(
            consumer_key=os.getenv("TWITTER_API_KEY"),
            consumer_secret=os.getenv("TWITTER_KEY_SECRET"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        )

        response = client.create_tweet(text=texto)
        print(f"Tweet publicado: {response.data['id']}")
        return True
    except tweepy.TweepyException as e:
        print(f"Error al publicar tweet: {e}")
        return False