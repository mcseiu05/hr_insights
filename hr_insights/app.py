import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="HR Insight 360", layout="wide")
st.title("📊 HR Insight 360 Dashboard")

# Load data
leave_df = pd.read_csv("leave_data.csv")
payroll_df = pd.read_csv("payroll_data.csv")

# Merge on common keys
common_cols = [
    "ProjectID", "ProjectName", "DepartmentID", "DepartmentName",
    "SalarySessionID", "SessionName", "EmployeeID", "EmployeeCode", "EmployeeFullName"
]
df = pd.merge(leave_df, payroll_df, on=common_cols, how="inner", suffixes=("_Leave", "_Payroll"))

# Sidebar filters
st.sidebar.header("📌 Filters")
projects = ["All"] + sorted(df["ProjectName"].dropna().unique())
sessions = ["All"] + sorted(df["SessionName"].dropna().unique())

selected_project = st.sidebar.selectbox("Select Project", projects)
selected_session = st.sidebar.selectbox("Select Session", sessions)

# Apply filters
if selected_project != "All":
    df = df[df["ProjectName"] == selected_project]
if selected_session != "All":
    df = df[df["SessionName"] == selected_session]

# Derived Metrics
if not df.empty:
    df["Leave Ratio (%)"] = (df["TotalLeaveDays_Leave"] / df["TotalDaysInSession"]) * 100
    df["Payable Per Day"] = df["NetPayable"] / df["PayableDays"]

    tab1, tab2, tab3 = st.tabs(["📋 Leave Summary", "💰 Payroll Summary", "📈 Insights"])

    with tab1:
        st.subheader("Leave Summary")
        st.dataframe(df[["EmployeeFullName", "DepartmentName", "TotalLeaveDays_Leave", "UnplannedLeaveDays", "Leave Ratio (%)"]])

        st.subheader("Total Leave Days per Employee")
        leave_chart = alt.Chart(df).mark_bar().encode(
            x="EmployeeFullName",
            y="TotalLeaveDays_Leave",
            color="DepartmentName"
        ).properties(height=350)
        st.altair_chart(leave_chart, use_container_width=True)

    with tab2:
        st.subheader("Payroll Summary")
        st.dataframe(df[["EmployeeFullName", "NetPayable", "PayableDays", "TotalDaysInSession", "Payable Per Day"]])

        st.subheader("Payable Per Day")
        pay_chart = alt.Chart(df).mark_bar().encode(
            x="EmployeeFullName",
            y="Payable Per Day",
            color="DepartmentName"
        ).properties(height=350)
        st.altair_chart(pay_chart, use_container_width=True)

    with tab3:
        st.subheader("Key Insights")
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Leave Days", f"{df['TotalLeaveDays_Leave'].mean():.1f}")
        col2.metric("Avg Leave Ratio", f"{df['Leave Ratio (%)'].mean():.1f}%")
        col3.metric("Max Pay/Day", f"{df['Payable Per Day'].max():,.0f} BDT")

        st.markdown("---")
        st.markdown("### 🚩 Top 5 Employees with Most Unplanned Leaves")
        top_unplanned = df.sort_values(by="UnplannedLeaveDays", ascending=False).head(5)
        st.dataframe(top_unplanned[["EmployeeFullName", "DepartmentName", "UnplannedLeaveDays"]])

else:
    st.warning("No data available for the selected filters.")
