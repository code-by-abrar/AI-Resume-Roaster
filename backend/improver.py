"""
improver.py
-----------
LangChain + Groq se resume improve karne ka module.
Improved resume JSON return karta hai jo frontend mein live edit ho sakta hai.
"""

import os
import json
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from backend.prompts import IMPROVE_PROMPT
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable set nahi hai!")
    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.4,   # Lower temp for consistent structured output
        max_tokens=3000,
    )


def improve_resume(resume_text: str, job_role: str) -> dict:
    """
    Resume text le ke improved structured resume JSON return karo.

    Args:
        resume_text: Original resume ka plain text
        job_role: Target job role

    Returns:
        dict: Structured improved resume data
    """
    if not resume_text or len(resume_text.strip()) < 50:
        raise ValueError("Resume text bahut chhota hai ya empty hai.")

    if not job_role or not job_role.strip():
        job_role = "Software Engineer"

    llm = get_llm()
    chain = LLMChain(llm=llm, prompt=IMPROVE_PROMPT)

    try:
        raw = chain.run(
            resume_text=resume_text[:4000],
            job_role=job_role.strip()
        ).strip()

        # Extract JSON properly from markdown blocks
        import re
        from json_repair import repair_json
        match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw, re.DOTALL)
        if match:
            raw = match.group(1).strip()
        else:
            # Fallback for when there are no markdown blocks but there might be pre/post text
            match = re.search(r'(\{.*?\})', raw, re.DOTALL)
            if match:
                raw = match.group(1).strip()

        # result = json.loads(raw)
        result = repair_json(raw, return_objects=True)
        if hasattr(result, "get") and result.get("name") is not None:
            return result
        else:
            raise ValueError("LLM JSON payload is not an object.")

    except json.JSONDecodeError as e:
        raise ValueError(f"LLM ne valid JSON nahi diya: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Resume improvement failed: {str(e)}")
