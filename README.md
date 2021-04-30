# Tickets

The interface is in Russian.

**Warning**: Django has to be upgraded because the version used in this project is no longer supported.

# Description

The system allows to add, edit and close tickets, browse the calendar of tickets, print ticket report for today. 

## Additional information
When choosing a date range, the date field is ignored.    
Days off should be entered with a number of the day of the week and separated by `,`. For example `1,2` - Monday and Tuesday.  
Images will be saved in `img` directory.

## Access rights
Users can add and edit tickets. Administrators can close tickets. Superadministrators can add ticket types, etc. 

## Prerequisites
* Docker
* Docker-compose
* Make
* Bower
* MySQL. You can use [mysql-docker](https://github.com/desecho/mysql-docker)

You can use [ubuntu-vm](https://github.com/desecho/ubuntu-vm) as a development VM.

## Installation instructions

* Modify the variables in the following file if needed:
    * `tickets_project/tickets_project/settings.py`
* Run `make bootstrap`
* Modify the following files:
    * `tickets_project/templates/report_header.html`
    * `tickets_project/static/js/settings.js`
* Depending on the availability of the API the `getSubscriberData` in `/tickets_project/static/js/edit_ticket.js` needs to be modified
* Enter the data on the admin page
* Add logo here - `tickets_project/static/img/logo.gif`

## Running 

To run in docker run:
```bash
make build
make run 
```

Open http://localhost:8000/ to access the web application.  
Open http://localhost:8000/admin to access the admin section.
