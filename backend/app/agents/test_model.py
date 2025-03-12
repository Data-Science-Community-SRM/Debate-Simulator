import os
from llama_cpp import Llama
import logging

#logging for debug
logging.basicConfig(level=logging.INFO)
model_path = r"C:\Users\kumar\OneDrive\Documents\debate-sim\backend\models\mistral-7b-v0.1.Q4_K_M.gguf"

def test_model():
    logging.info(f"Model file found. Size: {os.path.getsize(model_path) / (1024*1024):.2f} MB")

    try:
        logging.info("Initializing Llama model...")
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=4,
            verbose=True
        )
        logging.info("Model initialized successfully")
        prompt = "Explain the benefits of artificial intelligence in one sentence."
        logging.info(f"Sending prompt: {prompt}")

        #generate
        output = llm(prompt, max_tokens=50, echo=False)
        
        logging.info("Raw output:")
        logging.info(output)

        if output and 'choices' in output and output['choices']:
            response = output['choices'][0]['text'].strip()
            logging.info(f"Generated response: {response}")
        else:
            logging.error("No valid response generated")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", exc_info=True)

if __name__ == "__main__":
    test_model()
