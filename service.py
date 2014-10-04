#!/usr/bin/python

import logging
import logger_init
from flask import Flask, Response, url_for, jsonify, request
from search import Search
from handler import NoResultsError
from timer import Timer

release = "0.6.0"

app = Flask(__name__)
app.logger.addHandler(logger_init.fh)
app.logger.setLevel(logging.DEBUG)

def unprocessable_entity():
    message = {
        "status": 422,
        "message": "Parameter 'handelsnaam', 'kvknummer', 'straat', 'huisnummer', 'postcode' or 'plaats' must be specified"
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

def check_args(name):
    value = ""
    if name in request.args:
        value = request.args[name]
    return value

def check_args_boolean(name, default, zero_one):
    if zero_one:
        value = "1" if default else "0"
    else:
        value = "true" if default else "false"
    if name in request.args:
        if request.args[name] in ("true", "false"):
            if zero_one:
                value = "1" if request.args[name] == "true" else "0"
            else:
                value = request.args[name]
        else:
            raise "Illegal value"
    return value
                 
@app.route('/api/v1/organisations', methods = [ 'GET' ])
def api_organisations():
    timer = Timer()
    timer.start()

    app.logger.debug(request.args)

    filter = {}
    filter["handelsnaam"] = check_args("handelsnaam")
    filter["kvknummer"] = check_args("kvknummer")
    filter["straat"] = check_args("straat")
    filter["huisnummer"] = check_args("huisnummer")
    filter["postcode"] = check_args("postcode")
    filter["plaats"] = check_args("plaats")
    filter["hoofdvestiging"] = check_args_boolean("hoofdvestiging", True, False)
    filter["nevenvestiging"] = check_args_boolean("nevenvestiging", True, False) 
    filter["rechtspersoon"] = check_args_boolean("rechtspersoon", True, False)
    filter["vervallen"] = check_args_boolean("vervallen", False, True)
    filter["uitgeschreven"] = check_args_boolean("uitgeschreven", False, True)

    app.logger.debug(filter)
                                
    if filter["handelsnaam"] == "" and filter["kvknummer"] == "" and filter["straat"] == "" and filter["huisnummer"] == "" and filter["postcode"] == "" and filter["plaats"] == "":
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
            
            results["total_exectime"] = timer.exectime()
            results["api_version"] = "v1"
            results["release"] = release

            resp = jsonify(results)
            resp.status_code = 200
                                             
            return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
