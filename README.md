# Airline-Booking-Management-System

This is a web application for airline booking management system that helps users in booking flight tickets. The source code for backend is in Python utilizing its Flask microweb framework.
MySQL is used as the database for storing data and querying for required functionality.

## Usage

To run the project:

1. Clone the git repository
2. Install the dependencies using `pip install -r requirements.txt`
3. Run `python app.py`

## Description

The web app offers the following functionality:
1. **Log in**: User can enter their login details: username and password to login. 
2. **Sign up**: If the user does not have an account, he/she can create an account by entering their information such as name, phone userid and password.

**Customers can perform the following**:
1. **Search for flights**: Once a user is signed in, they can search for flights by entering date of travel, from location and to location. A list of matches will show up. 
2. **Book a flight**: The user can book a particular seat in a flight which will be stored in bookings table.
3. **Retrieve a booking**: User can retrieve information about their bookings by entering their userid.
4. **Cancel a booking**: The user can cancel a booking by entering the userid, seat number, flight number and date. 
5. User can add additional filters to flight search such as sorting or generating statistical report. 

## Entity Relationship Diagram

![image](https://user-images.githubusercontent.com/37876923/182477309-e0441d33-5bf1-4ab9-b0c5-5bb394bed168.png)

## Logical Mapping (ERD to Relations) 

![image](https://user-images.githubusercontent.com/37876923/182477393-8a3f8df1-f8c3-4c0b-b2cd-c4538fdc6caa.png)


