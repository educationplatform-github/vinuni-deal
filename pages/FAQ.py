import streamlit as st

st.title('FAQ - Frequently Asked Questions')

faqs = [
    ("What is your return policy?", "Our return policy is 30 days. If 30 days have gone by since your purchase, unfortunately we can’t offer you a refund or exchange."),
    ("How do I track my order?", "You can track your order by logging into your account and visiting the 'Orders' section."),
    ("Do you ship internationally?", "Yes, we ship worldwide. Shipping costs will apply, and will be added at checkout."),
    # Add more FAQs here
]

for question, answer in faqs:
    with st.expander(question):
        st.write(answer)