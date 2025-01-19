import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


# Ρυθμίσεις σελίδας
st.set_page_config(page_title="Euroleague Player Analysis", use_container_width=True)

# Τίτλος Εφαρμογής
st.title("Euroleague: Ανακάλυψε τους Υποτιμημένους Παίκτες")
st.markdown("""
🔍 **Αναλύστε τα Στατιστικά και Βρείτε τους Κρυφούς Superstars!** 🔍

Χρησιμοποιήστε προηγμένα εργαλεία στατιστικής ανάλυσης και τεχνητή νοημοσύνη για να **εντοπίσετε υποτιμημένους παίκτες** με **μεγάλες δυνατότητες** στην Euroleague.

""")






# Προσθήκη banner εικόνας στο sidebar
st.sidebar.image("dream5.png", use_column_width=True)

# Λήψη Δεδομένων
#st.sidebar.header("Λήψη Δεδομένων")
#st.sidebar.markdown("Κατεβάστε το αρχείο Excel με τα στατιστικά δεδομένα.")
@st.cache_data
def load_data(filepath):
    data = pd.read_excel(filepath)
    return data

# Φόρτωση του αρχείου Excel
file_path = "euroleague_stats.xlsx"  # Προσαρμόστε το path στο αρχείο σας
try:
    data = load_data(file_path)
except FileNotFoundError:
    st.error("Το αρχείο στατιστικών δεν βρέθηκε. Βεβαιωθείτε ότι υπάρχει στο σωστό path.")
    st.stop()

st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)


# Δημιουργία expanders για να εμφανίσεις το Excel σαν το glossary
with st.expander("Στατιστικά Παίκτες Euroleague (Excel Data)"):
    st.write(data)  # Εμφάνιση του πίνακα από το αρχείο Excel


# Πρόσθεση Glossary με δυνατότητα dropdown
with st.expander("Αναλυτικός Οδηγός (Glossary)"):
    glossary = """
    - **MIN**: Minutes played
    - **ST**: Starter
    - **GP**: Games played
    - **PTS**: Points
    - **AST**: Assists
    - **STL**: Steals
    - **BLK**: Blocks
    - **BA**: Blocks against
    - **FGM**: Field goals made
    - **FGA**: Field goals attempted
    - **FG%**: Field goals percentage
    - **3PM**: 3 point field goals made
    - **3PA**: 3 point field goals attempted
    - **3P%**: 3 point field goals percentage
    - **FTM**: Free throws made
    - **FTA**: Free throws attempted
    - **FT%**: Free throws percentage
    - **OREB**: Offensive rebounds
    - **DREB**: Defensive rebounds
    - **TOV**: Turnovers
    - **PF**: Personal fouls
    - **FD**: Fouls received
    - **+/-**: Plus Minus
    """
    st.text(glossary)

# Προσθήκη πληροφοριών για προηγμένες μετρικές σε μορφή dropdown
with st.expander("Περισσότερα για τις Προηγμένες Μετρικές"):
    advanced_metrics_info = """
    **1. eFG% (Effective Field Goal Percentage - Αποτελεσματικότητα Σκοραρίσματος)**:
    Η eFG% είναι μια βελτιωμένη μέθοδος για να αξιολογείται η αποτελεσματικότητα ενός παίκτη στο σκοράρισμα, η οποία λαμβάνει υπόψη και τα τρίποντα, καθώς αυτά αξίζουν περισσότερους πόντους από τα κανονικά σουτ.
    Υπολογίζεται ως εξής:

    𝑒𝐹𝐺% = (𝐹𝐺𝑀 + 0.5 × 3𝑃𝑀) / 𝐹𝐺𝐴

    **Παράδειγμα**:
    Αν ο παίκτης έχει 100 εύστοχα σουτ (FGM), 50 τρίποντα (3PM) και 200 προσπάθειες (FGA), η eFG% υπολογίζεται ως εξής:
    𝑒𝐹𝐺% = (100 + 0.5 × 50) / 200 = 0.625 (62.5%)

    **2. TS% (True Shooting Percentage - Πραγματική Ποσοστιαία Απόδοση Σκοραρίσματος)**:
    Η TS% είναι ένας πιο ακριβής τρόπος για να μετρήσουμε την αποτελεσματικότητα ενός παίκτη στο σκοράρισμα, καθώς λαμβάνει υπόψη όλες τις πηγές σκοραρίσματος: σουτ από το πεδίο (2 πόντοι και 3 πόντοι) και ελεύθερες βολές.

    𝑇𝑆% = 𝑃𝑇𝑆 / (2 × (𝐹𝐺𝐴 + 0.44 × 𝐹𝑇𝐴))

    **Παράδειγμα**:
    Αν ο παίκτης έχει 500 πόντους (PTS), 400 προσπάθειες για σουτ (FGA) και 100 ελεύθερες βολές (FTA), η TS% υπολογίζεται ως εξής:
    𝑇𝑆% = 500 / (2 × (400 + 0.44 × 100)) = 0.563 (56.3%)

    **3. AST/TOV (Assist to Turnover Ratio - Αναλογία Ασίστ προς Λάθη)**:
    Η AST/TOV είναι μια μέτρηση που μας δείχνει πόσο καλά ο παίκτης διαχειρίζεται την μπάλα σε σχέση με τα λάθη του. Αν ο παίκτης κάνει πολλές ασίστ χωρίς να κάνει πολλά λάθη, η αναλογία αυτή είναι υψηλή και δείχνει καλές επιδόσεις στο παιχνίδι.

    𝐴𝑆𝑇/𝑇𝑂𝑉 = 𝐴𝑆𝑇 / 𝑇𝑂𝑉

    **Παράδειγμα**:
    Αν ο παίκτης έχει 100 ασίστ και 20 λάθη, η αναλογία του θα είναι:
    AST/TOV = 100 / 20 = 5
    Αυτό σημαίνει ότι για κάθε λάθος, ο παίκτης δημιουργεί 5 ασίστ.
    """
    st.text(advanced_metrics_info)


