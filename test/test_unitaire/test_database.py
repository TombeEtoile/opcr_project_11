import pytest
from server import app, load_clubs, load_competitions


# TEST CLUBS.JSON
def test_clubs_name_type():
    for club in load_clubs():
        assert isinstance(club['name'], str)


def test_clubs_email_type():
    for club in load_clubs():
        assert isinstance(club['email'], str)


def test_clubs_points_type():
    for club in load_clubs():
        assert isinstance(club['points'], int)


def test_negative_clubs_point():
    for club in load_clubs():
        assert club['points'] >= 0


# TEST COMPETITIONS.JSON
def test_competitions_name_type():
    for competition in load_competitions():
        assert isinstance(competition['name'], str)


def test_competitions_date_type():
    for competition in load_competitions():
        assert isinstance(competition['date'], str)


def test_competitions_available_places_type():
    for competition in load_competitions():
        assert isinstance(competition['available_places'], int)


def test_negative_competitions_available_places():
    for competition in load_competitions():
        assert competition['available_places'] >= 0
