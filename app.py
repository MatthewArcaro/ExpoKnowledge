from flask import Flask, request, redirect, url_for, render_template
import psycopg2
import os

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
        service=request.form["service"]
        staff=request.form["staff"]
        opt_in = True if "opt_in" in request.form else False


        # Save to PostgreSQL
        conn = connect_db()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO check_ins (first_name, last_name, phone_number, email, service, staff, opt_in)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (first_name, last_name, phone_number, email,service, staff, opt_in)
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
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
