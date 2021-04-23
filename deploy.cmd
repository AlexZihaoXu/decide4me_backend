#! /bin/sh

docker build -t gcr.io/decide4me-pegasis/server .
docker push gcr.io/decide4me-pegasis/server:latest
gcloud run deploy server --image=gcr.io/decide4me-pegasis/server:latest --allow-unauthenticated --platform=managed --service-account=firebase-adminsdk-262l9@decide4me-pegasis.iam.gserviceaccount.com --region=northamerica-northeast1 --project=decide4me-pegasis --cpu=1 --memory=512Mi --concurrency=10 --timeout=30