import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta


def form_date3(number_of_days, target_recall_percentage, gap=1, recall_factor_present=65, recall_factor_previous=6):
    x = np.arange(1, number_of_days, gap)
    y = np.exp(-x / number_of_days)
    coeff = np.log((number_of_days * 0.047 * recall_factor_present) / target_recall_percentage)
    if coeff >= 1:
        coeff -= 1
    y1 = np.interp(y, [y[-1], y[0]],
                   [recall_factor_present * coeff - (target_recall_percentage - recall_factor_present), 100])
    # y = np.interp(y, [y[-1],y[0]], [recall_factor_present*0.3, 100])
    if coeff <= 0:
        y1 = np.interp(y, [y[-1], y[0]], [0, 100])
    return x[len(y1[y1 >= (target_recall_percentage)])], x, y, y1


def form_timeline(number_of_days=30, target_recall_percentage=75, gap=1, recall_factor_present=65,
                  recall_factor_previous=60):
    if number_of_days <= 10:
        ints = 4
    elif number_of_days <= 15:
        ints = 5
    elif number_of_days <= 30:
        ints = 6
    else:
        ints = 8

    target_recall_vals = np.linspace(70, 95, ints)

    days = number_of_days
    date = datetime.now()
    for d in target_recall_vals:
        interval, x, y, y1 = form_date3(days, d, gap, recall_factor_present,
                                        recall_factor_previous)

        st.write("Date: {}".format(str(date).split()[0]))

        plt.figure(figsize=(10, 5))
        plt.plot(x, y)
        plt.xlim(0, number_of_days)
        st.pyplot()

        days -= interval
        date = date + timedelta(days=np.float64(interval))
        if d != target_recall_vals[-1]:
            st.write("Next Revision Date: {}".format(str(date).split()[0]))
            st.empty()

def main():

    st.title("Revision Timeline Optimized by Spaced Repetition")

    days = st.number_input("Total Days", value=30)
    value = 0
    if st.checkbox("Optional Parameters"):

        trp = st.number_input("Target Recall Percentage", value=75)
        gap = st.number_input("Gap between consecutive values", value=1)
        rfp = st.number_input("Recall Percentage", value=65)
        value = 1

    if st.button("Generate Revision Schedule"):
        if value == 1:
            form_timeline(days, trp, gap, rfp)
            st.header("This took place")
        else:
            form_timeline(days)

if __name__ == "__main__":
    main()


