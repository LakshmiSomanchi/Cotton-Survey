import streamlit as st
import pandas as pd
import datetime
import os
import io
from PIL import Image
import zipfile

ADMIN_USERS = {"ksuneha@tns.org", "rsomanchi@tns.org", "shifalis@tns.org"}


SAVE_DIR = "responses"
os.makedirs(SAVE_DIR, exist_ok=True)


PHOTOS_DIR = "photos"
os.makedirs(PHOTOS_DIR, exist_ok=True)


SAVE_CSV_PATH = os.path.join(SAVE_DIR, "all_survey_responses_persistent.csv")

st.set_page_config(page_title="Cotton Farming Questionnaire", layout="wide")
st.title("🌾 Cotton Farming Questionnaire (किसान सर्वे)")


language = st.selectbox(
    "Select Language / भाषा निवडा / ભાષા પસંદ કરો",
    ["English", "Hindi", "Marathi", "Gujarati"],
    key="language_select"
)

dict_translations = {
    "English": {
        "1": "Farmer Tracenet Code", "2": "Farmer Full Name", "3": "Mobile no.", "4": "Gender",
        "5": "Highest education", "6": "Village", "7": "Taluka/Block", "8": "District",
        "9": "State", "10": "Pincode", "11": "No. of males (adult) in household",
        "12": "No. of females (adult) in household", "13": "Children (<16) in household",
        "14": "Total Member of Household", "15": "No. of school-going children",
        "16": "No. of earning members in the family", "17": "Total Landholding (in acres)",
        "18": "Primary crop", "19": "Secondary crops", "20": "Non-organic Cotton land (in acre) (if any)",
        "21": "Organic Cotton land (in acre)", "22": "Years since practicing organic cotton (#)",
        "23": "Certification status (certified/IC1..)", "24": "Source of irrigation",
        "25": "Cultivable area (acre)", "26": "No. of cattle (cow and Buffalo)",
        "27": "Source of drinking water", "28": "Preferred selling point (Aggregator/Suminter/APMC/other Gin)",
        "29": "Has space for harvested cotton storage (Y/N)", "30": "Receives any agro advisory (Y/N)",
        "31": "Received any training on best practices for organic cotton?",
        "32": "Membership in FPO/FPC/SHG", "33": "Maintaining any Diary or Register for record keeping (Y/N)",
        "34": "Annual household income(in Rs)", "35": "Primary source of income",
        "36": "Secondary source of income", "37": "Income from Primary source (Rs.)",
        "38": "Certification cost per annum/acre", "39": "Avg. production of organic cotton/acre (Kg)",
        "40": "Cost of cultivation/acre (Rs)", "41": "Quantity sold of organic cotton (in kg)",
        "42": "Selling price per kg (Rs.)", "43": "Material cost for bio-inputs",
        "44": "Name of bio-input used for pest and disease management",
        "45": "Name of bio-fertilizer/compost used", "46": "No. of pheromone traps used / acre",
        "47": "Cost per pheromone trap", "48": "No. of Yellow sticky traps used / acre",
        "49": "Cost per yellow sticky trap", "50": "No. of Blue sticky traps used / acre",
        "51": "Cost per blue sticky trap", "52": "No. of bird perches used / acre",
        "53": "Irrigation cost/acre", "54": "No. of irrigation required for organic cotton",
        "55": "Irrigation method used", "56": "Any farm machinery hired (Y/N)",
        "57": "Cost of machinery hiring (Rs.)/acre", "58": "Local labour cost per day",
        "59": "Migrant labour cost per day", "60": "No. of workers required during sowing/acre",
        "61": "No. of workers required during harvesting/acre",
        "62": "Harvesting time (1st, 2nd & 3rd picking) (month)",
        "63": "Weeding method used (manual/mechanical)", "64": "Weeding cost/acre",
        "65": "Cost of mulching/acre", "66": "No. of tillage practiced", "67": "Tillage cost/acre",
        "68": "Land preparation cost/acre", "69": "Seed rate of organic cotton/acre",
        "70": "Variety of organic cotton seed (Name)", "71": "Name of border crop used",
        "72": "Name of the inter crop used", "73": "Name of cover crop", "74": "Name of trap crop",
        "75": "Mulching used (Y/N)", "76": "Type of mulching used (Bio-plastic/green/dry)",
        "77": "What precautions used during storage", "78": "Hired vehicle used for transportation of seed cotton (Y/N)",
        "79": "Transportation cost (Rs.)/Kg of seed cotton",
        "80": "Any quantity rejection due to contamination/impurities (Kg)",
        "81": "Price discovery mechanism", "82": "Payment Transaction type (Cash/online)",
        "83": "Days of credit after sell", "84": "Availing any govt. scheme or subsidy benefits (Y/N)",
        "85": "Opted for crop insurance (Y/N)", "86": "Cost of crop insurance per acre",
        "87": "Possess KCC (Y/N)", "88": "Possess active bank account (Y/N)",
        "89": "Crop rotation used (Y/N)", "90": "Crops used for rotation",
        "91": "Using any water tracking devices (Y/N)", "92": "Capacity of pump (in HP)",
        "93": "Maintaining Buffer zone (Y/N)",
        "94": "Utilization of crop residue (Fuel/cattle feed/biochar/in-situ composting/burning)",
        "95": "Mode of payment to workers (cash/online)",
        "96": "Any wage difference for Men and Women workers (Y/N)",
        "97": "Using any labour register (Y/N)",
        "98": "Any arrangement of safety-kit / first-aid for workers",
        "99": "Any provision of shelter & safe drinking water for workers",
        "100": "Any provision for lavatory for workers",
        "101": "Involve family members (Women) in agricultural operations",
        "102": "Any community water harvesting structure (Y/N)",
        "103": "Use of soil moisture meter (Y/N)",
    },
    "Hindi": {
        "1": "किसान ट्रेसेनेट कोड", "2": "किसान का पूरा नाम", "3": "मोबाइल नंबर", "4": "लिंग",
        "5": "उच्चतम शिक्षा", "6": "गाँव", "7": "तालुका/ब्लॉक", "8": "जिला",
        "9": "राज्य", "10": "पिनकोड", "11": "घर में पुरुषों (वयस्क) की संख्या",
        "12": "घर में महिलाओं (वयस्क) की संख्या", "13": "घर में बच्चे (<16)",
        "14": "परिवार के कुल सदस्य", "15": "स्कूल जाने वाले बच्चों की संख्या",
        "16": "परिवार में कमाने वाले सदस्यों की संख्या", "17": "कुल भूमि जोत (एकड़ में)",
        "18": "प्राथमिक फसल", "19": "द्वितीयक फसलें", "20": "गैर-जैविक कपास भूमि (एकड़ में) (यदि कोई हो)",
        "21": "जैविक कपास भूमि (एकड़ में)", "22": "जैविक कपास का अभ्यास करने के बाद से वर्ष (#)",
        "23": "प्रमाणीकरण स्थिति (प्रमाणित/IC1..)", "24": "सिंचाई का स्रोत",
        "25": "कृषि योग्य क्षेत्र (एकड़)", "26": "मवेशियों की संख्या (गाय और भैंस)",
        "27": "पीने के पानी का स्रोत", "28": "पसंदीदा बिक्री बिंदु (एग्रीगेटर/सुमिंटर/एपीएमसी/अन्य जिन)",
        "29": "कटी हुई कपास भंडारण के लिए जगह है (हाँ/नहीं)", "30": "कोई कृषि सलाहकार प्राप्त होता है (हाँ/नहीं)",
        "31": "क्या जैविक कपास के लिए सर्वोत्तम प्रथाओं पर कोई प्रशिक्षण प्राप्त हुआ है?",
        "32": "एफपीओ/एफपीसी/एसएचजी में सदस्यता", "33": "रिकॉर्ड रखने के लिए कोई डायरी या रजिस्टर बनाए रखना (हाँ/नहीं)",
        "34": "वार्षिक घरेलू आय (रुपये में)", "35": "आय का प्राथमिक स्रोत",
        "36": "आय का द्वितीयक स्रोत", "37": "प्राथमिक स्रोत से आय (रु.)",
        "38": "प्रति वर्ष/एकड़ प्रमाणीकरण लागत", "39": "जैविक कपास/एकड़ का औसत उत्पादन (किलो)",
        "40": "प्रति एकड़ खेती की लागत (रु)", "41": "जैविक कपास की बेची गई मात्रा (किलो में)",
        "42": "प्रति किलो विक्रय मूल्य (रु.)", "43": "जैव-इनपुट के लिए सामग्री लागत",
        "44": "कीट और रोग प्रबंधन के लिए उपयोग किए जाने वाले जैव-इनपुट का नाम",
        "45": "उपयोग किए जाने वाले जैव-उर्वरक/खाद का नाम", "46": "फेरोमोन जाल का उपयोग / एकड़",
        "47": "प्रति फेरोमोन जाल लागत", "48": "पीले चिपचिपे जाल का उपयोग / एकड़",
        "49": "प्रति पीले चिपचिपे जाल लागत", "50": "नीले चिपचिपे जाल का उपयोग / एकड़",
        "51": "प्रति नीले चिपचिपे जाल लागत", "52": "पक्षी पर्च का उपयोग / एकड़",
        "53": "सिंचाई लागत/एकर", "54": "जैविक कपास के लिए आवश्यक सिंचाई की संख्या",
        "55": "सिंचाई विधि का उपयोग किया गया", "56": "क्या कोई कृषि मशीनरी किराए पर ली गई है (हाँ/नहीं)",
        "57": "मशीनरी किराए पर लेने की लागत (रु.))/एकड़", "58": "स्थानीय श्रम लागत प्रति दिन",
        "59": "प्रवासी श्रम लागत प्रति दिन", "60": "बुवाई के दौरान आवश्यक श्रमिकों की संख्या/एकड़",
        "61": "कटाई के दौरान आवश्यक श्रमिकों की संख्या/एकड़",
        "62": "कटाई का समय (1st, 2nd और 3rd पिकिंग) (महीना)",
        "63": "खरपतवार विधि का उपयोग किया गया (मैनुअल/मैकेनिकल)", "64": "खरपतवार लागत/एकड़",
        "65": "पलवार लागत/एकर", "66": "जुताई का अभ्यास किया गया", "67": "जुताई लागत/एकड़",
        "68": "भूमि तैयारी लागत/एकड़", "69": "सेंद्रिय कापसाचा बियाणे दर/एकर",
        "70": "सेंद्रिय कपास बियाण्याची जात (नाव)", "71": "उपयोग केलेल्या बॉर्डर पिकाचे नाव",
        "72": "उपयोग केलेल्या आंतरपिकाचे नाव", "73": "कवर पाकाचे नाव", "74": "ट्रैप फसलाचे नाव",
        "75": "आच्छादन का उपयोग किया गया (हाँ/नहीं)", "76": "आच्छादन के प्रकार का उपयोग किया गया (जैव-प्लास्टिक/हरा/सूखा)",
        "77": "भंडारण के दौरान क्या सावधानियां बरती जाती हैं",
        "78": "बीज कपास के परिवहन के लिए किराए पर वाहन का उपयोग किया जाता है (हाँ/नहीं)",
        "79": "परिवहन लागत (रु.)/बीज कपास का किलो", "80": "प्रदूषण/अशुद्धियों के कारण कोई मात्रा अस्वीकृति (किलो)",
        "81": "मूल्य खोज तंत्र", "82": "भुगतान लेनदेन प्रकार (नकद/ऑनलाइन)",
        "83": "बेचने के बाद क्रेडिट के दिन", "84": "किसी भी सरकारी योजना या सब्सिडी लाभ का लाभ उठाना (हाँ/नहीं)",
        "85": "फसल बीमा के लिए चुना गया (हाँ/नहीं)", "86": "फसल बीमा की लागत प्रति एकड़",
        "87": "केसीसी है (हाँ/नहीं)", "88": "सक्रिय बैंक खाता है (हाँ/नहीं)",
        "89": "फसल रोटेशन का उपयोग किया गया (हाँ/नहीं)", "90": "रोटेशन के लिए उपयोग की जाने वाली फसलें",
        "91": "क्या किसी जल ट्रैकिंग डिवाइस का उपयोग किया जा रहा है (हाँ/नहीं)",
        "92": "पंप की क्षमता (एचपी में)", "93": "बफर जोन बनाए रखना (हाँ/नहीं)",
        "94": "फसल अवशेष का उपयोग (ईंधन/पशु चारा/बायोचार/इन-सीटू कंपोस्टिंग/जलाना)",
        "95": "श्रमिकों को भुगतान का तरीका (नकद/ऑनलाइन)",
        "96": "पुरुष और महिला श्रमिकों के लिए कोई वेतन अंतर (हाँ/नहीं)",
        "97": "क्या किसी श्रम रजिस्टर का उपयोग किया जा रहा है (हाँ/नहीं)",
        "98": "श्रमिकों के लिए सुरक्षा-किट/प्राथमिक चिकित्सा की कोई व्यवस्था",
        "99": "श्रमिकों के लिए आश्रय और सुरक्षित पेयजल का कोई प्रावधान",
        "100": "श्रमिकों के लिए शौचालय का कोई प्रावधान",
        "101": "कृषि कार्यों में परिवार के सदस्यों (महिलाओं) को शामिल करना",
        "102": "कोई सामुदायिक जल संचयन संरचना (हाँ/नहीं)",
        "103": "मृदा नमी मीटर का उपयोग (हाँ/नाही)",
    },
    "Marathi": {
        "1": "शेतकरी ट्रेसनेट कोड", "2": "शेतकऱ्याचे पूर्ण नाव", "3": "मोबाईल नंबर", "4": "लिंग",
        "5": "उच्चतम शिक्षण", "6": "गाव", "7": "तालुका/ब्लॉक", "8": "जिल्हा",
        "9": "राज्य", "10": "पिनकोड", "11": "घरातील पुरुषांची (प्रौढ) संख्या",
        "12": "घरातील महिलांची (प्रौढ) संख्या", "13": "घरातील मुले (<16)",
        "14": "घरातील एकूण सदस्य", "15": "शाळेत जाणाऱ्या मुलांची संख्या",
        "16": "कुटुंबातील कमावत्या सदस्यांची संख्या", "17": "एकूण जमिनीची मालकी (एकरमध्ये)",
        "18": "प्राथमिक पीक", "19": "दुय्यम पिके", "20": "गैर-सेंद्रिय कापूस जमीन (एकरमध्ये) (असल्यास)",
        "21": "सेंद्रिय कापूस जमीन (एकरमध्ये)", "22": "सेंद्रिय कापूस लागवडीपासूनची वर्षे (#)",
        "23": "प्रमाणीकरण स्थिती (प्रमाणित/IC1..)", "24": "सिंचनाचा स्रोत",
        "25": "कृषि योग्य क्षेत्र (एकर)", "26": "जनावरांची संख्या (गाय आणि म्हैस)",
        "27": "पिण्याच्या पाण्याचे स्रोत", "28": "पसंतीचे विक्री केंद्र (एग्रीगेटर/सुमिंटर/एपीएमसी/इतर जिन)",
        "29": "कापणी केलेल्या कापसाच्या साठवणुकीसाठी जागा आहे (होय/नाही)", "30": "कोणताही कृषी सल्ला मिळतो (होय/नाही)",
        "31": "सेंद्रिय कापसासाठी सर्वोत्तम पद्धतींवर कोणतेही प्रशिक्षण मिळाले आहे का?",
        "32": "एफपीओ/एफपीसी/एसएचजी मध्ये सदस्यता", "33": "नोंद ठेवण्यासाठी कोणतीही डायरी किंवा रजिस्टर ठेवणे (होय/नाही)",
        "34": "वार्षिक घरगुती उत्पन्न (रुपयांमध्ये)", "35": "उत्पन्नाचा प्राथमिक स्रोत",
        "36": "उत्पन्नाचा दुय्यम स्रोत", "37": "प्राथमिक स्रोताकडून उत्पन्न (रु.)",
        "38": "प्रति वर्ष/एकर प्रमाणीकरण खर्च", "39": "सेंद्रिय कापूस/एकरचे सरासरी उत्पादन (किलो)",
        "40": "प्रति एकर लागवडीचा खर्च (रु.)", "41": "सेंद्रिय कापसाची विक्री केलेली मात्रा (किलोमध्ये)",
        "42": "प्रति किलो विक्री किंमत (रु.)", "43": "जैव-इनपुटसाठी सामग्री खर्च",
        "44": "कीड आणि रोग व्यवस्थापनासाठी वापरल्या जाणाऱ्या जैव-इनपुटचे नाव",
        "45": "वापरल्या जाणाऱ्या जैव-खत/खादचे नाव", "46": "फेरोमोन सापळे वापरले / एकर",
        "47": "प्रति फेरोमोन सापळा खर्च", "48": "पिवळे चिकट सापळे वापरले / एकर",
        "49": "प्रति पिवळा चिकट सापळा खर्च", "50": "निळे चिकट सापळे वापरले / एकर",
        "51": "प्रति निळा चिकट सापळा खर्च", "52": "पक्षी थांबे वापरले / एकर",
        "53": "सिंचन खर्च/एकर", "54": "सेंद्रिय कापसासाठी आवश्यक सिंचनाची संख्या",
        "55": "वापरलेली सिंचन पद्धत", "56": "कोणतीही शेती अवजारे भाड्याने घेतली आहेत (होय/नाही)",
        "57": "अवजारे भाड्याने घेण्याचा खर्च (रु.)/एकर", "58": "स्थानिक मजुरीचा दर प्रति दिवस",
        "59": "स्थलांतरित मजुरीचा दर प्रति दिवस", "60": "वावणीच्या वेळी आवश्यक कामगारांची संख्या/एकर",
        "61": "कापणीच्या वेळी आवश्यक कामगारांची संख्या/एकर",
        "62": "कापणीची वेळ (1 ली, 2 री आणि 3 री निवड) (महिना)",
        "63": "तण काढण्याची पद्धत वापरली (हाताने/यांत्रिक)", "64": "तण काढण्याचा खर्च/एकर",
        "65": "आच्छादन खर्च/एकर", "66": "किती वेळा नांगरणी केली", "67": "नांगरणी खर्च/एकर",
        "68": "जमीन तयार करण्याचा खर्च/एकर", "69": "सेंद्रिय बियाण्याचा दर/एकर",
        "70": "सेंद्रिय कापसाच्या बियाण्याची जात (नाव)", "71": "वापरलेल्या बॉर्डर पिकाचे नाव",
        "72": "वापरलेल्या आंतरपिकाचे नाव", "73": "कवर पिकाचे नाव", "74": "ट्रॅप पिकाचे नाव",
        "75": "मल्चिंग वापरले (होय/नाही)", "76": "वापरलेल्या मल्चिंगचा प्रकार (जैव-प्लास्टिक/हिरवा/कोरडा)",
        "77": "साठवणुकीदरम्यान कोणती खबरदारी घेतली जाते",
        "78": "बीज कपासाच्या वाहतुकीसाठी भाड्याचे वाहन वापरले (होय/नाही)",
        "79": "वाहतूक खर्च (रु.)/बीज कपासाचे किलो", "80": "प्रदूषण/अशुद्धतेमुळे कोणतीही मात्रा नाकारली (किलो)",
        "81": "किंमत शोधण्याची यंत्रणा", "82": "चुकवणी व्यवहार प्रकार (रोख/ऑनलाइन)",
        "83": "विक्री केल्यानंतर क्रेडिटचे दिवस", "84": "कोणत्याही सरकारी योजना किंवा अनुदानाचा लाभ घेणे (होय/नाही)",
        "85": "पीक विमा घेतला (होय/नाही)", "86": "प्रति एकर पीक विमा खर्च",
        "87": "केसीसी आहे (होय/नाही)", "88": "सक्रिय बँक खाते आहे (होय/नाही)",
        "89": "पीक परिभ्रमण वापरले (होय/नाही)", "90": "परिभ्रमणासाठी वापरलेली पिके",
        "91": "कोणतेही जल ट्रॅकिंग उपकरण वापरत आहात (होय/नाही)",
        "92": "पंपाची क्षमता (एचपी मध्ये)", "93": "बफर झोन राखणे (होय/नाही)",
        "94": "पीक अवशेषांचा वापर (इंधन/जनावरांचे खाद्य/बायोचार/इन-सीटू कंपोस्टिंग/जाळणे)",
        "95": "कामगारांना देयकाची पद्धत (रोख/ऑनलाइन)",
        "96": "पुरुष आणि महिला कामगारांसाठी कोणताही वेतन तफावत (होय/नाही)",
        "97": "कोणतेही कामगार रजिस्टर वापरत आहात (होय/नाही)",
        "98": "कामगारांसाठी सुरक्षा-किट/प्राथमिक उपचारांची कोणतीही व्यवस्था",
        "99": "कामगारांसाठी निवारा आणि सुरक्षित पिण्याच्या पाण्याची कोणतीही तरतूद",
        "100": "कामगारांसाठी शौचालयाची कोणतीही तरतूद",
        "101": "कृषी कार्यांमध्ये कुटुंबातील सदस्यांना (महिलांना) सामील करणे",
        "102": "कोणतीही सामुदायिक जल संचयन रचना (होय/नाही)",
        "103": "मातीतील ओलावा मीटरचा वापर (होय/नाही)",
    },
    "Gujarati": {
        "1": "ખેડૂત ટ્રેસનેટ કોડ", "2": "ખેડૂતનું પૂરું નામ", "3": "મોબાઇલ નંબર", "4": "લિંગ",
        "5": "કેટલો અભ્યાસ કરેલો છે", "6": "ગામ", "7": "તાલુકો/બ્લોક", "8": "જિલ્લો",
        "9": "રાજ્ય", "10": "પિનકોડ", "11": "ઘરમાં પુરુષોની (પુખ્ત) સંખ્યા",
        "12": "ઘરમાં મહિલાઓની (પુખ્ત) સંખ્યા", "13": "ઘરમા બાળકોની સંખ્યા (૧૬ થી ઓછી ઉમરના )",
        "14": "પરિવારના કુલ સભ્યો", "15": "શાળાએ જતા બાળકોની સંખ્યા",
        "16": "પરિવારમાં કમાતા સભ્યની સંખ્યા", "17": "કુલ જમીન ધારણ (એકરમાં)",
        "18": "મુખ્ય પાક", "19": "ગૌણ પાક", "20": "બિન-ઓર્ગેનિક કપાસની જમીન (એકરમાં)",
        "21": "ઓર્ગેનિક કપાસની જમીન (એકરમાં)", "22": "ઓર્ગનીક કપાસની ખેતી કેટલા વર્ષથી કરો છો",
        "23": "સર્ટિફિકેસન સ્ટેટસ (સર્ટિફાઇડ/IC-1,2,3)", "24": "સિંચાઈનો સ્ત્રોત",
        "25": "ખેતીલાયક વિસ્તાર (એકર)", "26": "ઢોરની સંખ્યા (ગાય અને ભેંસ)",
        "27": "પીવાના પાણીનો સ્ત્રોત", "28": "પસંદગીનું વેચાણ સ્થળ (એગ્રીગેટર/સુમિન્ટર/એપીએમસી/અન્ય જીન)",
        "29": "વીણી કરેલા કપાસના સંગ્રહ માટે જગીયા છે", "30": "કોઈ પણ ખેતી સંબધિત સલાહ મળે છે",
        "31": "શું ઓર્ગેનિક કપાસ માટેની શ્રેષ્ઠ પદ્ધતિ પર કોઈ તાલીમ મળી છે",
        "32": "એફપીઓ/એફપીસી/એસએચજીમાં સભ્યપદ ધરાવો છો", "33": "રેકોર્ડ રાખવા માટે કોઈ ડાયરી અથવા રજિસ્ટર જાળવો છો",
        "34": "વાર્ષિક ઘરગથ્થુ આવક (રૂપિયામાં)", "35": "આવકનો પ્રાથમિક સ્ત્રોત",
        "36": "આવકનો ગૌણ સ્ત્રોત", "37": "પ્રાથમિક સ્ત્રોતમાંથી આવક (રૂ.)",
        "38": "સર્ટિફિકેસન ખર્ચ પ્રતિ વર્ષ/એકર", "39": "ઓર્ગનીક કપાસનું સરેરાશ ઉત્પાદન (કિલો/એકર)",
        "40": "ખેતીનો ખર્ચ (રૂપીયા/એકર)", "41": "ઓર્ગેનિક કપાસનો વેચાણ કરેલો જથ્થો (કિલોમાં)",
        "42": "વેચાણ કિંમત પ્રતિ કિલો (રૂ.)", "43": "બાયો-ઇનપુટ્સ માટે સામગ્રી ખર્ચ",
        "44": "જંતુ અને રોગ વ્યવસ્થાપન માટે વપરાતા બાયો-ઇનપુટનું નામ",
        "45": "વપરાતા બાયો-ખત/ખાદનું નામ", "46": "ફેરોમોન ટ્રેપનો ઉપયોગ / એકર",
        "47": "ખર્ચ પ્રતિ ફેરોમોન ટ્રેપ", "48": "પીળા સ્ટીકી ટ્રેપનો ઉપયોગ / એકર",
        "49": "ખર્ચ પ્રતિ પીળો સ્ટીકી ટ્રેપ", "50": "વાદળી સ્ટીકી ટ્રેપનો ઉપયોગ / એકર",
        "51": "ખર્ચ પ્રતિ વાદળી સ્ટીકી ટ્રેપ", "52": "પક્ષી સ્ટેન્ડનો ઉપયોગ પ્રતિ એકર",
        "53": "सिંચાઈ ખર્ચ/એકર", "54": "ઓર્ગેનિક કપાસ માટે જરૂરી સિંચાઈની સંખ્યા",
        "55": "વપરાયેલી સિંચાઈ પદ્ધતિ", "56": "કોઈપણ ખેતી મશીનરી ભાડે લીધી છે (હા/ના)",
        "57": "મશીનરી ભાડે લેવાનો ખર્ચ (રૂ.)/એકર", "58": "સ્થાનિક મજૂરી ખર્ચ પ્રતિ દિવસ",
        "59": "સ્થળાંતરિત મજૂરી ખર્ચ પ્રતિ દિવસ", "60": "વાવણીના સમયે જરૂરી કામદારોની સંખ્યા/એકર",
        "61": "વીણીના સમયે જરૂરી કામદારોની સંખ્યા/એકર",
        "62": "વીણી સમય (1 લી, 2 જી અને 3 જી વીણીનો મહિનો)",
        "63": "નિંદામણ પદ્ધતિનો પ્રકાર (હાથ વડે /સાધન દ્વારા)", "64": "નિંદામણ ખર્ચ/એકર",
        "65": "મલ્ચિંગ ખર્ચ/એકર", "66": "કેટલી વખત ખેડ કરો છો", "67": "ખેડ ખર્ચ/એકર",
        "68": "જમીન તૈયારી ખર્ચ/એકર", "69": "ઓર્ગનિકં કપાસનો બીજનો દર/એકર",
        "70": "ઓર્ગનિકં કપાસના બીજની જાતનું નામ", "71": "બોર્ડર પાકનું નામ",
        "72": "આંતરપાકનું નામ", "73": "કવર પાકનું નામ", "74": "ટ્રેપ પાકનું નામ",
        "75": "મલ્ચિંગ વાપરો છે (હા/ના)", "76": "વપરાયેલા મલ્ચિંગનો પ્રકાર (જૈવ-પ્લાસ્ટિક/લીલો/સૂકો)",
        "77": "સંગ્રહ દરમિયાન શું સાવચેતીઓ રાખો છો",
        "78": "વીણી કરેલા કપાસના પરિવહન માટે ભાડે લીધેલ વાહન વપરાય છે (હા/ના)",
        "79": "પરિવહન ખર્ચ રૂપિયા/કિલો", "80": "દૂષણ/અશુદ્ધિઓને કારણે કોઈપણ જથ્થાનો અસ્વીકાર (કિલો)",
        "81": "કપાસના ભાવ જાણવાની રીત", "82": "ચુકવણી વ્યવહારનો પ્રકાર (રોકડા/ઓનલાઇન)",
        "83": "વેચાણ કર્યા પછી કેટલા દિવસોમાં રૂપીયા મળે છે",
        "84": "કોઈપણ સરકારી યોજના અથવા સબસીડીનો લાભ મળે છે (હા/ના)",
        "85": "પાક વીમો ઉતારો છો (હા/ના)", "86": "દર એકર પાક વીમાનો ખર્ચ",
        "87": "કિશાન ક્રેડિટ કાર્ડ છે (હા/ના)", "88": "સક્રિય બેંક ખાતું છે (હા/ના)",
        "89": "પાક ફેરબદલી કરો છો (હા/ના)", "90": "પાક ફેરબદલી માટે વપરાતા પાક",
        "91": "કોઈપણ પાણી ટ્રેકિંગ ઉપકરણોનો ઉપયોગ કરો છો (હા/ના)",
        "92": "કૂવા કે બોરવેલના પંપની ક્ષમતા (એચપીમાં)",
        "93": "બફર ઝોન જાળવો છો (હા/ના)",
        "94": "પાકના અવશેષોનો ઉપયોગ (બળતણ/પશુઓનો ખોરાક/બાયોચાર/इन-सीटू कंपोस्टिंग/सળગાવવું/कંપोस्ट)",
        "95": "કામદારને ચૂકવણીની પદ્ધતિ (રોકડા/ઓનલાઇન)",
        "96": "પુરુષ અને મહિલા કામદારો માટે કોઈપણ વેતન તફાવત (હા/ના)",
        "97": "કોઈ શ્રમ રજીસ્ટરનો ઉપયોગ કરી રહ્યા છો (હા/ના)",
        "98": "કામદારો માટે સલામતી-કીટ/પ્રાથમિક સારવારની કોઈપણ વ્યવસ્થા",
        "99": "કામદારો માટે આશ્રય અને સુરક્ષિત पिण्याच्या पाण्याची કોઈ જોગવાઈ",
        "100": "કામદારો માટે શૌચાલયની કોઈ જોગવાઈ",
        "101": "ખેતીકામમાં કુટુંબના સભ્યો (મહિલાઓ) ને સામેલ કરો છો",
        "102": "કોઈપણ સામુદાયિક જળ સંચય માળખું (હા/ના)",
        "103": "માટી ભેજ મીટરનો ઉપયોગ (હા/ના)"
    },
}


