<p align="center">
<a href="https://dscommunity.in">
	<img src="https://raw.githubusercontent.com/Data-Science-Community-SRM/Debate-Simulator/main/static/images/header.png" width=80%/>
</a>
	<h2 align="center"> AI Debate Simulator </h2>
	<h4 align="center"> A real-time AI-powered debate simulator using FastAPI, LangGraph, and local LLMs. <h4>
</p>

---
[![Documentation](https://img.shields.io/badge/Documentation-See%20Docs-green?style=flat-square&logo=readthedocs)](https://example.com/ai-debate-simulator/docs)
[![UI Demo](https://img.shields.io/badge/User%20Interface-Live%20Demo-orange?style=flat-square&logo=appveyor)](https://example.com/ai-debate-simulator/demo)

## Preview
- The AI Debate Simulator is a dynamic application that pits an AI proponent against an AI opponent in structured debates. Real-time updates keep users engaged, while a streamlined user interface makes it easy to explore a variety of debate topics.
<p align="center">
    <img src="https://raw.githubusercontent.com/Data-Science-Community-SRM/Debate-Simulator/main/static/images/simulator.png" width=60%/>
</p>

## Functionalities

- [x]  Real-time argument generation by AI agents.
- [x]  Turn-based debate flow managed by LangGraph.
- [x]  Utilizes **WebSockets** for seamless, real-time communication between the backend and frontend.
- [x] Employs a cloud-based model, **GPT-3.5-turbo**, for the proponent.
- [x] Leverages a local LLM, **Mistral-7B-v0.1**, for the opponent.
- [x] Arguments are generated with both cloud-based and local LLMs, managed for optimal performance.
- [x] Interactive UI with round indicators and progress tracking.
<br>

## Instructions to Run

* Pre-requisites:
    - Python 3.9+
    - Conda or venv set up for virtual environment management.
    - CUDA-enabled GPU (for optimal local LLM performance).
    - **Mistral-7B-v0.1 GGUF model**: You can download the quantized model file (e.g., `mistral-7b-v0.1.Q4_K_M.gguf`) from [TheBloke's Hugging Face repository](https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF). Place the downloaded file in the `backend/models/` directory.

* Installation:
    - Clone the repository:

    ```
    git clone https://github.com/Data-Science-Community-SRM/Debate-Simulator.git
    cd Debate-Simulator
    ```

    - Create a virtual environment:

    ```
    conda create -n debate-sim python=3.9
    conda activate debate-sim
    ```

    - Install the required packages:

    ```
    pip install -r requirements.txt
    ```

* Execution:
    - Configure the environment variables:

    ```
    cp .env.example .env
    # Edit .env with your actual OPENAI_API_KEY and SERPAPI_KEY
    ```

    - Run the FastAPI backend:

    ```
    cd backend
    uvicorn app.main:app --reload --port 8000
    ```

    - Run the Flask frontend:

    ```
    cd flask_frontend
    flask run --port 5000
    ```
### Storage
   - We have used chrome DB with sqlite3
## Contributors

<table>
  <tr align="center">
    <td>
      <a href="github.com/adityaxdubey">
        <img src="[https://avatars.githubusercontent.com/u/0000000?v=4](https://media.licdn.com/dms/image/v2/D5603AQGVhbZVk4NksQ/profile-displayphoto-shrink_400_400/B56ZQluq8IGQAg-/0/1735799780169?e=1747267200&v=beta&t=gmEZLLhj4vUvhfyczebXd_S1DJ6mrPl5NDfLMx2sQH4)" height="120" alt="Aditya Dubey"/>
      </a>
      <p align="center">
        <a href="https://github.com/your-github-username-1">
          <img src="http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height="36"/>
        </a>
        <a href="https://www.linkedin.com/in/your-linkedin-profile-1">
          <img src="http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
        </a>
      </p>
    </td>
    <td>
      <a href="https://github.com/your-github-username-2">
        <img src="https://avatars.githubusercontent.com/u/0000000?v=4" height="120" alt="Your Name Here"/>
      </a>
      <p align="center">
        <a href="https://github.com/your-github-username-2">
          <img src="http://www.iconninja.com/files/241/825/211/round-collaboration-social-github-code-circle-network-icon.svg" width="36" height="36"/>
        </a>
        <a href="https://www.linkedin.com/in/your-linkedin-profile-2">
          <img src="http://www.iconninja.com/files/863/607/751/network-linkedin-social-connection-circular-circle-media-icon.svg" width="36" height="36"/>
        </a>
      </p>
    </td>
  </tr>
</table>

## License
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

<p align="center">
    Made with :heart: by <a href="https://dscommunity.in">DS Community SRM</a>
</p>
