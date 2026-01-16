
## 🧩 Tech Stack

**Backend**

- ⚡ FastAPI  
- 🧠 Sentence Transformers  
- 🔍 FAISS Vector Search  
- 📦 Pandas, NumPy  
- 🧬 Context Engine  
- 🎭 Emotion Detection (DeepFace compatible)  
- 🌍 Geo-location  
- 📈 Behavior Analytics  

**Frontend**

- HTML + CSS + JavaScript  
- Responsive Grid UI  
- Animated Cards  
- Auto-refreshing Dashboard  
- Image-based Content Cards  
- Trending Sidebar  
- Sliding Advertisement Banner  

## 📁 Project Directory Structure
## 🏗 Directory Structure
```text
IIT_ROPAR_PROJECT/
├── app/                      # FastAPI Web Server & UI Logic
│   ├── static/               # Frontend Assets (JS/CSS)
│   ├── templates/            # HTML Dashboards
│   ├── main.py               # API Entry Point
│   └── recommender.py        # Core Orchestration Logic
├── backend/                  # Data Loading & Processing
│   ├── loaders/              # Domain-specific data loaders
│   └── preprocessing/        # Data cleaning & transformation
├── context/                  # Real-time Contextual Intelligence
│   ├── detectors/            # CV & Logic based state detectors
│   ├── rules/                # Business logic for context scoring
│   ├── context_manager.py    # State aggregator
│   └── scoring.py            # Re-ranking algorithms
├── data/                     # Raw & Cleaned Datasets
├── embeddings/               # Precomputed Vector Embeddings (NPY)
├── index/                    # FAISS / Retrieval Indices (PKL)
├── llm/                      # Semantic Intelligence Layer
│   ├── retrieval/            # Vector Search implementation
│   ├── intent_parser.py      # Query understanding
│   └── generate_embeddings.py # Embedding pipeline
└── README.md
## 🧠 Core Components

### 1️⃣ SmartRecommender Engine

```python
class SmartRecommender:
    - Loads embedding model
    - Loads FAISS retrievers
    - Loads datasets
    - Pulls live context
    - Performs semantic search
    - Applies context-aware scoring
    - Returns ranked recommendations
2️⃣ Context Engine
Located in context/

DetectorRoleEmotionDetectorWebcam emotion recognitionTimeDetectorMorning / Afternoon / EveningLocationDetectorGeo contextScrollDetectorFast / Slow readingFeedbackDetectorUser preferences
Context is unified via:
PythonContextManager.get_live_context()
3️⃣ Semantic Retrieval Engine
Each domain has:

FAISS vector index
Precomputed embeddings
Metadata lookup

textQuery → Embedding → FAISS Search → Candidate Content
4️⃣ Contextual Scoring Engine
Each result is re-ranked using rules like:

If user is 😄 happy → boost comedy movies
If morning → boost news
If scrolling fast → short content
If negative feedback → reduce similar items

Implemented in: context/scoring.py
🎛 API Endpoints

EndpointPurpose/Dashboard UI/contextLive context/recommend?query=...&domain=...Search/random?domain=...Discover/trendingTrending content/healthSystem status
🖥 Frontend Dashboard Features

✔ Live emotion tracking
✔ Auto-refresh recommendations
✔ Animated content cards
✔ Image-based UI
✔ Trending sidebar
✔ Discovery sections
✔ Search by domain
✔ Sliding advertisement bar

⚙ Setup Instructions

Create Environment

Bashconda create -n recsys python=3.10
conda activate recsys

Install Dependencies

Bashpip install fastapi uvicorn pandas numpy sentence-transformers faiss-cpu opencv-python deepface

Generate Embeddings

Bashpython llm/generate_embeddings.py

Build Index

Bashpython llm/retrieval/index_builder.py

Run Server

Bashuvicorn app.main:app --reload
Open:
http://127.0.0.1:8000
🚀 How the System Works (Execution Flow)

User opens dashboard
Context engine starts detectors
Emotion, time, location detected
Auto-trigger recommendations
Query embedded using transformer
FAISS retrieves candidates
Context scoring ranks results
UI renders animated cards
System refreshes every few seconds

🧪 Example Use Cases

Morning commute → News + short reads
Happy mood → Comedy movies
Late night → Thrillers
Fast scrolling → Short articles
Repeated dislikes → Adaptive filtering
Location → Regional trends

🏆 Key Highlights

✅ Real-time emotion-aware AI
✅ Multi-domain recommendation
✅ Context-aware ranking
✅ Live adaptive dashboard
✅ Production-grade architecture
✅ Recruiter-grade system design
✅ Research-ready extensibility

🔮 Future Enhancements

🎙 Voice input
🤖 Chatbot assistant
📱 Mobile app
🧠 Reinforcement learning
🔐 User authentication
📊 Analytics dashboard
🕶 AR/VR recommendation
🎮 Gamified discovery

🧑‍💻 Author
Dipshikha Chakraborty
AI Systems Engineer | ML | LLM | Recommender Systems
IIT Ropar Project
