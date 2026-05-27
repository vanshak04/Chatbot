from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import re

import uuid
import pycountry
import phonenumbers

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}
registrations = {}

COUNTRIES = [country.name for country in pycountry.countries]

class ChatInput(BaseModel):
    sessionId: str
    answer: str

def validate_phone(number):

    try:
        parsed = phonenumbers.parse(number, None)

        return phonenumbers.is_valid_number(parsed)

    except:
        return False

def is_valid_email(email):

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern, email)

# ---- FLOW ----
FLOW = {
    "start": {
        "question": "Hi 👋 What are you looking for?",
        "options": [
            "Exams",
            "Programs",
            "Courses",
            "Not sure"
        ]
    },

    # ---------- EXAMS ----------
    "Exams": {
        "question": "Which exam are you targeting?",
        "options": ["Medical", "Pharmacists", "Nurse Licensing", "Dentist"]
    },

    "Medical": {
        "question": "Which medical exam are you looking for?",
        "options": ["FMGE", "DHA-GP", "UKMLA", "GMC","AMC", "MCCQE", "USMLE"]
    },

    "FMGE": {
        "result": "🎯 Recommended:\n• Foreign Medical Graduate Examination (FMGE)?",
        "cta": "https://www.terraleap.com/ForeignMedicalGraduateExamination-FMGE"
    },

    "DHA-GP": {
        "result": "🎯 Recommended:\n• Dubai Health Authority (DHA) General Practitioner (GP) Examination",
        "cta": "https://www.terraleap.com/DHA-GeneralPractitioner-GP"
    },

    "UKMLA": {
        "result": "🎯 Recommended:\n• United Kingdom Medical Licensing Assessment (UKMLA)",
        "cta": "https://www.terraleap.com/UnitedKingdomMedicalLicensingAssessment-UKMLA"
    },
    
    "GMC":{
        "result": "🎯 Recommended:\n• General Medical Council (GMC) Membership Examination",
        "cta": "https://www.terraleap.com/GeneralMedicalCouncil-GMC"
    },
    
    "AMC":{
        "result": "🎯 Recommended:\n• Australian Medical Council (AMC) Examination",
        "cta": "https://www.terraleap.com/AustralianMedicalCouncil-AMC"
    },
    
    "MCCQE":{
        "result": "🎯 Recommended:\n• Medical Council of Canada Qualifying Examination (MCCQE)",
        "cta": "https://www.terraleap.com/MedicalCouncilofCanadaQualifyingExamination-MCCQE"
    },
    
    "USMLE":{
        "result": "🎯 Recommended:\n• United States Medical Licensing Examination (USMLE)",
        "cta": "https://www.terraleap.com/UnitedStatesMedicalLicensingExamination-USMLE"
    },

    # Pharmacists
    "Pharmacists": {
        "question": "Which pharmacists exam are you looking for?",
        "options": ["PEBC-Technician Examination", "DHA", "PLE", "PEBC- Qualifying Examination", "PEBC-Evaluating Examination", "CAOP", "OPRA", "FPGEE", "NAPLEX", "GPAT"]
    },

    "PEBC-Technician Examination": {
        "result": "🎯 Recommended:\n• Pharmacy Examining Board of Canada (PEBC) -Technicians Examination",
        "cta": "https://www.terraleap.com/PharmacyExaminingBoardofCanada-TechniciansExamination"
    },

    "DHA": {
        "result": "🎯 Recommended:\n• Dubai Health Authority (DHA) Pharmacist Examination   ",
        "cta": "https://www.terraleap.com/DHAPharmacistExamination"
    },

    "PLE": {
        "result": "🎯 Recommended:\n• Pharmaceutical Licensing Examination (PLE)",
        "cta": "https://www.terraleap.com/Pharmaceutical-Licensing-Examination-PLE"
    },

    "PEBC- Qualifying Examination": {
        "result": "🎯 Recommended:\n• Pharmacy Examining Board of Canada-Qualifying Examination",
        "cta": "https://www.terraleap.com/PharmacyExaminingBoardofCanadaQualifyingExamination-PEBCQE"
    },
    
    "PEBC-Evaluating Examination": {
        "result": "🎯 Recommended:\n• Pharmacy Examining Board of Canada-Evaluating Examination",
        "cta": "https://www.terraleap.com/PharmacyExaminingBoardofCanadaEvaluatingExamination-PEBCEE"
    },
    
    "CAOP": {
        "result": "🎯 Recommended:\n• The Competency Assessment of Overseas Pharmacists (CAOP)",
        "cta": "https://www.terraleap.com/CompetencyAssessmentofOverseasPharmacistsExam-CAOP"
    },
    
    "OPRA": {
        "result": "🎯 Recommended:\n• Overseas Pharmacist Readiness Assessment (OPRA)",
        "cta": "https://www.terraleap.com/OverseasPharmacistReadinessAssessment-OPRA"
    },
    
    "FPGEE": {
        "result": "🎯 Recommended:\n•  Foreign Pharmacy Graduate Equivalency Examination (FPGEE)",
        "cta": "https://www.terraleap.com/ForeignPharmacyGraduateEquivalencyExamination-FPGEE"
    },
    
    "NAPLEX": {
        "result": "🎯 Recommended:\n• North American Pharmacist Licensure Examination (NAPLEX)",
        "cta": "https://www.terraleap.com/NorthAmericanPharmacistLicensureExamination-NAPLEX"
    },
    
    "GPAT": {
        "result": "🎯 Recommended:\n• Graduate Pharmacy Aptitude Test (GPAT)",
        "cta": "https://www.terraleap.com/GraduatePharmacyAptitudeTest-GPAT"
    },
    
    # Nurse Licensing
    "Nurse Licensing": {
        "question": "Which Nurse Licensing exam are you looking for?",
        "options": ["FNP-ANCC", "FNP-AANP", "NCLEX-PN", "DHA-Nurse Licensing Examination", "NCLEX-RN"]
    },

    "FNP-ANCC": {
        "result": "🎯 Recommended:\n• Family Nurse Practitioner (FNP) Certification Exam - ANCC",
        "cta": "https://www.terraleap.com/"
    },

    "FNP-AANP": {
        "result": "🎯 Recommended:\n• Family Nurse Practitioner (FNP) Certification Exam - AANP",
        "cta": "https://www.terraleap.com/FamilyNursePractitionerCertificationExam-FNP"
    },

    "NCLEX-PN": {
        "result": "🎯 Recommended:\n• National Council Licensure Examination (NCLEX-PN)",
        "cta": "https://www.terraleap.com/NationalCouncilLicensureExamination-NCLEX-PN"
    },

    "DHA-Nurse Licensing Examination": {
        "result": "🎯 Recommended:\n• Dubai Health Authority(DHA) -Nurse Licensing Examination",
        "cta": "https://www.terraleap.com/DubaiHealthAuthority-DHA-NurseLicensingExamination"
    },
    
    "NCLEX-RN": {
        "result": "🎯 Recommended:\n• National Council Licensure Examination (NCLEX-RN)",
        "cta": "https://www.terraleap.com/NationalCouncilLicensureExamination-NCLEX-RN"
    },
    
    # Dentist Exams
    "Dentist": {
        "question": "Which Dentist exam are you looking for?",
        "options": ["NDEB-ACJ", "NDEB-AFK", "SDC", "NDEB-Written Examination", "ADC", "ORE", "INBDE"]
    },

    "NDEB-ACJ": {
        "result": "🎯 Recommended:\n• National Dental Examining Board of Canada (NDEB) -ACJ",
        "cta": "https://www.terraleap.com/NationalDentalExaminingBoardofCanada-NDEB-ACJ-AssessmentofClinicalJudgment"
    },

    "NDEB-AFK": {
        "result": "🎯 Recommended:\n• National Dental Examining Board of Canada (NDEB)-AFK",
        "cta": "https://www.terraleap.com/NationalDentalExaminingBoardofCanada-NDEB-AssesmentofFundamentalKnowledge(AFK)"
    },

    "SDC": {
        "result": "🎯 Recommended:\n• Singapore Dental Council (SDC) Examination",
        "cta": "https://www.terraleap.com/SingaporeDentalCouncil-SDC"
    },

    "NDEB-Written Examination": {
        "result": "🎯 Recommended:\n• National Dental Examining Board of Canada (NDEB) -Written Examination",
        "cta": "https://www.terraleap.com/NationalDentalExaminingBoardofCanada-NDEB-WrittenExamination"
    },
    
    "ADC": {
        "result": "🎯 Recommended:\n• Australian Dental Council (ADC) Examination",
        "cta": "https://www.terraleap.com/AustralianDentalCouncilExamination-ADC"
    },
    
    "ORE": {
        "result": "🎯 Recommended:\n• Overseas Registration Examination (ORE)",
        "cta": "https://www.terraleap.com/OverseasRegistrationExamination-ORE"
    },
    
    "INBDE": {
        "result": "🎯 Recommended:\n• Integrated National Board Dental Examination (INBDE)",
        "cta": "https://www.terraleap.com/IntegratedNationalBoardDentalExamination-INBDE"
    },
    
    # ---------- PROGRAMS ----------
    "Programs": {
        "result": "🎯 Recommended:\n• Medical Programs",
        "cta": "https://www.terraleap.com/medical-programs"
    },

    # ---------- COURSES ----------
    "Courses": {
        "question": "Which courses you looking for to learn?",
        "options": [
            "Medical Courses", 
            "IPC"
        ]
    },

    "Medical Courses": {
        "result": "📘 Recommended:\nMedical Courses",
        "cta": "https://www.terraleap.com/medical-courses"
    },
    
    "IPC": {
        "result": "📘 Recommended:\n IPC Courses",
        "cta": "https://www.terraleap.com/ipc-courses"
    },

    # ---------- NOT SURE ----------
    "Not sure": {
        "question": "Do you already have a TerraLeap account?",
        "options": [
             "Yes, I have an account",
             "No, I'm new"
        ]
    },

    "Yes, I have an account": {
        "result": "Great 👋 Please login to continue.",
        "cta": "https://www.terraleap.com/Login.aspx"
},

    "No, I'm new": {
        "question": "What is your first name?",
        
}
}


