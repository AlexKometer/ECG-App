import json
import os
from classes import Person

"""Load the user data from the JSON file."""
def load_user_data():
    try:
        with open('data/users.json') as file:
            user_data = json.load(file)
        return user_data
    except json.JSONDecodeError:
        return []  # Return an empty list if JSON is invalid or empty

 """Save the user data to the JSON file."""
def save_user_data(user_data):

    with open('data/users.json', 'w') as file:
        json.dump(user_data, file, indent=4)

"""checks for the next unused ID"""
def get_next_id():
    person_dict = Person.load_person_data()
    ids = [entry["id"] for entry in person_dict]
    return max(ids) + 1 if ids else 1

"""saving the picture of a subject"""
def save_picture(picture, firstname, lastname):
    picture_dir = "data/pictures/"
    os.makedirs(picture_dir, exist_ok=True)
    picture_path = os.path.join(picture_dir, f"{firstname}_{lastname}.jpg")
    with open(picture_path, "wb") as f:
        f.write(picture.getbuffer())
    return picture_path

"""adding a owner to the subject"""
def save_new_subject(new_subject, owner):
    person_dict = Person.load_person_data()
    new_subject["owner"] = owner  # Add the owner field
    person_dict.append(new_subject)
    with open('data/person_db.json', 'w') as f:
        json.dump(person_dict, f, indent=4)

"""grands the user permissions"""
def get_user_permissions(username):
    user_data = load_user_data()
    for user in user_data:
        if user['username'] == username:
            return user.get('permissions', [])
    return []

"""updating a user permission"""
def update_user_permissions(username, permissions):
    user_data = load_user_data()
    for user in user_data:
        if user['username'] == username:
            user['permissions'] = permissions
            break
    save_user_data(user_data)

"""deleting a  user from the Database"""
def delete_user(username):
    user_data = load_user_data()
    user_data = [user for user in user_data if user['username'] != username]
    save_user_data(user_data)

""""updating a subject"""
def update_subject(subject):
    person_dict = Person.load_person_data()
    for idx, entry in enumerate(person_dict):
        if entry["id"] == subject.id:
            person_dict[idx] = subject.to_dict()
            break
    with open('data/person_db.json', 'w') as f:
        json.dump(person_dict, f, indent=4)