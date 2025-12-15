import nltk
import os
import sys

def setup_and_run():
    print("Checking NLTK data...")
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        print("NLTK data downloaded/verified.")
    except Exception as e:
        print(f"Warning: Could not download NLTK data: {e}")

    print("Starting Flask app...")
    try:
        # Import app to verify dependencies
        from app import app
        # Run the app
        app.run(debug=True, use_reloader=False, port=5000)
    except ImportError as e:
        print(f"Error importing app: {e}")
    except Exception as e:
        print(f"Error running app: {e}")

if __name__ == "__main__":
    setup_and_run()
