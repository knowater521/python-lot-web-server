# coding=utf-8
from flask import Flask, json
import logging as log

app = Flask(__name__)


@app.route("/")
def main():
    log.info("进入主页")
    print("sahfskhfsaklhfsakhh")
    return "主页！"


if __name__ == "__main__":
    app.run(debug=False, threaded=True)