questions = [str(i) for i in range(1, 104)]


labels = dict_translations.get(language, dict_translations["English"])


numeric_questions = list(set([
    "11", "12", "13", "14", "15", "16", "17", "20", "21", "22", "25", "26", "34", "37",
    "38", "39", "40", "41", "42", "43", "46", "47", "48", "49", "50", "51", "52",
    "53", "54", "57", "58", "59", "60", "61", "64", "65", "66", "67", "68", "69",
    "79", "80", "83", "86", "92",
]))
numeric_questions = [q for q in numeric_questions if q not in ["3", "6"]] 

yes_no_questions = ["29", "30", "33", "56", "75", "78", "84", "85", "87", "88", "89", "91", "93", "96", "97", "98", "99", "100", "101", "102", "103"]
irrigation_source_options = ["Canal", "Well", "Borewell", "River", "Farm Pond", "Community Pond", "Rain-fed not irrigated"]
irrigation_method_options = ["Drip irrigation", "Sprinkler irrigation", "Flood irrigation", "Ridge and Furrow Irrigation", "Other"]
weeding_method_options = ["Manual", "Mechanical", "Both", "Other"]
gender_options = ["Male", "Female", "Others"]

MULTISELECT_QUESTIONS = {
    "23": ["Certified", "Non-Certified", "IC1", "IC2", "Others"],
    "32": ["FPO", "FPC", "SHG", "Others"],
    "94": ["Fuel", "Cattle feed", "Biochar", "In-situ composting", "Burning"],
}



