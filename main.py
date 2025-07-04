import streamlit as st
import time
import Database as dt


def encode_email(email):
    return email.replace(".", "_").replace("@", "_at_")
def add_footer():
    st.markdown("""
        <hr style="margin-top: 50px; margin-bottom: 10px; border: none; border-top: 1px solid #ccc;" />
        <p style="text-align: center; color: #888; font-size: 14px; font-family: 'Segoe UI', sans-serif;">
            © 2025 <strong style="color: #0077ff;">Aayushya-Paswan</strong> | All Rights Reserved 🚀 <br>
            <a href="https://www.linkedin.com/in/aayushya78" target="_blank" style="color: #0077ff; text-decoration: none;">
                🔗 Connect on LinkedIn
            </a>
        </p>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=30)
def get_all_users_cached():
    return dt.get_all_users()

@st.cache_data(ttl=10)
def get_all_equipments_cached():
    return dt.get_all_equipments()

@st.cache_data(ttl=5)
def get_all_bookings_cached():
    return dt.get_all_bookings()

def decode_email(encoded):
    return encoded.replace("_at_", "@").replace("_", ".")


if 'mode' not in st.session_state:
    st.session_state.mode = 'login'

if 'show_bookings' not in st.session_state:
    st.session_state.show_bookings = False


st.markdown("<h2 style='text-align: center;'>🔐 TinkerLab Portal</h2>", unsafe_allow_html=True)
st.markdown("---")

users = get_all_users_cached()

# ---------------- SIGNUP ----------------
if st.session_state.mode == 'signup':
    st.subheader("📝 Create a New Account")

    name = st.text_input("Full Name", key="signup_name")
    email = st.text_input("Email", key="signup_email", placeholder="xyz@gmail.com")
    password = st.text_input("Password", type="password", key="signup_pass")
    dept = st.selectbox("Department", ["CSE", "ECE", "MECH", "Smart manufacturing", "Design"], key="signup_dept")
    role = st.selectbox("Role", ["Student", "Admin"], key="signup_role")

    if st.button("Create Account"):
        if name != "" and email != "" and password != "":
            encoded_email = encode_email(email)
            if encoded_email in users:
                st.warning("⚠️ Account already exists! Please log in.")
            else:
                dt.add_new_person(email, name, password, dept, role)
                st.success("✅ Account created successfully!")
                time.sleep(2)
                st.session_state.mode = 'login'
                st.rerun()
        else:
            st.warning("Fill all the details.")

    if st.button("🔄 Already signed in? Switch to Login"):
        st.session_state.mode = 'login'
        st.rerun()

    add_footer()

elif st.session_state.mode == 'login':
    st.subheader("🔓 Login to Your Account")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        encoded_email = encode_email(email)
        if encoded_email not in users:
            st.warning("👤 No account found. Please sign up!")
        elif users[encoded_email]["password"] != password:
            st.error("❌ Incorrect password")
        else:
            st.session_state.email = email
            st.session_state.mode = 'Home'
            st.rerun()

    if st.button("🔄 Create an account"):
        st.session_state.mode = 'signup'
        st.rerun()
    add_footer()
elif st.session_state.mode == 'Home':
    user = users[encode_email(st.session_state.email)]

    if user["role"] == "Student":
        if st.session_state.show_bookings:
            col1, col2, col3 = st.columns([2,2,1])
            with col2:
                if st.button("🏠 Back to Equipment Catalog"):
                    st.session_state.show_bookings = False
                    st.rerun()
            st.subheader("📊 My Booking Requests")



            bookings = dt.get_all_bookings_for_user(st.session_state.email)

            if not bookings:
                st.info("ℹ  No bookings made yet.")
            else:
                for bk in bookings:
                    st.markdown(f"**🛠 {bk['equipment_name']}** — `{bk['slot']}`")
                    st.markdown(f"📌 Status: `{bk['status']}` | Purpose: {bk['purpose']}")
                    st.caption(f"🕒 Requested on {bk['timestamp'].split('T')[0]}")
                    if bk['status'] == "accepted":
                        st.success("✅ Accepted!")
                    elif bk['status'] == "rejected":
                        st.error("❌ Rejected")
                    st.markdown("---")
        else:
            st.subheader("📦 EQUIPMENT CATALOG")

            col1, col2, col3 = st.columns([2, 2, 1])
            user_name = user['name']
            dept = user['department']
            with col2:
                if st.button("📊 My Bookings"):
                    st.session_state.show_bookings = True
                    st.rerun()
            st.markdown(f"""
                <h2 style="
                    font-family: 'Segoe UI', sans-serif;
                    font-weight: bold;
                    text-align: center;
                    margin-top: 20px;
                    margin-bottom: 10px;
                    color: #0077ff;
                ">
                    🎓 Welcome, <span style='color:red'>{user_name}</span> from <span style='color:red'>{dept}</span> branch
                </h2>
            """, unsafe_allow_html=True)

            st.markdown("---")

            st.sidebar.markdown("## 🔍 Filter Equipments")
            search = st.sidebar.text_input("Search by name")
            category = st.sidebar.selectbox("Category", ["All", "mechanical", "electronics", "testing"])
            slot_duration = st.sidebar.selectbox("⏱️ Select Slot Duration", [1, 2, 3], index=2)  # default 3 hrs



            eq_data = get_all_equipments_cached()
            if not eq_data:
                st.info("⚠️ No equipment available currently. Admin has not deployed any equipments.")
            else:
                st.subheader("📦 EQUIPMENT CATALOG")
                filtered_eq = {}

                for eid, eq in eq_data.items():
                    name_match = search.lower() in eq.get("name", "").lower() or search.lower() in eq.get("description",
                                                                                                          "").lower()
                    cat_match = category == "All" or eq.get("category", "Others").lower() == category.lower()

                    if name_match and cat_match:
                        filtered_eq[eid] = eq

                if not filtered_eq:
                    st.warning("No equipment matches your filters.")
                else:
                    for eid, eq in filtered_eq.items():
                        with st.container():
                            st.header(f"{eq['name']}")
                            image_url = eq.get("image_url") or "https://via.placeholder.com/300x200.png?text=No+Image"
                            yt_video = eq.get("video_url", "")

                            st.image(image_url, width=300, caption=eq["name"])
                            st.markdown(f"**Category:** {eq['category']}")
                            st.markdown(f"**📘 Description:** {eq['description']}")
                            st.markdown(
                                f"**📍 Location:** {eq.get('location', 'TinkerLab')}  |  **Status:** `{eq['status']}`")
                            st.markdown(f"**📦 Available Units:** `{eq['quantity']}`")

                            if yt_video:
                                st.markdown(f"""
                                    <div style="text-align: center; margin-top: 10px;">
                                        <a href="{yt_video}" target="_blank" style="
                                            background-color: #FF0000;
                                            color: white;
                                            padding: 10px 20px;
                                            text-decoration: none;
                                            border-radius: 8px;
                                            display: inline-block;
                                            font-weight: bold;
                                            font-size: 16px;
                                            font-family: 'Segoe UI', sans-serif;
                                        ">
                                            ▶️ Watch Training Video on YouTube
                                        </a>
                                    </div>
                                """, unsafe_allow_html=True)

                            st.progress(eq["quantity"] / 10 if eq["quantity"] <= 10 else 1.0)

                            with st.expander("Book this equipment"):
                                from datetime import datetime

                                # Step 1: Get all bookings
                                all_bookings = get_all_bookings_cached()

                                # Step 2: Extract already-booked slots for this equipment
                                booked_slots = [
                                    booking["slot"] for booking in all_bookings.values()
                                    if booking["equipment_id"] == eid and booking["status"] == "accepted"
                                ]

                                # Step 3: Generate all possible time slots
                                all_slots = dt.generate_time_slots(duration_hours=slot_duration)

                                # Step 4: Filter only available ones
                                available_slots = [slot for slot in all_slots if slot not in booked_slots]

                                if not available_slots:
                                    st.info("No time slots available for this equipment in the next 3 days.")
                                else:
                                    slot = st.selectbox("Select Time Slot (Only available time slots given)", available_slots, key=f"{eid}_slot")
                                    purpose = st.text_input("Booking Purpose", key=f"{eid}_purpose")

                                    if st.button("Request Booking", key=f"{eid}_book"):
                                        booking_id = f"{eid}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                                        dt.add_booking_request({
                                            "booking_id": booking_id,
                                            "equipment_id": eid,
                                            "equipment_name": eq["name"],
                                            "slot": slot,
                                            "purpose": purpose,
                                            "status": "pending",
                                            "timestamp": datetime.now().isoformat(),
                                            "user": st.session_state.email
                                        })
                                        st.success("Booking request submitted! Waiting for admin approval.")
                        st.markdown("---")


                st.markdown("---")
                st.subheader("📊 My Booking Requests")
                bookings = dt.get_all_bookings_for_user(st.session_state.email)

                if not bookings:
                    st.info("ℹ  No bookings made yet.")
                else:
                    for bk in bookings:
                        st.markdown(f"**🛠 {bk['equipment_name']}** — `{bk['slot']}`")
                        st.markdown(f"📌 Status: `{bk['status']}` | Purpose: {bk['purpose']}")
                        st.caption(f"🕒 Requested on {bk['timestamp'].split('T')[0]}")
                        if bk['status'] == "accepted":
                            st.write("Congratulations! Your booking has been accepted by the admin")
                        if bk['status'] == "rejected":
                            st.write("Your booking could not be accepted due to some unavoidable reasons")
                        st.markdown("---")
        add_footer()
    else:
        st.title(f"🛡️ Welcome Admin, {user['name']}")
        st.subheader("🧾 Admin Control Panel")
        st.markdown("---")

        equipments = get_all_equipments_cached()
        bookings = get_all_bookings_cached()
        users = get_all_users_cached()

        tab1, tab2, tab3 = st.tabs(["📦 Equipment Manager", "📑 Booking Requests", "📈 Usage Tracking"])

        with tab1:
            st.markdown("### ➕ Add or Update Equipment")

            with st.form(key="update equipment"):
                eid = st.text_input("Equipment ID (unique, e.g. eq1)", value="")
                name = st.text_input("Equipment Name")
                description = st.text_area("Description")
                category = st.selectbox("Category", ["mechanical", "electronics", "testing"])
                status = st.selectbox("Status", ["available", "in-use", "maintenance"])
                quantity = st.number_input("Quantity", min_value=0, step=1)
                image_url = st.text_input("Image URL (optional)")
                video_url = st.text_input("Training YouTube Link (optional)")

                if st.form_submit_button("💾 Save Equipment"):
                    dt.add_or_update_equipment(eid, {
                        "name": name,
                        "description": description,
                        "status": status,
                        "quantity": quantity,
                        "image_url": image_url,
                        "video_url": video_url,
                        "category": category
                    })
                    st.success(f"✅ Equipment `{eid}` saved successfully!")
                    st.rerun()

            st.markdown("---")
            st.markdown("### 📋 Inventory")

            if not equipments:
                st.info("No equipments found.")
            else:
                for eid, eq in equipments.items():
                    with st.expander(f"🛠️ {eq['name']}"):
                        st.header(f"{eq['name']}")
                        st.subheader(f"{eid}")
                        st.write(f"**Description:** {eq['description']}")
                        st.write(f"**Status:** {eq['status']}")
                        st.write(f"**Quantity:** {eq['quantity']}")
                        if eq.get("image_url"):
                            st.image(eq["image_url"], width=300)

        # ---------------------- BOOKING MANAGEMENT ----------------------
        with tab2:
            st.markdown("### 📑 Pending Booking Requests")

            pending = {
                k: v for k, v in bookings.items()
                if v.get("status", "").lower().strip() == "pending"
            }

            if not pending:
                st.info("No pending requests.")
            else:
                for bkid, booking in pending.items():
                    user_email = booking["user"]
                    user_obj = users.get(encode_email(user_email), {})
                    student_name = user_obj.get("name", "Unknown")

                    st.markdown(f"#### 🔄 Booking ID: `{bkid}`")
                    st.markdown(f"👤 Student: **{student_name}** ({user_email})")
                    st.markdown(f"🛠 Equipment: `{booking['equipment_name']}`")
                    st.markdown(f"📅 Slot: `{booking['slot']}`")
                    st.markdown(f"📋 Purpose: {booking['purpose']}")
                    st.markdown(f"🕒 Requested: {booking['timestamp'].split('T')[0]}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Approve", key=f"approve_{bkid}"):
                            dt.update_booking_status(bkid, "accepted")
                            st.success("Approved!")
                            st.rerun()
                    with col2:
                        if st.button("❌ Reject", key=f"reject_{bkid}"):
                            dt.update_booking_status(bkid, "rejected")
                            st.warning("Rejected!")
                            st.rerun()
                    if booking["status"] == "accepted" and "checkin_time" not in booking:
                        if st.button("📥 Check-In", key=f"checkin_{bkid}"):
                            success = dt.check_in_booking(bkid)
                            if success:
                                st.success("Check-in completed.")
                                st.rerun()
                            else:
                                st.error("Failed to check-in booking.")


                    st.markdown("---")
        add_footer()

        with tab3:
            st.markdown("### 📈 Equipment Usage Logs")

            bookings = get_all_bookings_cached()
            if not bookings:
                st.info("No usage data available.")
            else:
                usage_logs = [bk for bk in bookings.values() if "checkin_time" in bk]

                if not usage_logs:
                    st.info("No check-in records yet.")
                else:
                    for log in usage_logs:
                        st.markdown(f"""
                            #### 🔧 {log['equipment_name']}
                            - 👤 User: `{log['user']}`
                            - ⏱️ Slot: `{log['slot']}`
                            - 📥 Checked In: `{log['checkin_time'].split('T')[0]}`
                            - 📌 Purpose: {log['purpose']}
                            ---
                        """)

