import json
import os
from classes import Person

def load_user_data():
    """Load the user data from the JSON file."""
    try:
        with open('data/users.json') as file:
            user_data = json.load(file)
        return user_data
    except json.JSONDecodeError:
        return []  # Return an empty list if JSON is invalid or empty

def save_user_data(user_data):
    """Save the user data to the JSON file."""
    with open('data/users.json', 'w') as file:
        json.dump(user_data, file, indent=4)

def get_next_id():
    person_dict = Person.load_person_data()
    ids = [entry["id"] for entry in person_dict]
    return max(ids) + 1 if ids else 1

def save_picture(picture, firstname, lastname):
    picture_dir = "data/pictures/"
    os.makedirs(picture_dir, exist_ok=True)
    picture_path = os.path.join(picture_dir, f"{firstname}_{lastname}.jpg")
    with open(picture_path, "wb") as f:
        f.write(picture.getbuffer())
    return picture_path

def save_new_subject(new_subject, owner):
    person_dict = Person.load_person_data()
    new_subject["owner"] = owner  # Add the owner field
    person_dict.append(new_subject)
    with open('data/person_db.json', 'w') as f:
        json.dump(person_dict, f, indent=4)

def get_user_permissions(username):
    user_data = load_user_data()
    for user in user_data:
        if user['username'] == username:
            return user.get('permissions', [])
    return []

def update_user_permissions(username, permissions):
    user_data = load_user_data()
    for user in user_data:
        if user['username'] == username:
            user['permissions'] = permissions
            break
    save_user_data(user_data)

def delete_user(username):
    user_data = load_user_data()
    user_data = [user for user in user_data if user['username'] != username]
    save_user_data(user_data)