if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'uploaded_photo_info' not in st.session_state:
    st.session_state.uploaded_photo_info = None
if 'form_submitted_for_review' not in st.session_state:
    st.session_state.form_submitted_for_review = False
if 'has_validation_error' not in st.session_state:
    st.session_state.has_validation_error = False
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False


if 'all_survey_data' not in st.session_state:
    if os.path.exists(SAVE_CSV_PATH):
        try:
            st.session_state.all_survey_data = pd.read_csv(SAVE_CSV_PATH)
            st.info(f"Loaded {len(st.session_state.all_survey_data)} existing responses.")
        except pd.errors.EmptyDataError:
            initial_columns = ["Timestamp", "Surveyor Name"]
            for q_key in questions:
                initial_columns.append(labels.get(q_key, f"Question {q_key}"))
            initial_columns.append("Others Gender Specify")
            st.session_state.all_survey_data = pd.DataFrame(columns=initial_columns)
            st.info("Existing CSV found but was empty. Initializing new DataFrame.")
        except Exception as e:
            st.error(f"Error loading existing survey data: {e}. Starting with an empty DataFrame.")
            initial_columns = ["Timestamp", "Surveyor Name"]
            for q_key in questions:
                initial_columns.append(labels.get(q_key, f"Question {q_key}"))
            initial_columns.append("Others Gender Specify")
            st.session_state.all_survey_data = pd.DataFrame(columns=initial_columns)
    else:
        initial_columns = ["Timestamp", "Surveyor Name"]
        for q_key in questions:
            initial_columns.append(labels.get(q_key, f"Question {q_key}"))
        initial_columns.append("Others Gender Specify")
        st.session_state.all_survey_data = pd.DataFrame(columns=initial_columns)
        st.info("No existing survey data found. Starting a new DataFrame.")



