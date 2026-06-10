import streamlit as st
import pandas as pd
from pypdf import PdfReader

# Page Configuration
st.set_page_config(
    page_title="Holistic Profile Matcher",
    page_icon="🎓",
    layout="wide"
)

st.title("🎯 Holistic Student Profile Analyzer & Placement Matcher")
st.write("Fill out the evaluation metrics below to automatically calculate a candidate profile score and map calibrated university tiers.")

# --- FORM ENTRY ---
with st.form("comprehensive_profile_form"):
    
    # 1. Basic Info
    st.subheader("1. Demographics & Context")
    c1, c2 = st.columns(2)
    with c1:
        student_name = st.text_input("Student Name")
        school_board = st.selectbox("School Board", ["CBSE", "ICSE", "IGCSE", "IB", "Stateboard"])
    with c2:
        career_choices = st.multiselect(
            "Target Career Choice (Select max 2)", 
            ["Finance", "Tech/AI", "Medical", "Business Administration", "Media", "Psychology", "Engineering"],
            max_selections=2
        )
        countries = st.multiselect(
            "Preferred Countries (Select max 3)",
            ["US", "UK", "Canada", "Singapore", "Ireland", "Australia", "New Zealand", "Germany", "France", "Japan", "Netherlands", "Hong Kong", "UAE"],
            max_selections=3
        )

    # 2. Academics Grid (Grades 8-12 only)
    st.subheader("2. Academic Metrics (Grades 8-12)")
    st.caption("Provide percentages for completed terms. Leave at 0.0 if not completed yet.")
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        g8 = st.number_input("Grade 8 (%)", min_value=0.0, max_value=100.0, value=0.0)
        g9 = st.number_input("Grade 9 (%)", min_value=0.0, max_value=100.0, value=0.0)
    with g_col2:
        g10 = st.number_input("Grade 10 (%)", min_value=0.0, max_value=100.0, value=0.0)
        g11 = st.number_input("Grade 11 (%)", min_value=0.0, max_value=100.0, value=0.0)
    with g_col3:
        g12 = st.number_input("Grade 12 (%)", min_value=0.0, max_value=100.0, value=0.0)
        sat_act = st.number_input("SAT / ACT Standardized Score (Enter 0 if not taken)", min_value=0, max_value=1600, value=0, step=10)

    # 3. Core Profile Pillars
    st.subheader("3. Core Profile Pillars")
    p_col1, p_col2, p_col3 = st.columns(3)
    
    with p_col1:
        research_project = st.selectbox(
            "Research Project Experience",
            ["NO", "Research under PhD Scholar - No publication", "Published Research Paper"]
        )
    with p_col2:
        internship = st.selectbox(
            "Internship Experience", 
            [
                "NO", 
                "Original self-built apps/sites/tools with traction (>200 users)", 
                "Applied Coding Internship (2–4 Weeks, 1–2 Tasks)",
                "Freelance tech work or internships in unrelated fields", 
                "Shadowed a relative or short-term project"
            ]
        )
    with p_col3:
        social_impact = st.selectbox(
            "Social Impact Project or Volunteering",
            [
                "None / Not Selected",
                "Tech-based impact (app for social change, teaching coding, etc.)",
                "General volunteering with measurable outcomes",
                "One-time activities or school requirements"
            ]
        )

    # 4. Qualitative Fields & Document Attachment
    st.subheader("4. Qualitative Context & Psychometric Report")
    comp_exams = st.text_area("Competitive Exams (e.g. Olympiads, National Competitions, JEE/NEET entries)")
    awards = st.text_area("Honors & Awards")
    ecs_text = st.text_area("Additional Extracurricular Activities Summary")
    
    # PDF Upload Field
    uploaded_pdf = st.file_uploader("Upload Psychometric PDF Report", type=["pdf"])

    # Submission Action
    submit_button = st.form_submit_button("Analyze Complete Profile")

