from flask import Flask, render_template, request, url_for, redirect
from flask_mysqldb import MySQL
import random
import yaml




app = Flask(__name__)


## Configuring database
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']


mysql = MySQL(app)



@app.route("/", methods = ['GET', 'POST'])
def hello_world():

    if request.method == 'POST' and request.form['button'] == 'Log In':
        # fetch form data
        customerDetails = request.form
        username = customerDetails['Uname']
        password = customerDetails['Pass']
        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) FROM CUSTOMER WHERE UserID = (%s) AND Password = (%s) ', (username, password))
        
        data = cur.fetchall()  

        if data == ((1,),): 
            return redirect(url_for('member'))
            #return redirect(url_for('member_page'))
        else:
            return "Failed to login, please check your credentials!"

    # if request.method == 'POST' and request.form['button'] == 'Staff Log In':
    #     # fetch form data
    #     customerDetails = request.form
    #     username = customerDetails['Uname']
    #     password = customerDetails['Pass']
    #     cur = mysql.connection.cursor()
    #     cur.execute('SELECT COUNT(*) FROM AIRLINE WHERE Manager_Username = (%s) AND Manager_Password = (%s) ', (username, password))
        
    #     data = cur.fetchall()  

    #     if data == ((1,),): 
    #         return "Successful login!"
    #         #return redirect(url_for('member_page'))
    #     else:
    #         return "Failed to login, please check your credentials!"
    

    if request.method == 'POST' and request.form['button'] == 'Sign Up':
        # fetch form data
        customerDetails = request.form
        username = customerDetails['Uname']
        password = customerDetails['Pass']
        name = customerDetails['Name']
        # email = customerDetails['Email']
        # dob = customerDetails['DOB']
        phone = customerDetails['phone']
        # city = customerDetails['City']
        # sex = customerDetails['gender']
        # if sex == 'Female':
        #     sex = 'F'
        # else:
        #     sex = 'M'

        # print(dob)

        cur = mysql.connection.cursor()
        # custID = random.randint(10032, 99999)
        value = [username, password, name, phone]
        cur.execute('INSERT INTO Customer VALUES((%s), (%s), (%s), (%s))', value)
        mysql.connection.commit()
        return "Signup successful"        
        

    

    return render_template("index.html")
    #return "<p>Hello, World!</p>"

@app.route("/functions.html", methods = ['GET', 'POST'])
def member() :
    data = ''