if not st.session_state.form_submitted_for_review:
    with st.form("questionnaire_form"):
        surveyor_name_label = ""
        if language == "English":
            surveyor_name_label = "Surveyor Name"
        elif language == "Hindi":
            surveyor_name_label = "सर्वेयर का नाम"
        elif language == "Marathi":
            surveyor_name_label = "सर्वेयरचे नाव"
        elif language == "Gujarati":
            surveyor_name_label = "સર્વેયરનું નામ"

        st.session_state.responses["surveyor_name"] = st.text_input(
            surveyor_name_label,
            key="surveyor_name_input",
            value=st.session_state.responses.get("surveyor_name", "")
        )

        for question_key in questions:
            question_text = labels.get(question_key, f"Question {question_key} (No translation)")
            current_value = st.session_state.responses.get(question_key, "")

            if question_key in MULTISELECT_QUESTIONS:
                selected_values = []
                if isinstance(current_value, str) and current_value:
                    selected_values = [v.strip() for v in current_value.split(',')]
                elif isinstance(current_value, list):
                    selected_values = current_value

                selected_options = st.multiselect(
                    question_text,
                    MULTISELECT_QUESTIONS[question_key],
                    default=selected_values,
                    key=f"question_{question_key}"
                )
                st.session_state.responses[question_key] = ", ".join(selected_options) if selected_options else ""

            elif question_key == "4":
                default_index = 0
                if current_value and current_value in gender_options:
                    default_index = gender_options.index(current_value)

                selected_gender = st.selectbox(
                    question_text,
                    gender_options,
                    key=f"question_{question_key}",
                    index=default_index
                )
                st.session_state.responses[question_key] = selected_gender

                if selected_gender == "Others":
                    st.session_state.responses["others_gender"] = st.text_input(
                        "If selected 'Others', please specify:",
                        key="others_gender_specify",
                        value=st.session_state.responses.get("others_gender", "")
                    )
                else:
                    st.session_state.responses.pop("others_gender", None)

            elif question_key == "24":
                default_index = 0
                if current_value and current_value in irrigation_source_options:
                    default_index = irrigation_source_options.index(current_value)
                st.session_state.responses[question_key] = st.selectbox(
                    question_text,
                    irrigation_source_options,
                    key=f"question_{question_key}",
                    index=default_index
                )

            elif question_key == "55":
                default_index = 0
                if current_value and current_value in irrigation_method_options:
                    default_index = irrigation_method_options.index(current_value)
                st.session_state.responses[question_key] = st.selectbox(
                    question_text,
                    irrigation_method_options,
                    key=f"question_{question_key}",
                    index=default_index
                )

            elif question_key == "63":
                default_index = 0
                if current_value and current_value in weeding_method_options:
                    default_index = weeding_method_options.index(current_value)
                st.session_state.responses[question_key] = st.selectbox(
                    question_text,
                    weeding_method_options,
                    key=f"question_{question_key}",
                    index=default_index
                )

            elif question_key == "62":
                st.session_state.responses[question_key] = st.text_input(
                    question_text,
                    placeholder="e.g., month 1, month 2, month 3",
                    key=f"question_{question_key}",
                    value=current_value
                )

            elif question_key in yes_no_questions:
                default_index = 0
                if current_value == "No":
                    default_index = 1
                elif current_value == "":
                    current_value = "Yes"

                st.session_state.responses[question_key] = st.selectbox(
                    question_text,
                    ["Yes", "No"],
                    key=f"question_{question_key}",
                    index=default_index
                )
            
            elif question_key in numeric_questions:
                num_val = 0.0
                try:
                    if current_value is not None and str(current_value).replace('.', '', 1).isdigit():
                        num_val = float(current_value)
                except ValueError:
                    num_val = 0.0
                
                st.session_state.responses[question_key] = st.number_input(
                    question_text,
                    min_value=0.0,
                    format="%.2f",
                    key=f"question_{question_key}",
                    value=num_val
                )
            else:
                st.session_state.responses[question_key] = st.text_input(
                    question_text,
                    key=f"question_{question_key}",
                    value=current_value
                )

        uploaded_photo = st.file_uploader(
            "Upload a photo (optional):",
            type=["jpg", "jpeg", "png"],
            key="uploaded_photo_form",
        )

        if uploaded_photo:
            st.session_state.uploaded_photo_info = {
                "name": uploaded_photo.name,
                "data": uploaded_photo.getvalue(),
                "type": uploaded_photo.type
            }
        elif st.session_state.uploaded_photo_info and not uploaded_photo:
            st.image(st.session_state.uploaded_photo_info["data"], caption="Previously uploaded photo", width=100)
            if st.button("Clear Photo", key="clear_photo_button"):
                st.session_state.uploaded_photo_info = None
                st.rerun()

        if st.form_submit_button("Review and Proceed"):
            st.session_state.has_validation_error = False

            if not st.session_state.responses.get("surveyor_name"):
                st.error("Surveyor Name is required.")
                st.session_state.has_validation_error = True

            required_fields = ["1", "2", "3", "4", "6", "8", "9", "10", "34", "35", "37", "39", "41", "42"]
            for field in required_fields:
                val = st.session_state.responses.get(field)
                if val is None or val == "" or \
                   (isinstance(val, (int, float)) and val == 0 and field in ["34", "37", "39", "41", "42"]):
                    st.error(f"Field '{labels[field]}' is required.")
                    st.session_state.has_validation_error = True

            phone_number = str(st.session_state.responses.get("3", "")).strip()
            if not phone_number.isdigit() or len(phone_number) != 10:
                st.error("Mobile no. must be exactly 10 digits.")
                st.session_state.has_validation_error = True
            
            for field in numeric_questions:
                val = st.session_state.responses.get(field)
                try:
                    if val is not None and str(val).strip() != "":
                        num_val = float(val)
                        if num_val < 0:
                            st.error(f"Field '{labels[field]}' must be a non-negative number.")
                            st.session_state.has_validation_error = True
                except (ValueError, TypeError):
                    st.error(f"Field '{labels[field]}' must be a valid number.")
                    st.session_state.has_validation_error = True

            harvesting_time = st.session_state.responses.get("62")
            if harvesting_time:
                months = [m.strip() for m in harvesting_time.split(",") if m.strip()]
                if len(months) != 3:
                    st.error(f"Field '{labels['62']}' must contain exactly 3 months, separated by commas (e.g., month 1, month 2, month 3).")
                    st.session_state.has_validation_error = True

            if not st.session_state.has_validation_error:
                st.session_state.form_submitted_for_review = True
                st.rerun()

