# import os
# import streamlit as st
# from dotenv import load_dotenv
# from openai import OpenAI


# load_dotenv()


# api_key = os.getenv("FIREWORKS_API_KEY")

# if not api_key:
#     st.error("🔥 FIREWORKS_API_KEY not found in environment variables. Please set it in your .env file.")
#     st.stop()


# client = OpenAI(
#     api_key=api_key,
#     base_url="https://api.fireworks.ai/inference/v1"
# )

# st.title("🧠 Assistente AI con Fireworks.ai")

# user_input = st.text_area("Fai una domanda:", height=150)

# if user_input:
#     with st.spinner("AI sta rispondendo..."):
#         try:
#             response = client.chat.completions.create(
#                 model="accounts/fireworks/models/mixtral-8x7b-instruct",
#                 messages=[{"role": "user", "content": user_input}],
#                 max_tokens=300,
#                 temperature=0.7,
#             )
#             answer = response.choices[0].message.content
#             st.markdown("### 🤖 Risposta dell'AI:")
#             st.write(answer)
#         except Exception as e:
#             st.error(f"Errore durante la chiamata API: {e}")

import streamlit as st
from dotenv import load_dotenv
import os
from web_scraping import get_data
from fireworks import LLM  

load_dotenv()

st.title("🧠 Assistente AI per le Recensioni di Ristoranti")

@st.cache_data
def load_reviews():
    return get_data()

@st.cache_resource
def load_model():
    api_key = os.getenv("FIREWORKS_API_KEY")
    if not api_key:
        st.error("🔥 FIREWORKS_API_KEY non trovato nelle variabili d'ambiente.")
        st.stop()
    # Initialize Fireworks LLM client with your API key
    llm = LLM(
        api_key=api_key,
        model="accounts/fireworks/models/llama-v3p1-405b-instruct",  # Your model here
        deployment_type="serverless"
    )
    return llm

df = load_reviews()
model = load_model()

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
            response = model.chat.completions.create(
                messages=[{"role": "user", "content": full_prompt}],
                max_tokens=300,
                temperature=0.7,
            )
        st.markdown("### 🤖 AI Risposta:")
        st.write(response.choices[0].message.content)
else:
    st.warning("Nessuna recensione trovata.")