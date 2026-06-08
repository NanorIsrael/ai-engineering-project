# ai-engineering-project
This project includes designing, building and evaluating a Retrieval-Augmented Generation (RAG) LLM-based application that answers user questions about a corpus of company policies & procedures. Deployed on Render with a basic CI/CD pipeline using GitHub Actions that triggers deployment on push when the app builds successfully

## setup
1. run $ pip install -r requirements.txt
2. create and copy the content of the example-env into a .env file and provide your open router key.


## Run
run $ python app.py




## Design Justification
This RAG setup is designed for production-ready document Q&A with a focus on efficiency, accuracy, and simplicity. The combination creates a balanced system that works well without excessive computational overhead.

Why sentence-transformers/all-MiniLM-L6-v2 model?

- Production economics: 22.7MB means faster deployment, lower memory usage, and cheaper scaling

- CPU-only inference: Unlike OpenAI's text-embedding-3-small (requires API calls) or larger models requiring GPUs, this runs anywhere

- Sufficient for most documents: For policy documents, technical manuals, and FAQ-style content, 384 dimensions capture semantic meaning effectively

- Industry standard: This is the most downloaded embedding model on Hugging Face for RAG (over 20M downloads)

Why 1000 characters (not 500 or 2000)?

text
Research-backed rationale:
- Too small (500 chars): Loses context, misses cross-chunk references
- Too large (2000 chars): Dilutes semantic meaning, slower retrieval
- 1000 chars: Sweet spot for most enterprise documents

Why 100 character overlap (10%)?

- Prevents information loss at chunk boundaries

Example: "The policy applies to... [chunk ends] ...all employees" → Without overlap, "all employees" might be lost

- 10% is standard across production RAG systems (LangChain default, LlamaIndex recommendation)

Prompt format
-	Clear separation of context, instructions, and question (proven to improve adherence)

- Explicit boundaries: Prevents prompt injection and context mixing

- Sourced answers: Encourages citation, critical for policy documents


ChromaDB persistence (cost-effective, production-ready)