# Simple HTTP Server


# Link for download docker image from docker hub
  https://hub.docker.com/r/fred99/simple-server
  
# docker command
  docker pull fred99/simple-server


# Usage
Open http://localhost:3000 in your browser to access the home page.
Navigate to http://localhost:3000/message.html to access the form for sending messages.
The form submission will be sent to the UDP server, and the data will be stored in storage/data.json.

## Notes
Ensure the storage directory exists on your host machine. It will be created if it doesn't exist, but it must be present for Docker volume mounting.
Modify the HTML files and Python scripts as needed for your project.
