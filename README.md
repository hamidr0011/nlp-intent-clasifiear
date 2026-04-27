# Intelligent Intent Classifier

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-latest-orange.svg)](https://scikit-learn.org/)
[![Dataset: MASSIVE](https://img.shields.io/badge/Dataset-Amazon%20MASSIVE-green.svg)](https://huggingface.co/datasets/AmazonScience/massive)
[![NLU](https://img.shields.io/badge/NLU-Intent%20Classification-blueviolet.svg)](#)

A offline-first Natural Language Understanding (NLU) engine designed for high-precision intent classification. This system leverages the **Amazon MASSIVE dataset** (1M+ utterances) and a optimized Scikit-Learn pipeline to provide millisecond-latency predictions for 60 distinct intent types.

---

## Key Features

- **Industrial-Grade Data**: Trained on the English partition of the **Amazon MASSIVE** dataset, covering 18 domains (IoT, Social, Transport, etc.).
- **60 Distinct Intents**: Understands a wide range of commands, from `iot_hue_lighton` to `weather_query` and `qa_currency`.
- **Low Latency**: Optimized Logistic Regression pipeline ensures near-instant classification on standard consumer hardware.
- **Privacy Centric**: 100% offline execution. No data ever leaves your machine.
- **Automated Workflow**: Includes a one-click training and deployment script for seamless setup.

---

## Technology Stack

- **Core Engine**: Python 3.x
- **Machine Learning**: Scikit-Learn (Logistic Regression, TF-IDF Vectorization)
- **Data Handling**: Pandas, PyArrow (Parquet support)
- **Web API Backend**: Flask, Flask-CORS
- **Web UI Frontend**: React 18, Vite, Tailwind CSS (Bauhaus Design System)

---

## Project Structure

```text
.
├── train.py               # Data ingestion, preprocessing, and model training
├── predict.py             # CLI interface for real-time intent classification
├── api.py                 # Flask REST API backend serving the model
├── frontend/              # React + Vite frontend Web UI application
├── run_classifier.bat     # Automation script (Check -> Train -> Run CLI)
├── requirements.txt       # Project dependencies
├── model.pkl              # Serialized trained model (generated after training)
└── README.md              # Project documentation
```

---

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hamidr0011/nlp-intent-clasifiear.git
   cd nlp-intent-clasifiear
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Train the Model**:
   If `model.pkl` doesn't exist yet, run the training script or batch file:
   ```bash
   python train.py
   # OR
   run_classifier.bat
   ```

4. **Install Frontend dependencies**:
   ```bash
   cd frontend
   npm install
   ```

---

## Usage

### Interactive Web UI (Recommended)

To run the full Bauhaus Web Interface:

1. **Start the Backend API** (in the root directory):
   ```bash
   python api.py
   ```
   *Runs on `http://127.0.0.1:5000`*

2. **Start the Frontend UI** (in a new terminal):
   ```bash
   cd frontend
   npm run dev
   ```
   *Runs on `http://localhost:5173`*

### Interactive CLI Prediction
Run the prediction interface directly in the terminal:
```bash
python predict.py
```
**Example Interaction:**
```text
You: "What is the weather like today?"
Intent: weather_query
Confidence: 0.98
```

### Manual Training
To retrain the model with the latest dataset partition:
```bash
python train.py
```

---

## Model Architecture

The classifier uses a **Multi-class Logistic Regression** model within a Scikit-Learn Pipeline:
1. **CountVectorizer**: Captures Unigrams and Bigrams (`ngram_range=(1, 2)`) to understand both individual words and short phrases.
2. **TfidfTransformer**: Weights word importance based on inverse document frequency.
3. **Logistic Regression**: A robust linear classifier optimized with `max_iter=5000` to ensure convergence on complex, multi-label datasets.

**Performance**: Achieves **~79.5% Accuracy** across 60 classes on the Amazon MASSIVE test set.

---

## Future Roadmap

- [x] **Web API**: Wrap the model in a FastAPI or Flask microservice.
- [x] **GUI**: Develop a modern React/Vite dashboard for interaction using Bauhaus design.
- [ ] **Advanced NLP**: Implement BERT/DistilBERT for deeper contextual understanding.
- [ ] **Multilingual support**: Extend training to Spanish, French, and other MASSIVE partitions.

---

## License

This project is open-source and available under the MIT License.
