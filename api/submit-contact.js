// Vercel Serverless Function to submit contact form to Google Sheets
// Requires: GOOGLE_SHEET_ID and GOOGLE_SERVICE_ACCOUNT_KEY environment variables

const { google } = require('googleapis');

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Get environment variables
    const sheetId = process.env.GOOGLE_SHEET_ID;
    const serviceAccountKey = process.env.GOOGLE_SERVICE_ACCOUNT_KEY;

    if (!sheetId || !serviceAccountKey) {
      console.error('Missing environment variables');
      return res.status(500).json({ error: 'Server configuration error' });
    }

    // Parse service account credentials
    const credentials = JSON.parse(serviceAccountKey);

    // Authenticate with Google Sheets API
    const auth = new google.auth.GoogleAuth({
      credentials: credentials,
      scopes: ['https://www.googleapis.com/auth/spreadsheets'],
    });

    const sheets = google.sheets({ version: 'v4', auth });

    // Get form data
    const { name, _replyto, message } = req.body;
    const email = _replyto || req.body.email || '';
    const timestamp = new Date().toISOString();

    // Append data to sheet
    await sheets.spreadsheets.values.append({
      spreadsheetId: sheetId,
      range: 'Sheet1!A:D', // Adjust range if your sheet name is different
      valueInputOption: 'USER_ENTERED',
      resource: {
        values: [[timestamp, name || '', email, message || '']],
      },
    });

    // Return success
    return res.status(200).json({
      success: true,
      message: 'Form submitted successfully',
    });
  } catch (error) {
    console.error('Error submitting to Google Sheets:', error);
    return res.status(500).json({
      error: 'Failed to submit form',
      message: error.message,
    });
  }
}