#2
    details = request.form
    
    if request.method == "POST" and request.form['button'] == 'Search for flights':
        
        from_location = details['from_location']
        to_location = details['to_location']
        date_of_travel = details['date_of_travel']
        type_of_ticket = details["type_of_ticket"]
        cur = mysql.connection.cursor()
        query = "SELECT df.flight_number, df.date, df.number_of_seats_available, a.Airport_Name, b.Airport_Name, ar.airline_name, f.departure_time, f.arrival_time FROM flight as f, daily_flight as df, airport as a, airport as b, airline as ar WHERE df.flight_number = f.flight_number AND f.from_airport_code = a.airport_code AND f.to_airport_code = b.airport_code AND f.airline_id = ar.airline_code AND df.date = (%s) AND a.city = (%s) AND b.city = (%s);" 
        cur.execute(query, [date_of_travel, from_location, to_location])
        data = cur.fetchall()
        cur.close()
        length = 8
        headers = ['Flight_no', 'Date', 'Number of seats available', 'From', 'To', 'Airline Name','Departure Time', 'Arrival Time']
        return render_template('table.html', data=(data, length, headers))
    
    if request.method == "POST" and request.form['button'] == 'Search for flight with minimum fare':
        
        from_location = details['from_location']
        to_location = details['to_location']
        date_of_travel = details['date_of_travel']
        type_of_ticket = details["type_of_ticket"]
        cur = mysql.connection.cursor()
        query = "SELECT df.flight_number, df.date, df.number_of_seats_available, a.Airport_Name, b.Airport_Name, ar.airline_name, f.departure_time, f.arrival_time, min(fare.amount) as minimum_fare FROM flight as f, daily_flight as df, airport as a, airport as b, airline as ar, fare WHERE df.flight_number = f.flight_number AND f.from_airport_code = a.airport_code AND f.to_airport_code = b.airport_code AND f.airline_id = ar.airline_code AND df.date = (%s) AND a.city = (%s) AND b.city = (%s) AND fare.type = (%s);" 
        cur.execute(query, [date_of_travel, from_location, to_location, type_of_ticket])
        data = cur.fetchall()
        cur.close()
        length = 9
        headers = ['Flight_no', 'Date', 'Number of seats available', 'From', 'To', 'Airline Name','Departure Time', 'Arrival Time', 'Minimum Fare']
        return render_template('table.html', data=(data, length, headers))
    
    if request.method == "POST" and request.form['button'] == 'Generate a report of fares by airlines':
        
        details = request.form
        from_location = details['from_location']
        to_location = details['to_location']
        date_of_travel = details['date_of_travel']

        cur = mysql.connection.cursor()
        cur.execute("select min(fare.amount), max(fare.amount), avg(fare.amount), ar.Airline_Name from fare, airport as a, airport as b, airline as ar, flight as f, daily_flight as df where df.Flight_Number = f.Flight_Number and df.date = (%s) and a.city = (%s) and b.city = (%s) and f.from_airport_code = a.airport_code and f.to_airport_code = b.airport_code and fare.flight_number = df.Flight_Number and df.date = fare.date and f.airline_id = ar.Airline_Code GROUP BY(ar.Airline_Name);", [date_of_travel, from_location, to_location])
        data = cur.fetchall()
        cur.close()
        length = 4
        headers = ['Min(Fare)', 'MAX(Fare)', 'AVG(Fare)', 'Airline Name']
        return render_template('table.html', data=(data, length, headers))

    if request.method == "POST" and request.form['button'] == 'Order flights by cost':
        
        from_location = details['from_location']
        to_location = details['to_location']
        date_of_travel = details['date_of_travel']
        type_of_ticket = details["type_of_ticket"]
        cur = mysql.connection.cursor()
        cur.execute("Select df.flight_number, df.date, a.Airport_Name, b.Airport_Name, f.departure_time, f.arrival_time, fare.amount from fare, flight as f, daily_flight as df, airport as a, airport as b, airline as ar where df.flight_number = f.flight_number AND f.from_airport_code = a.airport_code and f.to_airport_code = b.airport_code and f.airline_id = ar.airline_code and df.date = (%s) and a.city = (%s) and b.city = (%s) AND Fare.Flight_Number = DF.FLIGHT_NUMBER AND FARE.DATE = (%s) AND FARE.TYPE = (%s) order by fare.amount", [date_of_travel, from_location, to_location, date_of_travel,type_of_ticket])
        data = cur.fetchall()
        cur.close()
        length = 7
        headers = ['Flight Number', 'Date', 'From', 'To', 'Departure Time', 'Arrival Time', 'Amount']
        return render_template('table.html', data=(data, length, headers))

    if request.method == "POST" and request.form['button'] == 'Order flights by duration':
        
        from_location = details['from_location']
        to_location = details['to_location']
        date_of_travel = details['date_of_travel']
        type_of_ticket = details["type_of_ticket"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT df.flight_number, a.Airport_Name, b.Airport_Name, f.departure_time, f.arrival_time FROM flight as f, daily_flight as df, airport as a, airport as b, airline as ar  WHERE df.flight_number = f.flight_number AND f.from_airport_code = a.airport_code and f.to_airport_code = b.airport_code and f.airline_id = ar.airline_code and df.date = (%s) AND a.City = (%s) AND b.City = (%s) ORDER BY f.arrival_time - f.departure_time;", [date_of_travel, from_location, to_location])
        data = cur.fetchall()
        cur.close()
        length = 5
        headers = ['Flight Number', 'From', 'To', 'Departure Time', 'Arrival Time']
        return render_template('table.html', data=(data, length, headers))

    if request.method == "POST" and request.form['button'] == 'Search flights by this airline':
        
        from_location = details['from_location']
        to_location = details['to_location']
        date_of_travel = details['date_of_travel']
        type_of_ticket = details["type_of_ticket"]
        airline_name = details["airline_name"]
        
        cur = mysql.connection.cursor()
        query = "SELECT df.flight_number, df.date, df.number_of_seats_available, a.Airport_Name, b.Airport_Name, ar.airline_name, f.departure_time, f.arrival_time FROM flight as f, daily_flight as df, airport as a, airport as b, airline as ar WHERE df.flight_number = f.flight_number AND f.from_airport_code = a.airport_code AND f.to_airport_code = b.airport_code AND f.airline_id = ar.airline_code AND df.date = (%s) AND a.city = (%s) AND b.city = (%s) AND ar.Airline_Name = (%s);" 
        cur.execute(query, [date_of_travel, from_location, to_location, airline_name])
        data = cur.fetchall()
        cur.close()
        length = 8
        headers = ['Flight_no', 'Date', 'Number of seats available', 'From', 'To', 'Airline Name','Departure Time', 'Arrival Time']
        return render_template('table.html', data=(data, length, headers))

    if request.method == "POST" and request.form['button'] == 'Find flights between given departure time':
        
        from_location = details['from_location']
        to_location = details['to_location']
        date_of_travel = details['date_of_travel']
        type_of_ticket = details["type_of_ticket"]
        departure_time_start = int(details["start"])
        departure_time_stop = int(details["stop"])
       

        cur = mysql.connection.cursor()
        query = "SELECT df.flight_number, df.date, df.number_of_seats_available, a.Airport_Name, b.Airport_Name, ar.airline_name, f.departure_time, f.arrival_time FROM flight as f, daily_flight as df, airport as a, airport as b, airline as ar WHERE df.flight_number = f.flight_number AND f.from_airport_code = a.airport_code AND f.to_airport_code = b.airport_code AND f.airline_id = ar.airline_code AND df.date = (%s) AND a.city = (%s) AND b.city = (%s) AND f.departure_time between (%s) AND (%s) ORDER BY f.departure_time;" 
        cur.execute(query, [date_of_travel, from_location, to_location, departure_time_start, departure_time_stop])
        data = cur.fetchall()
        cur.close()
        length = 8
        headers = ['Flight_no', 'Date', 'Number of seats available', 'From', 'To', 'Airline Name','Departure Time', 'Arrival Time']
        return render_template('table.html', data=(data, length, headers))
    
    if request.method == "POST" and request.form['button'] == 'Book':
        charc = ['A', 'B', 'C', 'D', 'E']
        flight_number = details['flight number']
        date_of_flight = details['date of flight']
        #seat_number = details["seat number"]
        seat_number = str(str(random.randint(1,30)) + charc[random.randint(0, 4)])
        print(seat_number)
        userid = details["userid"]
        cur = mysql.connection.cursor()
        query1 = "SELECT Number_of_seats_available FROM daily_flight as D WHERE D.Flight_Number = (%s) AND D.Date = (%s);"
        cur.execute(query1, [flight_number, date_of_flight])
        data1 = cur.fetchall()
        print("here")
        # print(data1[0][0])
        if data1[0][0] > 0:   
            query2 = "INSERT INTO SEAT_PASSENGER_BOOKINGS VALUES((%s), (%s), (%s), (%s));" 
            cur.execute(query2, [flight_number, date_of_flight, seat_number, userid])
            mysql.connection.commit()
            query3 = "UPDATE DAILY_FLIGHT SET Number_of_seats_available = Number_of_seats_available - 1 WHERE Flight_Number = (%s) AND Date = (%s);"
            cur.execute(query3, [flight_number, date_of_flight])
            mysql.connection.commit()
            return "Seat number " + seat_number + " booked successfully in flight : " + flight_number + " on date: " + date_of_flight     
        else:
            return "No seats left!"
        
    if request.method == "POST" and request.form['button'] == 'Retreive my bookings':
        
        userid = details["custID"]
        cur = mysql.connection.cursor()
        query = "SELECT * FROM SEAT_PASSENGER_BOOKINGS WHERE PASSENGERID = (%s)" 
        cur.execute(query, [userid])
        data = cur.fetchall()
        cur.close()
        length = 4
        headers = ['Flight_Number', 'Date', 'Seat Number', 'PassengerID']
        return render_template('table.html', data=(data, length, headers))

    if request.method == "POST" and request.form['button'] == 'Cancel':
        
        flight_number = details['flight number']
        date_of_flight = details['date of flight']
        #seat_number = details["seat number"]
        userid = details["userid"]
        cur = mysql.connection.cursor()
        query = "DELETE FROM SEAT_PASSENGER_BOOKINGS AS S WHERE S.FLIGHT_NUMBER = (%s) AND S.DATE = (%s) AND S.PASSENGERID = (%s)" 
        cur.execute(query, [flight_number, date_of_flight, userid])
        mysql.connection.commit()
        return "Seat cancelled successfully"  
       

    return render_template("functions.html")



if __name__ == "__main__":
    app.run(debug = True, port = 8000)
