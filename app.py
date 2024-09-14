import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL
import datetime
from twilio.rest import Client
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

mysql = MySQL(app)

# Routes
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    
    # Total Events
    cur.execute("SELECT COUNT(*) FROM events")
    total_events = cur.fetchone()[0]
    
    # Upcoming Events
    today = datetime.date.today()
    cur.execute("SELECT COUNT(*) FROM events WHERE event_date >= %s", (today,))
    upcoming_events = cur.fetchone()[0]
    
    # Total Attendees
    cur.execute("SELECT COUNT(*) FROM rsvps")
    total_attendees = cur.fetchone()[0]
    
    # Avg. Attendees/Event
    cur.execute("SELECT AVG(attendee_count) FROM (SELECT COUNT(*) as attendee_count FROM rsvps GROUP BY event_id) AS subquery")
    avg_attendees = cur.fetchone()[0]
    if avg_attendees:
        avg_attendees = round(avg_attendees, 2)
    else:
        avg_attendees = 0
    
    # Recent Events
    cur.execute("SELECT e.id, e.name, e.event_date, COUNT(r.id) as attendees FROM events e LEFT JOIN rsvps r ON e.id = r.event_id GROUP BY e.id ORDER BY e.event_date DESC LIMIT 5")
    recent_events = cur.fetchall()
    
    cur.close()
    
    return render_template('index.html', 
                        total_events=total_events,
                        upcoming_events=upcoming_events,
                        total_attendees=total_attendees,
                        avg_attendees=avg_attendees,
                        recent_events=recent_events)


@app.route('/dashboard_data')
def dashboard_data():
    cur = mysql.connection.cursor()
    
    # Total Events
    cur.execute("SELECT COUNT(*) FROM events")
    total_events = cur.fetchone()[0]
    
    # Upcoming Events
    today = datetime.date.today()
    cur.execute("SELECT COUNT(*) FROM events WHERE event_date >= %s", (today,))
    upcoming_events = cur.fetchone()[0]
    
    # Total Attendees
    cur.execute("SELECT COUNT(*) FROM rsvps")
    total_attendees = cur.fetchone()[0]
    
    # Avg. Attendees/Event
    cur.execute("SELECT AVG(attendee_count) FROM (SELECT COUNT(*) as attendee_count FROM rsvps GROUP BY event_id) AS subquery")
    avg_attendees = cur.fetchone()[0]
    if avg_attendees:
        avg_attendees = round(avg_attendees, 2)
    else:
        avg_attendees = 0
    
    # Recent Events
    cur.execute("SELECT e.id, e.name, e.event_date, COUNT(r.id) as attendees FROM events e LEFT JOIN rsvps r ON e.id = r.event_id GROUP BY e.id ORDER BY e.event_date DESC LIMIT 5")
    recent_events = cur.fetchall()
    
    cur.close()
    
    return jsonify({
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'total_attendees': total_attendees,
        'avg_attendees': avg_attendees,
        'recent_events': [
            {
                'id': event[0],
                'name': event[1],
                'date': event[2].strftime('%Y-%m-%d'),
                'attendees': event[3]
            } for event in recent_events
        ]
    })


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

@app.route('/generate_report')
@app.route('/generate_report')
def generate_report():
    cur = mysql.connection.cursor()
    
    # Get event data for the past 6 months
    six_months_ago = datetime.date.today() - datetime.timedelta(days=180)
    cur.execute("SELECT DATE_FORMAT(event_date, '%%Y-%%m') as month, COUNT(*) as count FROM events WHERE event_date >= %s GROUP BY month ORDER BY month", (six_months_ago,))
    event_data = cur.fetchall()
    
    cur.close()
    
    # Prepare data for the chart
    months = [data[0] for data in event_data]
    counts = [data[1] for data in event_data]
    
    # Create the chart
    plt.figure(figsize=(12, 6))
    bars = plt.bar(months, counts, color='skyblue', edgecolor='black')
    
    # Add title and labels
    plt.title('Events per Month (Last 6 Months)', fontsize=16, fontweight='bold')
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Number of Events', fontsize=14)
    plt.xticks(rotation=45, fontsize=12)
    plt.yticks(fontsize=12)
    
    # Add value labels on top of the bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center', fontsize=12, fontweight='bold')
    
    # Add gridlines for better readability
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save the chart to a base64 encoded string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    chart_image = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    
    return jsonify({'chart_image': chart_image})



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
