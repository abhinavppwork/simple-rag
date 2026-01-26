from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ---- Load everything exactly like your retrieval pipeline ----
embedding_model = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

db = Chroma(
    persist_directory="db/chroma_db",
    embedding_function=embedding_model
)

model = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

chat_history = []


# -------- Gemini Safe Text Extractor (IMPORTANT FIX) --------
def extract_text(result):
    """
    Gemini 3 sometimes returns [] or list instead of string.
    This function safely extracts the text.
    """
    if isinstance(result.content, str):
        return result.content

    if isinstance(result.content, list):
        if len(result.content) == 0:
            return ""
        if "text" in result.content[0]:
            return result.content[0]["text"]

    return ""


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_question = data["question"]

    # ---- Question rewriting ----
    if chat_history:
        messages = [
            SystemMessage(content="Rewrite the question as a standalone searchable query")
        ] + chat_history + [
            HumanMessage(content=user_question)
        ]

        result = model.invoke(messages)
        search_question = extract_text(result)
    else:
        search_question = user_question

    # ---- Retrieve from Chroma ----

    retriever = db.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(search_question)
    use_docs = len(docs) > 0 and any(len(d.page_content.strip()) > 30 for d in docs)

    if use_docs:
        context = "\n".join([doc.page_content for doc in docs])

        prompt = f"""
        Answer using the following documents if they are relevant.
        If the documents do not contain the answer, use your own knowledge.

        Documents:
        {context}

        Question: {user_question}
        """
    else:
        prompt = f"""
    Answer the following question using your own knowledge:

    {user_question}
    """

    result = model.invoke(prompt)
    answer = extract_text(result)

    # ---- Store conversation ----
    chat_history.append(HumanMessage(content=user_question))
    chat_history.append(AIMessage(content=answer))

    return jsonify({"answer": answer})


if __name__ == "__main__":
    # Disable debug auto-reloader to avoid Windows socket crashes
    app.run(port=5000, debug=False)
