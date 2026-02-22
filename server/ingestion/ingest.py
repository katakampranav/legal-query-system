import os
import re
from dotenv import load_dotenv
import time

# LlamaIndex core
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.settings import Settings
from llama_index.core.schema import Document
from pypdf import PdfReader

# Cohere embeddings
from llama_index.embeddings.cohere import CohereEmbedding

# Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

# Load environment variables
load_dotenv()

# ---- Cohere Rate Limit Fix ----
class ThrottledCohereEmbedding(CohereEmbedding):
    def _get_text_embeddings(self, texts):
        embeddings = super()._get_text_embeddings(texts)
        time.sleep(2)
        return embeddings

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("INDEX_NAME")

# ---------------------------
# 1️⃣ Setup embedding model
# ---------------------------
Settings.embed_model = ThrottledCohereEmbedding(
    api_key=COHERE_API_KEY,
    model_name="embed-english-v3.0",
    embed_batch_size=5
)

# ---------------------------
# 2️⃣ Smart chunking (VERY IMPORTANT FOR LAW)
# ---------------------------
Settings.node_parser = SentenceSplitter(
    chunk_size=1500,
    chunk_overlap=200
)

# ---------------------------
# 3️⃣ Connect Pinecone
# ---------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

# create index if not exists
if INDEX_NAME not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=INDEX_NAME,
        dimension=1024,  # Cohere embedding dimension
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

pinecone_index = pc.Index(INDEX_NAME)

vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

storage_context = StorageContext.from_defaults(vector_store=vector_store)

# ---------------------------
# 4️⃣ Read PDF and split by legal sections
# ---------------------------

def load_bns_sections(pdf_path):
    reader = PdfReader(pdf_path)
    full_text = ""

    # combine all pages
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += "\n" + text

    # split using section pattern like "318. Cheating"
    pattern = r"\n\s*(\d{2,4})\.\s+([A-Za-z ,\-()]+)"
    splits = re.split(pattern, full_text)

    documents = []

    # reassemble sections
    for i in range(1, len(splits), 3):
        section_number = splits[i]
        section_title = splits[i+1]
        section_text = splits[i+2]

        content = f"Section {section_number}: {section_title}\n{section_text}"

        documents.append(
            Document(
                text=content,
                metadata={
                    "section": section_number,
                    "offence": section_title.strip(),
                    "act": "BNS"
                }
            )
        )

    return documents

documents = load_bns_sections("data/bharatiya nyaya sanhita.pdf")

print(f"Loaded {len(documents)} legal sections")

# ---------------------------
# 5️⃣ Create Index (THE MAGIC LINE)
# ---------------------------
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    show_progress=True
)

print("✅ IPC/BNS successfully ingested into Pinecone!")