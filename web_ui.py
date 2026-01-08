<<<<<<< HEAD
=======
# ## text only version
# import gradio as gr

# from app import run_pipeline
# from db.banking_db import login_user


# # =========================
# # SESSION (DEMO)
# # =========================
# SESSION = {
#     "user_id": None,
#     "logged_in": False
# }


# # =========================
# # LOGIN HANDLER
# # =========================
# def handle_login(email, password):
#     user_id, msg = login_user(email, password)

#     if user_id:
#         SESSION["user_id"] = user_id
#         SESSION["logged_in"] = True
#         return msg, gr.update(visible=False), gr.update(visible=True)

#     return msg, gr.update(visible=True), gr.update(visible=False)


# # =========================
# # TEXT HANDLER (CORE FIX)
# # =========================
# def handle_text(user_text, history):
#     """
#     IMPORTANT:
#     - Never mutate history
#     - Always return NEW history object
#     """

#     if history is None:
#         history = []

#     # Login check
#     if not SESSION["logged_in"]:
#         msg = "Please login first."
#         new_history = history + [{"role": "assistant", "content": msg}]
#         return new_history, "", new_history

#     if not user_text.strip():
#         return history, "", history

#     # Run backend
#     response = run_pipeline(user_text, SESSION["user_id"])

#     # IMMUTABLE UPDATE
#     new_history = history + [
#         {"role": "user", "content": user_text},
#         {"role": "assistant", "content": response}
#     ]

#     return new_history, "", new_history


# # =========================
# # UI
# # =========================
# with gr.Blocks(title="Omni BankPilot – Text Only") as demo:

#     gr.Markdown("## 🏦 Omni BankPilot – Text Mode (Stable)")

#     # -------- LOGIN --------
#     with gr.Column(visible=True) as login_panel:
#         gr.Markdown("###  Login")
#         email = gr.Textbox(label="Email")
#         password = gr.Textbox(label="Password", type="password")
#         login_btn = gr.Button("Login")
#         login_status = gr.Markdown()

#     # -------- CHAT --------
#     with gr.Column(visible=False) as chat_panel:
#         chatbot = gr.Chatbot(height=420)
#         chat_state = gr.State([])

#         text_input = gr.Textbox(
#             placeholder="Type message or OTP here"
#         )
#         send_btn = gr.Button("Send")

#     # -------- EVENTS --------
#     login_btn.click(
#         handle_login,
#         inputs=[email, password],
#         outputs=[login_status, login_panel, chat_panel]
#     )

#     send_btn.click(
#         handle_text,
#         inputs=[text_input, chat_state],
#         outputs=[chatbot, text_input, chat_state],
#         queue=True
#     )

# demo.launch()






# ## tts version
# import gradio as gr
# from app import run_pipeline
# from services.tts import text_to_speech
# from db.banking_db import login_user

# # =========================
# # SESSION
# # =========================
# SESSION = {
#     "user_id": None,
#     "logged_in": False
# }

# # =========================
# # LOGIN
# # =========================
# def handle_login(email, password):
#     user_id, msg = login_user(email, password)

#     if user_id:
#         SESSION["user_id"] = user_id
#         SESSION["logged_in"] = True
#         return msg, gr.update(visible=False), gr.update(visible=True)

#     return msg, gr.update(visible=True), gr.update(visible=False)

# # =========================
# # TEXT + TTS HANDLER
# # =========================
# def handle_text(user_text, history):
#     if history is None:
#         history = []

#     if not SESSION["logged_in"]:
#         msg = " Please login first."
#         new_history = history + [{"role": "assistant", "content": msg}]
#         audio = text_to_speech(msg)
#         return new_history, "", new_history, audio

#     if not user_text.strip():
#         return history, "", history, None

#     response = run_pipeline(user_text, SESSION["user_id"])

#     new_history = history + [
#         {"role": "user", "content": user_text},
#         {"role": "assistant", "content": response}
#     ]

#     audio = text_to_speech(response)
#     return new_history, "", new_history, audio

# # =========================
# # UI
# # =========================
# with gr.Blocks(title="Omni BankPilot – Text + TTS") as demo:

#     gr.Markdown("## Omni BankPilot – Text + Voice Output")

#     # -------- LOGIN --------
#     with gr.Column(visible=True) as login_panel:
#         email = gr.Textbox(label="Email")
#         password = gr.Textbox(label="Password", type="password")
#         login_btn = gr.Button("Login")
#         login_status = gr.Markdown()

#     # -------- CHAT --------
#     with gr.Column(visible=False) as chat_panel:
#         chatbot = gr.Chatbot(height=420)
#         chat_state = gr.State([])

#         text_input = gr.Textbox(
#             placeholder="Type message or OTP here"
#         )
#         send_btn = gr.Button("Send")

