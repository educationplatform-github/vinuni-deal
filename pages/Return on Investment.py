import streamlit as st
import matplotlib.pyplot as plt


# Create tabs
list_tabs=["Total Payment", "Return on Investment"]
total_payment, ROI = st.tabs(list_tabs)

# Function to calculate The Rest and Total
def calculate_values(upfront_cost, money_per_student, students_enrolled):
    global Auditorium_cost
    total = money_per_student * students_enrolled
    the_rest = total - upfront_cost
    return the_rest, total

# Function to plot the waterfall chart
def plot_waterfall(upfront_cost, the_rest, total):
    global Auditorium_cost
    fig, ax = plt.subplots(figsize=(16, 8))  # Increase figure size
    
    # Plot bars with adjusted positions and labels
    ax.bar("Upfront Cost", upfront_cost, color='green')
    ax.bar("Remainder Payment for Referral", the_rest, bottom=upfront_cost, color='green')
    ax.bar("Total ", total, bottom=0, color='grey')
    ax.bar("Auditorium Cost", Auditorium_cost, bottom=upfront_cost + the_rest-Auditorium_cost, color='red')
    ax.bar("Total Payment from VinUni", total-Auditorium_cost, bottom=0, color='grey')
    
    # Set y-axis label and title
    ax.set_ylabel("Money")
    ax.set_title("Chart Total Payment")
    
    # Adjust layout to prevent text overlap
    plt.tight_layout(pad=3.0)  # Increase padding
    
    # Show the plot
    st.pyplot(fig)


Auditorium_cost = 165 # Million Dong

with total_payment:
    st.title("Chart Total Payment")

    # Slider for upfront cost
    upfront_cost = st.slider("Upfront Cost (Million VND)", min_value=0, max_value=1000, step=50, value=300)
    money_per_student = st.slider("Money per Student", min_value=0, max_value=20, step=1, value=10)
    students_enrolled = st.slider("Students Enrolled", min_value=0, max_value=200, step=10, value=100)
    # Calculate values
    the_rest, total = calculate_values(upfront_cost, money_per_student, students_enrolled)
    # Plot the waterfall chart
    plot_waterfall(upfront_cost, the_rest, total)

with ROI:
    st.title("Chart ")