import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Student Profile Analyzer",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Student Profile Analyzer & University Matcher")
st.write("Enter the student's academic and extracurricular details below to generate a profile score and university recommendations.")

# --- FORM ENTRY ---
with st.form("student_profile_form"):
    st.subheader("1. Basic Information")
    student_name = st.text_input("Student Name")
    
    col1, col2 = st.columns(2)
    with col1:
        school_board = st.selectbox("School Board", ["CBSE", "ICSE", "IGCSE", "IB", "Stateboard"])
    with col2:
        current_grade = st.selectbox("Current Grade Level", ["Grade 6", "Grade 7", "Grade 8", "Grade 9", "Grade 10", "Grade 11", "Grade 12"])

    st.subheader("2. Academic Performance")
    st.write("Enter the percentages for completed grades (leave at 0 if not applicable yet):")
    
    # Grid for Grade percentages
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    with g_col1:
        g6 = st.number_input("Grade 6 (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        g7 = st.number_input("Grade 7 (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with g_col2:
        g8 = st.number_input("Grade 8 (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        g9 = st.number_input("Grade 9 (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with g_col3:
        g10 = st.number_input("Grade 10 (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
        g11 = st.number_input("Grade 11 (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)
    with g_col4:
        g12 = st.number_input("Grade 12 (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1)

    sat_act = st.number_input("SAT / ACT Score (Enter 0 if test-blind/not taken)", min_value=0, max_value=1600, value=0, step=10)

    st.subheader("3. Career & Destination Preferences")
    career_choices = st.multiselect(
        "Career Choice (Select up to 2)", 
        ["Finance", "Tech/AI", "Medical", "Business Administration", "Media", "Psychology", "Engineering"],
        max_selections=2
    )
    
    countries = st.multiselect(
        "Preferred Countries (Select up to 3)",
        ["US", "UK", "Canada", "Singapore", "Ireland", "Australia", "New Zealand", "Germany", "France", "Japan"],
        max_selections=3
    )

    st.subheader("4. Profile Builders & Holistic Review")
    research_project = st.selectbox(
        "Research Project Experience",
        ["NO", "Research under PhD Scholar - No publication", "Published Research Paper"]
    )
    
    internship = st.selectbox("Internship Experience", ["NO", "1 short internship"])
    
    psychometric = st.selectbox("Psychometric Report Status", ["Not Done", "Completed - Shared with Student", "Completed - Internal Only"])

    st.subheader("5. Achievements & Extracurriculars")
    competitive_exams = st.text_area("Competitive Exams (e.g., Olympiads, JEE, NEET results)")
    awards = st.text_area("Any Awards / Honors")
    ecs = st.text_area("Extra-curricular Activities (Sports, Arts, Community Service)")

    # Submit button inside the form
    submit_button = st.form_submit_button("Analyze Profile")

# --- SCORING & ANALYSIS LOGIC ---
if submit_button:
    if not student_name:
        st.error("Please enter the student's name before running the analysis.")
    elif not career_choices or not countries:
        st.error("Please select at least one Career Choice and one Preferred Country.")
    else:
        st.success(f"Analysis Complete for {student_name}!")
        
        # 1. Calculate Academic Average (Only considering fields that are non-zero)
        grades_entered = [g for g in [g6, g7, g8, g9, g10, g11, g12] if g > 0]
        academic_avg = sum(grades_entered) / len(grades_entered) if grades_entered else 0
        
        # 2. Weighted Profile Scoring Algorithm (Max: 100 Points)
        score = 0
        
        # Academics weight (Max 50 points)
        score += (academic_avg / 100) * 45
        if school_board in ["IB", "IGCSE"]: # Rigor adjustment
            score += 5
        elif school_board in ["CBSE", "ICSE"]:
            score += 3
            
        # Standardized Testing weight (Max 15 points)
        if sat_act >= 1500: score += 15
        elif sat_act >= 1400: score += 12
        elif sat_act >= 1200: score += 8
        elif sat_act > 0: score += 5
        else: score += 5 # If test-optional/not taken, assume baseline portfolio weight
        
        # Research Project weight (Max 15 points)
        if research_project == "Published Research Paper": score += 15
        elif research_project == "Research under PhD Scholar - No publication": score += 10
        
        # Internship weight (Max 10 points)
        if internship == "1 short internship": score += 10
        
        # Manual Text Fill Adjustments (Max 10 points allocated for presence of robust profiles)
        if len(competitive_exams.strip()) > 5: score += 3
        if len(awards.strip()) > 5: score += 3
        if len(ecs.strip()) > 5: score += 4
        
        # Cap score at 100
        final_score = min(round(score, 1), 100.0)
        
        # Display Results Header
        st.markdown("---")
        st.header(f"📊 Assessment Report: {student_name}")
        
        # Metrics Visual Display
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="Overall Profile Score", value=f"{final_score} / 100")
        with col_m2:
            st.metric(label="Academic Track Record Avg", value=f"{round(academic_avg, 1)}%")

        # Tiering Logic based on Profile Score
        if final_score >= 85:
            tier = "Tier 1 (Highly Competitive)"
        elif final_score >= 70:
            tier = "Tier 2 (Competitive)"
        else:
            tier = "Tier 3 (Developing Profile)"
            
        st.info(f"**Profile Classification:** {tier}")

        # 3. Mock Database Engine for Safe, Target, Dream Tiering
        # Mapping: Country -> Tier -> List of Universities
        uni_db = {
            "US": {
                "Dream": ["Harvard University", "Stanford University", "UC Berkeley", "UPenn", "MIT"],
                "Target": ["Boston University", "NYU", "UIUC", "Purdue University", "University of Washington"],
                "Safe": ["Arizona State University", "Penn State", "Rutgers", "Ohio State University", "UT Dallas"]
            },
            "UK": {
                "Dream": ["Oxford", "Cambridge", "LSE", "Imperial College London", "UCL"],
                "Target": ["University of Edinburgh", "King's College London", "Manchester", "Warwick", "Bath"],
                "Safe": ["University of Birmingham", "Leeds", "Southampton", "Lancaster", "Nottingham"]
            },
            "Canada": {
                "Dream": ["University of Toronto", "UBC", "McGill University"],
                "Target": ["University of Waterloo", "McMaster", "University of Alberta", "Western University"],
                "Safe": ["York University", "Simon Fraser University", "Concordia", "University of Victoria"]
            },
            "Singapore": {
                "Dream": ["NUS", "NTU"],
                "Target": ["SMU (Singapore Management Univ)"],
                "Safe": ["SUTD", "SIM Global Education"]
            },
            "Australia": {
                "Dream": ["University of Melbourne", "University of Sydney", "UNSW Sydney"],
                "Target": ["Monash University", "UQ", "ANU", "University of Adelaide"],
                "Safe": ["UTS", "Macquarie University", "RMIT University", "Curtin University"]
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

        # Dynamic adjustments based on score tiering
        # If profile score is lower, things move up (What is a Target for an 85+ score becomes a Dream for a <70 score)
        st.subheader("🎯 Curated University Mapping")
        st.write(f"Based on the targeted disciplines: **{', '.join(career_choices)}**")
        
        for country in countries:
            st.markdown(f"### 📍 {country}")
            
            # Fetch base lists
            base_dream = uni_db.get(country, {}).get("Dream", [])
            base_target = uni_db.get(country, {}).get("Target", [])
            base_safe = uni_db.get(country, {}).get("Safe", [])
            
            # Calibration based on user score
            if final_score >= 85:
                # Elite profile: Standard alignment
                dream, target, safe = base_dream, base_target, base_safe
            elif final_score >= 68:
                # Good profile: Base dreams are out of reach, base targets become dreams, base safes become targets
                dream = base_dream[1:] if len(base_dream)>1 else base_dream
                target = base_target
                safe = base_safe + ["Local Premium Specialized Institutes"]
            else:
                # Developing profile: Adjust aspirations safely
                dream = base_target[:2]
                target = base_safe
                safe = [f"Regional {country} Pathways & Community Core Colleges"]

            # Display Categories using columns
            c_dream, c_target, c_safe = st.columns(3)
            with c_dream:
                st.markdown("❤️ **Dream (Reach)**")
                for u in dream: st.write(f"- {u}")
            with c_target:
                st.markdown("🎯 **Target (Match)**")
                for u in target: st.write(f"- {u}")
            with c_safe:
                st.markdown("🛡️ **Safe (Safety)**")
                for u in safe: st.write(f"- {u}")