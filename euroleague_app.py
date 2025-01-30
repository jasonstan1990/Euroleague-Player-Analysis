import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page settings
st.set_page_config(page_title="Euroleague Player Analysis", layout="wide")

# App Title
st.title("Euroleague: Discover the Undervalued Players")
st.markdown("""
🔍 **Analyze the Statistics and Find the Hidden Superstars!** 🔍

Use advanced statistical analysis and artificial intelligence tools to **identify undervalued players** with **great potential** in the Euroleague.

""")

# Add banner image in the sidebar
st.sidebar.image("dream5.png",  use_container_width=True)

# Load Data
@st.cache_data
def load_data_from_file(filepath):
    data = pd.read_excel(filepath)
    return data

# Sidebar to select dataset
st.sidebar.header("Select Dataset")
selected_dataset = st.sidebar.selectbox(
    "Select the Dataset",
    options=["euroleague_stats.xlsx", "eurocup_stats.xlsx"]
)

# Define the file path based on the selection
if selected_dataset == "euroleague_stats.xlsx":
    file_path = "euroleague_stats.xlsx"
elif selected_dataset == "eurocup_stats.xlsx":
    file_path = "eurocup_stats.xlsx"

# Load the data
try:
    data = load_data_from_file(file_path)
except Exception as e:
    st.error(f"Error loading the file: {e}")
    st.stop()

st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)

# Create expanders to show the Excel data like a glossary
with st.expander("Euroleague Players Statistics (Excel Data)"):
    st.write(data)  # Display the table from the Excel file

# Calculate new statistics with full names
data["Points_per_36_minutes"] = (data["Points"] / data["Minutes_played"]) * 36
data["Assists_per_36_minutes"] = (data["Assists"] / data["Minutes_played"]) * 36
data["Rebounds_per_36_minutes"] = ((data["Offensive_rebounds"] + data["Defensive_rebounds"]) / data["Minutes_played"]) * 36
data["Effective_Field_Goal_Percentage"] = (data["Field_goals_made"] + 0.5 * data["3_point_field_goals_made"]) / data["Field_goals_attempted"]
data["True_Shooting_Percentage"] = data["Points"] / (2 * (data["Field_goals_attempted"] + 0.44 * data["Free_throws_attempted"]))
data["Assist_to_Turnover_Ratio"] = data["Assists"] / data["Turnovers"]
data['Minutes_per_Game'] = data["Minutes_played"] / data["Games_played"]

# Calculate Value-to-Minutes (Value_to_Minutes)
data["Value_to_Minutes"] = (data["Points_per_36_minutes"] + data["Assists_per_36_minutes"] + data["Rebounds_per_36_minutes"]) / data["Minutes_played"]

# Add filters in the Sidebar
st.sidebar.header("Search Filters")
selected_teams = st.sidebar.multiselect("Select Teams", options= list(data["Team"].unique()))
selected_positions = st.sidebar.multiselect("Select Player Positions", options= list(data["Position"].unique()))
selected_players = st.sidebar.multiselect("Select Players", options=list(data["Player"].unique()), default=[])


# Clean data to ensure no NaN or infinite values
data = data.replace([np.inf, -np.inf], np.nan)  # Replace infinities with NaN
data = data.dropna(subset=["Points_per_36_minutes", "Rebounds_per_36_minutes", "Assists_per_36_minutes"])  # Drop rows with NaN in key columns


st.sidebar.header("Advanced Filters")
pts_min = st.sidebar.slider(
    "Minimum Points per 36 Minutes (PTS/36)",
    min_value=float(data["Points_per_36_minutes"].min()),
    max_value=float(data["Points_per_36_minutes"].max()),
    value=float(data["Points_per_36_minutes"].min())
)

reb_min = st.sidebar.slider(
    "Minimum Rebounds per 36 Minutes (REB/36)",
    min_value=float(data["Rebounds_per_36_minutes"].min()),
    max_value=float(data["Rebounds_per_36_minutes"].max()),
    value=float(data["Rebounds_per_36_minutes"].min())
)

ast_min = st.sidebar.slider(
    "Minimum Assists per 36 Minutes (AST/36)",
    min_value=float(data["Assists_per_36_minutes"].min()),
    max_value=float(data["Assists_per_36_minutes"].max()),
    value=float(data["Assists_per_36_minutes"].min())
)

