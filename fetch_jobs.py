import firebase_admin
from firebase_admin import credentials, db
import requests
import time
import json
import os
from datetime import datetime

def initialize_firebase():
    """Initialize Firebase using env var or file-based service account."""
    service_account_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
    
    if service_account_json:
        service_account_dict = json.loads(service_account_json)
        cred = credentials.Certificate(service_account_dict)
    elif os.path.exists('serviceAccountKey.json'):
        cred = credentials.Certificate('serviceAccountKey.json')
    else:
        raise FileNotFoundError(
            "No Firebase credentials found. Set FIREBASE_SERVICE_ACCOUNT env var "
            "or place serviceAccountKey.json in the project root."
        )
    
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://job-india-55dd2-default-rtdb.firebaseio.com/'
    })

def fetch_and_update_jobs():
    print(f"[{datetime.now()}] Starting automated job fetch...")

    try:
        response = requests.get('https://remotive.com/api/remote-jobs?limit=5', timeout=30)
        response.raise_for_status()
        data = response.json()
        jobs = data.get('jobs', [])

        if not jobs:
            print("No jobs returned from API.")
            return

        for job_data in jobs:
            category = 'category_private'
            job_id = str(job_data.get('id'))

            job_object = {
                'job_id': job_id,
                'title': job_data.get('title'),
                'organization': job_data.get('company_name'),
                'state': 'Remote',
                'apply_link': job_data.get('url'),
                'posted_at': int(time.time() * 1000),
                'is_active': True
            }

            ref = db.reference(f'jobs/{category}/{job_id}')
            ref.set(job_object)
            print(f"Updated: {job_object['title']}")

        print(f"[{datetime.now()}] Successfully updated {len(jobs)} jobs.")

    except requests.exceptions.RequestException as e:
        print(f"Network error fetching jobs: {e}")
    except json.JSONDecodeError as e:
        print(f"Error parsing API response: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    initialize_firebase()
    fetch_and_update_jobs()
