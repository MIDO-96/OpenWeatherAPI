from datetime import datetime
from tkinter import *
from tkinter import messagebox

import PIL.Image
import requests
from PIL import ImageTk

'''
API_KEY
 Should be probably added as an env variable instead.
 but for the sake of smoothness it is included as it is.
'''
api_key = "4ea29b17431a3e15b9c3ac321d7c231c"

# api initial url
initial_url = "http://api.openweathermap.org/data/2.5/weather?appid=" + api_key

# Tkinter setup code
window = Tk()
window.title('CTK CASE, OpenWeatherApi connection')
window.geometry('525x450')
window.resizable(width=False, height=False)
window.configure(bg='white')

# Get current date and time
now = datetime.now()
now_string = now.strftime("%d-%m-%Y %H:%M:%S")


# Since the API returns temperature in Kelvin

def kelvin_to_celsius(temp):
    return temp - 273


def kelvin_to_fah(temp):
    return (temp - 273) * 9 / 5 + 32


'''
Function to communicate with owm api by sending a query including
desired city name. The function checks for the status of the fetched
response and at success it parses the obtained data and returns them 
in tuple format 
'''
def fetch_info(city):
    url = initial_url + "&q=" + city # final url request
    response = requests.get(url)
    if response.status_code == 200: # check for positive response
        # data parsin
        data = response.json()
        main = data['main']
        temp = main['temp']
        feels_like = main['feels_like']
        humidity = main['humidity']
        pressure = main['pressure']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        country_code = data['sys']['country']
        min_temp = main['temp_min']
        max_temp = main['temp_max']
        parsed_data = (
            temp, feels_like, humidity, pressure, wind_speed, description, icon, country_code, min_temp, max_temp)
        return parsed_data # the needed object
    else:
        messagebox.showerror('bad request', 'Invalid city name') # throw error at bad request (in our case restricted
        # to bad city name )

        return None


# Function used to populate the GUI with the relevant info
def populate_window():
    city_name = city_text.get()
    weather_info = fetch_info(city_name)
    city_name_text['text'] = '{}, {}'.format(city_name, weather_info[7])

    # check for metric system used
    if drop_down_variable.get() == 'Metric':
        temp_text['text'] = ' {:.0f}°C'.format(kelvin_to_celsius(weather_info[0]))
        multi_temp_text['text'] = '{:.0f}° / {:.0f}° Feels like: {:.0f}°'.format(kelvin_to_celsius(weather_info[8]),
                                                                                 kelvin_to_celsius(weather_info[9]),
                                                                                 kelvin_to_celsius(weather_info[1]))
    else:
        temp_text['text'] = ' {:.0f}°F'.format(kelvin_to_fah(weather_info[0]))
        multi_temp_text['text'] = '{:.0f}° / {:.0f}° Feels like: {:.0f}°'.format(kelvin_to_fah(weather_info[8]),
                                                                                 kelvin_to_fah(weather_info[9]),
                                                                                 kelvin_to_fah(weather_info[1]))

    humidity_text['text'] = 'Humidity: {} %'.format(weather_info[2])
    pressure_text['text'] = 'Pressure: {} bar'.format(weather_info[3])
    wind_speed_text['text'] = 'wind speed: {} km/h'.format(weather_info[4])
    description_text['text'] = 'the weather today is : {}'.format(weather_info[5])
    image = PIL.Image.open('icons/{}.png'.format(weather_info[6]))
    date_text['text'] = now_string

    # show correct icon
    render = ImageTk.PhotoImage(image)
    weather_icon = Label(window, image=render, bg='white')
    weather_icon.image = render
    weather_icon.place(x=115, y=190)





# Tkinter components and widgets code
welcome_text = Label(window,
                     text='Welcome to python weather app \n Enter the city name below to get weather information',
                     bg='white')
welcome_text.pack(pady=3)

city_text = StringVar()
city_entry = Entry(window, textvariable=city_text, fg="grey20", bg="white smoke")
city_entry.pack(pady=8)

fetch_button = Button(window, text='Fetch weather info', command=populate_window, bg='white')
fetch_button.pack(pady=5)

city_name_text = Label(window, text='', font=('bold', 18), fg="royal blue", bg='white')
city_name_text.pack(pady=5)

date_text = Label(window, text='', font=(14), bg='white')
date_text.pack(pady=10)

temp_text = Label(window, text='', bg='white', fg="royal blue", font=('bold', 28))
temp_text.pack(pady=20, padx=25)

multi_temp_text = Label(window, text='', bg='white', font=('bold', 14))
multi_temp_text.pack(pady=5)

humidity_text = Label(window, text='', fg="royal blue", bg='white')
humidity_text.pack(pady=5)

wind_speed_text = Label(window, text='', bg='white')
wind_speed_text.pack(pady=5)

pressure_text = Label(window, text='', fg="royal blue", bg='white')
pressure_text.pack(pady=5)

description_text = Label(window, text='', bg='white')
description_text.pack(pady=5)

OPTIONS = ['Metric','Imperial']

drop_down_variable = StringVar(window)
drop_down_variable.set(OPTIONS[0])  # default value

drop_down_menu = OptionMenu(window, drop_down_variable, *OPTIONS)
drop_down_menu.config(width=5, bg='white')
drop_down_menu.place(x=55, y=43)

window.mainloop()

# Commented Code
'''
def fetch_data(city):
    url = initial_url + "&q=" + city
    response = requests.get(url)
    data = {}
    if response.status_code == 200:
        print('Success \n')
        data = response.json()
    elif response.status_code == 400:
        print('bad request, please check for correct info')
    elif response.status_code == 401:
        print('unauthorized access, please give correct credentials')
    else:
        print('something went wrong, please try again')
    return data
'''