min_playtime = st.sidebar.slider(
    "Select Playtime Range (MIN)",
    min_value=int(data["Minutes_played"].min()),
    max_value=int(data["Minutes_played"].max()),
    value=(int(data["Minutes_played"].min()), int(data["Minutes_played"].max())),
    step=1,
    key="playtime_slider"
)

# Apply filters
filtered_data = data[
    (data["Points_per_36_minutes"] >= pts_min) &
    (data["Rebounds_per_36_minutes"] >= reb_min) &
    (data["Assists_per_36_minutes"] >= ast_min) &
    (data["Minutes_played"] >= min_playtime[0]) &
    (data["Minutes_played"] <= min_playtime[1])
]

if selected_teams:
    filtered_data = filtered_data[filtered_data["Team"].isin(selected_teams)]
if selected_positions:
    filtered_data = filtered_data[filtered_data["Position"].isin(selected_positions)]
if selected_players:
    filtered_data = filtered_data[filtered_data["Player"].isin(selected_players)]

# Display the filtered data
#st.dataframe(filtered_data)




st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)



# Radar Chart
st.subheader("Player Radar Chart")
# Description of methodology and purpose
st.markdown("""
    The **Radar Chart** allows us to compare multiple statistical parameters between 
    different players visually. We use this chart to depict 
    the overall performance of players based on various metrics like points, assists, rebounds, etc.
    This methodology helps us understand which players have a stronger skill set, 
    aiding in the evaluation of undervalued players to build a stronger team.
""")

# If no players are selected, select all players from the filtered data
if len(selected_players) == 0:
    selected_players = filtered_data["Player"].unique()

radar_data = filtered_data[filtered_data["Player"].isin(selected_players)]

# Define categories for the Radar Chart
categories = ['Points_per_36_minutes', 'Rebounds_per_36_minutes', 'Assists_per_36_minutes']

# If there are players to compare
if len(radar_data) >= 1:
    fig = go.Figure()
    for player in radar_data["Player"].unique():
        values = radar_data[radar_data["Player"] == player][categories].values.flatten().tolist()
        values += values[:1]  # Close the loop in the radar chart
        angles = list(np.linspace(0, 2 * np.pi, len(categories), endpoint=False))
        angles += angles[:1]  # Close the loop in the radar chart
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=player
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title="Player Radar Chart",
        height=700,
        width=1000,
        legend=dict(
            x=1,
            y=1,
            traceorder='normal',
            font=dict(size=12),
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='Black',
            borderwidth=1
        )
    )
    st.plotly_chart(fig)
else:
    st.write("There are no players that meet the filtering criteria.")



st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)



st.subheader("Regression Charts")
# Description of methodology and purpose
st.markdown("""
    In this chart, we perform **Regression Analysis** to understand the relationship 
    between different statistics and other parameters. This analysis helps us understand which parameters affect player 
    performance most effectively, allowing us to identify undervalued players.
""")

# Create columns for the Regression Charts
col1, col2 = st.columns(2)

# First Regression Chart
with col1:
    # Select axes for the first chart
    x_axis_1 = st.selectbox(
        "Select Variable for the Horizontal Axis (Chart 1)",
        options=filtered_data.columns,
        index=list(filtered_data.columns).index("Minutes_per_Game")  # Default: "Minutes_per_Game"
    )
    y_axis_1 = st.selectbox(
        "Select Variable for the Vertical Axis (Chart 1)",
        options=filtered_data.columns,
        index=list(filtered_data.columns).index("Points_per_36_minutes")  # Default: "Points_per_36_minutes"
    )
    fig1 = px.scatter(
        filtered_data,
        x=x_axis_1,
        y=y_axis_1,
        hover_name="Player",
        hover_data=["Team", "Position", x_axis_1, y_axis_1],
        trendline="ols",
        title=f"Relationship between {x_axis_1} and {y_axis_1}"
    )
    fig1.update_layout(
        xaxis_title=x_axis_1,
        yaxis_title=y_axis_1,
        template="plotly_white"
    )
    st.plotly_chart(fig1)