# ---------- START ----------
@app.post("/start")
def start():
    session_id = str(uuid.uuid4())

    sessions[session_id] = {
        "step": "start",
        "context": {}
    }

    return {
        "sessionId": session_id,
        "message": FLOW["start"]["question"],
        "options": FLOW["start"]["options"]
    }


# ---------- CHAT ----------
@app.post("/chat")
def chat(data: ChatInput):
    session = sessions.get(data.sessionId)

    if not session:
        return {"error": "invalid session"}

    step = session["step"]
    context = session["context"]
    answer = data.answer
    
    registration_steps = [
    "first_name",
    "last_name",
    "country",
    "mobile",
    "email"
    ]



    # 🔄 Restart
    if answer == "Restart":
        session["step"] = "start"
        session["context"] = {}

        return {
            "message": FLOW["start"]["question"],
            "options": FLOW["start"]["options"]
        }


    # 🚀 START REGISTRATION FLOW
    if answer == "No, I'm new":

        session["step"] = "first_name"

        return {
            "message": "What is your first name?",
            "options": []
        }
        
    # ---------- REGISTRATION FLOW ----------

    if step in registration_steps:

        # FIRST NAME
        if step == "first_name":

            if len(answer.strip()) < 2:

                return {
                    "message": "Please enter a valid first name 🙂",
                    "options": []
                }

            context["first_name"] = answer

            session["step"] = "last_name"

            return {
                "message": "What is your last name?",
                "options": []
            }

        # LAST NAME
        if step == "last_name":

            if len(answer.strip()) < 2:

                return {
                    "message": "Please enter a valid last name 🙂",
                    "options": []
                }

            context["last_name"] = answer

            session["step"] = "country"

            return {
                "message": "Which country are you from?",
                "options": []
            }

        # COUNTRY
        if step == "country":

            matched_country = None

            for country in COUNTRIES:

                if country.lower() == answer.lower():

                    matched_country = country
                    break

            if not matched_country:

                return {
                    "message": "Please enter a valid country 🌍",
                    "options": []
                }

            context["country"] = matched_country

            session["step"] = "mobile"

            return {
                "message": "Enter your mobile number with country code 📱\nExample: +919876543210",
                "options": []
            }

        # MOBILE
        if step == "mobile":

            if not validate_phone(answer):

                return {
                    "message": "Please enter a valid mobile number 📱",
                    "options": []
                }

            context["mobile"] = answer

            session["step"] = "email"

            return {
                "message": "Enter your email address 📧",
                "options": []
            }

        # EMAIL
        if step == "email":

            if not is_valid_email(answer):

                return {
                    "message": "Please enter a valid email address 📧",
                    "options": []
                }

            context["email"] = answer
            
            registration_id = str(uuid.uuid4())
            
            registrations[registration_id] = {
                "first_name": context["first_name"],
                "last_name": context["last_name"],
                "country": context["country"],
                "mobile": context["mobile"],
                "email": context["email"]
            }

            return {
                "message": "Perfect 🚀 Redirecting you to registration.",
                "options": ["Restart"],
                "cta": f"register.html?session={registration_id}"
            }
        
    # 🧠 Store memory
    context[step] = answer

    previous_step = step

    # 🔁 Update step early
    session["step"] = answer

    
    # 🤖 Smart text matching
    answer_lower = answer.lower()
    for key in FLOW.keys():
        if key.lower() in answer_lower:
            answer = key
            break

    # 🔗 Combined key logic
    combined_key = answer
    if previous_step in ["KAPS", "NAPLEX", "GPAT"]:
        combined_key = f"{previous_step} {answer}"

    next_node = FLOW.get(combined_key) or FLOW.get(answer)

    # ❌ Fallback
    if not next_node:
        return {
            "message": "I didn’t quite get that 🤔\nPlease choose an option:",
            "options": FLOW[previous_step]["options"]
        }

    # ✅ Final result
    if "result" in next_node:
        return {
            "message": next_node["result"],
            "options": ["Restart"],
            "cta": next_node.get("cta")
        }

    # ➡️ Next question
    options = next_node["options"] + ["Restart"]

    return {
        "message": next_node["question"],
        "options": options
    }
    
    # ---------- REGISTRATION ---------- 
@app.get("/registration/{registration_id}")
def get_registration(registration_id: str):

    data = registrations.get(registration_id)

    if not data:
        return {"error": "registration not found"}

    return data