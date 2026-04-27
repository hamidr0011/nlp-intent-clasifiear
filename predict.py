import joblib
import os

MODEL_FILE = "model.pkl"

def predict_intent(text, model):
    prediction = model.predict([text])[0]
    return prediction

def main():
    if not os.path.exists(MODEL_FILE):
        print(f"Model file '{MODEL_FILE}' not found. Please run train.py first.")
        return

    print("Loading model...")
    model = joblib.load(MODEL_FILE)
    print("Model loaded! Type a command to test intent classification (or 'q' to quit).")
    print("-" * 50)

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ('q', 'quit', 'exit'):
                break
            if not user_input:
                continue

            intent = predict_intent(user_input, model)
            print(f"Intent: {intent}")
            
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba([user_input])[0]
                max_prob = max(probs)
                print(f"Confidence: {max_prob:.2f}")
            print("-" * 30)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
