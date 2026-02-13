import re
import csv
import io

def process_recovery_data(input_content):
    # Regex for BATCH records (RN-CBL codes)
    rn_pattern = re.compile(r'RN-CBL-([\d]+).*?Batch-1.*?APS-[\d]+.*?([A-Z\s\.]{5,})', re.I)
    # Regex for LOG records (SME codes with dates)
    sme_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}).*?(SME-[\d-]+).*?([A-Z\s]{5,})', re.I)
    
    results = []
    lines = input_content.splitlines()
    
    for line in lines:
        # Check for RN-CBL records
        for match in rn_pattern.findall(line):
            results.append({'Type': 'PROJECT', 'Date': 'N/A', 'Code': match[0], 'Name': match[1].strip()})
        
        # Check for SME log records
        for match in sme_pattern.findall(line):
            results.append({'Type': 'TRANSACTION', 'Date': match[0], 'Code': match[1], 'Name': match[2].strip()})
            
    return results

# Standard execution for local testing
if __name__ == "__main__":
    with open('FULL_RECOVERY_DATABASE.csv', 'r', encoding='utf-8', errors='ignore') as f:
        data = process_recovery_data(f.read())
        
    with open('refined_output.csv', 'w', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=['Type', 'Date', 'Code', 'Name'])
        writer.writeheader()
        writer.writerows(data)
    print(f"Streamlined {len(data)} records.")
