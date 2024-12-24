#this is the chatbot database chat
import re
POSSIBLE_QUESTIONS = """
    - What are the symptoms of breast cancer?
    - What are the signs of breast cancer?
    - What is a benign tumor?
    - What is a malignant tumor?
    - How is breast cancer diagnosed?
    - What treatments are available for breast cancer?
    - What is the difference between benign and malignant tumors?
    - What are the risk factors for breast cancer?
    - How can I prevent breast cancer?
    - What is chemotherapy?
    - How does breast cancer spread?
    - What is a mammogram?
    - Is breast cancer hereditary?
    - How can I perform a self-exam for breast cancer?
    - What are the stages of breast cancer?
    - What is a lumpectomy?
    - What is a mastectomy?
    - What is the purpose of a breast self-exam?
    - How do I diagnose breast cancer?
    - How do I get tested for breast cancer?
    - What is breast cancer screening?
    - What is breast cancer prevention?
    - Can breast cancer be hereditary?
    - What are BRCA1 and BRCA2?
    - How can lifestyle changes prevent breast cancer?
    - What are the side effects of chemotherapy?
    - How can I manage the side effects of chemotherapy?
    - How can I prepare for a mammogram?
    - How can I reduce my risk of breast cancer?
"""

USER_GUIDE_TEXT = """
    **Breast Cancer Prediction Tool - User Guide**

    1. **Input Data**: Use the sidebar to adjust the values of different tumor characteristics like radius, texture, area, etc.
    2. **Predictions**: Based on the input data, the tool predicts whether the tumor is benign or malignant with a confidence level.
    3. **Radar Chart**: Visualizes the characteristics of the tumor at different levels (mean, standard error, worst).
    4. **Donut Chart**: Displays the probability of benign vs. malignant diagnosis.
    5. **Chatbot**: Use the chatbot to ask questions related to breast cancer, its symptoms, diagnosis, treatments, and more.
    6. **Help Buttons**: The "Possible Questions" button provides a list of common questions related to breast cancer. The "User Guide" button gives a detailed guide on how to use the tool.
"""



