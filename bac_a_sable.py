import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from slugify import slugify


def load_clubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


competitions = load_competitions()

competitions_good_date = []
for competition in load_competitions():
    if competition['date'] >= str(datetime.now()):
        competitions_good_date.append(sorted(competition))

print(competitions_good_date)
print(datetime.now())
