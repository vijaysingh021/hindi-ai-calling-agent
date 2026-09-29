import csv

def get_leads():
    leads = []
    with open('leads.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            leads.append(row)
    return leads

def update_lead(lead_id, status, result):
    leads = get_leads()
    fieldnames = ["ID", "Name", "Phone", "Language", "Status", "Result", "Notes", "Callback"]
    
    # CSV को नए डेटा के साथ वापस राइट (write) करना
    with open('leads.csv', mode='w', encoding='utf-8', newline='') as file:
        # यहाँ extrasaction='ignore' लगा दिया है ताकि एक्स्ट्रा कॉमा से एरर न आए
        writer = csv.DictWriter(file, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for lead in leads:
            if lead['ID'] == str(lead_id):
                lead['Status'] = status
                lead['Result'] = result
            writer.writerow(lead)
            
    print(f"[Database] Lead ID {lead_id} updated -> Status: {status}, Result: {result}")

if __name__ == "__main__":
    print("Reading leads...")
    print(get_leads())