import gradio as gr

from app import run_pipeline
from services.stt import speech_to_text
from services.tts import text_to_speech
from db.banking_db import login_user


# -------------------------
# GLOBAL SESSION STATE
# -------------------------
SESSION = {
    "user_id": None,
    "logged_in": False
}


# -------------------------
# LOGIN HANDLER
# -------------------------
def handle_login(email, password):
    user_id, msg = login_user(email, password)

    if user_id:
        SESSION["user_id"] = user_id
        SESSION["logged_in"] = True
        return msg, gr.update(visible=False), gr.update(visible=True)

    return msg, gr.update(visible=True), gr.update(visible=False)


# -------------------------
# TEXT CHAT HANDLER
# -------------------------
def handle_text(user_text, history):
    if history is None:
        history = []

    # Login check
    if not SESSION["logged_in"]:
        history.append({
            "role": "assistant",
            "content": "⚠️ Please login first."
        })
        return history, gr.update(value=""), history

    # Empty input
    if not user_text or not user_text.strip():
        return history, gr.update(value=""), history

    # Run backend
    response = run_pipeline(user_text, SESSION["user_id"])

    # 🔔 AUTO TTS FOR REMINDER NOTIFICATION
    if response.startswith("🔔 Reminder"):
        text_to_speech(response)

    # ✅ REQUIRED MESSAGE FORMAT (Gradio v4+)
    history.append({
        "role": "user",
        "content": user_text
    })
    history.append({
        "role": "assistant",
        "content": response
    })

    # OTP UX
    if "OTP" in response:
        return (
            history,
            gr.update(
                value="",
                placeholder="Enter OTP here",
                interactive=True
            ),
            history
        )

    return history, gr.update(value=""), history


# -------------------------
# VOICE INPUT HANDLER (STT → TEXT)
# -------------------------
def handle_voice(audio, history):
    if history is None:
        history = []

    if not SESSION["logged_in"]:
        history.append({
            "role": "assistant",
            "content": "⚠️ Please login first."
        })
        return history, gr.update(value=""), history

    user_text = speech_to_text(audio)

    if not user_text:
        history.append({
            "role": "assistant",
            "content": "I could not understand your voice clearly."
        })
        return history, gr.update(value=""), history

    return handle_text(user_text, history)


# -------------------------
# AUDIO OUTPUT HANDLER (TTS)
# -------------------------
def handle_audio(history):
    if not history:
        return None

    # Find last assistant message safely
    for msg in reversed(history):
        if msg.get("role") == "assistant":
            text = msg.get("content")
            if text:
                return text_to_speech(text)

    return None


# -------------------------
# UI
# -------------------------
with gr.Blocks(title="Omni BankPilot – Secure AI Banking Assistant") as demo:

    gr.Markdown("## 🏦 Omni BankPilot – Secure AI Banking Assistant")

    # ---------- LOGIN PANEL ----------
    with gr.Column(visible=True) as login_panel:
        gr.Markdown("### 🔐 Login")
        email = gr.Textbox(label="Email", placeholder="paro@example.com")
        password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_status = gr.Markdown()

    # ---------- CHAT PANEL ----------
    with gr.Column(visible=False) as chat_panel:
        chatbot = gr.Chatbot(label="Chat", height=400)
        chat_state = gr.State([])

        gr.Markdown("### 💬 Type your query")
        text_input = gr.Textbox(
            placeholder="Type your message or OTP here",
            interactive=True
        )

        send_btn = gr.Button("Send")
        speak_btn = gr.Button("🔊 Speak")

        audio_out = gr.Audio(label="Bot speaks 🔊")

    # ---------- EVENTS ----------
    login_btn.click(
        handle_login,
        inputs=[email, password],
        outputs=[login_status, login_panel, chat_panel]
    )

    send_btn.click(
        handle_text,
        inputs=[text_input, chat_state],
        outputs=[chatbot, text_input, chat_state]
    )

    speak_btn.click(
        handle_audio,
        inputs=[chat_state],
        outputs=[audio_out]
    )

demo.launch()