# Υπολογισμός νέων στατιστικών
data["PTS/36"] = (data["PTS"] / data["MIN"]) * 36
data["AST/36"] = (data["AST"] / data["MIN"]) * 36
data["REB/36"] = ((data["OREB"] + data["DREB"]) / data["MIN"]) * 36
data["eFG%"] = (data["FGM"] + 0.5 * data["3PM"]) / data["FGA"]
data["TS%"] = data["PTS"] / (2 * (data["FGA"] + 0.44 * data["FTA"]))
data["AST/TOV"] = data["AST"] / data["TOV"]
data['MIN/GP'] = data["MIN"] / data["GP"]

# Υπολογισμός Value-to-Minutes (VTM)
data["VTM"] = (data["PTS/36"] + data["AST/36"] + data["REB/36"]) / data["MIN"]

# Προσθήκη Φίλτρων στη Sidebar
st.sidebar.header("Φίλτρα Αναζήτησης")
selected_team = st.sidebar.selectbox("Επιλέξτε Ομάδα", options=["Όλες"] + list(data["Team"].unique()))
selected_pos = st.sidebar.selectbox("Επιλέξτε Θέση Παίκτη", options=["Όλες"] + list(data["Pos"].unique()))
selected_players = st.sidebar.multiselect("Επιλέξτε Παίκτες", options=list(data["Player"].unique()), default=[])

st.sidebar.header("Προηγμένα Φίλτρα")
pts_min = st.sidebar.slider(
    "Ελάχιστοι Πόντοι ανά 36 λεπτά (PTS/36)",
    min_value=float(data["PTS/36"].min()),
    max_value=float(data["PTS/36"].max()),
    value=float(data["PTS/36"].min())
)

reb_min = st.sidebar.slider(
    "Ελάχιστοι Ρεμπάουντ ανά 36 λεπτά (REB/36)",
    min_value=float(data["REB/36"].min()),
    max_value=float(data["REB/36"].max()),
    value=float(data["REB/36"].min())
)

ast_min = st.sidebar.slider(
    "Ελάχιστες Ασίστ ανά 36 λεπτά (AST/36)",
    min_value=float(data["AST/36"].min()),
    max_value=float(data["AST/36"].max()),
    value=float(data["AST/36"].min())
)

min_playtime = st.sidebar.slider(
    "Επιλέξτε Εύρος Χρόνου Συμμετοχής (MIN)",
    min_value=int(data["MIN"].min()),
    max_value=int(data["MIN"].max()),
    value=(int(data["MIN"].min()), int(data["MIN"].max())),
    step=1,
    key="playtime_slider"
)

# Εφαρμογή φίλτρων
filtered_data = data[
    (data["PTS/36"] >= pts_min) &
    (data["REB/36"] >= reb_min) &
    (data["AST/36"] >= ast_min) &
    (data["MIN"] >= min_playtime[0]) &
    (data["MIN"] <= min_playtime[1])
]

if selected_team != "Όλες":
    filtered_data = filtered_data[filtered_data["Team"] == selected_team]
