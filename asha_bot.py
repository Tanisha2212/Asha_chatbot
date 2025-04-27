import os
import streamlit as st
import json
import time
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
import styles  # Import the styles module

DB_FAISS_PATH = "vectorstore/db_faiss"
ANALYTICS_FILE = "data/analytics.json"

BIAS_KEYWORDS = ["bad women", "inferior", "weak", "should not work", "can't work", "unsuitable for women"]

@st.cache_resource
def get_vectorstore():
    embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/paraphrase-MiniLM-L6-v2')
    db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)
    return db

def set_custom_prompt(custom_prompt_template):
    prompt = PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])
    return prompt

def load_llm(huggingface_repo_id, HF_TOKEN):
    llm = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        model_kwargs={"token": HF_TOKEN,
                      "max_length": "600"}
    )
    return llm

def detect_bias(prompt):
    prompt = prompt.lower()
    return any(keyword in prompt for keyword in BIAS_KEYWORDS)

def load_analytics():
    if not os.path.exists(ANALYTICS_FILE):
        return {"questions": 0, "bias_detected": 0, "feedback_positive": 0, "feedback_negative": 0}
    with open(ANALYTICS_FILE, "r") as f:
        return json.load(f)

def save_analytics(analytics):
    with open(ANALYTICS_FILE, "w") as f:
        json.dump(analytics, f, indent=4)

def create_custom_header():
    st.markdown(styles.HEADER_HTML, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Asha - Women Empowerment Chatbot",
        page_icon="👩‍💼",
        layout="wide"
    )
    
    # Apply the custom CSS
    styles.apply_custom_css()
    
    # Header with logo and title
    create_custom_header()
    
    # Stats Container
    analytics = load_analytics()
    
    # Welcome message
    if 'first_time' not in st.session_state:
        st.session_state.first_time = True
        st.markdown(styles.WELCOME_CARD_HTML, unsafe_allow_html=True)

    # Layout
    col1, col2 = st.columns([3, 1])
    
    with col2:
        # Stats and info sidebar
        st.markdown(styles.SIDEBAR_ABOUT_HTML, unsafe_allow_html=True)
        
        # Analytics display
        st.markdown("<h3 style='color: #89C76F;'>Analytics</h3>", unsafe_allow_html=True)
        metric_col1, metric_col2 = st.columns(2)
        
        with metric_col1:
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-value">{analytics["questions"]}</div>
                <div class="stats-label">Questions Asked</div>
            </div>
            """, unsafe_allow_html=True)
            
        with metric_col2:
            pos_percent = 0 if analytics["feedback_positive"] + analytics["feedback_negative"] == 0 else \
                int((analytics["feedback_positive"] / (analytics["feedback_positive"] + analytics["feedback_negative"])) * 100)
            st.markdown(f"""
            <div class="stats-card">
                <div class="stats-value">{pos_percent}%</div>
                <div class="stats-label">Positive Feedback</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Refresh Button
        st.button("🔄 Refresh Knowledge Base", key="refresh_kb", help="Update Asha's knowledge with the latest information")
    
    with col1:
        # Chat container
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        
        # Initialize chat history
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {'role': 'assistant', 'content': "Hello! I'm Asha, your AI career assistant. How can I help you with your professional journey today?"}
            ]
        if 'history' not in st.session_state:
            st.session_state.history = []

        # Display chat messages
        for message in st.session_state.messages:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="assistant-message">
                    <strong>Asha:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        with st.container():
            prompt = st.chat_input("Ask Asha about career opportunities, mentorship, or professional development...")
            
            if prompt:
                if detect_bias(prompt):
                    st.warning("⚠️ Asha promotes positive and empowering conversations!")
                    analytics["bias_detected"] += 1
                else:
                    st.session_state.messages.append({'role': 'user', 'content': prompt})
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You:</strong> {prompt}
                    </div>
                    """, unsafe_allow_html=True)

                    with st.spinner("Asha is thinking..."):
                        try:
                            # Load vector store
                            vectorstore = get_vectorstore()
                            
                            HF_TOKEN = os.environ.get("HF_TOKEN")
                            HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

                            CUSTOM_PROMPT_TEMPLATE = """
                            You are Asha, an AI chatbot focused on women empowerment and career development.
                            Always start your answer with a short encouraging line like "Let's explore some opportunities!" or "Here's what I found to help you!"

                            Use the context provided to suggest specific job roles, mentorship programs, or events related to women's careers.
                            If detailed information is missing, politely guide the user to visit https://www.herkey.com/jobs for updated listings.

                            Context: {context}
                            Question: {question}

                            Keep your tone supportive, encouraging, and career-focused. 
                            Never invent fake job titles if not found.
                            """

                            qa_chain = RetrievalQA.from_chain_type(
                                llm=load_llm(huggingface_repo_id=HUGGINGFACE_REPO_ID, HF_TOKEN=HF_TOKEN),
                                chain_type="stuff",
                                retriever=vectorstore.as_retriever(search_kwargs={'k': 5}),
                                return_source_documents=True,
                                verbose=False,
                                chain_type_kwargs={'prompt': set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
                            )

                            response = qa_chain.invoke({'query': prompt})
                            result = response["result"]
                            source_documents = response["source_documents"]

                            # Handle empty result fallback
                            if not result.strip():
                                result = "I'm sorry, I couldn't find detailed job listings right now. You can explore [HerKey Jobs](https://www.herkey.com/jobs) directly!"

                            # Format sources
                            sources_text = ""
                            unique_sources = set()
                            for doc in source_documents:
                                source = doc.metadata.get('source', 'Unknown')
                                if source not in unique_sources:
                                    unique_sources.add(source)
                                    sources_text += f"- {source}\n"

                            if sources_text:
                                result_with_sources = f"{result}\n\n<div class='sources'><strong>Sources:</strong><br/>{'<br/>'.join(unique_sources)}</div>"
                            else:
                                result_with_sources = result

                            st.markdown(f"""
                            <div class="assistant-message">
                                <strong>Asha:</strong> {result_with_sources}
                            </div>
                            """, unsafe_allow_html=True)

                            st.session_state.messages.append({'role': 'assistant', 'content': result_with_sources})
                            st.session_state.history.append({"user": prompt, "assistant": result})

                            analytics["questions"] += 1

                            # Feedback section
                            st.markdown("<div style='text-align: center; margin-top: 20px; color: #D0D0D0;'>Was this response helpful?</div>", unsafe_allow_html=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("👍 Yes", key="positive_feedback", help="Mark this response as helpful"):
                                    analytics["feedback_positive"] += 1
                                    st.success("Thank you for your feedback!")
                            with col2:
                                if st.button("👎 No", key="negative_feedback", help="Mark this response as not helpful"):
                                    analytics["feedback_negative"] += 1
                                    st.error("Thanks! We'll work to improve it.")

                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                            error_message = "I'm having trouble connecting to my knowledge base right now. Please try again in a moment."
                            st.markdown(f"""
                            <div class="assistant-message">
                                <strong>Asha:</strong> {error_message}
                            </div>
                            """, unsafe_allow_html=True)
                            st.session_state.messages.append({'role': 'assistant', 'content': error_message})
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Footer
        st.markdown(styles.FOOTER_HTML, unsafe_allow_html=True)
    
    save_analytics(analytics)

if __name__ == "__main__":
    main()