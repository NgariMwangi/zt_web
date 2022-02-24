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


    # messages = request.args['messages']

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
        # flash("sudf", 'success')

        # return redirect(url_for('index'))


    return render_template("index.html")

if __name__ == "__main__":
    app.run()