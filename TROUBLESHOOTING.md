# Troubleshooting Contact Form - Google Sheets Integration

## Common Issues and Solutions

### 1. Error 500 - Server Configuration Error

**Problem**: Environment variables are missing or incorrectly formatted.

**Solution**:
- Go to Vercel Dashboard → Your Project → Settings → Environment Variables
- Ensure both variables are set:
  - `GOOGLE_SHEET_ID`: Just the ID (e.g., `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`)
  - `GOOGLE_SERVICE_ACCOUNT_KEY`: The entire JSON as a **single-line string**

**How to format GOOGLE_SERVICE_ACCOUNT_KEY**:
1. Open your service account JSON file
2. Copy the entire JSON content
3. In Vercel, paste it as a single line (remove all line breaks)
4. Or use this format in Vercel (it accepts multi-line, but single-line is safer):
   ```json
   {"type":"service_account","project_id":"...","private_key_id":"...","private_key":"...","client_email":"...","client_id":"...","auth_uri":"...","token_uri":"...","auth_provider_x509_cert_url":"...","client_x509_cert_url":"..."}
   ```

### 2. Error 500 - Permission Denied

**Problem**: Service account doesn't have access to the Google Sheet.

**Solution**:
1. Open your Google Sheet
2. Click **Share** button (top right)
3. Add the service account email (found in your JSON: `client_email` field)
4. Give it **Editor** permissions
5. Click **Send** (you can uncheck "Notify people")

### 3. Error 500 - Sheet Not Found

**Problem**: Wrong Sheet ID or sheet name.

**Solution**:
- **Get Sheet ID**: From URL `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
- **Check Sheet Name**: The default is `Sheet1`. If you renamed it, update line 41 in `api/submit-contact.js`:
  ```javascript
  range: 'YourSheetName!A:D', // Change Sheet1 to your actual sheet name
  ```

### 4. Testing Locally

**Note**: Vercel serverless functions only work when deployed to Vercel. They don't work in local Jekyll development.

**To test**:
1. Deploy to Vercel
2. Test the form on the live site
3. Check Vercel Function Logs: Dashboard → Your Project → Functions → View Logs

### 5. Check Function Logs

1. Go to Vercel Dashboard
2. Select your project
3. Go to **Functions** tab
4. Click on `api/submit-contact`
5. View **Logs** to see detailed error messages

### 6. Verify Environment Variables

In Vercel Dashboard → Settings → Environment Variables, verify:
- Variables are set for **Production** environment (or All)
- `GOOGLE_SHEET_ID` contains only the ID (no URL)
- `GOOGLE_SERVICE_ACCOUNT_KEY` is valid JSON (can test at jsonlint.com)

### 7. Common JSON Format Issues

If your service account key has newlines, Vercel might not parse it correctly. Try:
- Remove all line breaks
- Ensure it's valid JSON
- Escape quotes properly if pasting manually

### Quick Test

After fixing, test by:
1. Filling out the contact form
2. Submitting
3. Checking your Google Sheet for the new row
4. If error persists, check Vercel Function Logs for specific error message