#         audio_out = gr.Audio(
#             label=" Assistant speaks",
#             autoplay=True,
#             interactive=False
#         )

#     # -------- EVENTS --------
#     login_btn.click(
#         handle_login,
#         inputs=[email, password],
#         outputs=[login_status, login_panel, chat_panel]
#     )

#     send_btn.click(
#         handle_text,
#         inputs=[text_input, chat_state],
#         outputs=[chatbot, text_input, chat_state, audio_out],
#         queue=True
#     )

# demo.launch()









>>>>>>> 92093a4197c705fd0ca1c769efdbddb3c4b08404
import gradio as gr
import os

from app import run_pipeline
from services.tts import text_to_speech
from services.stt import speech_to_text
from db.banking_db import login_user

# =========================
# SESSION
# =========================
SESSION = {
    "user_id": None,
    "logged_in": False
}

# =========================
# LOGIN
# =========================
def handle_login(email, password):
    user_id, msg = login_user(email, password)

    if user_id:
        SESSION["user_id"] = user_id
        SESSION["logged_in"] = True
        return msg, gr.update(visible=False), gr.update(visible=True)

    return msg, gr.update(visible=True), gr.update(visible=False)

# =========================
# TEXT HANDLER
# =========================
def handle_text(user_text, history):
    if history is None:
        history = []

    if not SESSION["logged_in"]:
<<<<<<< HEAD
        msg = "⚠️ Please login first."
=======
        msg = "Please login first."
>>>>>>> 92093a4197c705fd0ca1c769efdbddb3c4b08404
        new_history = history + [{"role": "assistant", "content": msg}]
        audio = text_to_speech(msg)
        return new_history, "", new_history, audio

    if not user_text.strip():
        return history, "", history, None

    response = run_pipeline(user_text, SESSION["user_id"])

    new_history = history + [
        {"role": "user", "content": user_text},
        {"role": "assistant", "content": response}
    ]

    audio = text_to_speech(response)
    return new_history, "", new_history, audio

# =========================
# 🎤 VOICE HANDLER (STT)
# =========================
def handle_voice(audio_path, history):
    if history is None:
        history = []

    if not SESSION["logged_in"]:
<<<<<<< HEAD
        msg = "⚠️ Please login first."
=======
        msg = "Please login first."
>>>>>>> 92093a4197c705fd0ca1c769efdbddb3c4b08404
        new_history = history + [{"role": "assistant", "content": msg}]
        audio = text_to_speech(msg)
        return new_history, new_history, audio

    if not audio_path or not os.path.exists(audio_path):
        return history, history, None

    # 🔹 Speech → Text
    user_text = speech_to_text(audio_path)

    if not user_text:
        msg = " Sorry, I could not understand your voice."
        new_history = history + [{"role": "assistant", "content": msg}]
        audio = text_to_speech(msg)
        return new_history, new_history, audio

    # 🔐 OTP SAFETY (voice blocked)
    clean = user_text.replace(" ", "")
    if clean.isdigit() and len(clean) >= 4:
        msg = " Please type the OTP instead of speaking it."
        new_history = history + [{"role": "assistant", "content": msg}]
        audio = text_to_speech(msg)
        return new_history, new_history, audio

    # 🔹 Run pipeline
    response = run_pipeline(user_text, SESSION["user_id"])

    new_history = history + [
        {"role": "user", "content": user_text},
        {"role": "assistant", "content": response}
    ]

    audio = text_to_speech(response)
    return new_history, new_history, audio

# =========================
# UI
# =========================
with gr.Blocks(title="Omni BankPilot – Voice Enabled") as demo:

    gr.Markdown("## 🏦 Omni BankPilot – Text + Voice")

    # -------- LOGIN --------
    with gr.Column(visible=True) as login_panel:
        email = gr.Textbox(label="Email")
        password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_status = gr.Markdown()

    # -------- CHAT --------
    with gr.Column(visible=False) as chat_panel:
        chatbot = gr.Chatbot(height=420)
        chat_state = gr.State([])

        text_input = gr.Textbox(placeholder="Type message or OTP")
        send_btn = gr.Button("Send")

        audio_input = gr.Audio(
            type="filepath",
            label="🎙️ Speak (press, talk, release)"
        )

        audio_out = gr.Audio(
            label="🔊 Assistant speaks",
            autoplay=True,
            interactive=False
        )

    # -------- EVENTS --------
    login_btn.click(
        handle_login,
        inputs=[email, password],
        outputs=[login_status, login_panel, chat_panel]
    )

    send_btn.click(
        handle_text,
        inputs=[text_input, chat_state],
        outputs=[chatbot, text_input, chat_state, audio_out],
        queue=True
    )

    audio_input.change(
        handle_voice,
        inputs=[audio_input, chat_state],
        outputs=[chatbot, chat_state, audio_out],
        queue=True
    )

demo.launch()
