import requests
import time
import random

def post():
    # Your API endpoint URL
    url = "http://127.0.0.1:8000/shorten"

    # A list of 100 payloads (example data)
    payloads = [
    {
        "original_url": "https://google.com",
        "custom_alias": "rahulgoogle",
        "ttl": 0
    },
    {
        "original_url": "https://openai.com",
        "custom_alias": "rahulopenai",
        "ttl": 0
    },
    {
        "original_url": "https://linkedin.com",
        "custom_alias": "rahullinkedin",
        "ttl": 25
    },
    {
        "original_url": "https://twitter.com",
        "custom_alias": "rahultwitter",
        "ttl": 30
    },
    {
        "original_url": "https://stackoverflow.com",
        "custom_alias": "rahulstackoverflow",
        "ttl": 0
    },
    {
        "original_url": "https://medium.com",
        "custom_alias": "rahulmedium",
        "ttl": 0
    },
    {
        "original_url": "https://youtube.com",
        "custom_alias": "rahulyoutube",
        "ttl": 22
    },
    {
        "original_url": "https://netflix.com",
        "custom_alias": "rahulnetflix",
        "ttl": 28
    },
    {
        "original_url": "https://amazon.com",
        "custom_alias": "rahulamazon",
        "ttl": 35
    },
        {
        "original_url": "https://microsoft.com",
        "custom_alias": "rahulmicrosoft",
        "ttl": 40
    },
    {
        "original_url": "https://apple.com",
        "custom_alias": "rahulapple",
        "ttl": 0
    },
    {
        "original_url": "https://reddit.com",
        "custom_alias": "rahulreddit",
        "ttl": 22
    },
    {
        "original_url": "https://quora.com",
        "custom_alias": "rahulquora",
        "ttl": 0
    },
    {
        "original_url": "https://slack.com",
        "custom_alias": "rahulslack",
        "ttl": 27
    },
    {
        "original_url": "https://discord.com",
        "custom_alias": "rahuldiscord",
        "ttl": 0
    },
    {
        "original_url": "https://zoom.us",
        "custom_alias": "rahulzoom",
        "ttl": 21
    },
    {
        "original_url": "https://notion.so",
        "custom_alias": "rahulnotion",
        "ttl": 0
    },
    {
        "original_url": "https://figma.com",
        "custom_alias": "rahulfigma",
        "ttl": 24
    },
    {
        "original_url": "https://dribbble.com",
        "custom_alias": "rahuldribbble",
        "ttl": 33
    },
    {
        "original_url": "https://behance.net",
        "custom_alias": "rahulbehance",
        "ttl": 26
    },
    {
        "original_url": "https://coursera.org",
        "custom_alias": "rahulcoursera",
        "ttl": 29
    },
    {
        "original_url": "https://udemy.com",
        "custom_alias": "rahuludemy",
        "ttl": 32
    },
    {
        "original_url": "https://kaggle.com",
        "custom_alias": "rahulkaggle",
        "ttl": 0
    },
    {
        "original_url": "https://wikipedia.org",
        "custom_alias": "rahulwiki",
        "ttl": 0
    },
    {
        "original_url": "https://dev.to",
        "custom_alias": "rahuldevto",
        "ttl": 37
    },
    {
        "original_url": "https://hashnode.com",
        "custom_alias": "rahulhashnode",
        "ttl": 0
    },
    {
        "original_url": "https://gitlab.com",
        "custom_alias": "rahulgitlab",
        "ttl": 23
    },
    {
        "original_url": "https://bitbucket.org",
        "custom_alias": "rahulbitbucket",
        "ttl": 34
    },
    {
        "original_url": "https://pypi.org",
        "custom_alias": "rahulpypi",
        "ttl": 28
    },
        {
        "original_url": "https://spotify.com",
        "custom_alias": "rahulspotify",
        "ttl": 0
    },
    {
        "original_url": "https://soundcloud.com",
        "custom_alias": "rahulsoundcloud",
        "ttl": 27
    },
    {
        "original_url": "https://twitch.tv",
        "custom_alias": "rahultwitch",
        "ttl": 22
    },
    {
        "original_url": "https://hulu.com",
        "custom_alias": "rahulhulu",
        "ttl": 34
    },
    {
        "original_url": "https://disneyplus.com",
        "custom_alias": "rahuldisney",
        "ttl": 25
    },
    {
        "original_url": "https://primevideo.com",
        "custom_alias": "rahulprimevideo",
        "ttl": 28
    },
    {
        "original_url": "https://airbnb.com",
        "custom_alias": "rahulairbnb",
        "ttl": 21
    },
    {
        "original_url": "https://booking.com",
        "custom_alias": "rahulbooking",
        "ttl": 29
    },
    {
        "original_url": "https://tripadvisor.com",
        "custom_alias": "rahultrip",
        "ttl": 32
    },
    {
        "original_url": "https://uber.com",
        "custom_alias": "rahuluber",
        "ttl": 23
    },
    {
        "original_url": "https://lyft.com",
        "custom_alias": "rahullyft",
        "ttl": 0
    },
    {
        "original_url": "https://zomato.com",
        "custom_alias": "rahulzomato",
        "ttl": 0
    },
    {
        "original_url": "https://swiggy.com",
        "custom_alias": "rahulswiggy",
        "ttl": 35
    },
    {
        "original_url": "https://blinkit.com",
        "custom_alias": "rahulblinkit",
        "ttl": 26
    },
    {
        "original_url": "https://instacart.com",
        "custom_alias": "rahulinstacart",
        "ttl": 24
    },
    {
        "original_url": "https://flipkart.com",
        "custom_alias": "rahulflipkart",
        "ttl": 33
    },
    {
        "original_url": "https://snapdeal.com",
        "custom_alias": "rahulsnapdeal",
        "ttl": 31
    },
    {
        "original_url": "https://shopify.com",
        "custom_alias": "rahulshopify",
        "ttl": 36
    },
    {
        "original_url": "https://ebay.com",
        "custom_alias": "rahulebay",
        "ttl": 0
    },
    {
        "original_url": "https://aliexpress.com",
        "custom_alias": "rahulaliexpress",
        "ttl": 27
    },
    {
        "original_url": "https://temu.com",
        "custom_alias": "rahultemu",
        "ttl": 30
    },
    {
        "original_url": "https://shein.com",
        "custom_alias": "rahulshein",
        "ttl": 22
    },
    {
        "original_url": "https://nike.com",
        "custom_alias": "rahulnike",
        "ttl": 0
    },
    {
        "original_url": "https://adidas.com",
        "custom_alias": "rahuladidas",
        "ttl": 25
    },
    {
        "original_url": "https://puma.com",
        "custom_alias": "rahulpuma",
        "ttl": 28
    },
    {
        "original_url": "https://underarmour.com",
        "custom_alias": "rahulua",
        "ttl": 29
    },
    {
        "original_url": "https://livescore.com",
        "custom_alias": "rahullivescore",
        "ttl": 26
    },
    {
        "original_url": "https://espn.com",
        "custom_alias": "rahulespn",
        "ttl": 23
    },
    {
        "original_url": "https://fifa.com",
        "custom_alias": "rahulfifa",
        "ttl": 0
    },
    {
        "original_url": "https://cricbuzz.com",
        "custom_alias": "rahulcricbuzz",
        "ttl": 0
    },  {
        "original_url": "https://imdb.com",
        "custom_alias": "rahulimdb",
        "ttl": 21
    },
    {
        "original_url": "https://rottentomatoes.com",
        "custom_alias": "rahultomatoes",
        "ttl": 25
    },
    {
        "original_url": "https://goodreads.com",
        "custom_alias": "rahulgoodreads",
        "ttl": 28
    },
    {
        "original_url": "https://archive.org",
        "custom_alias": "rahularchive",
        "ttl": 0
    },
    {
        "original_url": "https://gutenberg.org",
        "custom_alias": "rahulgutenberg",
        "ttl": 30
    },
    {
        "original_url": "https://openlibrary.org",
        "custom_alias": "rahulopenlib",
        "ttl": 23
    },
    {
        "original_url": "https://deezer.com",
        "custom_alias": "rahuldeezer",
        "ttl": 26
    },
    {
        "original_url": "https://bandcamp.com",
        "custom_alias": "rahulbandcamp",
        "ttl": 32
    },
    {
        "original_url": "https://pandora.com",
        "custom_alias": "rahulpandora",
        "ttl": 0
    },
    {
        "original_url": "https://last.fm",
        "custom_alias": "rahullastfm",
        "ttl": 34
    },
    {
        "original_url": "https://bbc.com",
        "custom_alias": "rahulbbc",
        "ttl": 0
    },
    {
        "original_url": "https://cnn.com",
        "custom_alias": "rahulcnn",
        "ttl": 27
    },
    {
        "original_url": "https://nytimes.com",
        "custom_alias": "rahulnytimes",
        "ttl": 22
    },
    {
        "original_url": "https://forbes.com",
        "custom_alias": "rahulforbes",
        "ttl": 0
    },
    {
        "original_url": "https://bloomberg.com",
        "custom_alias": "rahulbloomberg",
        "ttl": 36
    },
    {
        "original_url": "https://reuters.com",
        "custom_alias": "rahulreuters",
        "ttl": 24
    },
    {
        "original_url": "https://washingtonpost.com",
        "custom_alias": "rahulwapo",
        "ttl": 29
    },
    {
        "original_url": "https://theguardian.com",
        "custom_alias": "rahulguardian",
        "ttl": 26
    },
    {
        "original_url": "https://economist.com",
        "custom_alias": "rahuleconomist",
        "ttl": 30
    },
    {
        "original_url": "https://time.com",
        "custom_alias": "rahultime",
        "ttl": 0
    },
    {
        "original_url": "https://nationalgeographic.com",
        "custom_alias": "rahulnatgeo",
        "ttl": 25
    },
    {
        "original_url": "https://history.com",
        "custom_alias": "rahulhistory",
        "ttl": 21
    },
    {
        "original_url": "https://discovery.com",
        "custom_alias": "rahuldiscovery",
        "ttl": 23
    },
    {
        "original_url": "https://nasa.gov",
        "custom_alias": "rahulnasa",
        "ttl": 33
    },
    {
        "original_url": "https://esa.int",
        "custom_alias": "rahulesa",
        "ttl": 0
    },
    {
        "original_url": "https://spacex.com",
        "custom_alias": "rahulspacex",
        "ttl": 27
    },
    {
        "original_url": "https://blueorigin.com",
        "custom_alias": "rahulblueorigin",
        "ttl": 24
    },
    {
        "original_url": "https://tesla.com",
        "custom_alias": "rahultesla",
        "ttl": 35
    },
    {
        "original_url": "https://ford.com",
        "custom_alias": "rahulford",
        "ttl": 22
    },
    {
        "original_url": "https://bmw.com",
        "custom_alias": "rahulbmw",
        "ttl": 28
    },
    {
        "original_url": "https://mercedes-benz.com",
        "custom_alias": "rahulbenz",
        "ttl": 31
    },
    {
        "original_url": "https://audi.com",
        "custom_alias": "rahulaudi",
        "ttl": 26
    },
    {
        "original_url": "https://toyota.com",
        "custom_alias": "rahultoyota",
        "ttl": 0
    },
    {
        "original_url": "https://honda.com",
        "custom_alias": "rahulhonda",
        "ttl": 23
    },
    {
        "original_url": "https://suzuki.com",
        "custom_alias": "rahulsuzuki",
        "ttl": 0
    },
    {
        "original_url": "https://harley-davidson.com",
        "custom_alias": "rahulharley",
        "ttl": 29
    },
    {
        "original_url": "https://royalenfield.com",
        "custom_alias": "rahulre",
        "ttl": 21
    },
    {
        "original_url": "https://kawasaki.com",
        "custom_alias": "rahulkawasaki",
        "ttl": 27
    },
    {
        "original_url": "https://yamaha-motor.com",
        "custom_alias": "rahulyamaha",
        "ttl": 32
    }
    ]

    # Set the headers
    headers = {'Content-Type': 'application/json'}

    for payload in payloads:
        try:
            # Pass the headers directly to the post method
            time.sleep(0.3)
            response = requests.post(url, json=payload, headers=headers)
            
            print(f"Status Code: {response.status_code}")
            
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
# post()

