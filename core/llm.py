from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace, HuggingFaceEmbeddings

DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def load_chat_model(hf_token: str, model_id: str = DEFAULT_MODEL) -> ChatHuggingFace:
    llm_endpoint = HuggingFaceEndpoint(
        repo_id=model_id,
        huggingfacehub_api_token=hf_token,
        max_new_tokens=700,
        temperature=0.3,
    )
    return ChatHuggingFace(llm=llm_endpoint)


def load_embeddings(model_name: str = EMBEDDING_MODEL) -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=model_name)
