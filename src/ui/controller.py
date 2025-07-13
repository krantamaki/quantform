"""@package ui.controller
@author Kasper Rantamäki
The controller for handling the HTTP requests

Basic controller layer for handling HTTP requests. For more information
see e.g. the tutorial at Flask's webpage https://flask.palletsprojects.com/en/stable/tutorial/.
The controller works as an entrypoint for a Task object used to run the 
webpage from the Scheduler (ran once with a single worker as the first task)
"""
from flask import Flask
