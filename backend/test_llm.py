import urllib.request
import json
import time

url = 'http://host.docker.internal:11434/api/generate'
payload = {
    'model': 'qwen2.5:3b',
    'prompt': "You are an expert PostgreSQL Database Administrator. Your job is to translate the user's natural language request into a single, valid PostgreSQL SQL statement. Do not include any explanations, markdown formatting, or SQL block backticks. Output ONLY the raw SQL string ending with a semicolon. Example output: UPDATE p_dtl_tb SET p_dba_nam = 'testname' WHERE p_sys_id = 3163961;\nRelevant tables based on your keywords: p_lic_cert_tb\nExact columns from the Enterprise Data Dictionary for the relevant tables:\n- Table p_lic_cert_tb: p_sys_id (Provider Internal System Identifier.), p_lic_cert_sk (License Certification Surrogate Key), p_lic_cert_cd (This represents the license or certification type.), p_lic_cert_num (This is the license, certification, or accreditation number.), p_lic_cert_beg_dt (The start date for the specific License or certification code.), p_lic_cert_end_dt (The end date for the specific License or certification code.)\n\nUser Request: Delete the record from p_lic_cert_tb where the license number is LIC-9999",
    'stream': False,
    'options': { 'temperature': 0.0, 'num_predict': 300, 'top_k': 10 }
}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

print("Sending POST request to Ollama...")
t0 = time.time()
try:
    resp = urllib.request.urlopen(req, timeout=120)
    t1 = time.time()
    result = json.loads(resp.read().decode("utf-8"))
    print(f"SUCCESS in {t1-t0:.2f}s!")
    print(f"Response: {result.get('response')}")
except Exception as e:
    t1 = time.time()
    print(f"FAILED in {t1-t0:.2f}s: {str(e)}")
