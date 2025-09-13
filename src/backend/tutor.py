
import inspect
from gpt4all import GPT4All
from flask import Flask, request, jsonify
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
model=GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")
chathistory=[] #for the model to have context
def askChat(user_input):
    chathistory.append(f"Student: {user_input}")
    # Prompt for the model to see

    system_prompt = (
        "You are a Socratic tutor. Never give the user a direct answer. "
        "Instead, guide or nudge them toward the answer by asking questions, "
        "giving hints, and offering encouragement. Be supportive, patient, "
        "and focused on long-term understanding. If the user is correct, tell them so. "
        "If they demand the right answer, provide it. "
        "Do not hallucinate or invent information. Only respond based on what the user provides. "
        "Make replies short and avoid unnecessary details.\n\n"
    )

    #Last 4 messages and last 4 responses from model
    historyLast4= chathistory[-8:]

    full_convo=system_prompt+"\n".join(historyLast4)+"\nTutor:"

    print(full_convo)

    response = model.generate(system_prompt + full_convo, max_tokens=400)
    aiReply=response.strip().split("Student:")[0].strip()
    chathistory.append(f"Tutor: {aiReply}")

    return aiReply
@app.route("/chat", methods=["POST"])
def chat():
    data=request.get_json()
    user_message=data.get("message","")
    if not user_message:
        return jsonify({"reply":"Failure. Please send valid message"}),400
    reply=askChat(user_message)
    return jsonify({"reply":reply})
if __name__ == "__main__":
    app.run(port=5000,debug=True)
  
