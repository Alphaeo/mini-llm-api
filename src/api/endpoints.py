from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..core.llm import LLMWrapper
from ..types.schemas import ChatRequest, ChatResponse
import logging

router = APIRouter()
llm_wrapper = LLMWrapper()

logger = logging.getLogger("mini-llm-api")

@router.get("/health")
async def health_check():
    return {"status": "healthy"}

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")
    try:
        logger.info(f"Chat request: len={len(request.prompt)}, temp={request.temperature}, max_tokens={request.max_tokens}")
        response_text = llm_wrapper.generate_text(
            request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    def token_stream():
        # Utilise la méthode stream_text pour le streaming mot par mot
        for word in llm_wrapper.stream_text(
            request.prompt,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        ):
            yield word

    logger.info(f"Chat stream request: len={len(request.prompt)}, temp={request.temperature}, max_tokens={request.max_tokens}")
    return StreamingResponse(token_stream(), media_type="text/plain")