# Second Regression Chart
with col2:
    # Select axes for the second chart
    x_axis_2 = st.selectbox(
        "Select Variable for the Horizontal Axis (Chart 2)",
        options=filtered_data.columns,
        index=list(filtered_data.columns).index("Minutes_played"),  # Default: "Minutes_played"
        key="x_axis_2"
    )
    y_axis_2 = st.selectbox(
        "Select Variable for the Vertical Axis (Chart 2)",
        options=filtered_data.columns,
        index=list(filtered_data.columns).index("Points"),  # Default: "Points"
        key="y_axis_2"
    )
    fig2 = px.scatter(
        filtered_data,
        x=x_axis_2,
        y=y_axis_2,
        hover_name="Player",
        hover_data=["Team", "Position", x_axis_2, y_axis_2],
        trendline="ols",
        title=f"Relationship between {x_axis_2} and {y_axis_2}"
    )
    fig2.update_layout(
        xaxis_title=x_axis_2,
        yaxis_title=y_axis_2,
        template="plotly_white"
    )
    st.plotly_chart(fig2)

st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)








import plotly.express as px

# Filter for players with the highest Value-to-Minutes (VTM) ratio
st.subheader("Top 30 Players with High Value-to-Minutes (VTM)")
top_vtm_players = filtered_data[["Player", "Value_to_Minutes", "Points_per_36_minutes", "Assists_per_36_minutes", "Rebounds_per_36_minutes", "Minutes_played"]]
top_vtm_players = top_vtm_players.sort_values(by="Value_to_Minutes", ascending=False)

# Description of methodology and purpose
st.markdown("""
    The **VTM (Value-to-Minutes)** ratio is calculated by dividing the player's statistical performance ("Points_per_36_minutes", "Assists_per_36_minutes", "Rebounds_per_36_minutes") by their total minutes played.
    This metric helps identify players who deliver high performance in limited playing time, making it useful for spotting undervalued talents.

""")

# Display table with expander
with st.expander("See the table of players with the highest VTM ratio", expanded=False):
    st.write("Players with the highest Value-to-Minutes (VTM) ratio:")
    st.dataframe(top_vtm_players.head(30))

# Create Bar Chart for VTM ratio with larger size
fig_vtm = px.bar(
    top_vtm_players.head(30), 
    x="Player", 
    y="Value_to_Minutes", 
    title="Top 30 Players with High Value-to-Minutes (VTM)",
    labels={"Player": "Player", "Value_to_Minutes": "VTM (Value-to-Minutes)"},
    color="Value_to_Minutes",  # Coloring based on the VTM value
    color_continuous_scale="Viridis"  # Choose a color scale
)

# Graph size settings
fig_vtm.update_layout(
    height=400,  # Height of the chart
    width=500,  # Width of the chart
    font=dict(size=14)  # Font size
)

# Display the Bar Chart
st.plotly_chart(fig_vtm, use_container_width=True)


st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)




# Identifying Underrated Players
from plotly.subplots import make_subplots
import plotly.graph_objects as go
st.subheader("Identifying Underrated Players")

# Description of methodology and purpose
st.markdown("""
    In **Identifying Underrated Players**, we focus on players who have high scoring efficiency and strong offensive stats but may be overlooked due to other factors, such as overall play or team role. 
    The selection criteria for these players are:
    - **True Shooting Percentage (TS%) > 0.55**
    - **Points per 36 minutes (PTS/36) > 10**
    - **Assist-to-Turnover Ratio (AST/TOV) > 1.5**

    These metrics help us highlight players who are efficient and effective, despite potentially receiving limited recognition.

""")

# Filter for underrated players based on specific criteria
underrated_players = filtered_data[
    (filtered_data["True_Shooting_Percentage"] > 0.55) & 
    (filtered_data["Points_per_36_minutes"] > 10) & 
    (filtered_data["Assist_to_Turnover_Ratio"] > 1.5)
]

# Create a dropdown with an expander
with st.expander("Players with high efficiency but underrated:"):
    st.dataframe(underrated_players[["Player", "Points_per_36_minutes", "True_Shooting_Percentage", "Assist_to_Turnover_Ratio"]])

# Sort the underrated players by PTS/36 in descending order
underrated_players_sorted = underrated_players.sort_values(by="Points_per_36_minutes", ascending=False)

# Create combined chart (Bar + Line)
fig_underrated_combined = make_subplots(
    rows=1, cols=1, 
    shared_xaxes=True, 
    vertical_spacing=0.1,
    subplot_titles=["Underrated Players with High PTS/36 and Performance"]
)

