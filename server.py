'''
By:  Isaac Lehman
For: COMP 442

Simple contact book that stores contacts in an object.
They are available as long as the server is running.

To Run:
1. Navigate to this file
2. Execute: python server.py
'''
import os
from flask import Flask, render_template, request
from flask import redirect, url_for, flash


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # no cache
app.config["SECRET_KEY"] = os.urandom(32)


''' contact class '''
class Contact:
    def __init__(self, first, last, email, address):
        self.first   = first
        self.last    = last
        self.email   = email
        self.address = address
    def __str__(self):
        return f"{self.first} {self.last}"
    def __repr__(self):
        return f"{self.first} {self.last} {self.email} {self.address}"
    def __eq__(self, other):
        return (self.first == other.first
            and self.last == other.last
            and self.email == other.email
            and self.address == other.address)


# an array of contacts
contacts = []


@app.route("/contacts/")
def contacts_table():
    return render_template("contacts.html", contacts=contacts)


@app.route("/addcontact/", methods=["GET"])
def add_contact_get():
    return render_template("addcontact.html") # where you enter data


@app.route("/addcontact/", methods=["POST"])
def add_contact_post():
    # check first/last name
    first = request.form.get('first')
    last  = request.form.get('last')
    if first is None or first == "":
        flash("First Name is required")
        return redirect(url_for("add_contact_get"))
    if last is None or last == "":
        flash("Last Name is required")
        return redirect(url_for("add_contact_get"))

    # check email and address
    email = request.form.get('email')
    address = request.form.get('address')
    if email is None and address is None:
        flash("You must submit your email and/or address")
        return redirect(url_for("add_contact_get"))
    if email == "" and address == "":
        flash("You must submit your email and/or address")
        return redirect(url_for("add_contact_get"))

    # check if contact already exists
    new_contact = Contact(first, last, email, address)
    if new_contact in contacts:
        flash(f"This contact already exists: {new_contact}")
        return redirect(url_for("add_contact_get"))

    # if all data was good
    contacts.append(new_contact)
    return redirect(url_for("contacts_table"))


if __name__ == "__main__":
    app.run(debug=True)

# Having debug=True allows possible Python errors to appear on the web page
# run with $> python server.py
