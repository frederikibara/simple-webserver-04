# Simple HTTP-UDP Server


### Link for download docker image from docker hub
  https://hub.docker.com/r/fred99/simple-server
  
### docker command
  docker pull fred99/simple-server


## Usage
Open http://localhost:3000 in your browser to access the home page.
Navigate to http://localhost:3000/message.html to access the form for sending messages.
The form submission will be sent to the UDP server, and the data will be stored in storage/data.json.


### Description
The program is a Python web application consisting of HTTP and UDP servers. Here is a brief description of the functionality:

Program description
HTTP Server:

Serves static HTML pages and CSS styles.
Responds to requests to / (home page) and /message.html (message form).
Processes POST requests to /send_message, receives data from the form (user and message), and then forwards it to the UDP server.
UDP Server:

Receives data sent by the HTTP server.
Converts the received data (JSON format) into a dictionary.
Adds an entry to the JSON file (storage/data.json) with the time the message was received.
Docker:

Creates a Docker image and configuration for easy deployment of the application.
Uses the volumes mechanism to store data (data.json) outside the container, which ensures data retention between container restarts.
Main features
Home page (/): Welcome page with information about Python.
Message form (/message.html): A form for entering and sending messages via the UDP server.
Message processing: The data provided by the user (names and messages) is sent to the UDP server, which saves it to a JSON file.
How it works.
The user opens the main page or a form to send messages via a web browser.
When the user submits the form, the data is sent to an HTTP server.
The HTTP server sends the data to a UDP server.
The UDP server processes the data and stores it in the data.json file.
The program demonstrates the basic integration between HTTP and UDP protocols, as well as containerization capabilities for deployment.


## Notes
Ensure the storage directory exists on your host machine. It will be created if it doesn't exist, but it must be present for Docker volume mounting.
Modify the HTML files and Python scripts as needed for your project.
