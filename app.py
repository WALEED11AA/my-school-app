import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# 1. إعدادات الصفحة الأساسية والتصميم (Modern Custom CSS & RTL)
# ---------------------------------------------------------
st.set_page_config(
    page_title="منصة تقييم وإدارة الطلاب - المرحلة المتوسطة",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# نمط CSS مخصص لتحسين الخطوط، الألوان، البطاقات والاتجاهات
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif;
    }
    
    body {
        direction: rtl;
        text-align: right;
        background-color: #f8f9fa;
    }
    
    /* الهيدر الرئيسي */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 24px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-weight: 800;
        margin-bottom: 5px;
        font-size: 2rem;
    }
    
    .main-header p {
        color: #e0e6ed;
        font-size: 1rem;
        margin: 0;
    }
    
    /* بطاقات الإحصائيات والمعلومات */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .student-card {
        background: #ffffff;
        border-right: 5px solid #2a5298;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    .group-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-top: 4px solid #0d9488;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }

    /* أزرار وتنسيقات الطباعة */
    @media print {
        .no-print, header, footer, [data-testid="stSidebar"] { display: none !important; }
        .page-break { page-break-after: always; }
        body { font-size: 11pt; background: white; }
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. تهيئة حالة الجلسة (Session State) وتخزين البيانات
# ---------------------------------------------------------
if "students_df" not in st.session_state:
    st.session_state["students_df"] = pd.DataFrame([
        {"id": 101, "name": "أحمد المحمد", "grade": "الثاني", "class": "2/1", "year": "1447-1448"},
        {"id": 102, "name": "خالد العتيبي", "grade": "الثاني", "class": "2/1", "year": "1447-1448"},
        {"id": 103, "name": "سارة العلي", "grade": "الثاني", "class": "2/1", "year": "1447-1448"},
        {"id": 104, "name": "محمد الشمري", "grade": "الثاني", "class": "2/2", "year": "1447-1448"},
        {"id": 105, "name": "فهد الدوسري", "grade": "الثاني", "class": "2/2", "year": "1447-1448"},
    ])

if "evaluations" not in st.session_state:
    st.session_state["evaluations"] = []

if "term_exams" not in st.session_state:
    st.session_state["term_exams"] = {}

if "custom_notes" not in st.session_state:
    st.session_state["custom_notes"] = ["النوم داخل الصف", "الأكل داخل الصف", "الخروج من الصف بدون إذن", "الهروب من الدرس"]

if "comprehensive_scores" not in st.session_state:
    st.session_state["comprehensive_scores"] = {}

# ---------------------------------------------------------
# 3. الهيدر والقائمة الجانبية
# ---------------------------------------------------------
st.markdown("""
<div class="main-header">
    <h1>🎓 منصة تقييم وإدارة الطلاب</h1>
    <p>نظام التقييم الذكي لمتابعة الأداء، الاختبارات الفترية، والسلوك الرقمي للمرحلة المتوسطة</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("### 📌 القائمة الرئيسية")
page = st.sidebar.radio("اختر الصفحة:", [
    "1. إدخال التقييم اليومي",
    "2. الاختبارات الفترية (المتوسط)",
    "3. ترتيب الطلاب ونظام النقاط",
    "4. التقرير الفردي للطالب",
    "5. ملخص الفصل والمقارنات",
    "6. التقييم الشامل (20/60)",
    "7. إدارة بيانات الطلاب والنقل",
    "8. تقسيم المجموعات",
    "9. القرعة والاختيار العشوائي"
])

# ---------------------------------------------------------
# الصفحة 1: إدخال التقييم اليومي
# ---------------------------------------------------------
if page == "1. إدخال التقييم اليومي":
    st.header("📋 إدخال التقييم اليومي")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_class = st.selectbox("🎯 اختر الفصل", st.session_state["students_df"]["class"].unique())
    with col2:
        eval_date = st.date_input("📅 التاريخ")
        
    with st.expander("⚙️ تعديل / إضافة ملاحظات سلوكية مخصصة"):
        new_note = st.text_input("إضافة ملاحظة جديدة")
        if st.button("➕ إضافة الملاحظة", use_container_width=True):
            if new_note and new_note not in st.session_state["custom_notes"]:
                st.session_state["custom_notes"].append(new_note)
                st.success("تمت إضافة الملاحظة بنجاح!")

    students_in_class = st.session_state["students_df"][st.session_state["students_df"]["class"] == selected_class]
    
    with st.form("daily_form"):
        eval_data_today = []
        for idx, student in students_in_class.iterrows():
            st.markdown(f"""
            <div class="student-card">
                <h4 style="margin:0; color:#1e3c72;">👤 الطالب: <b>{student['name']}</b> <span style="font-size:0.85em; color:#64748b;">(رقم: {student['id']})</span></h4>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3, c4, c5 = st.columns(5)
            att = c1.selectbox("الحضور", ["حاضر", "غائب بعذر", "غائب بدون عذر", "متأخر بعذر", "متأخر بدون عذر"], key=f"att_{student['id']}")
            part = c2.selectbox("المشاركة", ["مشاركة مكتملة", "مشاركة غير مكتملة", "لم يشارك"], key=f"part_{student['id']}")
            hw = c3.selectbox("الواجبات", ["واجب مكتمل", "واجب غير مكتمل", "لم يحضر الواجب"], key=f"hw_{student['id']}")
            port = c4.selectbox("ملف الأعمال", ["ملف مكتمل", "ملف غير مكتمل", "لم يحضر الملف"], key=f"port_{student['id']}")
            task = c5.selectbox("المهام الأدائية", ["مكتمل", "غير مكتمل", "لم يقم بالمهمة"], key=f"task_{student['id']}")
            
            nc1, nc2 = st.columns(2)
            beh = nc1.selectbox("ملاحظة سلوكية محددة", ["لا يوجد"] + st.session_state["custom_notes"], key=f"beh_{student['id']}")
            custom_text = nc2.text_input("ملاحظة إضافية", key=f"txt_{student['id']}")
            st.markdown("---")
            
            eval_data_today.append({
                "date": str(eval_date), "id": student["id"], "name": student["name"], "class": selected_class,
                "att": att, "part": part, "hw": hw, "port": port, "task": task, "beh": beh, "custom_text": custom_text
            })
            
        if st.form_submit_button("💾 حفظ تقييم اليوم", use_container_width=True, type="primary"):
            st.session_state["evaluations"].extend(eval_data_today)
            st.success("🎉 تم حفظ بيانات التقييم اليومي بنجاح!")

# ---------------------------------------------------------
# الصفحة 2: الاختبارات الفترية (المتوسط)
# ---------------------------------------------------------
elif page == "2. الاختبارات الفترية (المتوسط)":
    st.header("📝 الاختبارات الفترية ومتوسط الدرجات")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_class = st.selectbox("🎯 اختر الفصل", st.session_state["students_df"]["class"].unique())
    with col2:
        selected_term = st.selectbox("📌 اختر الفترة", ["فترة اولى", "فترة ثانية"])
    
    students_in_class = st.session_state["students_df"][st.session_state["students_df"]["class"] == selected_class]
    
    st.subheader(f"رصد درجات {selected_term} (8 أسابيع)")
    
    for idx, student in students_in_class.iterrows():
        st.markdown(f"##### 👤 **{student['name']}**")
        cols = st.columns(8)
        scores = []
        for week in range(1, 9):
            key = f"t_{selected_term}_{student['id']}_w{week}"
            default_val = st.session_state["term_exams"].get(key, 0.0)
            score = cols[week-1].number_input(f"أسبوع {week}", 0.0, 20.0, float(default_val), key=key)
            scores.append(score)
            st.session_state["term_exams"][key] = score
        
        avg_score = sum(scores) / 8
        st.info(f"📊 المتوسط الحسابي لـ {selected_term}: **{avg_score:.2f} / 20**")
        st.markdown("---")

# ---------------------------------------------------------
# الصفحة 3: ترتيب الطلاب ونظام النقاط
# ---------------------------------------------------------
elif page == "3. ترتيب الطلاب ونظام النقاط":
    st.header("🏆 لوحة الصدارة وترتيب الطلاب")
    selected_class = st.selectbox("🎯 اختر الفصل", st.session_state["students_df"]["class"].unique())
    
    students_in_class = st.session_state["students_df"][st.session_state["students_df"]["class"] == selected_class]
    leaderboard = []
    
    for idx, student in students_in_class.iterrows():
        points = 0
        student_evals = [e for e in st.session_state["evaluations"] if e["id"] == student["id"]]
        
        for ev in student_evals:
            for key in ["part", "hw", "port", "task"]:
                if "مكتملة" in ev[key] or "مكتمل" in ev[key]: points += 1
                elif "غير مكتمل" in ev[key]: points -= 0.5
                elif "لم" in ev[key]: points -= 1
            if ev["att"] == "حاضر": points += 1
            elif "غائب" in ev["att"] or "متأخر" in ev["att"]: points -= 1
            if ev["beh"] != "لا يوجد": points -= 1
            
        avg_term1 = np.mean([st.session_state["term_exams"].get(f"t_فترة اولى_{student['id']}_w{w}", 0) for w in range(1,9)])
        avg_term2 = np.mean([st.session_state["term_exams"].get(f"t_فترة ثانية_{student['id']}_w{w}", 0) for w in range(1,9)])
        total_exam_avg = (avg_term1 + avg_term2) / 2
        
        total_points = points + total_exam_avg
        leaderboard.append({"اسم الطالب": student["name"], "نقاط السلوك والأداء": points, "متوسط الاختبارات": total_exam_avg, "مجموع النقاط الكلي": total_points})
        
    df_lb = pd.DataFrame(leaderboard).sort_values(by="مجموع النقاط الكلي", ascending=False).reset_index(drop=True)
    df_lb.index += 1
    
    # أوسمة المراكز الأولى
    if len(df_lb) >= 3:
        col_gold, col_silver, col_bronze = st.columns(3)
        col_gold.markdown(f"<div class='metric-card' style='border-top:4px solid #eab308;'>🥇 <b>المركز الأول</b><br><h3>{df_lb.iloc[0]['اسم الطالب']}</h3><small>{df_lb.iloc[0]['مجموع النقاط الكلي']:.1f} نقطة</small></div>", unsafe_allow_html=True)
        col_silver.markdown(f"<div class='metric-card' style='border-top:4px solid #94a3b8;'>🥈 <b>المركز الثاني</b><br><h3>{df_lb.iloc[1]['اسم الطالب']}</h3><small>{df_lb.iloc[1]['مجموع النقاط الكلي']:.1f} نقطة</small></div>", unsafe_allow_html=True)
        col_bronze.markdown(f"<div class='metric-card' style='border-top:4px solid #b45309;'>🥉 <b>المركز الثالث</b><br><h3>{df_lb.iloc[2]['اسم الطالب']}</h3><small>{df_lb.iloc[2]['مجموع النقاط الكلي']:.1f} نقطة</small></div>", unsafe_allow_html=True)
        st.write("")

    st.subheader("📊 جدول الترتيب العام")
    st.dataframe(df_lb, use_container_width=True)
    
    # رسم بياني جذاب
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ['#1e3c72' if i == 0 else '#2a5298' for i in range(len(df_lb))]
    ax.barh(df_lb["اسم الطالب"][::-1], df_lb["مجموع النقاط الكلي"][::-1], color=colors)
    ax.set_xlabel("مجموع النقاط")
    ax.set_title("مجموع نقاط الطلاب", fontsize=12, fontweight='bold')
    st.pyplot(fig)

# ---------------------------------------------------------
# الصفحة 4: التقرير الفردي للطالب
# ---------------------------------------------------------
elif page == "4. التقرير الفردي للطالب":
    st.header("👤 التقرير الشامل للطالب")
    selected_student_id = st.selectbox("🎯 اختر الطالب", st.session_state["students_df"]["id"].tolist(), format_func=lambda x: st.session_state["students_df"][st.session_state["students_df"]["id"]==x]["name"].values[0])
    
    student_info = st.session_state["students_df"][st.session_state["students_df"]["id"] == selected_student_id].iloc[0]
    
    st.markdown(f"""
    <div class='student-card'>
        <h3>👤 الطالب: {student_info['name']}</h3>
        <p style='margin:0; color:#475569;'>الصف: {student_info['grade']} متوسط | الفصل: {student_info['class']} | العام الدراسي: {student_info['year']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    score_hw, score_part, score_task, score_port = 10.0, 10.0, 15.0, 5.0
    
    avg_t1 = np.mean([st.session_state["term_exams"].get(f"t_فترة اولى_{selected_student_id}_w{w}", 0) for w in range(1,9)])
    avg_t2 = np.mean([st.session_state["term_exams"].get(f"t_فترة ثانية_{selected_student_id}_w{w}", 0) for w in range(1,9)])
    score_exam = (avg_t1 + avg_t2) / 2
    
    total_score = score_hw + score_part + score_task + score_port + score_exam
    grade_pct = (total_score / 60.0) * 100
    
    if grade_pct >= 90: grade = "ممتاز ✨"
    elif grade_pct >= 80: grade = "جيد جداً 🌟"
    elif grade_pct >= 70: grade = "جيد 👍"
    elif grade_pct >= 60: grade = "مقبول 👌"
    else: grade = "يحتاج تحسين ⚠️"
    
    c1, c2, c3 = st.columns(3)
    c1.markdown(f"<div class='metric-card'><h4>المجموع النهائي</h4><h2>{total_score:.1f} / 60</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><h4>التقدير العام</h4><h2>{grade}</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><h4>معدل الاختبارات</h4><h2>{score_exam:.1f} / 20</h2></div>", unsafe_allow_html=True)

    st.write("")
    st.subheader("📈 توزيع الدرجات المستحقة")
    fig, ax = plt.subplots(figsize=(7, 3.5))
    categories = ['الواجبات (10)', 'المشاركة (10)', 'المهام (15)', 'الملف (5)', 'الاختبارات (20)']
    scores = [score_hw, score_part, score_task, score_port, score_exam]
    colors = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ef4444']
    
    ax.bar(categories, scores, color=colors)
    ax.set_ylabel("الدرجة")
    ax.set_ylim(0, 22)
    st.pyplot(fig)

# ---------------------------------------------------------
# الصفحة 5: ملخص الفصل والمقارنات
# ---------------------------------------------------------
elif page == "5. ملخص الفصل والمقارنات":
    st.header("📊 مقارنة مستويات الفصول")
    
    classes = st.session_state["students_df"]["class"].unique()
    class_averages = []
    
    for c in classes:
        class_averages.append({"الفصل": c, "متوسط الدرجات الكلي": random.uniform(48, 58)})
        
    df_class_avg = pd.DataFrame(class_averages)
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader("جدول متوسطات الفصول")
        st.dataframe(df_class_avg, use_container_width=True)
    
    with c2:
        st.subheader("مقارنة بيانية")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(df_class_avg["الفصل"], df_class_avg["متوسط الدرجات الكلي"], color='#0d9488')
        ax.set_ylabel("المتوسط من 60")
        ax.set_ylim(0, 60)
        st.pyplot(fig)

# ---------------------------------------------------------
# الصفحة 6: التقييم الشامل (20/60)
# ---------------------------------------------------------
elif page == "6. التقييم الشامل (20/60)":
    st.header("📑 التقييم الشامل النهائي")
    selected_class = st.selectbox("🎯 اختر الفصل", st.session_state["students_df"]["class"].unique())
    students_in_class = st.session_state["students_df"][st.session_state["students_df"]["class"] == selected_class]
    
    comp_data = []
    for idx, student in students_in_class.iterrows():
        st.markdown(f"##### 👤 **{student['name']}**")
        col1, col2 = st.columns(2)
        e_score = col1.number_input(f"درجة الاختبارات (من 20)", 0.0, 20.0, 18.0, key=f"cs_e_{student['id']}")
        t_score = col2.number_input(f"درجة المهام والأعمال (من 60)", 0.0, 60.0, 55.0, key=f"cs_t_{student['id']}")
        comp_data.append({"اسم الطالب": student["name"], "الاختبارات (من 20)": e_score, "المهام والأعمال (من 60)": t_score, "المجموع": e_score + t_score})
        st.markdown("---")
        
    st.subheader("📋 كشف التقييم المجمع")
    st.dataframe(pd.DataFrame(comp_data), use_container_width=True)

# ---------------------------------------------------------
# الصفحة 7: إدارة بيانات الطلاب والنقل
# ---------------------------------------------------------
elif page == "7. إدارة بيانات الطلاب والنقل":
    st.header("⚙️ إدارة بيانات الطلاب وتحديث القوائم")
    
    file = st.file_uploader("📥 استرداد بيانات الطلاب من ملف Excel أو CSV", type=["xlsx", "csv"])
    if file:
        try:
            if file.name.endswith('.csv'): df_imported = pd.read_csv(file)
            else: df_imported = pd.read_excel(file)
            st.session_state["students_df"] = pd.concat([st.session_state["students_df"], df_imported]).drop_duplicates(subset=['id'])
            st.success("🎉 تم استيراد البيانات وإضافتها بنجاح!")
        except Exception as e:
            st.error(f"حدث خطأ أثناء قراءة الملف: {e}")
            
    st.subheader("📄 قائمة الطلاب الحالية")
    st.dataframe(st.session_state["students_df"], use_container_width=True)

# ---------------------------------------------------------
# الصفحة 8: تقسيم المجموعات
# ---------------------------------------------------------
elif page == "8. تقسيم المجموعات التفاعلية":
    st.header("👥 تقسيم الطلاب إلى مجموعات عمل")
    
    col1, col2 = st.columns(2)
    with col1:
        selected_class = st.selectbox("🎯 اختر الفصل", st.session_state["students_df"]["class"].unique())
    with col2:
        num_groups = st.number_input("🔢 عدد المجموعات المطلوبة", min_value=1, max_value=10, value=3)
        
    students_list = st.session_state["students_df"][st.session_state["students_df"]["class"] == selected_class]["name"].tolist()
    
    if st.button("🎲 تقسيم تلقائي للمجموعات", use_container_width=True, type="primary"):
        shuffled = students_list.copy()
        random.shuffle(shuffled)
        groups = np.array_split(shuffled, num_groups)
        
        cols = st.columns(num_groups)
        for idx, group in enumerate(groups):
            with cols[idx]:
                st.markdown(f"""
                <div class='group-card'>
                    <h4 style='color:#0d9488; text-align:center;'>المجموعة {idx+1}</h4>
                    <hr>
                """, unsafe_allow_html=True)
                for student in group:
                    st.write(f"• {student}")
                st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# الصفحة 9: القرعة والاختيار العشوائي
# ---------------------------------------------------------
elif page == "9. القرعة والاختيار العشوائي":
    st.header("🎲 القرعة والسحب العشوائي")
    selected_class = st.selectbox("🎯 اختر الفصل", st.session_state["students_df"]["class"].unique())
    students_list = st.session_state["students_df"][st.session_state["students_df"]["class"] == selected_class]["name"].tolist()
    
    st.write("")
    if st.button("🎯 إجراء القرعة الآن!", use_container_width=True, type="primary"):
        if students_list:
            chosen = random.choice(students_list)
            st.balloons()
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); color:white; padding: 30px; border-radius: 16px; text-align:center; box-shadow: 0 10px 20px rgba(0,0,0,0.15); margin-top:20px;'>
                <h2>🎉 الفائز / الطالب المختار هو:</h2>
                <h1 style='font-size: 2.8rem; font-weight:800; margin: 15px 0;'>{chosen}</h1>
                <p>حظ موفق للجميع في المرات القادمة!</p>
            </div>
            """, unsafe_allow_html=True)
