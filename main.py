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

        recommend = {}

        # print("jjjj",float_resp_list)

        if float_resp_list[6] != 5:
            recommend["MFA"] = "Adopt multifactor authentication to help protect your applications by requiring users to confirm their identity using a second source of validation, such as a phone or token, before access is granted."
        if float_resp_list[7] != 5:
            recommend["SSO"] ="Adopt SSO not only strengthens security by removing the need to manage multiple credentials for the same person but also delivers a better user experience with fewer sign-in prompts."
        if float_resp_list[5] != 1:
            recommend["Encryption"] = "At a minimum, setup encrypted admin access and embark to encrypt all traffic as organizations that fail to protect data in transit are more susceptible to man-in-the- middle attacks, eavesdropping, and session hijacking. These attacks can be the first step attackers use to gain access to confidential data."
        if  float_resp_list[4] != 1:
            recommend["Segmention"]= "Implement network segmentation through software-defined perimeters to reduce the lateral movement of threats."
        if float_resp_list[-1] != 1:
            recommend["DLP"] = "Adopt Data Loss Prevention Mechanisms. Once data access is granted, controlling what the user can do with your data is critical. For example, if a user accesses a document with a corporate identity, you want to prevent that document from being saved in an unprotected consumer storage location, or from being shared with a consumer communication or chat app."
        if float_resp_list[-3] != 1:
            recommend["Policy Engine"] = "Implement network access control to enforce granular control with risk-based adaptive access policies that integrate across endpoints, apps, and networks to better protect your data."
        if float_resp_list[-2] != 5:
            recommend["MDM"] ="Set up Mobile Device Management for internal users. MDM solutions enable endpoint provisioning, configuration, automatic updates, device wipe, and other remote actions."
   
        flash("Successfully Returned Zero Trust Level Prediction", 'success')

        return redirect(url_for("results", res=prediction, recom=recommend))
    return render_template("index.html")

@app.route("/results/<res>/<recom>", methods=["GET"])
def results(res, recom):
    # Prediction Cleaning
    r = [i.replace("\n", "") for i in list(res[2:-2].split(" ")) if i != ""]
    s = [f'{float(j):.5f}' for j in r]
    t = [(str(round((float(i)*100), 2)) + "%") for i in s]

    # Recom Cleaning
    import ast
    print("res 2", type((recom)))
    res = ast.literal_eval(recom)

    print("recommendations afre", res)

    return render_template("results.html", results=t,recom=res)

if __name__ == "__main__":
    app.run(debug=True)