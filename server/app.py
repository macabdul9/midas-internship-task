import flask
from flask import Flask, session, redirect, url_for, session, jsonify, request
import numpy as np
import requests
import os
import praw
from multiprocessing import cpu_count
from utils.ScrapSubmission import get_data
from inference import predict
# import simpletransformers

model_path = str(os.path.dirname(__file__)) + 'models/pytorch_model.bin'

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        print("GET REQUEST RECEIVED")
        # url = flask.request.form['url']
        url = request.args.get('url', '')
        print("hello", url)
        return {"get reponse":"model loaded"}

    if flask.request.method == 'POST':
        print("POST REQUEST RECEIVED")
        url = request.args.get('url', '')
        print("url", url)
        # actual, pred = return_out(url)
        text, flair =  get_data(url)
        pred, confi = predict(text)
        result = [str(cls)+" : "+str('%.4f'%confidence) for cls, confidence in zip(pred, confi)]
        print(confi)
        return {"top-3 pred":"   ".join(result), "flair":flair, "text":text}

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=80)