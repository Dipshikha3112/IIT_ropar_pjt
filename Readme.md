
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
IIT_ROPAR_PROJECT/
│
├── __pycache__/
├── .vscode/
│
├── app/
│   ├── __pycache__/
│   ├── static/
│   │   ├── app.js
│   │   └── style.css
│   ├── templates/
│   │   └── ui.html
│   ├── main.py
│   ├── recommender.py
│   └── schemas.py
│
├── backend/
│   ├── loaders/
│   │   ├── __init__.py
│   │   ├── load_amazon.py
│   │   ├── load_movie.py
│   │   └── load_news.py
│   │
│   └── preprocessing/
│       ├── processed/
│       ├── preprocess_amazon.py
│       ├── preprocess_movie.py
│       └── preprocess_news.py
│
├── context/
│   ├── __pycache__/
│   ├── detectors/
│   │   ├── __pycache__/
│   │   ├── emotion_detector.py
│   │   ├── feedback_detector.py
│   │   ├── location_detector.py
│   │   ├── scroll_detector.py
│   │   └── time_detector.py
│   │
│   ├── rules/
│   │   ├── __pycache__/
│   │   ├── emotion_rules.py
│   │   ├── location_rules.py
│   │   ├── scroll_rules.py
│   │   └── time_rules.py
│   │
│   ├── context_manager.py
│   └── scoring.py
│
├── data/
│   ├── cleaned/
│   │   ├── movies_cleaned.csv
│   │   ├── news_cleaned.csv
│   │   └── products_cleaned.csv
│   │
│   ├── e_commerce_data/
│   │   ├── amazon_review_polarity.csv.tgz
│   │   ├── train.csv
│   │   └── test.csv
│   │
│   ├── movie_data/
│   │   ├── allbut.pl
│   │   ├── mku.sh
│   │   ├── README
│   │   ├── u.data
│   │   ├── u.genre
│   │   ├── u.info
│   │   ├── u.item
│   │   ├── u.occupation
│   │   ├── u.user
│   │   ├── u1.base
│   │   ├── u1.test
│   │   ├── u2.base
│   │   ├── u2.test
│   │   ├── u3.base
│   │   ├── u3.test
│   │   ├── u4.base
│   │   ├── u4.test
│   │   ├── u5.base
│   │   ├── u5.test
│   │   ├── ua.base
│   │   ├── ua.test
│   │   ├── ub.base
│   │   └── ub.test
│   │
│   ├── news/
│   │   └── news_data.csv
│   │
│   └── docs/
│       ├── context_rules.md
│       ├── dataset_inventory.md
│       ├── loaders.md
│       ├── model_choices.md
│       ├── preprocessing.md
│       ├── retrieval.md
│       └── scoring.md
│
├── embeddings/
│   ├── movies_embeddings.npy
│   ├── movies_id2index.npy
│   ├── movies_index.csv
│   ├── news_embeddings.npy
│   ├── news_id2index.npy
│   ├── news_index.csv
│   ├── products_embeddings.npy
│   ├── products_id2index.npy
│   └── products_index.csv
│
├── index/
│   ├── movies_index.pkl
│   ├── news_index.pkl
│   └── products_index.pkl
│
├── llm/
│   ├── __pycache__/
│   ├── intent_parser.py
│   ├── intent_schema.py
│   ├── llm_client.py
│   ├── prompt_templates.py
│   ├── query_parser.py
│   │
│   ├── retrieval/
│   │   ├── __pycache__/
│   │   ├── index_builder.py
│   │   ├── movies_retriever.py
│   │   ├── news_retriever.py
│   │   ├── products_retriever.py
│   │   └── retriever.py
│   │
│   ├── build_id2.py
│   ├── embed_utils.py
│   ├── generate_embeddings.py
│   └── Readme.md
│
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