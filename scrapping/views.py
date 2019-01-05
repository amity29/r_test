# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .models import Flight

# Create your views here.
def index(request):
    return HttpResponse("Hello Amity 111")

def datadump(request):
    response_msg = "default"
    if True:
        if request.method == 'GET':
            key = "k1"
            data = "data"

            data = request.GET['data'].strip(' ')
            Flight.objects.create(key=key,dataval=data)

            all_flights = []
            try:
                json_data =  """{0}""".format(data)
                flight = {}
                flight = eval(data)

                print flight
                print flight['Date']

                response_msg = flight["Price"]

            except Exception, e:
                response_msg = "json issue: " + json_data + " error ---- " + str(e)

            sql_flight1 = "x"
            win_decision = "no competition"
            win_value = 0
            current_winner = "travelgenio.com"
            current_price = 'null'
            root_diff_val = 0

            second_competitor = 0

            if "rehlat" in flight["Competitors"]:
                win_decision = "eligible"
                win_value = str(flight["Price"])
                current_price = int(filter(str.isdigit, win_value))

                kk = str(flight["Competitors"])
                rehlat_price = int(filter(str.isdigit, kk.split('rehlat')[1].split('*_*')[0]))

                if current_price == rehlat_price:
                    second_competitor = int(filter(str.isdigit, kk.split('*_*')[1]))
                    win_decision = "increment"
                    root_diff_val = second_competitor - rehlat_price - 1

                elif current_price < rehlat_price:
                    win_decision = "decrement"
                    root_diff_val = rehlat_price - current_price + 1

            else:
                win_decision = "no competition"
                root_diff_val = 0

            sql_flight1 = ('INSERT INTO `test`.`flights_data` ( `val`, `decision`, `date`, `sc`, `dest`, `depart`, `arrival`, `airline`, `price`, `win_decision`, `win_value`, `current_winner`, `comp`) VALUES ("{0}","{1}","{2}","{3}","{4}","{5}","{6}","{7}","{8}","{9}","{10}","{11}", "{12}");'.
                            format(str(root_diff_val), current_price, flight["Date"], flight["Source"], flight["Destination"], flight["Departure"], flight["Arrival"], flight["Airline"], flight["Price"], win_decision,
                            str(win_value), current_winner, flight["Competitors"]))


            Flight.objects.create( val=str(root_diff_val), decision=current_price, date=flight["Date"], sc=flight["Source"], dest=flight["Destination"], depart=flight["Departure"] , arrival=flight["Arrival"], airline=flight["Airline"], price=flight["Price"], win_decision=win_decision, win_value=str(win_value), current_winner=current_winner, comp=flight["Competitors"])

    return HttpResponse(sql_flight1)




