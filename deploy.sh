
# Build the container image
gcloud builds submit --tag gcr.io/PROJECT-ID/resume-matcher

# Deploy to Cloud Run
gcloud run deploy resume-matcher \
  --image gcr.io/PROJECT-ID/resume-matcher \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
