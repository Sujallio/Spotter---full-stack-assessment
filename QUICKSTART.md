# Quick Start Guide - ELD Trip Planner

## Windows Quick Setup

### Terminal 1 - Backend Setup
```bash
cd eld-app/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Backend will run at: http://localhost:8000

### Terminal 2 - Frontend Setup
```bash
cd eld-app/frontend
npm install
npm start
```

Frontend will open at: http://localhost:3000

## Testing the Application

### Sample Test Data

**From:** Los Angeles, CA
**To:** San Francisco, CA

1. Open http://localhost:3000
2. Fill in the form:
   - Current Location: Los Angeles, CA
   - Pickup Location: San Francisco, CA
   - Dropoff Location: Seattle, WA
   - Current Cycle Used: 5

3. Click "Calculate Route"
4. View the interactive map and ELD logs

## API Testing

Use Postman or curl:

```bash
curl -X POST http://localhost:8000/api/trips/calculate_route/ \
  -H "Content-Type: application/json" \
  -d '{
    "current_location": "Los Angeles, CA",
    "pickup_location": "San Francisco, CA",
    "dropoff_location": "Seattle, WA",
    "current_cycle_used": 5
  }'
```

## Deployment

### Deploy Backend to Railway

1. Create Railway account at railway.app
2. Connect GitHub repository
3. Set environment variables
4. Deploy

### Deploy Frontend to Vercel

1. Create Vercel account at vercel.com
2. Import GitHub repository
3. Update API endpoints
4. Deploy

## Troubleshooting

### CORS Issues
Make sure CORS is configured in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
]
```

### Port Already in Use
Change port:
```bash
# Django on different port
python manage.py runserver 8001

# React on different port
PORT=3001 npm start
```

### Dependencies Not Installing
```bash
# Clear cache and reinstall
pip install --force-reinstall -r requirements.txt
npm install --legacy-peer-deps
```

## Features to Demo

1. **Route Calculation** - Show how distances and times are calculated
2. **HOS Compliance** - Explain 70hr/8day and 11hr driving rules
3. **ELD Logs** - Show automatic log generation
4. **Map Integration** - Interactive map with multiple locations
5. **Responsive Design** - Works on desktop, tablet, mobile

## Video Script (3-5 minutes)

0:00-0:30 - Intro: "This is an ELD Trip Planner app for truck drivers"
0:30-1:30 - Show UI and features
1:30-2:30 - Enter sample data and calculate route
2:30-3:30 - Show map, stats, and ELD logs
3:30-4:30 - Code walkthrough (key components)
4:30-5:00 - Closing and GitHub link

## Loom Recording Tips

1. Record at 1080p or higher
2. Speak clearly about what you're doing
3. Show both the app and code
4. Explain HOS regulations briefly
5. Keep it under 5 minutes




username: admin
password: admin123