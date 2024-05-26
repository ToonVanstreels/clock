import streamlit as st
from datetime import datetime, timedelta
import time

# Set the page configuration to use the entire screen width
st.set_page_config(layout="wide")

# Set the title of the web app
#st.title('RedAnt Racing Event Clock')

# Function to get current time and date
def get_current_time():
    return datetime.now().strftime('%H:%M:%S')

def get_current_date():
    return datetime.now().strftime("%A, %B %d, %Y")

# Function to update the event list
def update_event_list(events):
    current_time = datetime.now()
    upcoming_events = [(name, date) for name, date in events if date > current_time]
    return upcoming_events

# Function to get the next event and time remaining
def get_next_event(events):
    current_time = datetime.now()
    for event_name, event_date in events:
        if event_date > current_time:
            return event_name, event_date - current_time
    return None, None

# List of events
events = [
    ("Trackwalk start", datetime(2024, 5, 28, 19, 0, 0)),
    ("Trackwalk end ", datetime(2024, 5, 28, 20, 0, 0)),
    ("Pitlane open", datetime(2024, 5, 11, 10, 10, 0)),
    ("Race 1 start", datetime(2024, 5, 11, 10, 30, 0)),
    ("Race 1 end ", datetime(2024, 5, 11, 11, 5, 0))
]

# Create columns for time of day and countdown
col_time, col_countdown = st.columns([3, 4])

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
    
    col1, col2, col3 = st.columns([3,3,1])
    
    with col1:
        st.markdown("<h2 style='margin-bottom: 0px;'><u>Event Name</u></h2>", unsafe_allow_html=True)
        for event in event_names:
            st.markdown(f"<p style='font-size:30px; margin-bottom: 0px;'>{event}</p>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<h2 style='margin-bottom: 0px;'><u>Date</u></h2>", unsafe_allow_html=True)
        for date in event_dates:
            st.markdown(f"<p style='font-size:30px; margin-bottom: 0px;'>{date}</p>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<h2 style='margin-bottom: 0px;'><u>Time</u></h2>", unsafe_allow_html=True)
        for time in event_times:
            st.markdown(f"<p style='font-size:30px; margin-bottom: 0px;'>{time}</p>", unsafe_allow_html=True)

# Initial call to update
update()

# Set the app to refresh every second using st.experimental_rerun
while True:
    time.sleep(1)
    st.experimental_rerun()