def flight_decision(request):

    import mysql.connector
    from mysql.connector import Error
    import json

    searchtext = "Null"
    res_list = []
    try:
        # if request.method == 'GET':
        sc = str(request.GET['sc'].strip(' '))
        dest = str(request.GET['dest'].strip(' '))
        date = str(request.GET['date'].strip(' '))

        sqlquery = """SELECT `date`, `sc`, `dest`, `airline`, `price`, `win_decision`, `val`, `ts_recent`, `id`, `depart`, `decision`
                    from flightscrapdata
                    group by `date`, `sc`, `dest`, `airline`, `depart`
                    having `sc`="{0}" and `dest`="{1}" and `date`="{2}"
                    order by id desc  """.format(sc,dest,date)

        # # res1 = cursor.execute("select count(*) from test.allhotelsdata;")
        conn = mysql.connector.connect(host='localhost',
                                       database='Rehlat',
                                       user='root',
                                       password='asdf1234',
                                       auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        res1 = cursor.execute(sqlquery)
        aa_data = cursor.fetchall()


        print "Decision response : ", str(res1)

        conn.close()

        one_row = """{0}"""

        res_list = []

        row_json = {"No competition": "Data not found"}

        response = ""

        total_string = ""

        import re

        dict_airline_codes = {"Saudi Airlines Saudia": "SV", "EgyptAir": "MS", "Jet Airways": "9W", "Emirates": "EK",
                              "Jazeera Airways": "J9", "Nile Air": "NP", "Flynas": "XY", "Oman Air": "WY",
                              "Kuwait Airways": "KU", "Fly Dubai": "FZ", "Air India": "AI", "Gulf Air": "GF",
                              "Etihad Airways": "EY", "SaudiGulf Airlines": "6S", "SriLankan Airlines": "UL",
                              "Nesma Airlines": "NE", "Turkish Airlines": "TK", "Royal Jordanian": "RJ",
                              "AlMasria Universal Airlines": "UJ", "Pakistan International Airlines": "PK",
                              "Pegasus Airlines": "PC", "Qatar Airways": "QR", "Ethiopian Airlines": "ET",
                              "Philippine Airlines": "PR", "Cathay Pacific": "CX", "Middle East Airlines": "ME",
                              "SpiceJet": "SG", "Hahn Air Systems": "HR", "Atlasglobal": "KK", "Aegean Airlines": "A3",
                              "Biman Bangladesh Airlines": "BG", "British Airways": "BA", "Himalaya Airlines": "H9",
                              "Royal Air Maroc": "AT", "KLM": "KL", "Royal Brunei Airlines": "BI",
                              "Singapore Airlines": "SQ", "Kenya Airways": "KQ", "Onur Air": "8Q",
                              "Swiss International Air Lines": "LX", "Nepal Airlines": "RA",
                              "Ukraine International Airlines": "PS", "Air France": "AF", "Thai Airways": "TG",
                              "Lufthansa": "LH", "Garuda Indonesia": "GA", "Air Canada": "AC",
                              "Malaysia Airlines": "MH", "Delta Air Lines": "DL"}

        print

        for aa in aa_data:
            row_json = {}
            time_departure_in_db = ""
            date_in_db = []
            date_in_db = str(aa[0]).split('-')
            time_departure_in_db = str(aa[9])
            date_string_format = "YYYY-MM-DDT{0}:00".replace("YYYY",date_in_db[2]).replace("MM", date_in_db[1]).replace("DD", date_in_db[0]).format(time_departure_in_db)
            currency_str = ""
            currency_str = " ".join(re.findall("[a-zA-Z]+", str(aa[4])))

            row_json["DepartDate"] = str(date_string_format)
            row_json["Departure"] = str(time_departure_in_db)
            row_json["Source"] = str(aa[1])
            row_json["Destination"] = str(aa[2])
            row_json["Airline"] = str(aa[3])
            row_json["Price"] = str(aa[4])
            row_json["Price_numeric"] = "JJ".join(re.findall("[0-9]+", str(aa[4])))
            row_json["Price_currency"] = currency_str
            row_json["win_decision"] = str(aa[5])
            row_json["win_value"] = str(aa[6])
            row_json["cloud_id"] = str(aa[8])

            if str(aa[3]) in dict_airline_codes.keys():
                row_json["Airline"] = dict_airline_codes["EgyptAir"]

            res_list.append(row_json)

        final_html = "Response 200 - rehlat!"

        # *********************************

        response_msg = total_string

        # else:
        #     response_msg = "--------- Row ID : Wrong parameters --------- "
    except Exception, e:
        response_msg = e

    return HttpResponse(json.dumps(res_list))



def flightpricing(request):
    html_content = """

    <!DOCTYPE html>
            <html>
            <body>

            <embed src="https://datastudio.google.com/embed/reporting/1W6PIqNHRjz1wo6N0GIylRAipYOza795B/page/hYTV" width="100%" height="800px">

            </body>
            </html>

    """

    return HttpResponse(html_content)


def conncheck(request):
    import mysql.connector
    from mysql.connector import Error

    conn = mysql.connector.connect(host='localhost',
                                   database='Rehlat',
                                   user='root',
                                   password='asdf1234',
                                   auth_plugin='mysql_native_password')

    conn.close()
    return HttpResponse('db connected')
