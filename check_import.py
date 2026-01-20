# check_import.py
try:
    from langchain.chains.question_answering import load_qa_chain
    print("✅ SUCCESS: 'langchain.chains' is found!")
except ImportError as e:
    print(f"❌ ERROR: Still missing. Details: {e}")
    print("   Run: pip install langchain")