import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta


def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(st.secrets["firebase"])
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://tinker-lab-manager-default-rtdb.firebaseio.com/'
        })


def mark_in_use(booking_id):
    init_firebase()
    ref = db.reference(f"/bookings/{booking_id}")
    ref.update({
        "status": "in-use",
        "checkout_time": datetime.now().isoformat()
    })


def mark_returned(booking_id):
    init_firebase()
    ref = db.reference(f"/bookings/{booking_id}")
    ref.update({
        "status": "returned",
        "return_time": datetime.now().isoformat()
    })

    # Also update equipment quantity
    booking = ref.get()
    if booking:
        equip_ref = db.reference(f"/equipments/{booking['equipment_id']}")
        equipment = equip_ref.get()
        if equipment:
            equipment["quantity"] = int(equipment.get("quantity", 0)) + 1
            equip_ref.update({"quantity": equipment["quantity"]})


def generate_time_slots(duration_hours=3):
    from datetime import datetime, timedelta
    now = datetime.now()
    slots = []
    for day in range(3):
        date = now + timedelta(days=day)
        for hour in range(0, 24, duration_hours):
            start = datetime(date.year, date.month, date.day, hour)
            end = start + timedelta(hours=duration_hours)
            slot = f"{start.strftime('%Y-%m-%d %H:%M')} - {end.strftime('%H:%M')}"
            if start > now:
                slots.append(slot)
    return slots


def add_booking_request(data_dict):
    init_firebase()
    ref = db.reference("/booking_requests")
    ref.child(data_dict["booking_id"]).set(data_dict)


def get_all_bookings_for_user(user_email):
    init_firebase()
    ref = db.reference("/booking_requests")
    data = ref.get()
    return [d for d in data.values() if d["user"] == user_email] if data else []


def get_all_bookings():
    init_firebase()
    ref = db.reference("/booking_requests")
    return ref.get() or {}


def update_booking_status(booking_id, new_status):
    init_firebase()
    ref = db.reference(f"/booking_requests/{booking_id}")
    booking = ref.get()
    if booking:
        ref.update({
            "status": new_status,
            "checkout_time": datetime.now().isoformat() if new_status == "accepted" else None
        })

        if new_status == "accepted":
            # Update equipment quantity
            equip_ref = db.reference(f"/equipments/{booking['equipment_id']}")
            equipment = equip_ref.get()
            if equipment and equipment.get("quantity", 0) > 0:
                new_qty = equipment["quantity"] - 1
                equip_ref.update({"quantity": new_qty})


def add_or_update_equipment(equip_id, equip_data: dict):
    init_firebase()
    ref = db.reference("/equipments")
    ref.child(equip_id).set(equip_data)


def encode_email(email):
    return email.replace(".", "_").replace("@", "_at_")


def add_new_person(email, name, password, department, role="Student"):
    init_firebase()
    ref = db.reference("/users")
    encoded_email = encode_email(email)
    ref.child(encoded_email).set({
        "name": name,
        "password": password,
        "department": department,
        "role": role,
        "email": email
    })
    return True


def update_student(email, updated_data: dict):
    init_firebase()
    ref = db.reference("/users")

    if ref.child(email).get() is None:
        return False  # user not found

    ref.child(email).update(updated_data)
    return True


def get_all_users():
    init_firebase()
    ref = db.reference("/users")
    data = ref.get()
    if data is None:
        return {}
    return data


def add_equipment(equip_id, name, description, status, quantity, category, image_url=""):
    init_firebase()
    ref = db.reference("/equipments")

    if ref.child(equip_id).get() is not None:
        return False

    ref.child(equip_id).set({
        "name": name,
        "description": description,
        "status": status,
        "quantity": quantity,
        "image_url": image_url,
        "category": category
    })
    return True


def update_equipment(equip_id, updated_data: dict):
    init_firebase()
    ref = db.reference("/equipments")

    if ref.child(equip_id).get() is None:
        return False

    ref.child(equip_id).update(updated_data)
    return True


def get_all_equipments():
    init_firebase()
    ref = db.reference("/equipments")
    data = ref.get()
    return data if data else {}


def get_equipment_by_id(equip_id):
    init_firebase()
    ref = db.reference(f"/equipments/{equip_id}")
    return ref.get()


def delete_equipment(equip_id):
    init_firebase()
    ref = db.reference("/equipments")

    if ref.child(equip_id).get() is None:
        return False
    ref.child(equip_id).delete()
    return True
def check_in_booking(booking_id):
    init_firebase()

    ref = db.reference(f"/booking_requests/{booking_id}")
    booking = ref.get()
    if not booking:
        return False

    # Update check-in time
    ref.update({"checkin_time": datetime.now().isoformat()})

    # Update equipment quantity
    eq_ref = db.reference(f"/equipments/{booking['equipment_id']}")
    equipment = eq_ref.get()
    if equipment:
        eq_ref.update({
            "quantity": equipment.get("quantity", 0) + 1
        })

    return True


# add_new_person("test123@gmail.com","aayush" , "test", "cse")
users = get_all_users()
