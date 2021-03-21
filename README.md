# Scout Mulch Delivery Web Application

The intent of this project is to build a web application which can be used to coordinate the delivery of thousands of bags of mulch across hundreds of orders.

## Features

The web application will target the following user personas:
- Logistics Coordinator
- Delivery Truck Drivers and Navigators
- Chase Car Drivers
- Yard Boss
- Yard Crew
- Scouts
- Other parent volunteers

### General

- Login via email address and receive a cookie good for 24 hours (keeping the user signed into the application for the entire delivery day). No passwords to remember.
- View overall delivery progress in terms of bags delivered and routes completed.
- Receive delivery notifications.
- View where the trucks and chase cars are.

### Delivery Drivers & Navigators

- Receive an assigned route of deliveries.
- Tap on a delivery address to launch driving directions to that address.
- Confirm the number of bags delivered to an address (mark a delivery as complete).

### Chase Car Drivers

- Confirm the delivery truck being followed (so that if a parent needs to know where their scout is, they can find them).

### Logistics Coordinator

- Assign roles to various users, giving them increased permissions.
- View and Adjust the overall route plans.
- Compute real-time statistics regarding team performance.

### Yard Boss & Crew

- Receive notification when a truck has completed all deliveries for its route (and is on its way back to the yard).
- Confirm when the truck arrives at the yard and when it is done being loaded (to track load times).

## Getting up and running

### Prerequisites

Requires Java JDK version 8 or higher to be installed. To check, run ```java -version``` and [Gradle](https://gradle.org/install/).

### Running

```./gradlew bootRun```

## Screenshots
