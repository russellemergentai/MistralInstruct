from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
from langchain import LLMChain
from langchain.prompts import PromptTemplate

# Initialize the app
app = Flask(__name__)

# Load Mistral 7B model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B")
model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B")

# Define LangChain prompt template and chain
template = "Answer the following question: {question}"
prompt = PromptTemplate(template=template, input_variables=["question"])
chain = LLMChain(llm=model, prompt=prompt)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    question = data.get("question", "")
    # Use LangChain with Mistral model to get a response
    response = chain.run(question=question)
    return jsonify({"answer": response})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
