#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Bot's queried information message as class
class WeatherMessage:

    def __init__(self, query):
        # instantiate a WeatherMessage as an object holding a query (expects JSON content of API call)
        self.__query = query

    def get_message_blocks(self):
        # returns a list of blocks having the queried information
        res_weather = self.__query['weather'][0]
        res_city = self.__query['name']
        res_country = self.__query['sys']['country']
        res_state_main = res_weather['main'].capitalize()
        res_state_desc = ' '.join(map(lambda e: e.capitalize(), res_weather['description'].split()))
        res_humid_perc = self.__query['main']['humidity']
        res_ctemp_average = round(self.__kelv_to_cels(self.__query['main']['temp']), 1)
        res_ctemp_feeling = round(self.__kelv_to_cels(self.__query['main']['feels_like']), 1)
        res_wind_speed = round(self.__mps_to_kmph(self.__query['wind']['speed']), 1)

        return [
            self.__get_header(res_city, res_country),
            self.__get_section_1(res_state_main, res_state_desc, res_humid_perc),
            self.__get_section_2(res_ctemp_average, res_ctemp_feeling, res_wind_speed)
        ]

    def __get_header(self, param_city, param_country):
        # private method to return the header block (i.e. "Weather in <CITY>, <COUNTRY>")
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Weather in {}, {}:".format(param_city, param_country)
            }
        }

    def __get_section_1(self, param_state_main, param_state_desc, param_humid_perc):
        # private method to return the first section block (contains the weather descriptions and humidity)
        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Current State:*\n{} ({})".format(param_state_main, param_state_desc)
                },
                {
                    "type": "mrkdwn",
                    "text": "*Humidity:*\n{}%".format(param_humid_perc)
                }
            ]
        }

    def __get_section_2(self, param_ctemp_average, param_ctemp_feeling, param_wind_speed):
        # private method to return the second section block (contains the celsius temperature and wind speed)
        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Temperature:*\n{}°C, feels like {}°C".format(param_ctemp_average, param_ctemp_feeling)
                },
                {
                    "type": "mrkdwn",
                    "text": "*Wind:*\n{} km/h".format(param_wind_speed)
                }
            ]
        }

    def __kelv_to_cels(self, param_temp):
        # private method to convert kelvin to celsius and return the result
        return param_temp - 273.15

    def __mps_to_kmph(self, param_mps):
        # private method to convert m/s to km/h and return the result
        return 3.6 * param_mps