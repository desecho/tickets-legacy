# Tickets

The interface is in Russian.

# Description

The system allows to add, edit and close tickets, browse the calendar of tickets, print ticket report for today. 

## Additional information
When choosing a date range, the date field is ignored. 

## Access rights
Users can add and edit tickets. Administrators can close tickets. Superadministrators can add ticket types, etc. 
    
## Installation instructions

* Insert your database settings and modify the variables in the following file:
    * /tickets_project/settings.py
* Run install.sh
* Modify the following files:
    * /templates/report_header.html
    * /static/js/settings.js
* Import db.sql to your database. db.sql also includes some example data.
