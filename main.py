import streamlit as st
import sqlite3

conn = sqlite3.connect('packtrack.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS shipments (
    id INTEGER PRIMARY KEY,
    package_name TEXT,
    origin TEXT,
    destination TEXT,
    shipping_option TEXT,
    payment BOOLEAN
)
''')
conn.commit()

st.title("Pack&Track Express")

st.sidebar.subheader("Express Shipment")

package_name = st.sidebar.text_input("Package Name")
origin = st.sidebar.text_input("Origin")
destination = st.sidebar.text_input("Destination")
shipping_option = st.sidebar.selectbox("Shipping Option", ["Standard", "Express"])
payment = st.sidebar.checkbox("Pay Now")

if st.sidebar.button("Submit Shipment"):
  
    c.execute("INSERT INTO shipments (package_name, origin, destination, shipping_option, payment) VALUES (?, ?, ?, ?, ?)",
              (package_name, origin, destination, shipping_option, payment))
    conn.commit()
    st.write(f"Shipment Scheduled: {package_name} from {origin} to {destination} via {shipping_option}")
    if payment:
        st.write("Payment Processed")

st.subheader("Track Your Shipment")
tracking_id = st.text_input("Enter Tracking ID")
if st.button("Track Shipment"):
   
    c.execute("SELECT * FROM shipments WHERE id=?", (tracking_id,))
    result = c.fetchone()
    if result:
        st.write(f"Shipment Information for ID {tracking_id}:")
        st.write(f"Package Name: {result[1]}")
        st.write(f"Origin: {result[2]}")
        st.write(f"Destination: {result[3]}")
        st.write(f"Shipping Option: {result[4]}")
        st.write("Payment Processed" if result[5] else "Payment Pending")
    else:
        st.write("Shipment not found")


if st.sidebar.checkbox("Admin Panel"):
    st.subheader("Admin Panel")
    c.execute("SELECT * FROM shipments")
    all_shipments = c.fetchall()

    if all_shipments:
        st.write("All Shipments:")
        for shipment in all_shipments:
            st.write(f"ID: {shipment[0]}, Package Name: {shipment[1]}, Origin: {shipment[2]}, Destination: {shipment[3]}")
    else:
        st.write("No shipments to display")


conn.close()
