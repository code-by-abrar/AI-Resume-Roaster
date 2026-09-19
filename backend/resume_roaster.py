# """
# roaster.py
# ----------
# LangChain + Groq API ke saath resume roasting logic.
# """

# import os
# import json
# from langchain_groq import ChatGroq
# from langchain.chains import LLMChain
# from backend.prompts import ROAST_PROMPT
# from dotenv import load_dotenv

# load_dotenv()


# def get_llm():
#     """Groq LLM instance banao with Llama 3."""
#     api_key = os.getenv("GROQ_API_KEY")
#     if not api_key:
#         raise ValueError("GROQ_API_KEY environment variable set nahi hai!")

#     return ChatGroq(
#         groq_api_key=api_key,
#         model_name="llama-3.3-70b-versatile",  # Llama 3 70B — best quality
#         temperature=0.7,               # Thoda creative roasting ke liye
#         max_tokens=2048,
#     )


# def roast_resume(resume_text: str, job_role: str) -> dict:
#     """
#     Resume text aur job role le ke brutal analysis return karo.
    
#     Args:
#         resume_text: Parsed resume ka plain text
#         job_role: Target job role (e.g. "Software Engineer", "Data Scientist")
    
#     Returns:
#         dict: Structured roast analysis
#     """
#     if not resume_text or len(resume_text.strip()) < 50:
#         raise ValueError("Resume text bahut chhota hai ya empty hai.")

#     if not job_role or not job_role.strip():
#         job_role = "Software Engineer"  # Default role

#     llm = get_llm()
#     chain = LLMChain(llm=llm, prompt=ROAST_PROMPT)

#     try:
#         raw_response = chain.run(
#             resume_text=resume_text[:4000],  # Token limit ke andar raho
#             job_role=job_role.strip()
#         )

#         # JSON parse karo
#         from json_repair import repair_json
#         raw_response = raw_response.strip()
#         # Agar koi markdown wrapping ho toh remove karo
#         import re
#         match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', raw_response, re.DOTALL)
#         if match:
#             raw_response = match.group(1).strip()
#         else:
#             match = re.search(r'(\{.*?\})', raw_response, re.DOTALL)
#             if match:
#                 raw_response = match.group(1).strip()

#         result = repair_json(raw_response, return_objects=True)
#         if hasattr(result, "get") and result.get("overall_score") is not None:
#              return result
#         else:
#              raise ValueError("LLM ne valid JSON object nahi diya.")

#     except json.JSONDecodeError as e:
#         raise ValueError(f"LLM ne valid JSON nahi diya: {str(e)}\nResponse: {raw_response[:200]}")
#     except Exception as e:
#         raise RuntimeError(f"Roasting failed: {str(e)}")




"""
roaster.py
----------
LangChain + Groq API ke saath resume roasting logic.
"""

import os
import json
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from backend.prompts import ROAST_PROMPT
from dotenv import load_dotenv

load_dotenv()

# Default fallback structure agar koi field missing ho
SECTION_KEYS = ["contact_info", "summary", "experience", "skills", "education", "formatting"]

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable set nahi hai!")
    return ChatGroq(
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=2500,
    )


def sanitize_result(result: dict) -> dict:
    """
    LLM response ko sanitize karo — missing fields fill karo
    taake frontend crash na kare.
    """
    # Ensure top-level fields
    result.setdefault("overall_score", 0)
    result.setdefault("verdict", "Analysis incomplete.")
    result.setdefault("roast", "Could not fully analyze this resume.")
    result.setdefault("top_3_fixes", ["Re-upload a clearer resume for full analysis."])
    result.setdefault("hire_decision", "MAYBE")
    result.setdefault("hire_reason", "Incomplete analysis.")

    # Ensure sections dict exists
    if "sections" not in result or not isinstance(result["sections"], dict):
        result["sections"] = {}

    # Ensure every section key exists with score + issue + fix
    for key in SECTION_KEYS:
        sec = result["sections"].get(key)
        if not isinstance(sec, dict):
            result["sections"][key] = {
                "score": 0,
                "issue": "Could not analyze this section.",
                "fix": "Re-upload a clearer PDF for full breakdown."
            }
        else:
            # Make sure score is an integer
            raw_score = sec.get("score", 0)
            try:
                sec["score"] = int(raw_score)
            except (ValueError, TypeError):
                sec["score"] = 0
            sec.setdefault("issue", "No issue detected.")
            sec.setdefault("fix", "No fix needed.")

    # Ensure ATS block
    if "ats_compatibility" not in result or not isinstance(result["ats_compatibility"], dict):
        result["ats_compatibility"] = {
            "score": 0,
            "issues": ["Could not run ATS check."],
            "verdict": "ATS analysis unavailable."
        }
    else:
        ats = result["ats_compatibility"]
        try:
            ats["score"] = int(ats.get("score", 0))
        except (ValueError, TypeError):
            ats["score"] = 0
        ats.setdefault("issues", [])
        ats.setdefault("verdict", "")

    # overall_score as int
    try:
        result["overall_score"] = int(result["overall_score"])
    except (ValueError, TypeError):
        result["overall_score"] = 0

    return result


def roast_resume(resume_text: str, job_role: str) -> dict:
    """
    Resume text aur job role le ke brutal analysis return karo.
    """
    if not resume_text or len(resume_text.strip()) < 50:
        raise ValueError("Resume text bahut chhota hai ya empty hai.")

    job_role = (job_role or "Software Engineer").strip()

    llm = get_llm()
    chain = LLMChain(llm=llm, prompt=ROAST_PROMPT)

    try:
        raw = chain.run(
            resume_text=resume_text[:4000],
            job_role=job_role
        ).strip()

        # Strip markdown fences if present
        if raw.startswith("```"):
            lines = raw.split("\n")
            # Remove first and last fence lines
            raw = "\n".join(lines[1:-1]).strip()

        # Try to extract JSON if there's extra text
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            raw = raw[start:end]

        result = json.loads(raw)
        return sanitize_result(result)

    except json.JSONDecodeError as e:
        # Return a safe fallback with error info
        fallback = {
            "overall_score": 0,
            "verdict": "Analysis failed — JSON parse error.",
            "roast": f"The AI had trouble parsing your resume. Try uploading a cleaner PDF. Error: {str(e)[:100]}",
            "sections": {},
            "ats_compatibility": {"score": 0, "issues": ["Parse error"], "verdict": "N/A"},
            "top_3_fixes": ["Upload a cleaner, text-based PDF."],
            "hire_decision": "MAYBE",
            "hire_reason": "Analysis incomplete."
        }
        return sanitize_result(fallback)

    except Exception as e:
        raise RuntimeError(f"Roasting failed: {str(e)}")