CHATBOT_RESPONSES = {
    "symptoms": "The symptoms of breast cancer include a lump in the breast, unexplained pain, changes in breast size or shape, abnormal discharge from the nipple, redness or thickening of the skin on the breast, and sometimes pain in the armpit or near the collarbone. Not all symptoms indicate cancer, but it's important to get any concerning changes checked by a doctor.",
    "signs": "The signs of breast cancer can vary, but commonly include lumps in the breast or underarm, changes in the appearance or shape of the breast, or any unusual discharge from the nipple. Some individuals may experience pain or a change in the skin texture of the breast. Any changes should be reported to a healthcare provider.",
    "benign": "Benign tumors are non-cancerous growths that do not spread to other parts of the body. They may cause discomfort or grow in size, but they generally don't pose a life-threatening risk. However, monitoring by a healthcare provider may still be necessary.",
    "malignant": "Malignant tumors are cancerous and have the ability to invade nearby tissues and spread to other parts of the body through the bloodstream or lymphatic system. They often require medical treatments such as surgery, chemotherapy, or radiation therapy.",
    "diagnosis": "Breast cancer can be diagnosed using various methods, including mammograms, ultrasounds, MRIs, and biopsies. A biopsy, where a small sample of tissue is removed from the breast and examined, is the definitive test for diagnosing cancer.",
    "treatment": "Treatment options for breast cancer depend on the stage and type of cancer. Common treatments include surgery (lumpectomy or mastectomy), chemotherapy, radiation therapy, hormone therapy, and targeted therapies. Your doctor will create a treatment plan tailored to your situation.",
    "difference benign malignant": "The main difference between benign and malignant tumors is that benign tumors are non-cancerous and do not spread, while malignant tumors are cancerous and can invade surrounding tissues and spread to other areas of the body. Benign tumors may require monitoring, but malignant tumors usually require treatment.",
    "risk factors": "Risk factors for breast cancer include a family history of the disease, age (especially over 50), genetic mutations (such as BRCA1 or BRCA2), hormone replacement therapy, obesity, lack of physical activity, and alcohol consumption. While some risk factors are controllable, others are not.",
    "prevention": "While there's no guaranteed way to prevent breast cancer, there are steps you can take to lower your risk, including maintaining a healthy weight, exercising regularly, limiting alcohol intake, avoiding tobacco, and undergoing regular breast cancer screenings as recommended by your healthcare provider.",
    "chemotherapy": "Chemotherapy is a treatment that uses drugs to destroy cancer cells or stop their growth. It can be used before surgery to shrink tumors, after surgery to eliminate remaining cancer cells, or for advanced cancer to control the spread. Side effects can include nausea, fatigue, and hair loss.",
    "spread": "Breast cancer can spread (metastasize) to other parts of the body, such as the bones, liver, lungs, and brain, through the lymphatic system or bloodstream. This spread makes the cancer more difficult to treat and may require additional therapies.",
    "mammogram": "A mammogram is an X-ray of the breast that can help detect early signs of breast cancer, such as lumps or abnormalities. It's a critical screening tool for women, especially those over 40, or those with higher risk factors.",
    "hereditary": "Hereditary breast cancer is often associated with mutations in genes such as BRCA1 and BRCA2, which can significantly increase the risk of developing breast cancer. If you have a family history of breast cancer, genetic testing and counseling may be advised.",
    "self-exam": "A breast self-exam is a way for you to check your own breasts for lumps, changes, or abnormalities. To perform a self-exam, feel each breast for lumps or thickening, and look for any changes in size, shape, or skin texture. While self-exams are helpful, they should not replace regular mammograms or professional exams.",
    "stages": "Breast cancer is staged from 0 to 4, with stage 0 being a non-invasive form (such as DCIS) and stage 4 indicating metastatic breast cancer, where the cancer has spread to other parts of the body. The stage of the cancer helps guide treatment decisions and determine the prognosis.",
    "lumpectomy": "Lumpectomy is a type of surgery in which only the tumor and a small portion of surrounding tissue are removed, preserving most of the breast. It’s typically performed for early-stage breast cancer, often followed by radiation therapy.",
    "mastectomy": "A mastectomy is the surgical removal of one or both breasts, usually as a treatment for breast cancer. There are different types of mastectomies, including simple, modified radical, and nipple-sparing mastectomies, depending on the extent of the cancer.",
    "purpose of self-exam": "The purpose of a breast self-exam is to help you become familiar with the normal feel and look of your breasts so you can detect any unusual changes early. It’s not a diagnostic tool, but a way to stay proactive about your breast health.",
    "how to diagnose": "Breast cancer is diagnosed using imaging tests like mammograms and ultrasounds, followed by a biopsy to confirm whether the abnormal tissue is cancerous. A thorough medical evaluation is needed to make a definitive diagnosis.",
    "get tested for breast cancer": "To get tested for breast cancer, women over 40 should begin regular mammograms. Depending on your risk factors, additional tests such as ultrasound or MRI may be recommended. It's essential to talk to your healthcare provider to determine the best testing schedule for you.",
    "screening": "Breast cancer screening typically involves mammography, but for women at high risk, additional screenings such as MRI may be necessary. Early detection through regular screening can help identify cancer before symptoms appear.",
    "BRCA1 and BRCA2": "BRCA1 and BRCA2 are genes that produce proteins that help repair damaged DNA. Mutations in these genes can increase the risk of breast cancer and ovarian cancer. If you have a family history of cancer, genetic testing for BRCA mutations may be recommended.",
    "lifestyle changes": "Lifestyle changes such as a balanced diet, regular exercise, maintaining a healthy weight, and limiting alcohol intake can help reduce your risk of breast cancer. These lifestyle changes not only reduce risk but also promote overall health.",
    "side effects of chemotherapy": "Chemotherapy may cause side effects such as nausea, vomiting, hair loss, fatigue, and weakened immune function. The severity of side effects varies depending on the type of chemotherapy and the individual. Medications can help manage some of these side effects.",
    "manage side effects chemotherapy": "Managing the side effects of chemotherapy involves staying hydrated, eating small meals throughout the day, taking medications to reduce nausea, and getting adequate rest. Your healthcare provider can offer additional guidance based on your specific treatments.",
    "prepare for mammogram": "To prepare for a mammogram, avoid wearing deodorant, lotion, or powders on the day of the exam as these can interfere with the X-rays. Wear a comfortable two-piece outfit, as you'll be asked to undress from the waist up.",
    "reduce risk of breast cancer": "You can reduce your risk of breast cancer by maintaining a healthy weight, exercising regularly, limiting alcohol consumption, avoiding tobacco, and undergoing regular screenings. For those at higher risk, medications or preventive surgeries may be options."
}


SYNONYMS = {
    "symptoms": ["symptoms", "signs", "warning signs", "indicators"],
    "diagnosis": ["diagnosis", "how is it diagnosed", "test for cancer", "how to detect", "identify cancer"],
    "treatment": ["treatment", "cancer treatment", "therapy", "cancer therapy", "treatment options"],
    "benign": ["benign", "non-cancerous", "harmless tumor"],
    "malignant": ["malignant", "cancerous", "dangerous tumor", "spreading cancer"],
    "risk factors": ["risk factors", "causes", "what increases risk", "what leads to cancer"],
    "prevention": ["prevention", "how to prevent", "avoid cancer", "preventive measures"],
    "chemotherapy": ["chemotherapy", "cancer drugs", "drug treatment", "chemo"],
    "spread": ["spread", "how it spreads", "metastasis", "cancer spread"],
    "mammogram": ["mammogram", "breast X-ray", "breast screening", "X-ray for cancer"],
    "hereditary": ["hereditary", "genetic", "family history", "BRCA mutation"],
    "self-exam": ["self-exam", "breast self-check", "breast check", "how to check"],
    "stages": ["stages", "staging", "stages of cancer", "how cancer progresses"],
    "lumpectomy": ["lumpectomy", "tumor removal", "breast conserving surgery"],
    "mastectomy": ["mastectomy", "breast removal", "removal of breast"],
    "side effects of chemotherapy": ["side effects", "chemotherapy side effects", "chemo side effects", "chemotherapy reactions"]
}

def get_response(question):
    """
    Returns the most relevant response based on the user's question.
    """
    question = question.lower()
    for key, value in SYNONYMS.items():
        if any(re.search(r"\b" + synonym + r"\b", question) for synonym in value):
            return CHATBOT_RESPONSES[key]
    return "Sorry, I don't have an answer for that. Please try asking another question."

