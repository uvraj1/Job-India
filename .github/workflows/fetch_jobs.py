import firebase_admin
from firebase_admin import credentials, db
import requests
import time
from datetime import datetime

# 1. Firebase Initialization
# Make sure to download your serviceAccountKey.json from Firebase Console
# Settings -> Service Accounts -> Generate New Private Key
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://job-india-55dd2-default-rtdb.firebaseio.com/'
})

def fetch_and_update_jobs():
    print(f"[{datetime.now()}] Starting automated job fetch...")

    # Mocking a fetch from a public API (e.g., Remotive)
    # In a real scenario, you'd loop through your desired categories
    try:
        response = requests.get('https://remotive.com/api/remote-jobs?limit=5')
        data = response.json()
        jobs = data.get('jobs', [])

        for job_data in jobs:
            # Map API data to your structure
            category = 'category_private' # Default for this example
            job_id = str(job_data.get('id'))

            job_object = {
                'job_id': job_id,
                'title': job_data.get('title'),
                'organization': job_data.get('company_name'),
                'state': 'Remote',
                'apply_link': job_data.get('url'),
                'posted_at': int(time.time() * 1000), # Current Timestamp
                'is_active': True
            }

            # Push to Firebase
            ref = db.reference(f'jobs/{category}/{job_id}')
            ref.set(job_object)
            print(f"Updated: {job_object['title']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_update_jobs()
