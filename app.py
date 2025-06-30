import streamlit as st
import pandas as pd
import altair as alt

# --- PAGE CONFIG ---
st.set_page_config(page_title="HR Insight 360", layout="wide")
st.title("📊 HR Insight 360 Dashboard")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    leave_df = pd.read_csv("leave_data.csv")
    payroll_df = pd.read_csv("payroll_data.csv")
    return leave_df, payroll_df

leave_df, payroll_df = load_data()

# --- MERGE DATA ---
merge_keys = [
    "ProjectID", "ProjectName", "DepartmentID", "DepartmentName",
    "SalarySessionID", "SessionName", "EmployeeID", "EmployeeCode", "EmployeeFullName"
]
df = pd.merge(leave_df, payroll_df, on=merge_keys, how="inner", suffixes=("_Leave", "_Payroll"))

# --- SIDEBAR FILTERS ---
st.sidebar.header("📌 Filters")
project_list = ["All"] + sorted(df["ProjectName"].dropna().unique())
session_list = ["All"] + sorted(df["SessionName"].dropna().unique())

selected_project = st.sidebar.selectbox("Select Project", project_list)
selected_session = st.sidebar.selectbox("Select Session", session_list)

# Apply filters
if selected_project != "All":
    df = df[df["ProjectName"] == selected_project]

if selected_session != "All":
    df = df[df["SessionName"] == selected_session]

# --- DERIVED COLUMNS ---
if not df.empty:
    df["Leave Ratio (%)"] = (df["TotalLeaveDays_Leave"] / df["TotalDaysInSession"]).fillna(0) * 100
    df["Payable Per Day"] = (df["NetPayable"] / df["PayableDays"]).replace([float('inf'), -float('inf')], 0).fillna(0)
    df["EmployeeLabel"] = df["EmployeeCode"] + " - " + df["EmployeeFullName"]

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["📋 Leave Summary", "💰 Payroll Summary", "📈 Insights"])

    # --- LEAVE SUMMARY TAB ---
    with tab1:
        st.subheader("Leave Summary")
        st.dataframe(df[[
            "ProjectName", "EmployeeCode", "EmployeeFullName", "DepartmentName",
            "TotalLeaveDays_Leave", "UnplannedLeaveDays", "Leave Ratio (%)"
        ]].sort_values(by="TotalLeaveDays_Leave", ascending=False))

        st.subheader("Top 30 Employees by Leave Days")
        top_leave = df.sort_values(by="TotalLeaveDays_Leave", ascending=False).head(30)
        leave_chart = alt.Chart(top_leave).mark_bar().encode(
            x=alt.X("EmployeeLabel:N", sort="-y", title="Employee"),
            y=alt.Y("TotalLeaveDays_Leave", title="Leave Days"),
            color=alt.Color("DepartmentName:N", title="Department")
        ).properties(height=500)
        st.altair_chart(leave_chart, use_container_width=True)

    # --- PAYROLL SUMMARY TAB ---
    with tab2:
        st.subheader("Payroll Summary")
        st.dataframe(df[[
            "ProjectName", "EmployeeCode", "EmployeeFullName", "DepartmentName",
            "NetPayable", "PayableDays", "TotalDaysInSession", "Payable Per Day"
        ]].sort_values(by="NetPayable", ascending=False))

        st.subheader("Top 30 Employees by Net Payable")
        top_pay = df.sort_values(by="NetPayable", ascending=False).head(30)
        pay_chart = alt.Chart(top_pay).mark_bar().encode(
            x=alt.X("EmployeeLabel:N", sort="-y", title="Employee"),
            y=alt.Y("NetPayable:Q", title="Net Payable (BDT)"),
            color=alt.Color("DepartmentName:N", title="Department")
        ).properties(height=500)
        st.altair_chart(pay_chart, use_container_width=True)

    # --- INSIGHTS TAB ---
    with tab3:
        st.subheader("Key Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Avg Leave Days", f"{df['TotalLeaveDays_Leave'].mean():.1f}")
        col2.metric("📊 Avg Leave Ratio", f"{df['Leave Ratio (%)'].mean():.1f}%")
        col3.metric("💵 Max Pay/Day", f"{df['Payable Per Day'].max():,.0f} BDT")

        st.markdown("### 🚩 Top 5 Employees with Most Unplanned Leaves")
        top_unplanned = df.sort_values(by="UnplannedLeaveDays", ascending=False).head(5)
        st.dataframe(top_unplanned[[
            "ProjectName", "EmployeeCode", "EmployeeFullName", "DepartmentName", "UnplannedLeaveDays"
        ]])

else:
    st.warning("⚠️ No data available for the selected filters.")