if selected_pos != "Όλες":
    filtered_data = filtered_data[filtered_data["Pos"] == selected_pos]
if selected_players:
    filtered_data = filtered_data[filtered_data["Player"].isin(selected_players)]

st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)

# Radar Chart
st.subheader("Radar Chart Παίκτη")
#Περιγραφή μεθοδολογίας και στόχου
st.markdown("""
    Το **Radar Chart** μας επιτρέπει να συγκρίνουμε πολλές στατιστικές παράμετρους μεταξύ 
    διαφορετικών παικτών με οπτικό τρόπο. Χρησιμοποιούμε το γράφημα αυτό για να απεικονίσουμε 
    τη συνολική απόδοση παικτών με βάση διάφορους δείκτες όπως οι πόντοι, οι ασίστ, οι ριμπάουντ κ.ά.
    Η μεθοδολογία αυτή μας επιτρέπει να κατανοήσουμε ποιοι παίκτες έχουν πιο ισχυρό σύνολο δεξιοτήτων, 
    βοηθώντας στην αξιολόγηση υποτιμημένων παικτών για τη δημιουργία μιας ισχυρότερης ομάδας.
""")
selected_players = st.multiselect("Επιλέξτε Παίκτες για Σύγκριση", options=filtered_data["Player"].unique())

# Αν δεν επιλεγούν παίκτες, επιλέγονται όλοι οι παίκτες από τα φιλτραρισμένα δεδομένα
if len(selected_players) == 0:
    selected_players = filtered_data["Player"].unique()

radar_data = filtered_data[filtered_data["Player"].isin(selected_players)]
categories = ['PTS/36', 'REB/36', 'AST/36']

if len(radar_data) >= 1:
    fig = go.Figure()
    for player in radar_data["Player"].unique():
        values = radar_data[radar_data["Player"] == player][categories].values.flatten().tolist()
        values += values[:1]
        angles = list(np.linspace(0, 2 * np.pi, len(categories), endpoint=False))
        angles += angles[:1]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=player
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True,
        title="Radar Chart Παίκτη",
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
    st.write("Δεν υπάρχουν παίκτες που να πληρούν τα κριτήρια φιλτραρίσματος.")







st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)

st.subheader("Regression Charts")
# Περιγραφή μεθοδολογίας και στόχου
st.markdown("""
    Σε αυτό το γράφημα, πραγματοποιούμε **Regression Analysis** για να κατανοήσουμε τη σχέση 
    μεταξύ διαφορετικών στατιστικών (όπως PTS/36, AST/36, REB/36) και άλλων παραμέτρων 
    (όπως MIN, VTM). Η ανάλυση αυτή μας βοηθά να κατανοήσουμε ποιες παράμετροι επηρεάζουν την 
    απόδοση των παικτών με πιο αποτελεσματικό τρόπο, προκειμένου να εντοπίσουμε υποτιμημένους παίκτες.
""")


# Δημιουργία στήλης για τα Regression Charts
col1, col2 = st.columns(2)

# Πρώτο Regression Chart
with col1:
    #st.markdown("Regression Chart 1")
    x_axis_1 = st.selectbox(
        "Επιλέξτε Μεταβλητή για τον Οριζόντιο Άξονα (Chart 1)",
        options=filtered_data.columns,
        index=list(filtered_data.columns).index("MIN")  # Default: "MIN"
    )
    y_axis_1 = st.selectbox(
        "Επιλέξτε Μεταβλητή για τον Κάθετο Άξονα (Chart 1)",
        options=filtered_data.columns,
        index=list(filtered_data.columns).index("PTS/36")  # Default: "PTS/36"
    )
    fig1 = px.scatter(
        filtered_data,
        x=x_axis_1,
        y=y_axis_1,
        hover_name="Player",
        hover_data=["Team", "Pos", x_axis_1, y_axis_1],
        trendline="ols",
        title=f"Σχέση μεταξύ {x_axis_1} και {y_axis_1}"
    )
    fig1.update_layout(
        xaxis_title=x_axis_1,
        yaxis_title=y_axis_1,
        template="plotly_white"
    )
    st.plotly_chart(fig1)

