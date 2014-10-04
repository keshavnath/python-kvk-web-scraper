#!/usr/bin/python

import logging
import logger_init
from flask import Flask, Response, url_for, jsonify, request
from search import Search
from handler import NoResultsError
from timer import Timer

app = Flask(__name__)
app.logger.addHandler(logger_init.fh)
app.logger.setLevel(logging.INFO)

def unprocessable_entity():
    message = {
        "status": 422,
        "message": "Parameter 'handelsnaam' or 'plaats' must be specified"
    }
    resp = jsonify(message)
    resp.status_code = 422

    return resp

def not_found():
    message = {
        "status": 404,
        "message": "Geen resultaten gevonden"
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.route('/api/v1/organisations', methods = [ 'GET' ])
def api_organisations():
    timer = Timer()
    timer.start()

    filter = {}
    filter["handelsnaam"] = ""
    filter["kvknummer"] = ""
    filter["straat"] = ""
    filter["huisnummer"] = ""
    filter["postcode"] = ""
    filter["plaats"] = ""
                            
    if 'handelsnaam' in request.args:
        filter["handelsnaam"] = request.args['handelsnaam']
    if 'plaats' in request.args:
        filter["plaats"] = request.args['plaats']

    if filter["handelsnaam"] == "" and filter["plaats"] == "":
        return unprocessable_entity()
    else:
        if 'startpage' in request.args:
            startpage = int(request.args['startpage'])
        else:
            startpage = 1
        if 'maxpages' in request.args:
            maxpages = int(request.args['maxpages'])
        else:
            maxpages = 1

        try:
            search = Search(filter, startpage, maxpages)
        except NoResultsError:
            return not_found()
        else:
            results = search.run()
            
            timer.stop();
            
            results["version"] = "v1"
            results["total_exectime"] = timer.exectime()

            resp = jsonify(results)
            resp.status_code = 200
                                             
            return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
