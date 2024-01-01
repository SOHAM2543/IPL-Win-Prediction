import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt

teams = ['Sunrisers Hyderabad',
 'Mumbai Indians',
 'Royal Challengers Bangalore',
 'Kolkata Knight Riders',
 'Kings XI Punjab',
 'Chennai Super Kings',
 'Rajasthan Royals',
 'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi',
       'Chandigarh', 'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth',
       'Durban', 'Centurion', 'East London', 'Johannesburg', 'Kimberley',
       'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
       'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi',
       'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl','rb'))
st.title('IPL Win Predictor')

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select the batting team',sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team',sorted(teams))
# Check if both selected teams are the same
teams_are_same = batting_team == bowling_team

# Disable the button if teams are the same
button_disabled = teams_are_same

 # Check if both selected teams are the same
if batting_team == bowling_team:
    st.warning("Please select different teams for batting and bowling.")
else:
    st.success("You can proceed with the selected teams.")

selected_city = st.selectbox('Select host city',sorted(cities))

target = st.number_input('Target', step=1)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score', step=1)
with col4:
    overs = st.number_input('Overs completed')

with col5:
    wickets = st.number_input('Wickets out', step=1, max_value=10)

if st.button('Predict Probability' , disabled=button_disabled):
    st.write("Prediction in progress...")
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city],'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")

df = pd.DataFrame({
    'overs': [overs],
    'target': [target],
    'score': [score],
})


# Create a line chart
fig, ax = plt.subplots()
ax.plot(df['overs'], df['target'], label='Target Score', color='red', linestyle='-')
ax.plot(df['overs'], df['score'], label='Current Score', color='green', linestyle='-')

ax.set_xlabel('Overs')
ax.set_ylabel('Score')


# Display the chart in Streamlit
st.pyplot(fig)
