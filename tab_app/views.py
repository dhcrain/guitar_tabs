from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# Create your views here.

def tab_search_view(request):
    page_count = 10
    song_name = request.GET.get('song_name') or 'bohemian rhapsody'
    links = []
    band_names = []
    for page in range(1, page_count + 1):
        url = "http://www.guitartabs.cc/search.php?tabtype=any&band=&song={}&p={}".format(song_name, page)
        content = requests.get(url).text
        souper = BeautifulSoup(content, 'html.parser')
        song_links = souper.find_all("a", class_="ryzh22")
        band_name = souper.find_all(width="35%")
        for link in song_links:
            links.append(str(link))
        for name in band_name:
            band_names.append(str(name))
    context = {
        'search': song_name.title(),
        'links': links,
        'band_names': band_names,
    }
    return render(request, 'index.html', context)

def lyric_detail_view(request, url):
    song = requests.get("http://www.guitartabs.cc/" + url).text
    souper = BeautifulSoup(song, 'html.parser')
    tabs = str(souper.find(style="line-height:normal"))
    song_list = souper.find_all("a", class_="ryzh2")
    songs = []
    if tabs == 'None':  # display songs by band
        for song in song_list:  # wierd work around to get Django and BeautifulSoup to play nice
            songs.append(str(song))
        context = {'songs': songs}
    else:   # display tabs from a song
        context = {'tabs': tabs,}
    return render(request, 'detail.html', context)
