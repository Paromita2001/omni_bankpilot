# import gradio as gr

# from app import run_pipeline
# from services.stt import speech_to_text
# from services.tts import text_to_speech
# from db.banking_db import login_user

# # -------------------------
# # GLOBAL SESSION STATE
# # -------------------------
# SESSION = {
#     "user_id": None,
#     "logged_in": False
# }

# # -------------------------
# # LOGIN HANDLER
# # -------------------------
# def handle_login(email, password):
#     user_id, msg = login_user(email, password)

#     if user_id:
#         SESSION["user_id"] = user_id
#         SESSION["logged_in"] = True
#         return msg, gr.update(visible=False), gr.update(visible=True)

#     return msg, gr.update(visible=True), gr.update(visible=False)


# # -------------------------
# # TEXT CHAT HANDLER
# # -------------------------
# # def handle_text(user_text, history):
# #     if not SESSION["logged_in"]:
# #         history.append({
# #             "role": "assistant",
# #             "content": "⚠️ Please login first."
# #         })
# #         return history, None

# #     if not user_text or not user_text.strip():
# #         return history, None

# #     # ✅ PASS user_id TO PIPELINE
# #     response = run_pipeline(user_text, SESSION["user_id"])

# #     history.append({"role": "user", "content": user_text})
# #     history.append({"role": "assistant", "content": response})

# #     audio = text_to_speech(response)
# #     return history, audio

# def handle_text(user_text, history):
#     if not SESSION["logged_in"]:
#         history.append({
#             "role": "assistant",
#             "content": "⚠️ Please login first."
#         })
#         return history, None

#     if not user_text or not user_text.strip():
#         return history, None

#     response = run_pipeline(user_text, SESSION["user_id"])

#     history.append({
#         "role": "user",
#         "content": user_text
#     })
#     history.append({
#         "role": "assistant",
#         "content": response
#     })

#     audio = text_to_speech(response)
#     return history, audio

# # -------------------------
# # VOICE CHAT HANDLER
# # -------------------------
# def handle_voice(audio, history):
#     if not SESSION["logged_in"]:
#         history.append({
#             "role": "assistant",
#             "content": "⚠️ Please login first."
#         })
#         return history, None

#     user_text = speech_to_text(audio)

#     if not user_text:
#         history.append({
#             "role": "assistant",
#             "content": "I couldn’t understand your voice clearly. Please type your query."
#         })
#         return history, None

#     return handle_text(user_text, history)


# # -------------------------
# # UI
# # -------------------------
# with gr.Blocks(title="Omni BankPilot – Secure Banking Assistant") as demo:

#     gr.Markdown("## 🏦 Omni BankPilot – Secure AI Banking Assistant")

#     # ---------- LOGIN PANEL ----------
#     with gr.Column(visible=True) as login_panel:
#         gr.Markdown("### 🔐 Login")
#         email = gr.Textbox(label="Email", placeholder="paro@example.com")
#         password = gr.Textbox(label="Password", type="password")
#         login_btn = gr.Button("Login")
#         login_status = gr.Markdown()

#     # ---------- CHAT PANEL ----------
#     with gr.Column(visible=False) as chat_panel:
#         chatbot = gr.Chatbot(label="Chat", height=400)
#         state = gr.State([])

#         gr.Markdown("### 💬 Type your query")
#         text_input = gr.Textbox(
#             placeholder="What is my balance? / Send 500 to Rohit Sharma / Enter OTP"
#         )
#         send_btn = gr.Button("Send")

#         gr.Markdown("### 🎤 Or speak")
#         audio_input = gr.Audio()
#         voice_btn = gr.Button("Process Voice")

#         audio_out = gr.Audio(label="Bot speaks 🔊")

#     # ---------- EVENTS ----------
#     login_btn.click(
#         handle_login,
#         inputs=[email, password],
#         outputs=[login_status, login_panel, chat_panel]
#     )

#     send_btn.click(
#         handle_text,
#         inputs=[text_input, state],
#         outputs=[chatbot, audio_out]
#     )

#     voice_btn.click(
#         handle_voice,
#         inputs=[audio_input, state],
#         outputs=[chatbot, audio_out]
#     )

# demo.launch()


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
# TEXT CHAT HANDLER (TEXT ONLY)
# -------------------------
def handle_text(user_text, history):
    if history is None:
        history = []

    # Login check
    if not SESSION["logged_in"]:
        history.append({"role": "assistant", "content": "Please login first."})
        return history, gr.update(value="", interactive=True), ""

    # Empty input
    if not user_text or not user_text.strip():
        return history, gr.update(value="", interactive=True), ""

    # Run backend
    response = run_pipeline(user_text, SESSION["user_id"])

    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": response})

    # OTP UX
    if "OTP" in response:
        return history, gr.update(
            value="",
            placeholder="Enter OTP here",
            interactive=True
        ), response

    return history, gr.update(value="", interactive=True), response


# -------------------------
# AUDIO HANDLER (ONLY ON CLICK)
# -------------------------
def handle_audio(text):
    if not text:
        return None
    return text_to_speech(text)


# -------------------------
# VOICE INPUT HANDLER (STT → TEXT FLOW)
# -------------------------
def handle_voice(audio, history):
    if history is None:
        history = []

    if not SESSION["logged_in"]:
        history.append({"role": "assistant", "content": "Please login first."})
        return history, gr.update(value="", interactive=True), ""

    user_text = speech_to_text(audio)

    if not user_text:
        history.append({
            "role": "assistant",
            "content": "I could not understand your voice clearly. Please type your query."
        })
        return history, gr.update(value="", interactive=True), ""

    return handle_text(user_text, history)


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

        gr.Markdown("### 💬 Type your query")
        text_input = gr.Textbox(
            placeholder="Type your message or OTP here",
            interactive=True
        )

        send_btn = gr.Button("Send")
        speak_btn = gr.Button("🔊 Speak")

        audio_out = gr.Audio(label="Bot speaks")
        last_response = gr.State("")

    # ---------- EVENTS ----------
    login_btn.click(
        handle_login,
        inputs=[email, password],
        outputs=[login_status, login_panel, chat_panel]
    )

    # Text message
    send_btn.click(
        handle_text,
        inputs=[text_input, chatbot],
        outputs=[chatbot, text_input, last_response]
    )

    # Audio only when user clicks Speak
    speak_btn.click(
        handle_audio,
        inputs=[last_response],
        outputs=[audio_out]
    )

demo.launch()
