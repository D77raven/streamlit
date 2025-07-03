import streamlit as st
import openai
from web_scraping import get_data
import os
from dotenv import load_dotenv

load_dotenv()

st.title("🧠 Assistente AI per le Recensioni di Ristoranti")

@st.cache_data
def load_reviews():
    return get_data()

df = load_reviews()

# Make sure you set your API key properly
openai.api_key = os.getenv("api_key")

if df is not None:
    st.subheader("📥 Chiedi all'AI le recensioni")
    user_input = st.text_area("La tua domanda sulle recensioni:")

    if user_input:
        all_reviews = "\n".join(df['snippet'].dropna().tolist())
        full_prompt = f"""
Sei un esperto di customer experience. Di seguito trovi recensioni di clienti su un ristorante.
Recensioni:
{all_reviews}

Fornisci una risposta in italiano, chiara e concisa, che risponda alla domanda dell'utente.
Rispondi solo alla domanda, senza aggiungere altro.

Domanda dell'utente: {user_input}

Risposta:
"""
        with st.spinner("AI sta rispondendo..."):
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=300,
                temperature=0.7,
            )
        answer = response.choices[0].message.content
        st.markdown("### 🤖 AI Risposta:")
        st.write(answer)
else:
    st.warning("Nessuna recensione trovata.")
