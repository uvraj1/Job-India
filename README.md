# Job India - Automated Job Scout

Automated GitHub Actions workflow that fetches remote job listings and syncs them to Firebase Realtime Database.

## How It Works

- Runs every hour via GitHub Actions cron schedule
- Fetches jobs from the Remotive API
- Pushes job data to Firebase Realtime Database (`jobs/category_private/`)
- Can also be triggered manually via the Actions tab

## Setup

### 1. Firebase Service Account

1. Go to [Firebase Console](https://console.firebase.google.com/) → Project Settings → Service Accounts
2. Generate a new private key (JSON)
3. In your GitHub repo, go to Settings → Secrets and variables → Actions
4. Add a secret named `FIREBASE_SERVICE_ACCOUNT` with the JSON content

### 2. Run Locally (Optional)

```bash
pip install -r requirements.txt

# Set the environment variable with your service account JSON
export FIREBASE_SERVICE_ACCOUNT='{"type":"service_account",...}'

python fetch_jobs.py
```

## Files

| File | Description |
|------|-------------|
| `fetch_jobs.py` | Main script that fetches jobs and pushes to Firebase |
| `requirements.txt` | Python dependencies |
| `.github/workflows/automation.yml` | GitHub Actions workflow for scheduled execution |
