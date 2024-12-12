import requests
from datetime import datetime

def generate_rss():
    # API URL
    api_url = "https://api.fnugg.no/search?index=blog&facet=site:12&sort=date:desc"

    # Hent data fra API
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception("Kan ikke hente data fra API")

    data = response.json()

    # Generer RSS-XML
    rss_items = ""
    for item in data.get("hits", []):
        title = item.get("title", "Ingen tittel")
        link = item.get("url", "#")
        description = item.get("description", "Ingen beskrivelse")
        pub_date = item.get("date", datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000"))

        rss_items += f"""
        <item>
            <title>{title}</title>
            <link>{link}</link>
            <description>{description}</description>
            <pubDate>{pub_date}</pubDate>
        </item>
        """

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
      <channel>
        <title>Fnugg Blogg RSS</title>
        <link>https://api.fnugg.no</link>
        <description>Oppdaterte blogginnlegg fra Fnugg</description>
        {rss_items}
      </channel>
    </rss>"""

    # Lagre RSS som fil
    with open("feed.xml", "w", encoding="utf-8") as file:
        file.write(rss_feed)

if __name__ == "__main__":
    generate_rss()