# Δεύτερο Regression Chart
with col2:
    #st.markdown("Regression Chart 2")
    x_axis_2 = st.selectbox(
        "Επιλέξτε Μεταβλητή για τον Οριζόντιο Άξονα (Chart 2)",
        options=filtered_data.columns,
        index=list(filtered_data.columns).index("MIN"),  # Default: "MIN"
        key="x_axis_2"
    )
    y_axis_2 = st.selectbox(
        "Επιλέξτε Μεταβλητή για τον Κάθετο Άξονα (Chart 2)",
        options=filtered_data.columns,
        index=list(filtered_data.columns).index("PTS"),  # Default: "PTS"
        key="y_axis_2"
    )
    fig2 = px.scatter(
        filtered_data,
        x=x_axis_2,
        y=y_axis_2,
        hover_name="Player",
        hover_data=["Team", "Pos", x_axis_2, y_axis_2],
        trendline="ols",
        title=f"Σχέση μεταξύ {x_axis_2} και {y_axis_2}"
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

# Φίλτρο για τους παίκτες με τον υψηλότερο δείκτη VTM
st.subheader("Top 30 Παίκτες με Υψηλό Value-to-Minutes (VTM)")
top_vtm_players = filtered_data[["Player", "VTM", "PTS/36", "AST/36", "REB/36", "MIN"]]
top_vtm_players = top_vtm_players.sort_values(by="VTM", ascending=False)

# Περιγραφή μεθοδολογίας και στόχου
st.markdown("""
    Εδώ παρουσιάζονται οι 30 κορυφαίοι παίκτες με βάση τον δείκτη **VTM (Value-to-Minutes)**, 
    που υπολογίζεται ως ο λόγος της αξίας ενός παίκτη σε στατιστικά (PTS/36, AST/36, REB/36 κ.α.) προς τον χρόνο 
    παιχνιδιού που παίρνει. Ο στόχος είναι η εύρεση παικτών που είναι αποδοτικοί και αποτελεσματικοί σε περιορισμένο χρόνο.
""")

# Παρουσίαση πίνακα με expander
with st.expander("Δείτε τον πίνακα με τους παίκτες με τον υψηλότερο δείκτη VTM", expanded=False):
    st.write("Παίκτες με τον υψηλότερο δείκτη Value-to-Minutes (VTM):")
    st.dataframe(top_vtm_players.head(30))

# Δημιουργία Bar Chart για τον δείκτη VTM με μεγαλύτερο μέγεθος
fig_vtm = px.bar(
    top_vtm_players.head(30), 
    x="Player", 
    y="VTM", 
    title="Top 30 Παίκτες με Υψηλό Value-to-Minutes (VTM)",
    labels={"Player": "Παίκτης", "VTM": "VTM (Value-to-Minutes)"},
    color="VTM",  # Χρωματισμός με βάση την τιμή του VTM
    color_continuous_scale="Viridis"  # Επιλογή χρωματικής κλίμακας
)

# Ρυθμίσεις μεγέθους του γραφήματος
fig_vtm.update_layout(
    height=400,  # Ύψος του γραφήματος
    width=500,  # Πλάτος του γραφήματος
    font=dict(size=14)  # Μέγεθος γραμματοσειράς
)

# Εμφάνιση του Bar Chart
st.plotly_chart(fig_vtm, use_container_width=True)



st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)


# Εντοπισμός Υποτιμημένων Παίκτων
from plotly.subplots import make_subplots
import plotly.graph_objects as go
st.subheader("Εντοπισμός Υποτιμημένων Παίκτων")

# Περιγραφή μεθοδολογίας και στόχου
st.markdown("""
    Στον **Εντοπισμό Υποτιμημένων Παίκτων** εστιάζουμε σε παίκτες με υψηλή αποτελεσματικότητα στο σκοράρισμα 
    και καλές επιδόσεις στην επίθεση, αλλά που ενδέχεται να υποτιμώνται λόγω άλλων παραμέτρων, όπως το συνολικό 
    παιχνίδι ή ο ρόλος τους στην ομάδα. 
    Χρησιμοποιούμε τα **PTS/36** (πόντοι ανά 36 λεπτά), **TS%** (True Shooting Percentage) και την **AST/TOV** (αναλογία 
    ασίστ προς λάθη) για να εντοπίσουμε παίκτες που έχουν μεγάλες δυνατότητες, αλλά συχνά περνούν απαρατήρητοι.
    Η μεθοδολογία αυτή μας βοηθά να αναγνωρίσουμε παίκτες που μπορούν να προσφέρουν μεγαλύτερη αξία για την ομάδα 
    με βάση την αποδοτικότητα τους και την αποτελεσματικότητα τους, παρά την περιορισμένη αναγνώριση που έχουν.
""")


underrated_players = filtered_data[
    (filtered_data["TS%"] > 0.55) & 
    (filtered_data["PTS/36"] > 10) & 
    (filtered_data["AST/TOV"] > 1.5)
]

