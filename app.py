import streamlit as st
from pypdf import PdfReader

# Page Configuration
st.set_page_config(
    page_title="Admissions Profile Analyzer",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Holistic Student Profile Analyzer")
st.write("Fill out the candidate evaluation portfolio below to automatically calculate their holistic tier score and match target universities.")

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
            ["US", "UK", "Canada", "Singapore", "Ireland", "Australia", "New Zealand", "Germany", "France", "Japan"],
            max_selections=3
        )

    # 2. Academics Grid
    st.subheader("2. Academic Metrics (Grades 6-12)")
    st.caption("Provide percentages for completed terms. Leave at 0.0 if not completed yet.")
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    with g_col1:
        g6 = st.number_input("Grade 6 (%)", min_value=0.0, max_value=100.0, value=0.0)
        g7 = st.number_input("Grade 7 (%)", min_value=0.0, max_value=100.0, value=0.0)
    with g_col2:
        g8 = st.number_input("Grade 8 (%)", min_value=0.0, max_value=100.0, value=0.0)
        g9 = st.number_input("Grade 9 (%)", min_value=0.0, max_value=100.0, value=0.0)
    with g_col3:
        g10 = st.number_input("Grade 10 (%)", min_value=0.0, max_value=100.0, value=0.0)
        g11 = st.number_input("Grade 11 (%)", min_value=0.0, max_value=100.0, value=0.0)
    with g_col4:
        g12 = st.number_input("Grade 12 (%)", min_value=0.0, max_value=100.0, value=0.0)
        sat_act = st.number_input("SAT / ACT Standardized Score (Enter 0 if not taken)", min_value=0, max_value=1600, value=0, step=10)

    # 3. Core Extracurricular Tiers
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
                
                # Check for common traits within a psychometric report
                traits = ["analytical", "creative", "leadership", "technical", "artistic", "social", "enterprising"]
                for trait in traits:
                    if trait in full_pdf_text:
                        pdf_keywords_found.append(trait.capitalize())
            except Exception as e:
                st.warning("Psychometric PDF processed, but could not systematically extract text metadata.")

        # B. Core Score Computation Matrix (Base 100 System)
        score = 0.0
        
        # 1. Academic Tracking (Weight: 40 points)
        valid_grades = [g for g in [g6, g7, g8, g9, g10, g11, g12] if g > 0]
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
            st.metric("Academic Track Average", f"{round(academic_avg, 1)}%")
        with col_m3:
            st.metric("Psychometric Status", "Attached ✅" if uploaded_pdf else "No File Added ⚠️")

        if pdf_keywords_found:
            st.info(f"🧬 **Extracted Psychometric Traits:** {', '.join(pdf_keywords_found)}")

        # D. University Mapping Directory Matrix
        uni_db = {
            "US": {
                "Dream": ["Harvard", "Stanford", "MIT", "Columbia University", "UPenn"],
                "Target": ["NYU", "Boston University", "UIUC", "Purdue University", "USC"],
                "Safe": ["Arizona State University", "Penn State", "Rutgers", "Ohio State", "UT Dallas"]
            },
            "UK": {
                "Dream": ["Oxford", "Cambridge", "Imperial College London", "LSE"],
                "Target": ["University of Edinburgh", "King's College London", "Manchester", "Warwick"],
                "Safe": ["University of Birmingham", "Leeds", "Southampton", "Lancaster"]
            },
            "Canada": {
                "Dream": ["University of Toronto", "UBC", "McGill University"],
                "Target": ["University of Waterloo", "McMaster", "University of Alberta", "Western"],
                "Safe": ["York University", "Simon Fraser University", "Concordia", "UVic"]
            },
            "Singapore": {
                "Dream": ["NUS", "NTU"],
                "Target": ["SMU (Singapore Management University)"],
                "Safe": ["SUTD", "SIM Global Education"]
            },
            "Australia": {
                "Dream": ["University of Melbourne", "University of Sydney", "UNSW Sydney"],
                "Target": ["Monash University", "UQ", "ANU", "University of Adelaide"],
                "Safe": ["UTS", "Macquarie University", "RMIT University"]
            },
            "Ireland": {
                "Dream": ["Trinity College Dublin"],
                "Target": ["University College Dublin (UCD)", "University of Galway"],
                "Safe": ["Dublin City University (DCU)", "University of Limerick"]
            },
            "Germany": {
                "Dream": ["TU Munich", "LMU Munich"],
                "Target": ["RWTH Aachen", "Heidelberg University", "TU Berlin"],
                "Safe": ["Karlsruhe Institute of Technology", "University of Freiburg"]
            },
            "France": {
                "Dream": ["HEC Paris", "Sciences Po", "Sorbonne University"],
                "Target": ["École Polytechnique", "Université Paris-Saclay"],
                "Safe": ["NEOMA Business School", "SKEMA Business School"]
            },
            "Japan": {
                "Dream": ["University of Tokyo", "Kyoto University"],
                "Target": ["Osaka University", "Tohoku University", "Waseda University"],
                "Safe": ["Keio University", "Kyushu University"]
            },
            "New Zealand": {
                "Dream": ["University of Auckland"],
                "Target": ["University of Otago", "Victoria University of Wellington"],
                "Safe": ["University of Canterbury", "Massey University"]
            }
        }

        # Dynamic Target Calibration Algorithm 
        st.subheader("🎯 Institutional Category Matrix")
        st.write(f"Tailored mapping for tracking streams: **{', '.join(career_choices)}**")

        for country in countries:
            st.markdown(f"#### 📍 {country} Allocation")
            
            orig_dream = uni_db.get(country, {}).get("Dream", [])
            orig_target = uni_db.get(country, {}).get("Target", [])
            orig_safe = uni_db.get(country, {}).get("Safe", [])

            # Calibration shift rules depending on profile point score tiering
            if final_score >= 88:
                dream, target, safe = orig_dream, orig_target, orig_safe
            elif final_score >= 72:
                dream = orig_target
                target = orig_safe
                safe = [f"Regional Elite Institutes ({country})"]
            else:
                dream = orig_safe
                target = [f"Regional Core Programs ({country})"]
                safe = [f"International Pathway Providers ({country})"]

            # Visual Columns Layout
            dr_col, tg_col, sf_col = st.columns(3)
            with dr_col:
                st.markdown("🔴 **Dream (Reach)**")
                for u in dream: st.write(f"• {u}")
            with tg_col:
                st.markdown("🟡 **Target (Match)**")
                for u in target: st.write(f"• {u}")
            with sf_col:
                st.markdown("🟢 **Safe (Safety)**")
                for u in safe: st.write(f"• {u}")
