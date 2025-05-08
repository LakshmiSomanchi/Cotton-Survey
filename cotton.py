import streamlit as st
import pandas as pd
import datetime
import os

# Set the directory to save responses
SAVE_DIR = "responses"
os.makedirs(SAVE_DIR, exist_ok=True)

st.set_page_config(page_title="Cotton Farming Questionnaire", layout="wide")
st.title("🌾 Cotton Farming Questionnaire (किसान सर्वे)")

language = st.selectbox(
    "Select Language / भाषा निवडा / ભાષા પસંદ કરો",
    ["English", "Hindi", "Marathi", "Gujarati"],
)

dict_translations = {
    "English": {
        "1": "Farmer Tracenet Code",
        "2": "Farmer Full Name",
        "3": "Mobile no.",
        "4": "Gender",
        "5": "Highest education",
        "6": "Village",
        "7": "Taluka/Block",
        "8": "District",
        "9": "State",
        "10": "Pincode",
        "11": "No. of males (adult) in household",
        "12": "No. of females (adult) in household",
        "13": "Children (<16) in household",
        "14": "Total Member of Household",
        "15": "No. of school-going children",
        "16": "No. of earning members in the family",
        "17": "Total Landholding (in acres)",
        "18": "Primary crop",
        "19": "Secondary crops",
        "20": "Non-organic Cotton land (in acre) (if any)",
        "21": "Organic Cotton land (in acre)",
        "22": "Years since practicing organic cotton (#)",
        "23": "Certification status (certified/IC1..)",
        "24": "Source of irrigation",
        "25": "Cultivable area (acre)",
        "26": "No. of cattle (cow and Buffalo)",
        "27": "Source of drinking water",
        "28": "Preferred selling point (Aggregator/Suminter/APMC/other Gin)",
        "29": "Has space for harvested cotton storage (Y/N)",
        "30": "Receives any agro advisory (Y/N)",
        "31": "Received any training on best practices for organic cotton?",
        "32": "Membership in FPO/FPC/SHG",
        "33": "Maintaining any Diary or Register for record keeping (Y/N)",
        "34": "Annual household income(in Rs)",
        "35": "Primary source of income",
        "36": "Secondary source of income",
        "37": "Income from Primary source (Rs.)",
        "38": "Certification cost per annum/acre",
        "39": "Avg. production of organic cotton/acre (Kg)",
        "40": "Cost of cultivation/acre (Rs)",
        "41": "Quantity sold of organic cotton (in kg)",
        "42": "Selling price per kg (Rs.)",
        "43": "Material cost for bio-inputs",
        "44": "Name of bio-input used for pest and disease management",
        "45": "Name of bio-fertilizer/compost used",
        "46": "No. of pheromone traps used / acre",
        "47": "Cost per pheromone trap",
        "48": "No. of Yellow sticky traps used / acre",
        "49": "Cost per yellow sticky trap",
        "50": "No. of Blue sticky traps used / acre",
        "51": "Cost per blue sticky trap",
        "52": "No. of bird perches used / acre",
        "53": "Irrigation cost/acre",
        "54": "No. of irrigation required for organic cotton",
        "55": "Irrigation method used",
        "56": "Any farm machinery hired (Y/N)",
        "57": "Cost of machinery hiring (Rs.)/acre",
        "58": "Local labour cost per day",
        "59": "Migrant labour cost per day",
        "60": "No. of workers required during sowing/acre",
        "61": "No. of workers required during harvesting/acre",
        "62": "Harvesting time (1st, 2nd & 3rd picking) (month)",
        "63": "Weeding method used (manual/mechanical)",
        "64": "Weeding cost/acre",
        "65": "Cost of mulching/acre",
        "66": "No. of tillage practiced",
        "67": "Tillage cost/acre",
        "68": "Land preparation cost/acre",
        "69": "Seed rate of organic cotton/acre",
        "70": "Variety of organic cotton seed (Name)",
        "71": "Name of border crop used",
        "72": "Name of the inter crop used",
        "73": "Name of cover crop",
        "74": "Name of trap crop",
        "75": "Mulching used (Y/N)",
        "76": "Type of mulching used (Bio-plastic/green/dry)",
        "77": "What precautions used during storage",
        "78": "Hired vehicle used for transportation of seed cotton (Y/N)",
        "79": "Transportation cost (Rs.)/Kg of seed cotton",
        "80": "Any quantity rejection due to contamination/impurities (Kg)",
        "81": "Price discovery mechanism",
        "82": "Payment Transaction type (Cash/online)",
        "83": "Days of credit after sell",
        "84": "Availing any govt. scheme or subsidy benefits (Y/N)",
        "85": "Opted for crop insurance (Y/N)",
        "86": "Cost of crop insurance per acre",
        "87": "Possess KCC (Y/N)",
        "88": "Possess active bank account (Y/N)",
        "89": "Crop rotation used (Y/N)",
        "90": "Crops used for rotation",
        "91": "Using any water tracking devices (Y/N)",
        "92": "Capacity of pump (in HP)",
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
        "1": "किसान ट्रेसेनेट कोड",
        "2": "किसान का पूरा नाम",
        "3": "मोबाइल नंबर",
        "4": "लिंग",
        "5": "उच्चतम शिक्षा",
        "6": "गाँव",
        "7": "तालुका/ब्लॉक",
        "8": "जिला",
        "9": "राज्य",
        "10": "पिनकोड",
        "11": "घर में पुरुषों (वयस्क) की संख्या",
        "12": "घर में महिलाओं (वयस्क) की संख्या",
        "13": "घर में बच्चे (<16)",
        "14": "परिवार के कुल सदस्य",
        "15": "स्कूल जाने वाले बच्चों की संख्या",
        "16": "परिवार में कमाने वाले सदस्यों की संख्या",
        "17": "कुल भूमि जोत (एकड़ में)",
        "18": "प्राथमिक फसल",
        "19": "द्वितीयक फसलें",
        "20": "गैर-जैविक कपास भूमि (एकड़ में) (यदि कोई हो)",
        "21": "जैविक कपास भूमि (एकड़ में)",
        "22": "जैविक कपास का अभ्यास करने के बाद से वर्ष (#)",
        "23": "प्रमाणीकरण स्थिति (प्रमाणित/IC1..)",
        "24": "सिंचाई का स्रोत",
        "25": "कृषि योग्य क्षेत्र (एकड़)",
        "26": "मवेशियों की संख्या (गाय और भैंस)",
        "27": "पीने के पानी का स्रोत",
        "28": "पसंदीदा बिक्री बिंदु (एग्रीगेटर/सुमिंटर/एपीएमसी/अन्य जिन)",
        "29": "कटी हुई कपास भंडारण के लिए जगह है (हाँ/नहीं)",
        "30": "कोई कृषि सलाहकार प्राप्त होता है (हाँ/नहीं)",
        "31": "क्या जैविक कपास के लिए सर्वोत्तम प्रथाओं पर कोई प्रशिक्षण प्राप्त हुआ है?",
        "32": "एफपीओ/एफपीसी/एसएचजी में सदस्यता",
        "33": "रिकॉर्ड रखने के लिए कोई डायरी या रजिस्टर बनाए रखना (हाँ/नहीं)",
        "34": "वार्षिक घरेलू आय (रुपये में)",
        "35": "आय का प्राथमिक स्रोत",
        "36": "आय का द्वितीयक स्रोत",
        "37": "प्राथमिक स्रोत से आय (रु.)",
        "38": "प्रति वर्ष/एकड़ प्रमाणीकरण लागत",
        "39": "जैविक कपास/एकड़ का औसत उत्पादन (किलो)",
        "40": "प्रति एकड़ खेती की लागत (रु)",
        "41": "जैविक कपास की बेची गई मात्रा (किलो में)",
        "42": "प्रति किलो विक्रय मूल्य (रु.)",
        "43": "जैव-इनपुट के लिए सामग्री लागत",
        "44": "कीट और रोग प्रबंधन के लिए उपयोग किए जाने वाले जैव-इनपुट का नाम",
        "45": "उपयोग किए जाने वाले जैव-उर्वरक/खाद का नाम",
        "46": "फेरोमोन जाल का उपयोग / एकड़",
        "47": "प्रति फेरोमोन जाल लागत",
        "48": "पीले चिपचिपे जाल का उपयोग / एकड़",
        "49": "प्रति पीले चिपचिपे जाल लागत",
        "50": "नीले चिपचिपे जाल का उपयोग / एकड़",
        "51": "प्रति नीले चिपचिपे जाल लागत",
        "52": "पक्षी पर्च का उपयोग / एकड़",
        "53": "सिंचाई लागत/एकड़",
        "54": "जैविक कपास के लिए आवश्यक सिंचाई की संख्या",
        "55": "सिंचाई विधि का उपयोग किया गया",
        "56": "क्या कोई कृषि मशीनरी किराए पर ली गई है (हाँ/नहीं)",
        "57": "मशीनरी किराए पर लेने की लागत (रु.)/एकड़",
        "58": "स्थानीय श्रम लागत प्रति दिन",
        "59": "प्रवासी श्रम लागत प्रति दिन",
        "60": "बुवाई के दौरान आवश्यक श्रमिकों की संख्या/एकड़",
        "61": "कटाई के दौरान आवश्यक श्रमिकों की संख्या/एकड़",
        "62": "कटाई का समय (1st, 2nd और 3rd पिकिंग) (महीना)",
        "63": "खरपतवार विधि का उपयोग किया गया (मैनुअल/मैकेनिकल)",
        "64": "खरपतवार लागत/एकड़",
        "65": "पलवार लागत/एकड़",
        "66": "जुताई का अभ्यास किया गया",
        "67": "जुताई लागत/एकड़",
        "68": "भूमि तैयारी लागत/एकड़",
        "69": "सेंद्रिय कापसाचा बियाणे दर/एकर",
        "70": "सेंद्रिय कपास बियाण्याची जात (नाव)",
        "71": "उपयोग केलेल्या बॉर्डर पिकाचे नाव",
        "72": "उपयोग केलेल्या आंतरपिकाचे नाव",
        "73": "कवर पाकाचे नाव",
        "74": "ट्रैप फसलाचे नाव",
        "75": "आच्छादन का उपयोग किया गया (हाँ/नहीं)",
        "76": "आच्छादन के प्रकार का उपयोग किया गया (जैव-प्लास्टिक/हरा/सूखा)",
        "77": "भंडारण के दौरान क्या सावधानियां बरती जाती हैं",
        "78": "बीज कपास के परिवहन के लिए किराए पर वाहन का उपयोग किया जाता है (हाँ/नहीं)",
        "79": "परिवहन लागत (रु.)/बीज कपास का किलो",
        "80": "प्रदूषण/अशुद्धियों के कारण कोई मात्रा अस्वीकृति (किलो)",
        "81": "मूल्य खोज तंत्र",
        "82": "भुगतान लेनदेन प्रकार (नकद/ऑनलाइन)",
        "83": "बेचने के बाद क्रेडिट के दिन",
        "84": "किसी भी सरकारी योजना या सब्सिडी लाभ का लाभ उठाना (हाँ/नहीं)",
        "85": "फसल बीमा के लिए चुना गया (हाँ/नहीं)",
        "86": "फसल बीमा की लागत प्रति एकड़",
        "87": "केसीसी है (हाँ/नहीं)",
        "88": "सक्रिय बैंक खाता है (हाँ/नहीं)",
        "89": "फसल रोटेशन का उपयोग किया गया (हाँ/नहीं)",
        "90": "रोटेशन के लिए उपयोग की जाने वाली फसलें",
        "91": "क्या किसी जल ट्रैकिंग डिवाइस का उपयोग किया जा रहा है (हाँ/नहीं)",
        "92": "पंप की क्षमता (एचपी में)",
        "93": "बफर जोन बनाए रखना (हाँ/नहीं)",
        "94": "फसल अवशेष का उपयोग (ईंधन/पशु चारा/बायोचार/इन-सीटू कंपोस्टिंग/जलाना)",
        "95": "श्रमिकों को भुगतान का तरीका (नकद/ऑनलाइन)",
        "96": "पुरुष और महिला श्रमिकों के लिए कोई वेतन अंतर (हाँ/नहीं)",
        "97": "क्या किसी श्रम रजिस्टर का उपयोग किया जा रहा है (हाँ/नहीं)",
        "98": "श्रमिकों के लिए सुरक्षा-किट/प्राथमिक चिकित्सा की कोई व्यवस्था",
        "99": "श्रमिकों के लिए आश्रय और सुरक्षित पेयजल का कोई प्रावधान",
        "100": "श्रमिकों के लिए शौचालय का कोई प्रावधान",
        "101": "कृषि कार्यों में परिवार के सदस्यों (महिलाओं) को शामिल करना",
        "102": "कोई सामुदायिक जल संचयन संरचना (हाँ/नहीं)",
        "103": "मृदा नमी मीटर का उपयोग (हाँ/नहीं)",
    },
    "Marathi": {
        "1": "शेतकरी ट्रेसनेट कोड",
        "2": "शेतकऱ्याचे पूर्ण नाव",
        "3": "मोबाईल नंबर",
        "4": "लिंग",
        "5": "उच्चतम शिक्षण",
        "6": "गाव",
        "7": "तालुका/ब्लॉक",
        "8": "जिल्हा",
        "9": "राज्य",
        "10": "पिनकोड",
        "11": "घरातील पुरुषांची (प्रौढ) संख्या",
        "12": "घरातील महिलांची (प्रौढ) संख्या",
        "13": "घरातील मुले (<16)",
        "14": "घरातील एकूण सदस्य",
        "15": "शाळेत जाणाऱ्या मुलांची संख्या",
        "16": "कुटुंबातील कमावत्या सदस्यांची संख्या",
        "17": "एकूण जमिनीची मालकी (एकरमध्ये)",
        "18": "प्राथमिक पीक",
        "19": "दुय्यम पिके",
        "20": "गैर-सेंद्रिय कापूस जमीन (एकरमध्ये) (असल्यास)",
        "21": "सेंद्रिय कापूस जमीन (एकरमध्ये)",
        "22": "सेंद्रिय कापूस लागवडीपासूनची वर्षे (#)",
        "23": "प्रमाणीकरण स्थिती (प्रमाणित/IC1..)",
        "24": "सिंचनाचा स्रोत",
        "25": "कृषि योग्य क्षेत्र (एकर)",
        "26": "जनावरांची संख्या (गाय आणि म्हैस)",
        "27": "पिण्याच्या पाण्याचे स्रोत",
        "28": "पसंतीचे विक्री केंद्र (एग्रीगेटर/सुमिंटर/एपीएमसी/इतर जिन)",
        "29": "कापणी केलेल्या कापसाच्या साठवणुकीसाठी जागा आहे (होय/नाही)",
        "30": "कोणताही कृषी सल्ला मिळतो (होय/नाही)",
        "31": "सेंद्रिय कापसासाठी सर्वोत्तम पद्धतींवर कोणतेही प्रशिक्षण मिळाले आहे का?",
        "32": "एफपीओ/एफपीसी/एसएचजी मध्ये सदस्यता",
        "33": "नोंद ठेवण्यासाठी कोणतीही डायरी किंवा रजिस्टर ठेवणे (होय/नाही)",
        "34": "वार्षिक घरगुती उत्पन्न (रुपयांमध्ये)",
        "35": "उत्पन्नाचा प्राथमिक स्रोत",
        "36": "उत्पन्नाचा दुय्यम स्रोत",
        "37": "प्राथमिक स्रोताकडून उत्पन्न (रु.)",
        "38": "प्रति वर्ष/एकर प्रमाणीकरण खर्च",
        "39": "सेंद्रिय कापूस/एकरचे सरासरी उत्पादन (किलो)",
        "40": "प्रति एकर लागवडीचा खर्च (रु.)",
        "41": "सेंद्रिय कापसाची विक्री केलेली मात्रा (किलोमध्ये)",
        "42": "प्रति किलो विक्री किंमत (रु.)",
        "43": "जैव-इनपुटसाठी सामग्री खर्च",
        "44": "कीड आणि रोग व्यवस्थापनासाठी वापरल्या जाणाऱ्या जैव-इनपुटचे नाव",
        "45": "वापरल्या जाणाऱ्या जैव-खत/खादचे नाव",
        "46": "फेरोमोन सापळे वापरले / एकर",
        "47": "प्रति फेरोमोन सापळा खर्च",
        "48": "पिवळे चिकट सापळे वापरले / एकर",
        "49": "प्रति पिवळा चिकट सापळा खर्च",
        "50": "निळे चिकट सापळे वापरले / एकर",
        "51": "प्रति निळा चिकट सापळा खर्च",
        "52": "पक्षी थांबे वापरले / एकर",
        "53": "सिंचन खर्च/एकर",
        "54": "सेंद्रिय कापसासाठी आवश्यक सिंचनाची संख्या",
        "55": "वापरलेली सिंचन पद्धत",
        "56": "कोणतीही शेती अवजारे भाड्याने घेतली आहेत (होय/नाही)",
        "57": "अवजारे भाड्याने घेण्याचा खर्च (रु.)/एकर",
        "58": "स्थानिक मजुरीचा दर प्रति दिवस",
        "59": "स्थलांतरित मजुरीचा दर प्रति दिवस",
        "60": "वावणीच्या वेळी आवश्यक कामगारांची संख्या/एकर",
        "61": "कापणीच्या वेळी आवश्यक कामगारांची संख्या/एकर",
        "62": "कापणीची वेळ (1 ली, 2 री आणि 3 री निवड) (महिना)",
        "63": "तण काढण्याची पद्धत वापरली (हाताने/यांत्रिक)",
        "64": "तण काढण्याचा खर्च/एकर",
        "65": "आच्छादन खर्च/एकर",
        "66": "किती वेळा नांगरणी केली",
        "67": "नांगरणी खर्च/एकर",
        "68": "जमीन तयार करण्याचा खर्च/एकर",
        "69": "प्रति एकर सेंद्रिय बियाण्याचा खर्च",
        "70": "सेंद्रिय कापसाचा बियाणे दर/एकर",
        "71": "सेंद्रिय कापसाच्या बियाण्याची जात (नाव)",
        "72": "सेंद्रिय कापसाच्या बोडर पाकाचे नाव",
        "73": "सेंद्रिय कापसाच्या आंतर पाकाचे नाव",
        "74": "कवर पाकाचे नाव",
        "75": "मल्चिंग वापरले (होय/नाही)",
        "76": "वापरलेल्या मल्चिंगचा प्रकार (जैव-प्लास्टिक/लीरो/कोरडा)",
        "77": "साठवणुकीदरम्यान कोणती खबरदारी घेतली जाते",
        "78": "बीज कपासाच्या वाहतुकीसाठी भाड्याचे वाहन वापरले (होय/नाही)",
        "79": "वाहतूक खर्च (रु.)/बीज कपासाचे किलो",
        "80": "प्रदूषण/अशुद्धतेमुळे कोणतीही मात्रा नाकारली (किलो)",
        "81": "किंमत शोधण्याची यंत्रणा",
        "82": "चुकवणी व्यवहार प्रकार (रोख/ऑनलाइन)",
        "83": "विक्री केल्यानंतर क्रेडिटचे दिवस",
        "84": "किसान योजना किंवा अनुदानाचा लाभ घेणे (होय/नाही)",
        "85": "पाक विमा घेतला (होय/नाही)",
        "86": "प्रति एकर पाक विमा खर्च",
        "87": "केसीसी आहे (होय/नाही)",
        "88": "सक्रिय बँक खाते आहे (होय/नाही)",
        "89": "पाक परिभ्रमण वापरले (होय/नाही)",
        "90": "परिभ्रमणासाठी वापरलेली पिके",
        "91": "कोणतेही जल ट्रॅकिंग उपकरण वापरत आहात (होय/नाही)",
        "92": "पंपाची क्षमता (एचपी मध्ये)",
        "93": "बफर झोन जाळणे (होय/नाही)",
        "94": "पाक अवशेषांचा वापर (इंधन/जनावरांचे खाद्य/बायोचार/इन-सीटू कंपोस्टिंग/जलाना)",
        "95": "कामगारांना देयकाची पद्धत (रोख/ऑनलाइन)",
        "96": "पुरुष आणि महिला कामगारांसाठी कोणताही वेतन तफावत (होय/नाही)",
        "97": "कोणतेही कामगार रजिस्टर वापरत आहात (होय/नाही)",
        "98": "कामगारांसाठी सुरक्षा-किट/प्राथमिक उपचारांची कोणतीही व्यवस्था",
        "99": "कामगारांसाठी निवारा आणि सुरक्षित पिण्याच्या पाण्याची कोणतीही तरतूद",
        "100": "कामगारांसाठी शौचालयाची कोणतीही तरतूद",
        "101": "कृषी कार्यांमध्ये कुटुंबातील सदस्यांना (महिलांना) सामील करणे",
        "102": "कोणतीही सामुदायिक जल संचयन रचना (होय/नाही)",
        "103": "माती भिजवणारे मीटर वापरणे (होय/नाही)",
    },
   "Gujarati": {
        "1": "ખેડૂત ટ્રેસનેટ કોડ",
        "2": "ખેડૂતનું પૂરું નામ",
        "3": "મોબાઇલ નંબર",
        "4": "લિંગ",
        "5": "કેટલો અભ્યાસ કરેલો છે",
        "6": "ગામ",
        "7": "તાલુકો/બ્લોક",
        "8": "જિલ્લો",
        "9": "રાજ્ય",
        "10": "પિનકોડ",
        "11": "ઘરમાં પુરુષોની (પુખ્ત) સંખ્યા",
        "12": "ઘરમાં મહિલાઓની (પુખ્ત) સંખ્યા",
        "13": "ઘરમા બાળકોની સંખ્યા (૧૬ થી ઓછી ઉમરના )",
        "14": "પરિવારના કુલ સભ્યો",
        "15": "શાળાએ જતા બાળકોની સંખ્યા",
        "16": "પરિવારમાં કમાતા સભ્યની સંખ્યા",
        "17": "કુલ જમીન ધારણ (એકરમાં)",
        "18": "મુખ્ય પાક",
        "19": "ગૌણ પાક",
        "20": "બિન-ઓર્ગેનિક કપાસની જમીન (એકરમાં)",
        "21": "ઓર્ગેનિક કપાસની જમીન (એકરમાં)",
        "22": "ઓર્ગનીક કપાસની ખેતી કેટલા વર્ષથી કરો છો",
        "23": "સર્ટિફિકેસન સ્ટેટસ  (સર્ટિફાઇડ/IC-1,2,3)",
        "24": "સિંચાઈનો સ્ત્રોત",
        "25": "ખેતીલાયક વિસ્તાર (એકર)",
        "26": "ઢોરની સંખ્યા (ગાય અને ભેંસ)",
        "27": "પીવાના પાણીનો સ્ત્રોત",
        "28": "પસંદગીનું વેચાણ સ્થળ (એગ્રીગેટર/સુમિન્ટર/એપીએમસી/અન્ય જીન)",
        "29": "વીણી કરેલા કપાસના સંગ્રહ માટે જગીયા છે",
        "30": "કોઈ પણ ખેતી સંબધિત સલાહ મળે છે",
        "31": "શું ઓર્ગેનિક કપાસ માટેની શ્રેષ્ઠ પદ્ધતિ  પર કોઈ તાલીમ મળી છે",
        "32": "એફપીઓ/એફપીસી/એસએચજીમાં સભ્યપદ ધરાવો છો",
        "33": "રેકોર્ડ રાખવા માટે કોઈ ડાયરી અથવા રજિસ્ટર જાળવો છો",
        "34": "વાર્ષિક ઘરગથ્થુ આવક (રૂપિયામાં)",
        "35": "આવકનો પ્રાથમિક સ્ત્રોત",
        "36": "આવકનો ગૌણ સ્ત્રોત",
        "37": "પ્રાથમિક સ્ત્રોતમાંથી આવક (રૂ.)",
        "38": "સર્ટિફિકેસન ખર્ચ પ્રતિ વર્ષ/એકર",
        "39": "ઓર્ગનીક કપાસનું સરેરાશ ઉત્પાદન (કિલો/એકર)",
        "40": "ખેતીનો ખર્ચ (રૂપીયા/એકર)",
        "41": "ઓર્ગેનિક કપાસનો વેચાણ કરેલો જથ્થો (કિલોમાં)",
        "42": "વેચાણ કિંમત પ્રતિ કિલો (રૂ.)",
        "43": "બાયો-ઇનપુટ્સ માટે સામગ્રી ખર્ચ",
        "44": "જંતુ અને રોગ વ્યવસ્થાપન માટે વપરાતા બાયો-ઇનપુટનું નામ",
        "45": "વપરાતા બાયો-ખત/ખાદનું નામ",
        "46": "બાયો-ખત/ખાદનો ડોઝ વપરાય છે/એકર",
        "47": "ફેરોમોન ટ્રેપનો ઉપયોગ / એકર",
        "48": "ખર્ચ પ્રતિ ફેરોમોન ટ્રેપ",
        "49": "પીળા સ્ટીકી ટ્રેપનો ઉપયોગ / એકર",
        "50": "ખર્ચ પ્રતિ પીળો સ્ટીકી ટ્રેપ",
        "51": "ખર્ચ પ્રતિ વાદળી સ્ટીકી ટ્રેપ",
        "52": "પક્ષી સ્ટેન્ડનો ઉપયોગ પ્રતિ એકર",
        "53": "સિંચાઈ ખર્ચ/એકર",
        "54": "સિંચાઈ ખર્ચ/એકર",
        "55": "ઓર્ગેનિક કપાસ માટે જરૂરી સિંચાઈની સંખ્યા",
        "56": "વપરાયેલી સિંચાઈ પદ્ધતિ",
        "57": "કોઈપણ ખેતી મશીનરી ભાડે લીધી છે (હા/ના)",
        "58": "મશીનરી ભાડે લેવાનો ખર્ચ (રૂ.)",
        "59": "સ્થાનિક મજૂરી ખર્ચ પ્રતિ દિવસ",
        "60": "સ્થળાંતરિત મજૂરી ખર્ચ પ્રતિ દિવસ",
        "61": "વાવણીના સમયે જરૂરી કામદારોની સંખ્યા/એકર",
        "62": "વીણી સમય (1 લી, 2 જી અને 3 જી વીણીનો મહિનો)",
        "63": "નિંદામણ પદ્ધતિનો પ્રકાર (હાથ વડે /સાધન દ્વારા)",
        "64": "નિંદામણ પદ્ધતિનો ઉપયોગ કર્યો (મેન્યુઅલ/મિકેનિકલ)",
        "65": "નિંદામણ ખર્ચ/એકર",
        "66": "કેટલી વખત ખેડ કરો છો",
        "67": "ખેડ ખર્ચ/એકર",
        "68": "જમીન તૈયારી ખર્ચ/એકર",
        "69": "ઓર્ગનિકં કપાસનો બીજનો દર/એકર",
        "70": "ઓર્ગનિકં કપાસના બીજની જાતનું નામ",
        "71": "બોર્ડર પાકનું નામ",
        "72": "આંતરપાકનું નામ",
        "73": "કવર પાકનું નામ",
        "74": "ટ્રેપ પાકનું નામ",
        "75": "મલ્ચિંગ વાપરો છે (હા/ના)",
        "76": "વપરાયેલા મલ્ચિંગનો પ્રકાર (જૈવ-પ્લાસ્ટિક/લીલો/સૂકો)",
        "77": "સંગ્રહ દરમિયાન શું સાવચેતીઓ રાખો છો",
        "78": "વીણી કરેલા કપાસના પરિવહન માટે ભાડે લીધેલ વાહન વપરાય છે (હા/ના)",
        "79": "પરિવહન ખર્ચ  રૂપિયા/કિલો",
        "81": "કપાસના ભાવ જાણવાની ની રીત",
        "82": "ચુકવણી વ્યવહારનો  પ્રકાર (રોકડા/ઓનલાઇન)",
        "83": "વેચાણ કર્યા પછી કેટલા દિવસોમાં રૂપીયા મળે છે",
        "84": "કોઈપણ સરકારી યોજના અથવા સબસીડીનો લાભ મળે છે  (હા/ના)",
        "85": "પાક વીમો ઉતારો છો  (હા/ના)",
        "86": "કોઈપણ સરકારી યોજના અથવા અનુદાન લાભો મેળવવા (હા/ના)",
        "87": "કિશાન ક્રેડિટ કાર્ડ છે (હા/ના)",
        "88": "દર એકર પાક વીમાનો ખર્ચ",
        "89": "પાક ફેરબદલી કરો છો (હા/ના)",
        "90": "પાક ફેરબદલી માટે વપરાતા પાક",
        "91": "બૅંકમાંથી કોઈપણ કૃષિ લોન (હા/ના)",
        "92": "કૂવા કે બોરવેલના પંકીની ક્ષમતા (એચપીમાં)",
        "93": "બફર ઝોન જાળવો છો  (હા/ના)",
        "94": "પાકના અવશેષોનો ઉપયોગ (બળતણ/પશુઓનો ખોરાક/બાયોચાર/જમીનમાં ભેળવવું/સળગાવવું/કંપોસ્ટ)",
        "95": "કામદારને ચૂકવણીની પદ્ધતિ (રોકડા/ઓનલાઇન)",
        "96": "પંપની ક્ષમતા (એચપીમાં)",
        "97": "બફર ઝોન જાળવવું (હા/ના)",
        "98": "પાકના અવશેષોનો ઉપયોગ (ઇંધન/જનાવરોનું ખોરાક/બાયોચાર/ઇન-સિટુ કમ્પોસ્ટિંગ/જળાવવું)",
        "99": "કામદારોને ચુકવણીની રીત (રોમ/ઓનલાઇન)",
        "100": "પુરુષ અને મહિલા કામદારો માટે કોઈપણ વેતન તફાવત (હા/ના)",
        "101": "પરિવારના કેટલી મહિલાઓ ખેતીકાર્ય સાથે જોડાયેલ છે",
        "102": "કામદારો માટે સલામતી-કીટ/પ્રાથમિક સારવારની કોઈપણ વ્યવસ્થા",
        "103": "માટી ભેજ મીટરનો ઉપયોગ (હા/ના)"
    },
}

