import streamlit as st

st.title('FAQ - Frequently Asked Questions')

faqs = [
    ("Why Abroad in Vietnam wants to form this deal in the first place?", "Our return policy is 30 days. If 30 days have gone by since your purchase, unfortunately we can’t offer you a refund or exchange."),
    ("What if Abroad in Vietnam can't get this deal with VinUni?", "We are gonna go with another university"),
    ("Do you ship internationally?", "Yes, we ship worldwide. Shipping costs will apply, and will be added at checkout."),
    # Add more FAQs here
]

for question, answer in faqs:
    with st.expander(question):
        st.write(answer)