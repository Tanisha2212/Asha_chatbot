import os
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Constants
DB_FAISS_PATH = "vectorstore/db_faiss"
HF_TOKEN = os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

def load_llm(huggingface_repo_id):
    """Load HuggingFace LLM endpoint"""
    llm = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        model_kwargs={
            "token": HF_TOKEN,
            "max_length": "600"
        }
    )
    return llm

def set_custom_prompt(custom_prompt_template):
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt

def connect_memory():
    """Connect to FAISS vectorstore and prepare Retrieval QA chain"""
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

    CUSTOM_PROMPT_TEMPLATE = """
  You are Asha, an AI chatbot focused on women empowerment and career development.
Your goal: Help women navigate careers, find job opportunities, and access growth resources.

When suggesting jobs/resources:

Give specific roles (3–5 suggestions) with brief descriptions.

Share helpful company/industry context.

THEN add relevant links like https://www.herkey.com/jobs.

Rules:

Only answer career-related questions.

If information is missing, guide users to HerKey.

If you don't know, say you don't know — don't make things up.

Start answers directly. Be encouraging and empowering.



    Context: {context}
    Question: {question}

   
    """

    qa_chain = RetrievalQA.from_chain_type(
        llm=load_llm(HUGGINGFACE_REPO_ID),
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={'k': 5}),
        return_source_documents=True,
        chain_type_kwargs={'prompt': set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
    )

    return qa_chain

# For testing
if __name__ == "__main__":
    qa_chain = connect_memory()
    user_query = input("Ask Asha about women's career development: ")
    response = qa_chain.invoke({'query': user_query})

    print("\nASHA SAYS:", response["result"])
    print("\nSOURCE DOCUMENTS:")
    for i, doc in enumerate(response["source_documents"]):
        print(f"\nSource {i+1}: {doc.metadata.get('source', 'Unknown')}")
        print(f"Content snippet: {doc.page_content[:150]}...")
