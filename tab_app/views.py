from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.

def tab_search_view(request):
    song_name = request.GET.get('song_name')
    url = "http://www.guitartabs.cc/search.php?tabtype=any&band=&song={}".format(song_name)
    content = requests.get(url).text
    souper = BeautifulSoup(content, 'html.parser')
    song_links = souper.find_all("a", class_="ryzh22")
    band_name = souper.find(width="35%").text   # not working properly
    context = {
        'links': [link.attrs['href'] for link in song_links],
        'band_names': [str(band_name) for name in band_name], #not working currently

    }
    return render(request, 'index.html', context)

def lyric_detail_view(request, url):
    song = requests.get("http://www.guitartabs.cc/" + url).text
    souper = BeautifulSoup(song, 'html.parser')
    context = {
        'tabs': str(souper.find(style="line-height:normal")),
    }
    return render(request, 'detail.html', context)