# --- Review and Edit Section ---
if st.session_state.form_submitted_for_review and not st.session_state.has_validation_error:
    st.subheader("Review Your Responses")
    st.write("Please review the information below. If everything is correct, click 'Confirm and Save'.")

    for key, value in st.session_state.responses.items():
        if key == "surveyor_name":
            surveyor_name_label = ""
            if language == "English":
                surveyor_name_label = "Surveyor Name"
            elif language == "Hindi":
                surveyor_name_label = "सर्वेयर का नाम"
            elif language == "Marathi":
                surveyor_name_label = "सर्वेयरचे नाव"
            elif language == "Gujarati":
                surveyor_name_label = "સર્વેયરનું નામ"
            st.write(f"**{surveyor_name_label}:** {value}")
        elif key in questions:
            st.write(f"**{labels.get(key, f'Question {key}')}:** {value}")
        elif key == "others_gender":
            st.write(f"**If selected 'Others', please specify:** {value}")

    if st.session_state.uploaded_photo_info:
        st.image(st.session_state.uploaded_photo_info["data"], caption="Uploaded Photo", width=200)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Edit Responses"):
            st.session_state.form_submitted_for_review = False
            st.rerun()
    with col2:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        farmer_name_for_filename = "".join(filter(str.isalnum, st.session_state.responses.get("2", "unknown_farmer"))).lower()
        photo_ext = "jpg"
        if st.session_state.uploaded_photo_info and st.session_state.uploaded_photo_info["type"]:
            if "png" in st.session_state.uploaded_photo_info["type"]:
                photo_ext = "png"
            elif "jpeg" in st.session_state.uploaded_photo_info["type"]:
                photo_ext = "jpeg"
        photo_name = f"photo_{farmer_name_for_filename}_{timestamp}.{photo_ext}"


        if st.button("Confirm and Save"):
            try:
                current_response_data = {
                    "Timestamp": timestamp,
                    "Surveyor Name": st.session_state.responses.get("surveyor_name")
                }
                for q_key in questions:
                    current_response_data[labels.get(q_key, f"Question {q_key}")] = st.session_state.responses.get(q_key)
                if "others_gender" in st.session_state.responses:
                    current_response_data["Others Gender Specify"] = st.session_state.responses.get("others_gender")
                else:
                    current_response_data["Others Gender Specify"] = ""

                new_row_df = pd.DataFrame([current_response_data])
                for col in new_row_df.columns:
                    if col not in st.session_state.all_survey_data.columns:
                        st.session_state.all_survey_data[col] = None
                st.session_state.all_survey_data = pd.concat([st.session_state.all_survey_data, new_row_df], ignore_index=True)
                
                st.session_state.all_survey_data.to_csv(SAVE_CSV_PATH, index=False, encoding='utf-8')

                if st.session_state.uploaded_photo_info:
                    photo_path = os.path.join(PHOTOS_DIR, photo_name)
                    with open(photo_path, "wb") as f:
                        f.write(st.session_state.uploaded_photo_info["data"])
                    st.success(f"Survey data recorded and photo saved successfully! 🎉 Your photo is saved as {photo_name}.")
                else:
                    st.success("Survey data recorded successfully! 🎉")

                st.session_state.responses = {}
                st.session_state.uploaded_photo_info = None
                st.session_state.form_submitted_for_review = False
                st.rerun()

            except Exception as e:
                st.error(f"An error occurred while saving: {e}")


