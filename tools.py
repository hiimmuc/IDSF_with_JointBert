import datetime
import re
import webbrowser

import googlesearch
import requests
from google_trans_new import google_translator as Translator
# from googletrans import Translator
from youtube_search import YoutubeSearch


def convert_languages(txt, src='auto', dest='en'):
    """to convert between languages

    Args:
        txt (str): text string need to convert
        src (str, optional): source language. Defaults to 'vi'.
        dest (str, optional): destination language. Defaults to 'en'.

    Raises:
        Exception: [description]

    Returns:
        str: string after convert if able
    """
    script = txt
    try:
        translator = Translator()
        script = translator.translate(txt, lang_tgt=dest, lang_src=src)
        # script = translator.translate(txt)
        # script = script.text
        print(script)
    except Exception as e:
        print(e)
    return script


def gg_search(key, max_results=5):
    """to use google to search about something

    Args:
        key (str): keyword for searching
        max_results (int, optional): number of result to display. Defaults to 5.

    Raises:
        Exception: [description]

    Returns:
        list: list of link to search result
    """
    try:
        for i, url in enumerate(
                googlesearch.search(key,
                                    num=max_results,
                                    stop=max_results,
                                    pause=1)):
            print(f"{i + 1}-> {url}")
            webbrowser.open(str(url))
        return True
    except Exception as e:
        raise e


def weather_outdoor(city_name='Hanoi', specific=None):
    """Get the information about the weather in place

    Args:
        city_name (str, optional): city to get information. Defaults to 'Hanoi'.
        specific (str, optional): specify what factor to get temp, humidity, pressure, wind, clouds, dt. Defaults to None.
    """
    if not specific:
        specific = ''
    thinking = ''
    try:
        api = r"330ff11e86b5ccbeba0a2f71aab88014"
        # city_name = convert_languages(city_name, dest='en').replace(' ', '').lower()
        city_name = city_name.replace(' ', '').lower()
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api}&q={city_name}"
        response = requests.get(url)
        data = response.json()
        # print(data)
        if data["cod"] != "404":
            data_table = data["main"]
            current_temperature = data_table['temp'] - 273.15
            current_pressure = data_table["pressure"]
            current_humidity = data_table["humidity"]
            some_text = data["weather"]
            weather_description = some_text[0]["description"]
            # weather_description = convert_languages(
            #     weather_description, 'en', 'vi')
            thinking = f"City: {data['name']}, {data['sys']['country']}\n" \
                f"{datetime.datetime.now()}\n" \
                f"Weather summary: {weather_description}, \n" \
                f">The temperature {round(current_temperature, 2)} Celsius, \n" \
                f">The humidity is {current_humidity} %, \n" \
                f">The pressure is {current_pressure} Pa"
            if not specific:
                print(thinking)
            else:
                if specific in ['temp', 'pressure', 'humidity']:
                    print(f"{specific}: {data_table[f'{specific}']}")
                else:
                    print(f"{specific}: {data[f'{specific}']}")
    except Exception as r:
        print(r)
        print("not found in api, search web")
        kw = "Weather in" + city_name
        gg_search(kw, max_results=1)


def youtube(what):
    """play youtube video"""
    while True:
        result = YoutubeSearch(what, max_results=10).to_dict()
        # print(result)
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)


def get_expression(text):
    """Extract intents and slot values from text string"""
    pair = {}
    for slot_and_value in re.findall("<(.+?)>", text):
        value, slot = slot_and_value.split(":")
        pair[slot] = value
    return pair
    pass


if __name__ == '__main__':
    # print(convert_languages('안녕하세요.'))
    weather_outdoor(city_name='paris')
    # print(convert_languages('What is the weather in Hà Nội'))
    print(get_expression('GetWeather ->  What is the weather in <Hanoi:B-city>'))
    # slots_and_values = get_expression(
    #     'PlayMusic ->  let play the <song:B-object_type> <Hello:B-track> <aldele:I-track> for me')
    # yt_search = ''
    # for key in slots_and_values:
    #     if any(x in key for x in ['track', 'album']):
    #         yt_search += ('' + slots_and_values[key])
    # youtube(yt_search)