# Δημιουργία του dropdown με τον expander
with st.expander("Παίκτες με υψηλή αποτελεσματικότητα αλλά υποτιμημένοι:"):
    st.dataframe(underrated_players[["Player", "PTS/36", "TS%", "AST/TOV"]])

# Ταξινόμηση των υποτιμημένων παικτών κατά PTS/36 σε φθίνουσα σειρά
underrated_players_sorted = underrated_players.sort_values(by="PTS/36", ascending=False)

# Δημιουργία συνδυασμένου γραφήματος (Bar + Line)
fig_underrated_combined = make_subplots(
    rows=1, cols=1, 
    shared_xaxes=True, 
    vertical_spacing=0.1,
    subplot_titles=["Υποτιμημένοι Παίκτες με Υψηλό PTS/36 και TS%"],
    specs=[[{"secondary_y": True}]]  # Δημιουργία δευτερεύουσας Y-άξονας
)

# Δημιουργία Bar Chart για PTS/36
fig_underrated_combined.add_trace(
    go.Bar(
        x=underrated_players_sorted["Player"], 
        y=underrated_players_sorted["PTS/36"],
        name="PTS/36",
        marker_color='blue'
    ),
    secondary_y=False  # Προσθήκη στο βασικό Y-άξονα
)

# Δημιουργία Line Chart για TS%
fig_underrated_combined.add_trace(
    go.Scatter(
        x=underrated_players_sorted["Player"], 
        y=underrated_players_sorted["TS%"],
        mode="lines+markers",
        name="TS%",
        line=dict(color='red')
    ),
    secondary_y=True  # Προσθήκη στο δευτερεύον Y-άξονα
)

# Ρυθμίσεις του γραφήματος
fig_underrated_combined.update_layout(
    title="Υποτιμημένοι Παίκτες με Υψηλό PTS/36 και TS%",
    xaxis_title="Παίκτης",
    yaxis_title="PTS/36 (Πόντοι ανά 36 λεπτά)",
    yaxis2_title="TS% (True Shooting Percentage)",
    height=400,
    width=500,
    font=dict(size=14),
    showlegend=True
)

# Εμφάνιση του συνδυασμένου γραφήματος
st.plotly_chart(fig_underrated_combined, use_container_width=True)




st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)


import plotly.express as px
import pandas as pd

st.markdown("""
### Δείκτης Ανάγκης Ομάδας (Αντίθεση με τον Μέσο Όρο)

Αυτό το εργαλείο υπολογίζει τη **διαφορά** των ομάδων από τον μέσο όρο για τρία σημαντικά στατιστικά: **Rebounds (REB/36)**, **Assists (AST/36)** και **Points (PTS/36)**, χρησιμοποιώντας τα δεδομένα των παικτών ανά ομάδα. Τα αποτελέσματα αναπαρίστανται σε ένα **διαδραστικό γράφημα** που δείχνει τη διαφορά για κάθε ομάδα σε σχέση με τον μέσο όρο για κάθε στατιστικό.
Αυτό το εργαλείο είναι χρήσιμο για αναλυτές και προπονητές που επιθυμούν να κατανοήσουν τις αδυναμίες ή τις ανάγκες κάθε ομάδας και να εντοπίσουν ποιοι τομείς χρειάζονται ενίσχυση.
""")

# Δημιουργία πίνακα με τα δεδομένα των ομάδων
team_stats = filtered_data.groupby("Team")[["REB/36", "AST/36", "PTS/36", "MIN"]].mean()

# Υπολογισμός των διακυμάνσεων από τον μέσο όρο
avg_reb = team_stats["REB/36"].mean()
avg_ast = team_stats["AST/36"].mean()
avg_pts = team_stats["PTS/36"].mean()

# Υπολογισμός των διαφορών
team_stats["REB_diff"] = avg_reb - team_stats["REB/36"]
team_stats["AST_diff"] = avg_ast - team_stats["AST/36"]
team_stats["PTS_diff"] = avg_pts - team_stats["PTS/36"]

# Μετατροπή του πίνακα σε long format για να χρησιμοποιηθεί με Plotly
team_needs_long = team_stats[["REB_diff", "AST_diff", "PTS_diff"]].reset_index()
team_needs_long = pd.melt(team_needs_long, id_vars=["Team"], value_vars=["REB_diff", "AST_diff", "PTS_diff"], 
                          var_name="Statistic", value_name="Difference")