st.markdown("---")
st.subheader("Admin Login (for Data Access)")

if not st.session_state.admin_logged_in:
    with st.form("admin_login_form"):
        admin_email = st.text_input("Admin Email").lower() 
        login_button = st.form_submit_button("Login")

        if login_button:
            if admin_email in ADMIN_USERS:
                st.session_state.admin_logged_in = True
                st.success("Admin login successful!")
                st.rerun() 
            else:
                st.error("Invalid email. Please use an authorized admin email.")
else:
    st.success(f"You are logged in as Admin ({st.session_state.get('last_admin_email', 'unknown')}).")
    if st.button("Logout"):
        st.session_state.admin_logged_in = False
        st.session_state.pop('last_admin_email', None) 
        st.rerun()


if st.session_state.admin_logged_in:
    st.markdown("---")
    st.subheader("Admin Download")

    def create_zip_archive(csv_data_buffer, photo_dir):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            zip_file.writestr("all_survey_responses.csv", csv_data_buffer.getvalue())

            for folder, _, files in os.walk(photo_dir):
                for file in files:
                    if file.endswith((".jpg", ".jpeg", ".png")):
                        file_path = os.path.join(folder, file)
                        zip_file.write(file_path, os.path.relpath(file_path, photo_dir))
        zip_buffer.seek(0)
        return zip_buffer.getvalue()

    if st.button("Download All Data (CSV & Photos)", key="download_all_admin"):
        if not st.session_state.all_survey_data.empty:
            csv_buffer = io.StringIO()
            st.session_state.all_survey_data.to_csv(csv_buffer, index=False, encoding='utf-8')
            csv_buffer.seek(0)

            zip_data = create_zip_archive(csv_buffer, PHOTOS_DIR)
            st.download_button(
                label="Click to Download ZIP",
                data=zip_data,
                file_name="all_survey_data.zip",
                mime="application/zip",
                key="download_button_admin"
            )
            st.success("Your data download is ready!")
        else:
            st.info("No survey data collected yet to download.")

    
    st.markdown("---")
    st.subheader("View Submitted Responses")

    if not st.session_state.all_survey_data.empty:
        st.write("Here are all the survey responses submitted so far:")
        st.dataframe(st.session_state.all_survey_data)

        search_term = st.text_input("Search responses (e.g., by Farmer Full Name or Mobile no.)", key="search_admin_view")
        if search_term:
            filtered_df = st.session_state.all_survey_data[
                st.session_state.all_survey_data.apply(
                    lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1
                )
            ]
            if not filtered_df.empty:
                st.write("Filtered Results:")
                st.dataframe(filtered_df)
            else:
                st.info("No matching responses found.")
    else:
        st.info("No survey responses have been submitted yet.")
