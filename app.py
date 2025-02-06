from flask import Flask, request, redirect, url_for, render_template
import psycopg2

app = Flask(__name__)

# PostgreSQL connection details
DB_HOST = "localhost"
DB_NAME = "expoknowledge"
DB_USER = "postgres"
DB_PASSWORD = "Flowers12"  # Replace with your actual password

def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/", methods=["GET", "POST"])
def check_in():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        phone_number = request.form["phone_number"]
        email = request.form["email"]
        opt_in = "yes" if "opt_in" in request.form else "no"

        # Get the 'Type of Participate' and 'Company Name' (if applicable)
        participate_type = request.form["participate_type"]
        company_name = request.form["company_name"] if participate_type == "company" else None

        # Get number of guests only if attendee is selected
        number_of_guests = request.form["number_of_guests"] if participate_type == "attendee" else None

        # Save to PostgreSQL
        conn = connect_db()
        cur = conn.cursor()
        
        # Modify the SQL query to include 'number_of_guests'
        cur.execute(
            "INSERT INTO check_ins (first_name, last_name, phone_number, email, opt_in, participate_type, company_name, number_of_guests) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (first_name, last_name, phone_number, email, opt_in, participate_type, company_name, number_of_guests)
        )
        conn.commit()
        cur.close()
        conn.close()


        # Redirect to the success page
        return redirect(url_for('check_in_success'))

    return render_template('CheckIn.html')  # Serve the check-in form page

@app.route("/check_in_success")
def check_in_success():
    return render_template('check_in_success.html')  # Success page with countdown

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


##if __name__ == '__main__':
    ##app.run(debug=True)