# Δημιουργία διαδραστικού bar chart με Plotly
fig = px.bar(team_needs_long, 
             x="Difference",  # Ορίζουμε το "Difference" στον άξονα x για να έχουμε τις μπάρες οριζόντια
             y="Team",  # Η ομάδα στον άξονα y
             color="Statistic", 
             title="Δείκτης Ανάγκης Ομάδας (Αντίθεση με τον Μέσο Όρο)", 
             labels={"Difference": "Διαφορά από τον Μέσο Όρο", "Team": "Ομάδα"},
             hover_data={"Team": True, "Statistic": True, "Difference": True},
             orientation="h")  # Οριζόντιες μπάρες

# Ενημέρωση διαγράμματος με μεγαλύτερο μέγεθος
fig.update_layout(
    height=500,  # Αυξάνει το ύψος του διαγράμματος
    width=800,  # Αυξάνει το πλάτος του διαγράμματος
)

# Εμφάνιση του διαδραστικού γραφήματος στο Streamlit
st.plotly_chart(fig)





st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)

import pulp
import numpy as np


st.markdown("""
### Βελτιστοποίηση Επιλογής Παίκτων για Ομάδα

Αυτό το εργαλείο χρησιμοποιεί τη βιβλιοθήκη **pulp** για τη βελτιστοποίηση της σύνθεσης μιας ομάδας μπάσκετ, με στόχο τη μέγιστη απόδοση στα στατιστικά που επιθυμεί ο χρήστης. Η διαδικασία περιλαμβάνει:

1. **Φιλτράρισμα Παίκτων**: Επιλογή παικτών από κάθε θέση (Forwards, Guards, Centers) και καθορισμός στατιστικών για βελτιστοποίηση (π.χ. πόντους, ασίστ, rebounds).
2. **Περιορισμοί**: Ρύθμιση περιορισμών για την κατανομή θέσεων, τον συνολικό χρόνο παιχνιδιού (όριο 250 λεπτά για όλους τους παίκτες), και τη σύνθεση της δωδεκάδας.
3. **Βελτιστοποίηση Ομάδας**: Ανάλυση δεδομένων και επιλογή των καλύτερων παικτών για να μεγιστοποιηθεί η συνολική απόδοση της ομάδας, ενώ παράλληλα εξασφαλίζεται ότι ο χρόνος συμμετοχής κάθε παίκτη είναι ικανοποιητικός.
4. **Αποτελέσματα**: Εμφάνιση των επιλεγμένων παικτών με έναν πίνακα και διάγραμμα που απεικονίζει τα στατιστικά τους.

Αυτό το εργαλείο προσφέρει μια μαθηματική προσέγγιση για την **αποτελεσματική σύνθεση ομάδας**, διασφαλίζοντας ότι όλοι οι παίκτες έχουν ικανοποιητικό χρόνο συμμετοχής στο παιχνίδι, με το συνολικό χρόνο να μην ξεπερνά τα 200 λεπτά. Είναι ιδανικό για προπονητές, αναλυτές και επαγγελματίες του αθλητισμού που επιθυμούν να κάνουν πιο στρατηγικές και δεδομενικά υποστηριζόμενες επιλογές παικτών.
""")




# Φίλτρα για τις θέσεις πάνω από τον πίνακα
st.markdown("Επιλογή Παικτών Ανά Θέση και Στατιστικό Βελτιστοποίησης")
fwd_count = st.slider("Πόσοι Forwards (F) θέλεις;", min_value=0, max_value=5, value=4)
g_count = st.slider("Πόσοι Guards (G) θέλεις;", min_value=0, max_value=5, value=5)
c_count = st.slider("Πόσοι Centers (C) θέλεις;", min_value=0, max_value=5, value=3)

# Επιλογή των στατιστικών που θα βελτιστοποιούνται για κάθε θέση
fwd_stats = st.multiselect("Στατιστικά για Βελτιστοποίηση (Forwards)", 
                           ['PTS/36', 'AST/36', 'REB/36', 'VTM', 'eFG%', 'TS%'], 
                           default=['PTS/36'])
g_stats = st.multiselect("Στατιστικά για Βελτιστοποίηση (Guards)", 
                         ['PTS/36', 'AST/36', 'REB/36', 'VTM', 'eFG%', 'TS%'], 
                         default=['PTS/36'])
c_stats = st.multiselect("Στατιστικά για Βελτιστοποίηση (Centers)", 
                         ['PTS/36', 'AST/36', 'REB/36', 'VTM', 'eFG%', 'TS%'], 
                         default=['PTS/36'])