# Add Bar chart for PTS/36
fig_underrated_combined.add_trace(
    go.Bar(
        x=underrated_players_sorted["Player"], 
        y=underrated_players_sorted["Points_per_36_minutes"],
        name="PTS/36",
        marker=dict(color="blue"),
        yaxis="y1"
    )
)

# Add Line chart for TS%
fig_underrated_combined.add_trace(
    go.Scatter(
        x=underrated_players_sorted["Player"], 
        y=underrated_players_sorted["True_Shooting_Percentage"],
        name="TS%",
        mode="lines+markers",
        line=dict(color="red"),
        yaxis="y2"
    )
)

# Update chart settings
fig_underrated_combined.update_layout(
    title="Underrated Players with High PTS/36 and Performance",
    height=500,
    width=800,
    xaxis_title="Player",
    yaxis_title="PTS/36",
    yaxis2=dict(
        title="TS%",
        overlaying="y",
        side="right"
    ),
    template="plotly_white"
)

# Display the chart
st.plotly_chart(fig_underrated_combined, use_container_width=True)






st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)




import plotly.express as px
import pandas as pd
import streamlit as st

st.markdown("""
### Team Needs Index (Deviation from the Average)

This tool calculates the **difference** of teams from the average for three key statistics: **Rebounds (REB/36)**, **Assists (AST/36)**, and **Points (PTS/36)**, using player data per team. The results are presented in an **interactive chart** that shows the difference for each team compared to the average for each statistic.
This tool is useful for analysts and coaches who want to understand each team's weaknesses or needs and identify which areas require reinforcement.
""")

# Assuming filtered_data is already created correctly
filtered_data = filtered_data.copy()  # To avoid potential conflicts

# Create a table with the team's statistics
team_stats = filtered_data.groupby("Team")[["Points", "Rebounds", "Assists"]].mean()

# Calculate deviations from the average
avg_points = team_stats["Points"].mean()
avg_rebounds = team_stats["Rebounds"].mean()
avg_assists = team_stats["Assists"].mean()

# Calculate the differences
team_stats["Points_diff"] = avg_points - team_stats["Points"]
team_stats["Rebounds_diff"] = avg_rebounds - team_stats["Rebounds"]
team_stats["Assists_diff"] = avg_assists - team_stats["Assists"]

# Create dropdown for selecting the statistic
stat_choice = st.selectbox(
    "Select Statistic:",
    ("Points_diff", "Rebounds_diff", "Assists_diff"),
    index=0  # Default selection
)

# Convert the table to long format for use with Plotly
team_needs_long = team_stats[["Points_diff", "Rebounds_diff", "Assists_diff"]].reset_index()
team_needs_long = pd.melt(team_needs_long, id_vars=["Team"], value_vars=["Points_diff", "Rebounds_diff", "Assists_diff"], 
                          var_name="Statistic", value_name="Difference")

# Filter based on the selected variable
filtered_chart_data = team_needs_long[team_needs_long["Statistic"] == stat_choice]

# Calculate the standard deviation for the difference
std_diff = filtered_chart_data["Difference"].std()

# Calculate the average difference
mean_diff = filtered_chart_data["Difference"].mean()

# Display the standard deviation and the average
#st.write(f"Average Difference: {mean_diff:.2f}")
st.write(f"Standard Deviation: {std_diff:.2f}")
st.markdown(""" If the difference from the average is less than 1 standard deviation, it is considered normal. If it is greater, the difference exceeds 68% of cases and indicates a significant need for improvement in that area. """)


# Create the bar chart
fig = px.bar(filtered_chart_data, 
             x="Difference",  # Set "Difference" on the x-axis for horizontal bars
             y="Team",  # Set the team on the y-axis
             color="Statistic", 
             title=f"Team Needs Index (Deviation from the Average): {stat_choice}",
             labels={"Difference": "Difference from Average", "Team": "Team"},
             hover_data={"Team": True, "Statistic": True, "Difference": True},
             orientation="h")  # Horizontal bars

# Add a line for the average
fig.add_vline(
    x=mean_diff,
    line=dict(color="blue", dash="dash"),
    annotation_text="Average",
    annotation_position="top left"
)

# Add lines for 1 standard deviation above/below the average
fig.add_vline(
    x=mean_diff + std_diff,
    line=dict(color="green", dash="dash"),
    annotation_text="Average +1 Std Dev",
    annotation_position="top left"
)

