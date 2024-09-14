from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import datetime
from twilio.rest import Client
import os

app = Flask(__name__)



twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

mysql = MySQL(app)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def list_events():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events ORDER BY event_date")
    events = cur.fetchall()
    cur.close()
    return render_template('event_list.html', events=events)

@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        event_date = request.form['event_date']
        venue = request.form['venue']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO events (name, description, event_date, venue) VALUES (%s, %s, %s, %s)",
                    (name, description, event_date, venue))
        mysql.connection.commit()

        event_id = cur.lastrowid
        log_activity(f'Created event: {name} (ID: {event_id})')
        flash('Event created successfully!', 'success')
        return redirect(url_for('list_events'))
    return render_template('create_event.html')

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM events WHERE id = %s", (event_id,))
    mysql.connection.commit()
    cur.close()

    log_activity(f'Deleted event with ID: {event_id}')
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('list_events'))

@app.route('/rsvp/<int:event_id>', methods=['POST'])
def rsvp(event_id):
    user_name = request.form['user_name']
    user_phone = request.form['user_phone']
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO rsvps (event_id, user_name, user_phone) VALUES (%s, %s, %s)", 
                (event_id, user_name, user_phone))
    mysql.connection.commit()

    log_activity(f'{user_name} (phone: {user_phone}) RSVP\'d to event ID {event_id}')
    flash('RSVP successful!', 'success')
    return redirect(url_for('list_events'))

@app.route('/view_attendees/<int:event_id>')
def view_attendees(event_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_name, user_phone FROM rsvps WHERE event_id = %s", (event_id,))
    attendees = cur.fetchall()
    cur.close()
    return render_template('attendees.html', attendees=attendees, event_id=event_id)

@app.route('/send_reminder/<int:event_id>')
def send_reminder(event_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM events WHERE id = %s", (event_id,))
    event = cur.fetchone()
    
    cur.execute("SELECT user_name, user_phone FROM rsvps WHERE event_id = %s", (event_id,))
    attendees = cur.fetchall()
    
    for attendee in attendees:
        # Ensure phone number is correctly formatted for Twilio
        formatted_phone = format_phone_number(attendee[1])
        message_body = f"Hi {attendee[0]}, this is a reminder about {event[1]} on {event[3]} at {event[4]}. We look forward to seeing you there!"
        
        send_sms(formatted_phone, message_body)
    
    log_activity(f'Sent reminders for event ID {event_id}')
    flash('Reminders sent successfully!', 'success')
    return redirect(url_for('list_events'))

@app.route('/notifications')
def check_notifications():
    cur = mysql.connection.cursor()
    today = datetime.datetime.now()
    one_week_later = today + datetime.timedelta(days=7)
    
    cur.execute("SELECT * FROM events WHERE event_date BETWEEN %s AND %s ORDER BY event_date", (today, one_week_later))
    upcoming_events = cur.fetchall()
    cur.close()
    
    return jsonify({'upcoming_events': upcoming_events})

@app.route('/activity_logs')
def activity_logs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_activity ORDER BY timestamp DESC LIMIT 100")
    logs = cur.fetchall()
    cur.close()
    return render_template('activity_logs.html', logs=logs)

# Helper functions
def log_activity(action):
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user_activity (action) VALUES (%s)", (action,))
    mysql.connection.commit()
    cur.close()

def format_phone_number(phone_number):
    # Ensure +91 for Indian numbers
    if not phone_number.startswith('+'):
        return '+91' + phone_number
    return phone_number

def send_sms(to_number, body):
    try:
        message = twilio_client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_number
        )
        print(f"SMS sent successfully. SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")
        flash(f'Failed to send SMS to {to_number}: {str(e)}', 'error')

if __name__ == "__main__":
    app.run(debug=True)