# Δημιουργία dictionary με τους περιορισμούς για τις θέσεις
pos_constraints = {
    'F': fwd_count,
    'G': g_count,
    'C': c_count
}

# Δημιουργία dictionary με τα στατιστικά που θα βελτιστοποιούνται για κάθε θέση
pos_stats = {
    'F': fwd_stats,
    'G': g_stats,
    'C': c_stats
}

# Φιλτράρισμα των NaN/inf τιμών στα σχετικά πεδία
filtered_data_clean = filtered_data[
    filtered_data['PTS/36'].notna() & 
    filtered_data['PTS/36'].apply(np.isfinite) & 
    filtered_data['MIN/GP'].notna() & 
    filtered_data['MIN/GP'].apply(np.isfinite)
]

# Φίλτρο για την επιλογή παικτών που θα είναι σίγουρα στη δωδεκάδα
#st.subheader("Επιλέξτε Υποχρεωτικούς Παίκτες για τη Δωδεκάδα")
mandatory_players = st.multiselect(
    "Επιλέξτε παίκτες που θα περιλαμβάνονται υποχρεωτικά στη δωδεκάδα:",
    options=filtered_data_clean["Player"].unique(),
    default=[],
    help="Οι επιλεγμένοι παίκτες θα συμπεριληφθούν υποχρεωτικά στη δωδεκάδα."
)

# Φίλτρο για την επιλογή παικτών που δεν θα είναι στη δωδεκάδα
#st.subheader("Επιλέξτε Υποχρεωτικούς Παίκτες που δεν θα είναι στη Δωδεκάδα")
excluded_players = st.multiselect(
    "Επιλέξτε παίκτες που δεν θα περιλαμβάνονται στη δωδεκάδα:",
    options=[player for player in filtered_data_clean["Player"].unique() if player not in mandatory_players],
    default=[],
    help="Οι επιλεγμένοι παίκτες θα αποκλειστούν από τη δωδεκάδα."
)

# Δημιουργία του προβλήματος βελτιστοποίησης
prob = pulp.LpProblem("Optimized_Team_Selection", pulp.LpMaximize)

# Δημιουργία μεταβλητών για την επιλογή των παικτών
players = filtered_data_clean["Player"].unique().tolist()
player_vars = pulp.LpVariable.dicts("Player", players, cat='Binary')

# Αντικειμενική συνάρτηση: Μέγιστο στατιστικό ανά θέση
prob += pulp.lpSum([
    filtered_data_clean.loc[filtered_data_clean["Player"] == player, stat].values[0] * player_vars[player]
    for player in players for stat in pos_stats[filtered_data_clean.loc[filtered_data_clean["Player"] == player, 'Pos'].values[0]]
])

# Περιορισμός για το συνολικό χρόνο παιχνιδιού (min/gp ≤ 250)
prob += pulp.lpSum([
    filtered_data_clean.loc[filtered_data_clean["Player"] == player, 'MIN/GP'].values[0] * player_vars[player]
    for player in players
]) <= 250

# Περιορισμός για να επιλέξουμε ακριβώς 12 παίκτες
prob += pulp.lpSum([player_vars[player] for player in players]) == 12

# Περιορισμοί για τις θέσεις
for pos, count in pos_constraints.items():
    prob += pulp.lpSum([
        player_vars[player]
        for player in players if filtered_data_clean.loc[filtered_data_clean["Player"] == player, 'Pos'].values[0] == pos
    ]) == count

# Περιορισμός για τους υποχρεωτικούς παίκτες στη δωδεκάδα
for player in mandatory_players:
    prob += player_vars[player] == 1

# Περιορισμός για τους υποχρεωτικούς παίκτες εκτός δωδεκάδας
for player in excluded_players:
    prob += player_vars[player] == 0

# Λύση του προβλήματος
prob.solve()

# Ανάκτηση των επιλεγμένων παικτών
selected_players = [player for player in players if player_vars[player].varValue == 1]

# Εμφάνιση των επιλεγμένων παικτών
df_selected = filtered_data_clean[filtered_data_clean["Player"].isin(selected_players)]

# Εμφάνιση των δεδομένων των επιλεγμένων παικτών στον πίνακα
#st.write("Επιλεγμένοι Παίκτες για την Ομάδα:")
#st.write(df_selected)

# Δημιουργία expanders για την εμφάνιση των δεδομένων των επιλεγμένων παικτών
with st.expander("Επιλεγμένοι Παίκτες για την Ομάδα"):
    st.write(df_selected)

