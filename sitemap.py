#!/c/Python38/python

import sys


SITEMAP_HEADER = """<?xml version="1.0" encoding="utf-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">"""

SITEMAP_FOOTER = """
</urlset>
"""


def load_urls(links_file):
  urls = None
  
  with open(links_file) as file:
    urls = [line for line in file.read().split('\n') if line != '']

  return urls


def create_url_element(url):
  element = f"""
  <url>
    <loc>{url}</loc>
    <changefreq>daily</changefreq>
  </url>"""

  return element


def save_sitemap(url_elements):
  with open('sitemap.xml', 'w') as xml:
    xml.write(SITEMAP_HEADER)

    for element in url_elements:
      xml.write(element)

    xml.write(SITEMAP_FOOTER)


if __name__ == '__main__':  
  if len(sys.argv) < 2:
    print('Usage: ./sitemap.py <links file>')
    exit()
  
  url_elements = []
  urls = load_urls(sys.argv[1])

  for url in urls:
    url_elements.append(create_url_element(url))

  save_sitemap(url_elements)