fig.add_vline(
    x=mean_diff - std_diff,
    line=dict(color="green", dash="dash"),
    annotation_text="Average -1 Std Dev",
    annotation_position="top left"
)

# Update chart with larger size
fig.update_layout(
    height=500,  # Increases the height of the chart
    width=800,  # Increases the width of the chart
)

# Display the interactive chart in Streamlit
st.plotly_chart(fig)





st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)




import pulp
import numpy as np
import plotly.express as px

st.markdown("""
### Basketball Team Selection Optimization

This tool optimize a basketball team's roster with the goal of maximizing performance in the statistics the user selects. The process includes:

1. **Player Filtering**: Selection of players from each position (Forwards, Guards, Centers) and defining the statistics to optimize (e.g., points, assists, rebounds).
2. **Constraints**: Setting constraints for position distribution, total playing time (limit of 250 minutes for all players), and team composition.
3. **Team Optimization**: Analyzing the data and selecting the best players to maximize the team’s overall performance while ensuring that each player has sufficient playing time.
4. **Results**: Displaying the selected players with a table and a chart that shows their statistics.

This tool offers a mathematical approach for **effective team composition**, ensuring that all players have adequate playing time, and the total playing time does not exceed 250 minutes. It is ideal for coaches, analysts, and sports professionals who want to make more strategic and data-driven player selections.
""")

# Filters for positions above the table
st.markdown("Select Players by Position and Optimization Statistic")
fwd_count = st.slider("How many Forwards (F) do you want?", min_value=0, max_value=5, value=4)
g_count = st.slider("How many Guards (G) do you want?", min_value=0, max_value=5, value=5)
c_count = st.slider("How many Centers (C) do you want?", min_value=0, max_value=5, value=3)

# Select the statistics to be optimized for each position
fwd_stats = st.multiselect("Statistics to Optimize (Forwards)", 
                           ['Points_per_36_minutes', 'Assists_per_36_minutes', 'Rebounds_per_36_minutes'], 
                           default=['Points_per_36_minutes'])
g_stats = st.multiselect("Statistics to Optimize (Guards)", 
                         ['Points_per_36_minutes', 'Assists_per_36_minutes', 'Rebounds_per_36_minutes'], 
                         default=['Points_per_36_minutes'])
c_stats = st.multiselect("Statistics to Optimize (Centers)", 
                         ['Points_per_36_minutes', 'Assists_per_36_minutes', 'Rebounds_per_36_minutes'], 
                         default=['Points_per_36_minutes'])

# Creating dictionaries for position constraints
pos_constraints = {
    'F': fwd_count,
    'G': g_count,
    'C': c_count
}

# Creating dictionaries for the statistics to be optimized by position
pos_stats = {
    'F': fwd_stats,
    'G': g_stats,
    'C': c_stats
}

# Filtering NaN/inf values in relevant fields
filtered_data_clean = filtered_data[
    filtered_data['Points_per_36_minutes'].notna() & 
    filtered_data['Points_per_36_minutes'].apply(np.isfinite) & 
    filtered_data['Minutes_per_Game'].notna() & 
    filtered_data['Minutes_per_Game'].apply(np.isfinite)
]

# Filter for mandatory players to be included in the roster
mandatory_players = st.multiselect(
    "Select players who must be included in the roster:",
    options=filtered_data_clean["Player"].unique(),
    default=[],
    help="The selected players will be included in the roster."
)

# Filter for players to be excluded from the roster
excluded_players = st.multiselect(
    "Select players who will not be included in the roster:",
    options=[player for player in filtered_data_clean["Player"].unique() if player not in mandatory_players],
    default=[],
    help="The selected players will be excluded from the roster."
)

# Create the optimization problem
prob = pulp.LpProblem("Optimized_Team_Selection", pulp.LpMaximize)

# Create variables for player selection
players = filtered_data_clean["Player"].unique().tolist()
player_vars = pulp.LpVariable.dicts("Player", players, cat='Binary')

# Objective function: Maximize selected statistic per position
prob += pulp.lpSum([
    filtered_data_clean.loc[filtered_data_clean["Player"] == player, stat].values[0] * player_vars[player]
    for player in players for stat in pos_stats[filtered_data_clean.loc[filtered_data_clean["Player"] == player, 'Position'].values[0]]
])