# Define the questions using the keys from the dictionary
questions = [str(i) for i in range(1, 104)]  # Create a list of strings from "1" to "103"

# Get the translations for the selected language
labels = dict_translations.get(language, dict_translations["English"])

responses = {}

with st.form("questionnaire_form"):
    for question_key in questions:
        # Use the translated label for the question
        question_text = labels.get(
            question_key, f"Question {question_key} (No translation)"
        )

        # Define dropdown options for specific questions
        if question_key == "4":  # Gender
            responses[question_key] = st.selectbox(question_text, ["Male", "Female", "Others"])
            if responses[question_key] == "Others":
                responses["others_gender"] = st.text_input("If selected Others, please specify:")
        elif question_key == "24":  # Source of irrigation
            responses[question_key] = st.selectbox(question_text, ["Canal", "Well", "Borewell", "River", "Farm Pond", "Community Pond", "Rain-fed not irrigated"])
        elif question_key in ["29", "30", "33", "56", "75", "78", "84", "85", "87", "88", "89", "91", "93", "96", "97", "102", "103"]:  # Y/N Questions
            responses[question_key] = st.selectbox(question_text, ["Yes", "No"])
        elif question_key in ["62", "64", "65", "68", "69", "70", "71", "72", "73", "74", "80", "82", "83", "94", "95"]:  # Other specific questions
            responses[question_key] = st.text_input(question_text)
        elif question_key == "55":  # Irrigation method
            responses[question_key] = st.selectbox(question_text, ["Drip irrigation", "Sprinkler irrigation", "Flood irrigation", "Ridge and Furrow Irrigation", "Other"])
        elif question_key == "62":  # Harvesting time
            responses[question_key] = st.text_input(question_text, placeholder="e.g., month 1, month 2, month 3")
            # Validate comma-separated entries
            if responses[question_key]:
                months = responses[question_key].split(',')
                if len(months) != 3:
                    st.error("Please enter exactly three months separated by commas.")
        else:
            responses[question_key] = st.text_input(question_text)
            
    # Add an option to upload a photo
    uploaded_file = st.file_uploader("Upload a photo of your farm or crops", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        responses["uploaded_photo"] = uploaded_file.name
        submitted = st.form_submit_button("Submit")
        
responses["3"] = st.text_input("Mobile no.", max_chars=10)  # Assuming "3" is the key for phone number

# Data Validation
if submitted:
    # Check for required fields
    required_fields = ["1", "2", "3", "4", "6", "8", "9", "10", "34", "35", "37", "39", "41", "42"]
    for field in required_fields:
        if not responses.get(field):
            st.error(f"Field '{labels[field]}' is required.")
            break
    else:
        # Validate phone number length
        phone_number = responses.get("3")
        if phone_number and (len(phone_number) != 10 or not phone_number.isdigit()):
            st.error("Mobile no. must be exactly 10 digits.")
        else:
            # Validate numeric fields
            numeric_fields = ["11", "12", "13", "14", "15", "16", "17", "34", "37", "39", "41"]
            for field in numeric_fields:
                if not str(responses.get(field)).isdigit() or int(responses.get(field)) < 0:
                    st.error(f"Field '{labels[field]}' must be a non-negative number.")
                    break
            else:
                # If all validations pass, save the data
                now = datetime.datetime.now()

                # Use English labels for CSV headers
                english_labels = dict_translations["English"]
                data = {english_labels.get(k, k): v for k, v in responses.items() if k in english_labels}

                # Include any non-question keys like 'uploaded_photo'
                for k in responses:
                    if k not in english_labels:
                        data[k] = responses[k]

                df = pd.DataFrame([data])
                filename = f"survey_{now.strftime('%Y%m%d_%H%M%S')}.csv"
                df.to_csv(os.path.join(SAVE_DIR, filename), index=False, encoding='utf-8')
                st.success("✅ Survey Submitted and Saved!")


st.divider()
st.header("🔐 Admin Real-Time Access")

# Allowed Emails
ALLOWED_EMAILS = ["shifalis@tns.org", "rmukherjee@tns.org", "rsomanchi@tns.org", "mkaushal@tns.org", "bkharoo@tns.org", "rladdha@tns.org"]
admin_email = st.text_input("Enter your Admin Email to unlock extra features:")

if admin_email in ALLOWED_EMAILS:
    st.success("✅ Admin access granted! Real-time view enabled.")
else:
    if admin_email:
        st.error("❌ Not an authorized admin.")

if st.checkbox("📄 View Past Submissions"):
    files = [f for f in os.listdir(SAVE_DIR) if f.endswith('.csv')]
    if files:
        all_data = pd.concat([pd.read_csv(os.path.join(SAVE_DIR, f)) for f in files], ignore_index=True)
        st.dataframe(all_data)

        csv = all_data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download All Responses",
            data=csv,
            file_name='all_survey_responses.csv',
            mime='text/csv',
            key='public_csv_download'
        )
    else:
        st.warning("⚠️ No submissions found yet.")
