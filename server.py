from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Load the prayer times from the JSON file
with open('prayer_times.json') as f:
    prayer_times_data = json.load(f)

def get_prayer_times_for_day(date):
    formatted_date = date.strftime('%Y-%m-%d')
    return prayer_times_data.get(formatted_date, {})

def get_upcoming_prayer(prayer_times):
    now = datetime.now().time()
    for prayer, time_str in prayer_times.items():
        prayer_time = datetime.strptime(time_str, '%H:%M').time()
        if prayer_time > now:
            return prayer, prayer_time
    return None, None

def format_time_diff(time_diff):
    hours, remainder = divmod(time_diff.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

def get_current_prayer(prayer_times):
    now = datetime.now().time()
    current_prayer = None
    for prayer, time_str in prayer_times.items():
        prayer_time = datetime.strptime(time_str, '%H:%M').time()
        if prayer_time <= now:
            current_prayer = prayer
    return current_prayer

current_date = datetime.now().date()

@app.route('/')
def index():
    prayer_times = get_prayer_times_for_day(current_date)
    upcoming_prayer, prayer_time = get_upcoming_prayer(prayer_times)
    countdown = None
    if upcoming_prayer:
        current_datetime = datetime.combine(current_date, datetime.now().time())
        prayer_datetime = datetime.combine(current_date, prayer_time)
        time_diff = prayer_datetime - current_datetime
        countdown = format_time_diff(time_diff)
    
    current_prayer = get_current_prayer(prayer_times)
    
    return render_template('index.html', current_date=current_date, prayer_times=prayer_times, upcoming_prayer=upcoming_prayer, countdown_upcoming=countdown, current_prayer=current_prayer)

@app.route('/prev', methods=['POST'])
def prev_day():
    global current_date
    current_date -= timedelta(days=1)
    return redirect(url_for('index'))

@app.route('/next', methods=['POST'])
def next_day():
    global current_date
    current_date += timedelta(days=1)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
