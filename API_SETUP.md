# API Key Setup Instructions

## Problem
Your current Google Gemini API key ka free tier quota exceeded ho gaya. Aapko naya API key generate karna padega.

## Solution - Get Free API Key

### Step 1: Go to Google AI Studio
1. Visit: https://ai.google.dev/
2. Click "Get API Key" button
3. Click "Create API Key in new project" (if you don't have a project)

### Step 2: Copy the API Key
- The new API key will be shown
- Copy the entire key (starts with `AIza...`)

### Step 3: Update .env File
1. Open the `.env` file in this folder
2. Replace the old key with the new one:
```
GOOGLE_API_KEY=your_new_key_here
```
3. Save the file

### Step 4: Restart Your App
- Stop the Flask server (Ctrl+C)
- Run `python app.py` again

## If You Want Paid Tier (for Higher Limits)
1. Go to: https://console.cloud.google.com
2. Enable billing
3. Set up payment method
4. Your API calls will have higher quotas

## Important Notes
- Free tier resets daily
- Never share your API key publicly
- Store it in `.env` file (not in code)

## Troubleshooting
If API still doesn't work after adding new key:
1. Make sure `.env` file format is correct: `GOOGLE_API_KEY=your_key`
2. Restart Python/Flask completely
3. Check browser console for error messages
4. Use fallback knowledge base (already built in)