# Δημιουργία γραφήματος με οριζόντιες μπάρες για τους επιλεγμένους παίκτες
fig = px.bar(
    df_selected,
    x="PTS/36",  # Μπορείς να το αλλάξεις σε όποιο στατιστικό θέλεις (π.χ., 'REB/36', 'AST/36')
    y="Player",  # Παίκτης στον άξονα y
    title="Επιλεγμένοι Παίκτες και τα Στατιστικά τους",
    labels={"Player": "Παίκτης", "PTS/36": "Πόντοι ανά 36 λεπτά"},
    color="Pos",  # Χρωματισμός ανάλογα με τη θέση
    color_continuous_scale="Viridis",
    orientation="h"  # Ορίζει το διάγραμμα με οριζόντιες μπάρες
)

# Ενημέρωση διαγράμματος με μεγαλύτερο μέγεθος
fig.update_layout(
    height=500,  # Αυξάνει το ύψος του διαγράμματος
    width=800,  # Αυξάνει το πλάτος του διαγράμματος
)

# Εμφάνιση του γραφήματος
st.plotly_chart(fig)





st.markdown("""
    <hr style="height:2px; border:none; color:#1E90FF; background-color:#1E90FF;">
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors


# Λίστα στατιστικών για επιλογή
all_stats_columns = ["PTS/36", "REB/36", "AST/36", "VTM", "STL", "BLK"]

# Σύνταξη του Streamlit app
st.subheader("Πρόβλεψη Παρόμοιων Παικτών Βάσει Στατιστικών")
st.markdown("""
Ανακαλύψτε τους πιο παρόμοιους παίκτες με βάση τα στατιστικά τους.
Χρησιμοποιούμε προηγμένους αλγορίθμους μηχανικής μάθησης 
για να βρούμε τις πιο ακριβείς αντιστοιχίες σε πραγματικό χρόνο. 
""")

# Επιλογή των στατιστικών από το χρήστη
selected_stats = st.multiselect("Επιλέξτε τα Στατιστικά:", all_stats_columns, default=["PTS/36", "REB/36", "AST/36"])

# Έλεγχος αν έχει γίνει επιλογή
if not selected_stats:
    st.warning("Παρακαλώ επιλέξτε τουλάχιστον ένα στατιστικό για να προχωρήσουμε.")
else:
    # Κανονικοποίηση των δεδομένων για τα επιλεγμένα στατιστικά
    scaler = StandardScaler()
    data_normalized = scaler.fit_transform(filtered_data[selected_stats])

    # Δημιουργία μοντέλου k-NN
    model = NearestNeighbors(n_neighbors=6, metric='euclidean')  # Περισσότεροι γείτονες για να εξασφαλίσουμε ότι ο επιλεγμένος παίκτης θα εξαιρεθεί
    model.fit(data_normalized)

    # Επιλογή παίκτη από τον χρήστη
    player_name = st.selectbox("Επιλέξτε Παίκτη:", filtered_data["Player"])

    # Εύρεση του αντίστοιχου παίκτη από τα δεδομένα
    player_index = filtered_data[filtered_data["Player"] == player_name].index[0]

    # Εύρεση των πιο όμοιων παικτών
    distances, indices = model.kneighbors([data_normalized[player_index]])

    # Συγκέντρωση των δεδομένων για το γράφημα και αφαίρεση του επιλεγμένου παίκτη από τα αποτελέσματα
    similar_players = []
    for idx in indices[0]:
        if filtered_data.iloc[idx]["Player"] != player_name:  # Εξαιρούμε τον επιλεγμένο παίκτη
            similar_player = filtered_data.iloc[idx]
            similar_players.append((similar_player['Player'], distances[0][indices[0] == idx][0]))

    # Δημιουργία του διαδραστικού γραφήματος με Plotly
    player_names = [player[0] for player in similar_players]
    distances_values = [player[1] for player in similar_players]

# Δημιουργία του διαδραστικού γραφήματος με Plotly
fig = px.bar(
    x=distances_values,
    y=player_names,
    orientation='h',
    labels={'x': 'Απόσταση Στατιστικών', 'y': 'Παίκτες'},
    title='Πιο Όμοιοι Παίκτες με βάση τα Επιλεγμένα Στατιστικά',
    color=distances_values,
    color_continuous_scale='Viridis'
)

# Ρύθμιση του μεγέθους του διαγράμματος
fig.update_layout(
    width=600,  # Μέγεθος του πλάτους
    height=400,  # Μέγεθος του ύψους
)

# Εμφάνιση του διαδραστικού γραφήματος
st.plotly_chart(fig)




