from enum import Enum
from json import dumps, load
from logging import Logger, StreamHandler, INFO
from os.path import exists, dirname, join
from sys import stdout

from flask import Flask, Response
from requests import get, ReadTimeout
import yaml


class Format(Enum):
    JSON = "json"
    YAML = "yaml"


def generate_app(fn, fm=None):
    with open(fn) as fp:
        if fm == Format.YAML or (fm is None and (fn.endswith(".yaml") or fn.endswith(".yml"))):
            endpoints = yaml.safe_load(fp)
        else:
            endpoints = load(fp)

    for ep in endpoints.keys():
        assert isinstance(ep, str), "Endpoint has to be of type str (got: \"%s\", " \
                                    "of type \"%s\")" % (ep, type(ep))
        if ep.startswith("/"):
            endpoints[ep[1:]] = endpoints[ep]
            del endpoints[ep]

    for url in endpoints.values():
        assert isinstance(url, str), "Query URL has to be of type str (got: \"%s\", " \
                                    "of type \"%s\")" % (url, type(url))

    app = Flask("status-api", template_folder=None, static_folder=None)

    logger = Logger(__name__)
    logger.addHandler(StreamHandler(stdout))
    logger.setLevel(INFO)

    logger.info("Registered endpoints: %s" % ", ".join("\"/%s\"" % e for e in endpoints.keys()))

    @app.route("/<path:path>")
    def handler(path):
        if path not in endpoints.keys():
            logger.warning("Undefined endpoint %s was called" % path)
            return Response(
                dumps({"status": 404, "msg": "No such endpoint"}),
                status=404,
                mimetype="application/json"
            )

        try:
            response = get(endpoints[path], timeout=10)
        except ReadTimeout:
            logger.debug("Timeout received from %s" % path)
            return Response(
                dumps({"status": 408, "msg": "Timeout"}),
                status=408,
                mimetype="application/json"
            )
        if response.ok:
            if len(response.content) > 0:
                logger.debug("Everything okay with %s" % path)
                return Response(
                    dumps({"status": 200, "msg": "Okay", "code": response.status_code}),
                    status=200,
                    mimetype="application/json"
                )
            else:
                logger.debug("No body from %s" % path)
                return Response(
                    dumps({"status": 204, "msg": "Empty body", "code": response.status_code}),
                    status=204,
                    mimetype="application/json"
                )
        else:
            logger.debug("Bad response code from %s (%s)" % (path, response.status_code))
            return Response(
                {"status": 400, "msg": "Bad response", "code": response.status_code},
                status=400,
                mimetype="application/json"
            )
    return app


if __name__ == "__main__":
    bn = dirname(__file__)
    json = join(bn, "../../eps.json")
    yaml_file = join(bn, "../../eps.yaml")
    if exists(yaml_file):
        file = yaml_file
    else:
        file = json

    fa = generate_app(file)
    fa.run(port=4777, debug=True)