def get(limit=10):
    url = "http://127.0.0.1:8000/"

    short_ids = [
        'rahulgit', 'rahulgoogle', 'rahulopenai', 'rahullinkedin', 'rahultwitter', 'rahulstackoverflow', 'rahulmedium', 'rahulyoutube', 'rahulnetflix', 'rahulamazon', 'rahulmicrosoft', 'rahulapple', 'rahulreddit', 'rahulquora', 'rahulslack', 'rahuldiscord', 'rahulzoom', 'rahulnotion', 'rahulfigma', 'rahuldribbble', 'rahulbehance', 'rahulcoursera', 'rahuludemy', 'rahulkaggle', 'rahulwiki', 'rahuldevto', 'rahulhashnode', 'rahulgitlab', 'rahulbitbucket', 'rahulpypi', 'rahulspotify', 'rahulsoundcloud', 'rahultwitch', 'rahulhulu', 'rahuldisney', 'rahulprimevideo', 'rahulairbnb', 'rahulbooking', 'rahultrip', 'rahuluber', 'rahullyft', 'rahulzomato', 'rahulswiggy', 'rahulblinkit', 'rahulinstacart', 'rahulflipkart', 'rahulsnapdeal', 'rahulshopify', 'rahulebay', 'rahulaliexpress', 'rahultemu', 'rahulshein', 'rahulnike', 'rahuladidas', 'rahulpuma', 'rahulua', 'rahullivescore', 'rahulespn', 'rahulfifa', 'rahulcricbuzz', 'rahulimdb', 'rahultomatoes', 'rahulgoodreads', 'rahularchive', 'rahulgutenberg', 'rahulopenlib', 'rahuldeezer', 'rahulbandcamp', 'rahulpandora', 'rahullastfm', 'rahulbbc', 'rahulcnn', 'rahulnytimes', 'rahulforbes', 'rahulbloomberg', 'rahulreuters', 'rahulwapo', 'rahulguardian', 'rahuleconomist', 'rahultime', 'rahulnatgeo', 'rahulhistory', 'rahuldiscovery', 'rahulnasa', 'rahulesa', 'rahulspacex', 'rahulblueorigin', 'rahultesla', 'rahulford', 'rahulbmw', 'rahulbenz', 'rahulaudi', 'rahultoyota', 'rahulhonda', 'rahulsuzuki', 'rahulharley', 'rahulre', 'rahulkawasaki', 'rahulyamaha'
    ]

    for _ in range(limit):
        try:
            # Pick a random short_id
            short_id = random.choice(short_ids)
            new_url = url + short_id

            # Sleep for a random time between 0.0 and 0.5 seconds
            time.sleep(random.uniform(0.0, 0.2))

            # Send request
            response = requests.get(new_url)

            # Print the status code
            print(f"URL: {new_url} | Status Code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

get(1000)