# Constraint for total playing time (min/gp ≤ 250)
prob += pulp.lpSum([
    filtered_data_clean.loc[filtered_data_clean["Player"] == player, 'Minutes_per_Game'].values[0] * player_vars[player]
    for player in players
]) <= 250

# Constraint to select exactly 12 players
prob += pulp.lpSum([player_vars[player] for player in players]) == 12

# Position constraints
for pos, count in pos_constraints.items():
    prob += pulp.lpSum([
        player_vars[player]
        for player in players if filtered_data_clean.loc[filtered_data_clean["Player"] == player, 'Position'].values[0] == pos
    ]) == count

# Constraints for mandatory players in the roster
for player in mandatory_players:
    prob += player_vars[player] == 1

# Constraints for excluded players from the roster
for player in excluded_players:
    prob += player_vars[player] == 0

# Solve the problem
prob.solve()

# Retrieve selected players
selected_players = [player for player in players if player_vars[player].varValue == 1]

# Display the selected players
df_selected = filtered_data_clean[filtered_data_clean["Player"].isin(selected_players)]

# Show the selected players' data in a table
with st.expander("Selected Players for the Team"):
    st.write(df_selected)

# Create a bar chart with the selected players' statistics
fig = px.bar(
    df_selected,
    x="Points_per_36_minutes",  # You can change this to any statistic you like (e.g., 'Rebounds_per_36_minutes')
    y="Player",  # Player on the y-axis
    title="Selected Players and Their Statistics",
    labels={"Player": "Player", "Points_per_36_minutes": "Points per 36 Minutes"},
    color="Position",  # Color by position
    color_continuous_scale="Viridis",
    orientation="h"  # Defines the chart with horizontal bars
)

# Update chart with larger size
fig.update_layout(
    height=500,  # Increase height of the chart
    width=800,  # Increase width of the chart
)

# Display the chart
st.plotly_chart(fig)







st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)



import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

# New list of statistics for selection
all_stats_columns = [
    "Points_per_36_minutes", 
    "Assists_per_36_minutes", 
    "Rebounds_per_36_minutes"
]

# Streamlit app structure
st.subheader("Prediction of Similar Players Based on Statistics")
st.markdown("""
Discover the most similar players based on their statistics.
We use advanced machine learning algorithms 
to find the most accurate matches in real-time. 
""")

# Selecting statistics by the user
selected_stats = st.multiselect("Select Statistics:", all_stats_columns, default=["Points_per_36_minutes", "Rebounds_per_36_minutes", "Assists_per_36_minutes"])

# Checking if any statistics were selected
if not selected_stats:
    st.warning("Please select at least one statistic to proceed.")
else:
    # Normalizing the data for the selected statistics
    scaler = StandardScaler()
    data_normalized = scaler.fit_transform(filtered_data[selected_stats])

    # Creating a k-NN model
    model = NearestNeighbors(n_neighbors=6, metric='euclidean')  # More neighbors to ensure the selected player is excluded
    model.fit(data_normalized)

    # Selecting a player from the user
    player_name = st.selectbox("Select Player:", filtered_data["Player"])

    # Finding the corresponding player in the data
    player_index = filtered_data[filtered_data["Player"] == player_name].index[0]

    # Finding the most similar players
    distances, indices = model.kneighbors([data_normalized[player_index]])

    # Collecting the data for the chart and excluding the selected player from the results
    similar_players = []
    for idx in indices[0]:
        if filtered_data.iloc[idx]["Player"] != player_name:  # Excluding the selected player
            similar_player = filtered_data.iloc[idx]
            similar_players.append((similar_player['Player'], distances[0][indices[0] == idx][0]))

    # Creating the interactive chart with Plotly
    player_names = [player[0] for player in similar_players]
    distances_values = [player[1] for player in similar_players]

    # Creating the interactive chart with Plotly
    fig = px.bar(
        x=distances_values,
        y=player_names,
        orientation='h',
        labels={'x': 'Statistical Distance', 'y': 'Players'},
        title='Most Similar Players Based on Selected Statistics',
        color=distances_values,
        color_continuous_scale='Viridis'
    )

    # Adjusting the size of the chart
    fig.update_layout(
        width=600,  # Width size
        height=400,  # Height size
    )

    # Displaying the interactive chart
    st.plotly_chart(fig)

