from flask import Flask, redirect, render_template, request, flash, url_for, session
import numpy as np
import pickle
from settings.settings import DEV

app = Flask(__name__)
app.config.from_object(DEV)

# load model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route("/", methods=["GET","POST"])
def index():

    if request.method == "POST":
        institution =request.form['institution']
        sda =request.form['sda']
        sdwan =request.form['sdwan']
        sddc =request.form['sddc']
        segmentation =request.form['segmentation']
        encryption =request.form['encryption']
        mfa =request.form['mfa']
        sso =request.form['sso'] 
        policy_engine =request.form['policy_engine'] 
        mdm =request.form['mdm'] 
        dlp =request.form['dlp']

        response_list = [institution, sda, sdwan, sddc, segmentation, encryption, mfa, sso, policy_engine, mdm, dlp ]
        float_resp_list = list(map(lambda x: float(x), response_list))
        # make prediction using model loaded
        prediction = model.predict(np.array(float_resp_list))

        print("prediction", prediction)
        print("prediction type", type(prediction))
        flash("Successfully Returned Zero Trust Level Prediction", 'success')

        return redirect(url_for("results", res=prediction))
    return render_template("index.html")

@app.route("/results/<res>", methods=["GET"])
def results(res):
    # print("now", res[2:-2])
    r = [i.replace("\n", "") for i in list(res[2:-2].split(" ")) if i != ""]
    s = [f'{float(j):.5f}' for j in r]
    t = [(str(round((float(i)*100), 2)) + "%") for i in s]
    print("res 1",t)

    return render_template("results.html", results=t)

if __name__ == "__main__":
    app.run(debug=True)