from aiogram.fsm.state import StatesGroup, State
import json
import sqlite3

base = sqlite3.connect('Base.db')
cur = base.cursor()

def load_json():
    with open("starter/cfg.json", encoding="utf-8") as infile:
        return json.load(infile)

def write_json(content):
    with open("starter/cfg.json", "w") as outfile:
        json.dump(content, outfile, ensure_ascii=True, indent=4)

def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False

class Other(StatesGroup):
    name = State()
    name_edit = State()
    date = State()
    date_edit = State()
    end_date = State()
    end_date_edit = State()
    adres = State()
    adres_edit = State()
    who = State()
    who_edit = State()
    descrip = State()
    descrip_edit = State()
    count = State()
    count_edit = State()
    photo = State()
    contact = State()
    contact_edit = State()
    editmpid = State()
    deletempid = State()