# Smart Restaurant Reservation Engine
Intel Internship Challenge – 2 Submission

**Overview**

Smart Restaurant Reservation Engine- This is a Back-end system that is scheduled to work with the reservations of tables at restaurants in an organized way based on API logic. It is a project, which aims at developing the central reservation and allocation engine, which can be extended to achieve future integrations (chatbots, web apps, or mobile platforms).
The solution does not focus on the implementation of a conversational interface, but it rather focuses on creating a scalable and dependable backend that will deal with availability tracking, table assignment, cancellation, and waitlist. The aim is to portray clean architecture, structured design of backends, and intelligent capacity management.

**Problem Staement**

The operational challenges that restaurants often have to deal with are:
1.Handling of reservations manually or inefficiently.
2.Unwise table allocation techniques.
3.Customers have to wait too long.
4.Inconvenience in following the availability of the table in real time.

**Proposed Solution**

This project is defined as the implementation of a reservation engine based on the principles of a REST that will automatize the process of table management and booking.
The system:
1.Data that is stored in stores is seating capacity and availability status.
2.Dynamically check the availability of tables.
3.Gives the best table depending on the number of people.
4.Makes organized reservations.
5.Allows cancellations of reservations.

**System Architecture**

User Interface (Chatbot)
        ->
Reservation Engine
        ->
Availability & Optimization Logic
        ->
Database (Tables, Reservations, Waitlist)
        ->
Notification System (SMS/Confirmation)
        ->
Management Dashboard

**How it Works**

1.A reservation request is submitted with the required party size.
2.The system checks for available tables that match the requirement.
3.If a suitable table is available, it is marked as reserved and linked to the reservation.
4.If no table is available, the system supports structured waitlist handling.
5.When a reservation is canceled, the assigned table is automatically freed and made available again.

**Tech Stack**

i)Python
ii)FastAPI (or Flask, depending on implementation)
iii)REST APIs
iv)SQLite or in-memory database
v)Git & GitHub


**To Run the Project**

1.Clone the Repository : git clone https://github.com/Caro26lina/Challenge_2.git

2.Navigate to the Project Folder : cd restaurant-bot

3.Install Dependencies : pip install fastapi uvicorn sqlalchemy

4.Run the Application : uvicorn main:app --reload

5.Open in Browser : http://127.0.0.1:8000/docs


