"""
app.py
------
FastAPI REST API — frontend se requests receive karo aur roast return karo.
Run: fastapi dev backend/app.py
"""
# main.py ki top imports mein yeh add karo:

from typing import Annotated
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.resume_parser import parse_resume  # Tumhari custom file
from backend.resume_roaster import roast_resume # Tumhari custom file
import traceback
from backend.improver import improve_resume

app = FastAPI(
    title="Resume Roaster API",
    description="Brutally honest AI resume reviewer.",
    version="1.0.0"
)

# CORS configuration for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production mein isko frontend domain se restrict karna
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    """Server alive check."""
    return {"status": "ok", "message": "Resume Roaster API is running!"}

@app.post("/roast")
async def roast(
    resume: Annotated[UploadFile, File(...)], 
    job_role: Annotated[str, Form()] = "Software Engineer"
):
    """
    Main endpoint.
    Expects:
      - resume: PDF file
      - job_role: string (optional, defaults to Software Engineer)
    """
    try:
        # File extension validation
        if not resume.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Sirf PDF files allowed hain!")

        # Step 1: Read PDF into bytes
        pdf_bytes = await resume.read()
        
        # Step 2: Parse text (Tumhara custom function)
        try:
            resume_text = parse_resume(pdf_bytes)
        except Exception as e:
             raise HTTPException(status_code=422, detail=f"PDF parsing failed: {str(e)}")

        # Step 3: Roast it (Tumhara custom AI function)
        result = roast_resume(resume_text, job_role)

        return {
            "success": True,
            "job_role": job_role,
            "result": result
        }

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")





# @app.route("/improve", methods=["POST"])
# def improve():
#     """PDF upload karke AI-improved resume JSON lo."""
#     try:
#         if "resume" not in request.files:
#             return jsonify({"error": "Resume PDF upload karo!"}), 400

#         pdf_file = request.files["resume"]
#         if pdf_file.filename == "":
#             return jsonify({"error": "Koi file select nahi ki!"}), 400
#         if not pdf_file.filename.lower().endswith(".pdf"):
#             return jsonify({"error": "Sirf PDF files allowed hain!"}), 400

#         job_role = request.form.get("job_role", "Software Engineer").strip() or "Software Engineer"

#         pdf_bytes = pdf_file.read()
#         resume_text = parse_resume(pdf_bytes)
#         result = improve_resume(resume_text, job_role)

#         return jsonify({"success": True, "job_role": job_role, "resume": result})

#     except ValueError as e:
#         return jsonify({"error": str(e)}), 422
#     except RuntimeError as e:
#         return jsonify({"error": str(e)}), 500
#     except Exception as e:
#         traceback.print_exc()
#         return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.post("/improve")
async def improve(
    resume: UploadFile = File(...),
    job_role: str = Form("Software Engineer")
):
    try:
        # File extension validation
        if not resume.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Strictly PDF files allowed!")

        # Async read from memory
        pdf_bytes = await resume.read()
        
        # Text extraction via existing parser
        try:
            resume_text = parse_resume(pdf_bytes)
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Text extraction failed: {str(e)}")

        # AI Agent function call (Must return a dictionary/JSON)
        result = improve_resume(resume_text, job_role)

        # FastAPI auto-converts Python dictionaries to JSON
        return {
            "success": True, 
            "job_role": job_role, 
            "resume": result
        }

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")