# --- EXECUTION ENGINE ---
if submit_button:
    if not student_name:
        st.error("Missing mandatory data field: Student Name.")
    elif not career_choices or not countries:
        st.error("Please assign at least one Target Career Choice and one Destination Country.")
    else:
        # A. Process PDF if uploaded
        pdf_keywords_found = []
        if uploaded_pdf is not None:
            try:
                reader = PdfReader(uploaded_pdf)
                full_pdf_text = ""
                for page in reader.pages:
                    text_content = page.extract_text()
                    if text_content:
                        full_pdf_text += text_content.lower()
                
                traits = ["analytical", "creative", "leadership", "technical", "artistic", "social", "enterprising"]
                for trait in traits:
                    if trait in full_pdf_text:
                        pdf_keywords_found.append(trait.capitalize())
            except Exception as e:
                st.warning("Psychometric PDF attached, but text parsing extraction skipped.")

        # B. Core Score Computation Matrix (Base 100 System)
        score = 0.0
        
        # 1. Academic Tracking (Weight: 40 points) - Grade 8 to 12 strictly
        valid_grades = [g for g in [g8, g9, g10, g11, g12] if g > 0]
        academic_avg = sum(valid_grades) / len(valid_grades) if valid_grades else 0.0
        score += (academic_avg / 100) * 35
        
        if school_board == "IB": score += 5.0
        elif school_board in ["IGCSE", "ICSE"]: score += 3.0
        elif school_board == "CBSE": score += 2.0

        # 2. Standardized Assessment Factor (Weight: 15 points)
        if sat_act >= 1520: score += 15.0
        elif sat_act >= 1420: score += 12.0
        elif sat_act >= 1250: score += 8.0
        elif sat_act > 0: score += 4.0

        # 3. Research Pillar Evaluation (Weight: 15 points)
        if research_project == "Published Research Paper": score += 15.0
        elif research_project == "Research under PhD Scholar - No publication": score += 10.0

        # 4. Industry/Internship Track (Weight: 15 points)
        if "Original self-built" in internship: score += 15.0
        elif "Applied Coding" in internship: score += 11.0
        elif "Freelance" in internship: score += 7.0
        elif "Shadowed" in internship: score += 4.0

        # 5. Social Impact Contributions (Weight: 10 points)
        if "Tech-based impact" in social_impact: score += 10.0
        elif "General volunteering" in social_impact: score += 7.0
        elif "One-time" in social_impact: score += 3.0

        # 6. Manual Text Bonuses (Weight: 5 points based on depth of validation)
        if len(comp_exams.strip()) > 10: score += 2.0
        if len(awards.strip()) > 10: score += 1.5
        if len(ecs_text.strip()) > 10: score += 1.5

        final_score = min(round(score, 1), 100.0)

        # C. Evaluation Dashboard View
        st.markdown("---")
        st.subheader(f"📊 Diagnostic Breakdown for: {student_name}")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Composite Profile Score", f"{final_score} / 100")
        with col_m2:
            st.metric("Academic Track Average (G8-G12)", f"{round(academic_avg, 1)}%")
        with col_m3:
            st.metric("Psychometric Status", "Attached ✅" if uploaded_pdf else "No File Added ⚠️")

        if pdf_keywords_found:
            st.info(f"🧬 **Extracted Psychometric Traits:** {', '.join(pdf_keywords_found)}")

        # D. Unified Knowledge Base for Universities (Mapped by Country and Broad Clusters)
        # To avoid massive empty data frames, if a niche combo isn't explicit, it gracefully uses the country baseline.
        uni_master_db = {
            "US": {
                "Engineering": {"Dream": "MIT, Stanford, UC Berkeley", "Target": "Purdue, UIUC, Georgia Tech", "Safe": "ASU, Penn State, Ohio State"},
                "Tech/AI": {"Dream": "Carnegie Mellon, Stanford, MIT", "Target": "UT Austin, University of Washington", "Safe": "UT Dallas, Rutgers"},
                "Finance": {"Dream": "UPenn (Wharton), NYU (Stern)", "Target": "UMich (Ross), UVa (McIntire)", "Safe": "Indiana Kelly, Penn State"},
                "Business Administration": {"Dream": "Harvard, UPenn, UC Berkeley", "Target": "USC (Marshall), BU, NYU", "Safe": "Rutgers, ASU"},
                "Default": {"Dream": "Harvard, Stanford, Columbia", "Target": "NYU, Boston University, USC", "Safe": "Arizona State University, Rutgers, Penn State"}
            },
            "UK": {
                "Engineering": {"Dream": "Cambridge, Imperial College London", "Target": "Manchester, University of Edinburgh", "Safe": "Southampton, Leeds"},
                "Tech/AI": {"Dream": "Oxford, Imperial College London", "Target": "UCL, Edinburgh", "Safe": "Birmingham, Lancaster"},
                "Finance": {"Dream": "LSE, Oxford, Cambridge", "Target": "Warwick, Cass Business School", "Safe": "Leeds, Nottingham"},
                "Default": {"Dream": "Oxford, Cambridge, Imperial, LSE", "Target": "Edinburgh, King's College London, Warwick", "Safe": "Birmingham, Leeds, Lancaster"}
            },
            "Canada": {
                "Tech/AI": {"Dream": "University of Toronto, UBC", "Target": "University of Waterloo, McGill", "Safe": "Concordia, Simon Fraser"},
                "Engineering": {"Dream": "U of Toronto, UBC", "Target": "Waterloo, McMaster", "Safe": "York University, UVic"},
                "Default": {"Dream": "University of Toronto, UBC, McGill", "Target": "Waterloo, McMaster, Western", "Safe": "York University, Simon Fraser, Concordia"}
            },
            "Singapore": {
                "Default": {"Dream": "NUS (National Univ of Singapore), NTU", "Target": "SMU (Singapore Management University)", "Safe": "SUTD, SIM Global Education"}
            },
            "Netherlands": {
                "Tech/AI": {"Dream": "TU Delft, University of Amsterdam", "Target": "Eindhoven Univ of Tech, Utrecht Univ", "Safe": "Twente, Vrije Universiteit Amsterdam"},
                "Engineering": {"Dream": "TU Delft, Eindhoven University of Tech", "Target": "Twente University, Groningen", "Safe": "HAN University of Applied Sciences"},
                "Default": {"Dream": "TU Delft, University of Amsterdam", "Target": "Eindhoven Tech, Utrecht University, Leiden", "Safe": "University of Twente, Radboud University"}
            },
            "Hong Kong": {
                "Default": {"Dream": "HKU (Univ of Hong Kong), HKUST", "Target": "Chinese University of Hong Kong (CUHK)", "Safe": "City University of HK, PolyU HK"}
            },
            "UAE": {
                "Default": {"Dream": "NYU Abu Dhabi, Khalifa University", "Target": "American University of Sharjah, UAEU", "Safe": "Heriot-Watt Dubai, Birmingham Dubai"}
            },
            "Ireland": {
                "Default": {"Dream": "Trinity College Dublin", "Target": "University College Dublin (UCD), Galway", "Safe": "Dublin City University (DCU), Limerick"}
            },
            "Australia": {
                "Default": {"Dream": "University of Melbourne, University of Sydney, UNSW", "Target": "Monash University, ANU, Univ of Queensland", "Safe": "UTS, Macquarie University, RMIT"}
            },
            "New Zealand": {
                "Default": {"Dream": "University of Auckland", "Target": "University of Otago, Victoria University", "Safe": "University of Canterbury, Massey"}
            },
            "Germany": {
                "Default": {"Dream": "TU Munich, LMU Munich", "Target": "RWTH Aachen, Heidelberg, TU Berlin", "Safe": "Karlsruhe Institute of Technology, Freiburg"}
            },
            "France": {
                "Default": {"Dream": "HEC Paris, Sciences Po, Sorbonne", "Target": "École Polytechnique, Université Paris-Saclay", "Safe": "NEOMA, SKEMA Business School"}
            },
            "Japan": {
                "Default": {"Dream": "University of Tokyo, Kyoto University", "Target": "Osaka University, Tohoku, Waseda", "Safe": "Keio University, Kyushu"}
            }
        }

        # E. Table Construction Engine
        st.subheader("🎯 Calibrated Institutional Matrix")
        st.write("Below are the placement targeting matrices cross-referenced by your selected countries and career streams:")

        for country in countries:
            st.markdown(f"#### 📍 Destination Country: {country}")
            
            # Setup structured data collection for tables
            table_rows = []
            
            for career in career_choices:
                # Fetch specific career mappings or fall back to standard regional database defaults
                country_data = uni_master_db.get(country, uni_master_db["US"])
                tier_mapping = country_data.get(career, country_data.get("Default"))
                
                raw_dream = tier_mapping["Dream"]
                raw_target = tier_mapping["Target"]
                raw_safe = tier_mapping["Safe"]

                # Perform profile score adjustments (Slippage shifts if score is less than highly competitive)
                if final_score >= 87:
                    # No shifts required
                    final_dream, final_target, final_safe = raw_dream, raw_target, raw_safe
                elif final_score >= 70:
                    # Shift downward: original target becomes dream, original safe becomes target
                    final_dream = raw_target
                    final_target = raw_safe
                    final_safe = f"Regional Core Foundations / Pathway Institutes ({country})"
                else:
                    # Critical shift: original safe becomes dream tier recommendation
                    final_dream = raw_safe
                    final_target = f"State/Regional Access Colleges ({country})"
                    final_safe = f"International Pathway & Foundation Track Programs ({country})"

                table_rows.append({
                    "Career Track": career,
                    "❤️ Dream Universities": final_dream,
                    "🎯 Target Universities": final_target,
                    "🛡️ Safe Universities": final_safe
                })
            
            # Convert to Pandas Dataframe and display as a beautiful clean table
            df_country_matrix = pd.DataFrame(table_rows)
            st.dataframe(df_country_matrix, use_container_width=True, hide_index=True)
            st.write("") # Formatting space
