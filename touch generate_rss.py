import requests
from datetime import datetime

# API URL
api_url = "https://api.fnugg.no/search?index=blog&facet=site:12"

def generate_rss():
    # Hent data fra API
    response = requests.get(api_url)
    response.raise_for_status()  # Feil hvis API-kallet mislykkes
    data = response.json()

    # Bygg RSS-feed
    items = ""
    for entry in data.get("hits", {}).get("hits", []):
        source = entry.get("_source", {})
        title = source.get("title", "Ingen tittel")
        description = source.get("description", "Ingen beskrivelse")
        link = source.get("images", {}).get("image_full", "#")
        pub_date = datetime.strptime(source["date"], "%Y-%m-%dT%H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S +0000")
        author = f'{source.get("author", {}).get("first_name", "")} {source.get("author", {}).get("last_name", "")}'

        items += f"""
        <item>
            <title>{title}</title>
            <link>{link}</link>
            <description><![CDATA[{description}]]></description>
            <author>{author}</author>
            <pubDate>{pub_date}</pubDate>
        </item>
        """

    # Lag RSS-struktur
    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
        <channel>
            <title>Fnugg Blogg RSS</title>
            <link>https://fnugg.no</link>
            <description>Oppdateringer fra Fnugg Blogg</description>
            <language>no</language>
            {items}
        </channel>
    </rss>"""

    # Lagre RSS som en XML-fil
    with open("rss.xml", "w", encoding="utf-8") as file:
        file.write(rss_feed)
    print("RSS feed generated successfully!")

if __name__ == "__main__":
    generate_rss()
