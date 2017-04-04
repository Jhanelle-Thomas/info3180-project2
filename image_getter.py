import requests
from bs4 import BeautifulSoup
import urlparse

def getImages():
    url = "https://www.walmart.com/ip/54649026"
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    images = []
    
    # This will look for a meta tag with the og:image property
    og_image = (soup.find('meta', property='og:image') or
                        soup.find('meta', attrs={'name': 'og:image'}))
    
    
    # This will look for a link tag with a rel attribute set to 'image_src'
    thumbnail_spec = soup.find('link', rel='image_src')
    
    
    for img in soup.findAll("img", src=True):
        temp = urlparse.urljoin(url, img["src"])
        if temp not in images:
            images.append(temp)
            
    #print images
    return images