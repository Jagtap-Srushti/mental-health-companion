import streamlit as st
import pickle
import pandas as pd

# ===== Load model & vectorizer =====
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# ===== Bot replies =====
def bot_reply(sentiment):
    replies = {
        "Very Positive": "Amazing energy! Stay blessed ✨",
        "Positive": "That's wonderful! Keep going 😊",
        "Neutral": "Thanks for sharing! I'm here with you 🤝",
        "Negative": "I'm sorry you're feeling this way 🫂",
        "Very Negative": "That sounds really tough. Please talk to someone you trust 💛"
    }
    return replies.get(sentiment, "I'm here for you.")

# ===== Predict sentiment =====
def get_sentiment(text):
    x = vectorizer.transform([text])
    sentiment = model.predict(x)[0]
    return sentiment

# ===== Streamlit setup =====
st.set_page_config(page_title="💬 Mental Health Chatbot", layout="wide")

# ===== Custom CSS =====
st.markdown("""
<style>
body { background-color: #0E1117; font-family: 'Inter', sans-serif; color:white; }
.title { text-align:center; font-size:42px; font-weight:800; color:#736BFF; margin-top:15px; }
.subtitle { text-align:center; color:#A0A0A0; font-size:16px; margin-bottom:25px; }

.chat-wrapper {
    max-width: 700px;
    width: 90%;
    margin: 20px auto;
    background: #1A1D21;
    padding: 20px;
    border-radius: 20px;
    min-height: 400px;
    max-height: 70vh;  /* responsive height */
    overflow-y: auto;
    border: 1px solid #23262B;
    display: flex;
    flex-direction: column;
    gap: 10px;
    scroll-behavior: smooth;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}
.chat-wrapper::-webkit-scrollbar {
    width: 8px;
}
.chat-wrapper::-webkit-scrollbar-thumb {
    background: #736BFF;
    border-radius: 4px;
}

.user-bubble {
    background: linear-gradient(135deg, #4A69FF, #6A82FF);
    color: white;
    padding: 14px 18px;
    border-radius: 25px 25px 0 25px;
    margin: 8px 0;
    max-width: 75%;
    margin-left: auto;
    text-align: right;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
    word-wrap: break-word;
    animation: slideInRight 0.3s ease;
}

.bot-bubble {
    background: linear-gradient(135deg, #2D3239, #40444B);
    color: #E4E4E4;
    padding: 14px 18px;
    border-radius: 25px 25px 25px 0;
    margin: 8px 0;
    max-width: 75%;
    margin-right: auto;
    text-align: left;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.3);
    word-wrap: break-word;
    animation: slideInLeft 0.3s ease;
}

@keyframes slideInRight {
    from { opacity:0; transform: translateX(100px);}
    to { opacity:1; transform: translateX(0);}
}
@keyframes slideInLeft {
    from { opacity:0; transform: translateX(-100px);}
    to { opacity:1; transform: translateX(0);}
}

.input-container {
    display: flex;
    justify-content: center;
    margin-top: 15px;
    gap: 10px;
    position: sticky;
    bottom: 0;
    background: #1A1D21;
    padding: 10px;
    border-top: 1px solid #2E3239;
    border-radius: 0 0 15px 15px;
}

input[type="text"] {
    width: 100% !important;
    max-width: 600px;
    padding: 14px 20px !important;
    border-radius: 30px !important;
    border: 1px solid #30343A !important;
    background: #1F2329 !important;
    color: white !important;
    font-size: 16px;
    transition: 0.2s;
}
input[type="text"]:focus {
    border-color: #736BFF !important;
    outline: none !important;
    box-shadow: 0 0 10px rgba(115,107,255,0.5);
}

button {
    padding: 14px 24px !important;
    background: #736BFF !important;
    color: white;
    border-radius: 30px;
    font-weight: 600;
    border: none !important;
    cursor: pointer;
    transition: 0.3s ease-in-out;
}
button:hover {
    background: #5a52e6 !important;
    transform: translateY(-2px);
}

.stSidebar .sidebar-content {
    background-color: #111418;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ===== Title =====
st.markdown("<div class='title'>💬 Mental Health Chatbot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Understand your feelings using Machine Learning 🤖</div>", unsafe_allow_html=True)

# ===== Sidebar =====
st.sidebar.title("📌 Resources & Support")
with st.sidebar.expander("📞 Helplines"):
    st.write("National Suicide Prevention Lifeline: **1-800-273-8255**")
    st.write("Crisis Text Line: Text **'HELLO'** to **741741**")
    st.write("[🌍 More Resources](https://www.mentalhealth.gov/get-help/immediate-help)")
st.sidebar.markdown("---")
st.sidebar.subheader("🔐 Privacy Notice")
st.sidebar.info("This chatbot does not permanently store any personal information.")

# ===== Session state =====
if "history" not in st.session_state:
    st.session_state.history = [("bot", "Hello! I'm here to chat with you 🤖")]
if "mood_tracker" not in st.session_state:
    st.session_state.mood_tracker = []

# ===== Chat container =====
chat_container = st.container()

with chat_container:
    for sender, msg in st.session_state.history:
        if sender == "user":
            st.markdown(f"<div class='user-bubble'>🧑‍💬 {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'>🤖 {msg}</div>", unsafe_allow_html=True)

# Auto-scroll last message into view
st.markdown("""
<script>
const chatBubbles = window.parent.document.querySelectorAll('.user-bubble, .bot-bubble');
if(chatBubbles.length > 0){
    chatBubbles[chatBubbles.length-1].scrollIntoView({behavior: "smooth"});
}
</script>
""", unsafe_allow_html=True)


# ===== Input using form =====
with st.form(key="chat_form"):
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    user_input = st.text_input("", placeholder="Tell me how you're feeling...")
    send_btn = st.form_submit_button("Send")
    st.markdown("</div>", unsafe_allow_html=True)

    if send_btn and user_input.strip() != "":
        sentiment = get_sentiment(user_input)
        reply = bot_reply(sentiment)
        st.session_state.history.append(("user", user_input))
        st.session_state.history.append(("bot", reply))
        st.session_state.mood_tracker.append((user_input, sentiment))
        user_input = ""

# ===== Mood chart using Streamlit's line_chart =====
if st.session_state.mood_tracker:
    mood_data = pd.DataFrame(st.session_state.mood_tracker, columns=["Message", "Sentiment"])
    sentiment_mapping = {
        "Very Positive": 2,
        "Positive": 1,
        "Neutral": 0,
        "Negative": -1,
        "Very Negative": -2
    }
    mood_data["Polarity"] = mood_data["Sentiment"].map(sentiment_mapping).fillna(0)
    
    st.markdown("<div style='margin-top:30px;'>### 📊 Mood Trend</div>", unsafe_allow_html=True)
    st.line_chart(mood_data["Polarity"], height=250)

# ===== Session summary =====
if st.sidebar.button("📄 Show Session Summary"):
    st.sidebar.write("### Session Summary")
    for i, (msg, senti) in enumerate(st.session_state.mood_tracker):
        st.sidebar.write(f"{i+1}. **{msg}** → _{senti}_")
