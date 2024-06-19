import streamlit as st
from datetime import datetime, timedelta
import time
import pytz

# Set the page configuration to use the entire screen width
st.set_page_config(layout="wide")

# Define the desired time zone
time_zone = pytz.timezone('Europe/Paris')  # Change to your desired time zone

# Function to get current time and date
def get_current_time():
    return datetime.now(time_zone).strftime('%H:%M:%S')

def get_current_date():
    return datetime.now(time_zone).strftime("%A, %B %d, %Y")

# Function to update the event list
def update_event_list(events):
    current_time = datetime.now(time_zone)
    upcoming_events = [(name, date) for name, date in events if date > current_time]
    return upcoming_events

# Function to get the next event and time remaining
def get_next_event(events):
    current_time = datetime.now(time_zone)
    for event_name, event_date in events:
        if event_date > current_time:
            return event_name, event_date - current_time
    return None, None

# List of events with time zone information
events = [
    ("Cars ready", time_zone.localize(datetime(2024, 7, 1, 8, 30, 0))),
    ("Morning session start", time_zone.localize(datetime(2024, 7, 1, 9, 0, 0))),
    ("Morning session end", time_zone.localize(datetime(2024, 7, 1, 12, 0, 0))),
    ("Cars ready", time_zone.localize(datetime(2024, 7, 1, 13, 00, 0))),
    ("Afternoon session start", time_zone.localize(datetime(2024, 7, 1, 13, 30, 0))),
    ("Afternoon session end", time_zone.localize(datetime(2024, 7, 1, 17, 40, 0))),
    ("Boxes must be empty", time_zone.localize(datetime(2024, 7, 1, 20, 00, 0))),

    ("Track walk start", time_zone.localize(datetime(2024, 7, 4, 17, 15, 0))),
    ("Team managers meeting start", time_zone.localize(datetime(2024, 7, 4, 19, 0, 0))),
    ("Team managers meeting end", time_zone.localize(datetime(2024, 7, 4, 20, 0, 0))),

    ("Drivers briefing start", time_zone.localize(datetime(2024, 7, 5, 9, 0, 0))),
    ("Drivers briefing end", time_zone.localize(datetime(2024, 7, 5, 9, 30, 0))),
    ("Free practice 1 start", time_zone.localize(datetime(2024, 7, 5, 9, 50, 0))),
    ("Free practice 1 end", time_zone.localize(datetime(2024, 7, 5, 10, 30, 0))),
    ("Free practice 2 start", time_zone.localize(datetime(2024, 7, 5, 14, 15, 0))),
    ("Free practice 2 end", time_zone.localize(datetime(2024, 7, 5, 14, 55, 0))),

    ("Qualifying start", time_zone.localize(datetime(2024, 7, 6, 11, 45, 0))),
    ("Qualifying end", time_zone.localize(datetime(2024, 7, 6, 12, 20, 0))),
    ("Pitlane open", time_zone.localize(datetime(2024, 7, 6, 16, 15, 0))),
    ("Race 1 start", time_zone.localize(datetime(2024, 7, 6, 16, 35, 0))),
    ("Race 1 end", time_zone.localize(datetime(2024, 7, 6, 17, 10, 0))),

    ("Pitlane open", time_zone.localize(datetime(2024, 7, 7, 8, 20, 0))),
    ("Race 2 start", time_zone.localize(datetime(2024, 7, 7, 9, 0, 0))),
    ("Race 2 end", time_zone.localize(datetime(2024, 7, 7, 9, 35, 0))),

    
]

# Create columns for time of day and countdown
col_time, col_countdown = st.columns([2, 2])

with col_time:
    time_placeholder = st.empty()

with col_countdown:
    countdown_placeholder = st.empty()

# Create a container for the event list below the time and countdown
st.write('---')  # Add a horizontal line for separation
event_list_placeholder = st.empty()

# Main update function
def update():
    # Update current time and date
    time_placeholder.markdown(f"<h2 style='margin-bottom: 0px;'>Time:</h2> <p style='font-size:150px; margin-bottom: 0px;'>{get_current_time()}</p><h2 style='margin-bottom: 0px;'>Date: {get_current_date()}</h2>", unsafe_allow_html=True)

    # Update the countdown for the next event
    event_name, time_remaining = get_next_event(events)
    if event_name:
        hours, remainder = divmod(time_remaining.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        countdown_placeholder.markdown(f"<h2 style='margin-bottom: 0px;'>Next Event:</h2> <p style='font-size:80px; margin-bottom: 0px;'>{event_name}</p><p style='font-size:150px; margin-bottom: 0px;'><span style='background-color:blue'>{hours:02d}:{minutes:02d}:{seconds:02d}</span></p>", unsafe_allow_html=True)
    else:
        countdown_placeholder.markdown("<h2>No upcoming events</h2>", unsafe_allow_html=True)

    # Update the event list
    upcoming_events = update_event_list(events)
    
    event_names = [name for name, date in upcoming_events]
    event_dates = [date.strftime('%A %Y-%m-%d') for name, date in upcoming_events]
    event_times = [date.strftime('%H:%M') for name, date in upcoming_events]
    event_countdowns = [(date - datetime.now(time_zone)).total_seconds() for name, date in upcoming_events]
    
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    
    with col1:
        st.markdown("<h2 style='margin-bottom: 0px;'><u>Event Name</u></h2>", unsafe_allow_html=True)
        for event in event_names:
            st.markdown(f"<p style='font-size:35px; margin-bottom: 0px;'>{event}</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h2 style='margin-bottom: 0px;'><u>Date</u></h2>", unsafe_allow_html=True)
        for date in event_dates:
            st.markdown(f"<p style='font-size:35px; margin-bottom: 0px;'>{date}</p>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<h2 style='margin-bottom: 0px;'><u>Time</u></h2>", unsafe_allow_html=True)
        for time in event_times:
            st.markdown(f"<p style='font-size:35px; margin-bottom: 0px;'>{time}</p>", unsafe_allow_html=True)

    with col4:
        st.markdown("<h2 style='margin-bottom: 0px;'><u>Countdown</u></h2>", unsafe_allow_html=True)
        for time in event_countdowns:
            if time > 0:
                hours, remainder = divmod(int(time), 3600)
                minutes, seconds = divmod(remainder, 60)
                st.markdown(f"<p style='font-size:35px; margin-bottom: 0px;'><span style='color:Lime'>{hours:02d}:{minutes:02d}:{seconds:02d}</span></p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='font-size:35px; margin-bottom: 0px;'>00:00:00</p>", unsafe_allow_html=True)

# Initial call to update
update()

# Set the app to refresh every second using st.experimental_rerun
while True:
    time.sleep(1)
    st.experimental_rerun()
