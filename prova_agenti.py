import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from web_scraping import get_data

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("🧠 Assistente AI per le Recensioni di Ristoranti")

@st.cache_data
def load_reviews():
    return get_data()

df = load_reviews()

if df is not None:
    st.subheader("📥 Chiedi all'AI le recensioni")
    user_input = st.text_area("La tua domanda sulle recensioni:")

    if user_input:
        all_reviews = "\n".join(df['snippet'].dropna().tolist())

        full_prompt = f"""
Sei un esperto di customer experience. Di seguito trovi recensioni di clienti su un ristorante.

Recensioni:
{all_reviews}

Scrivi una risposta in italiano, chiara e concisa, che risponda alla domanda dell'utente.
Rispondi solo alla domanda dell'utente, senza aggiungere altro.

Domanda dell'utente: {user_input}

Risposta:
"""

        with st.spinner("AI sta rispondendo..."):
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": full_prompt}
                ],
                max_tokens=300,
                temperature=0.7,
            )

        st.markdown("### 🤖 Risposta dell'AI:")
        st.write(response.choices[0].message.content)
else:
    st.warning("Nessuna recensione trovata.")
