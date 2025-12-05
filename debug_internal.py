import sys
import os
sys.path.append(os.getcwd())
from src.core.detector import WatermarkDetector

def analyze(path):
    print(f"Scanning: {path}")
    detector = WatermarkDetector()
    results = detector.scan_pdf(path)
    print("Results:", results)

if __name__ == "__main__":
    analyze(r"d:\Work projects\Other\WaterMarkRemover\cleaned_302 schedule Modified.pdf")
