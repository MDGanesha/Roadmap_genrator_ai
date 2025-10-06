from googleapiclient.discovery import build

# replace with your actual API key
YOUTUBE_API_KEY = "AIzaSyADu7QTH71OOYzl3e76ek4roxfC9llcuJc"

def search_youtube(query: str, max_results=3):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    request = youtube.search().list(
        q=query,
        part="snippet",
        type="video",
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({"title": title, "url": url})

    return videos

if __name__ == "__main__":
    results = search_youtube("Learn Python for beginners")
    for r in results:
        print(r)
