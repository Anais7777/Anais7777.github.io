// Vercel Serverless Function to submit contact form to Google Sheets
// Requires: GOOGLE_SHEET_ID and GOOGLE_SERVICE_ACCOUNT_KEY environment variables

const { google } = require('googleapis');

module.exports = async (req, res) => {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Get environment variables
    const sheetId = process.env.GOOGLE_SHEET_ID;
    const serviceAccountKey = process.env.GOOGLE_SERVICE_ACCOUNT_KEY;

    if (!sheetId || !serviceAccountKey) {
      console.error('Missing environment variables:', {
        hasSheetId: !!sheetId,
        hasServiceAccountKey: !!serviceAccountKey
      });
      return res.status(500).json({ 
        error: 'Server configuration error',
        message: 'Missing required environment variables'
      });
    }

    // Parse service account credentials
    let credentials;
    try {
      credentials = typeof serviceAccountKey === 'string' 
        ? JSON.parse(serviceAccountKey) 
        : serviceAccountKey;
    } catch (parseError) {
      console.error('Error parsing service account key:', parseError);
      return res.status(500).json({ 
        error: 'Invalid service account key format',
        message: parseError.message
      });
    }

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

    // First, try to get the sheet metadata to verify access and get sheet name
    let sheetName = 'Sheet1'; // Default sheet name
    try {
      const spreadsheet = await sheets.spreadsheets.get({
        spreadsheetId: sheetId,
      });
      // Get the first sheet's name
      if (spreadsheet.data.sheets && spreadsheet.data.sheets.length > 0) {
        sheetName = spreadsheet.data.sheets[0].properties.title;
      }
    } catch (metaError) {
      console.error('Error getting sheet metadata:', metaError);
      // Continue with default Sheet1 name - might be a permissions issue
    }

    // Append data to sheet
    // Use range that covers all 4 columns (Timestamp, Name, Email, Message)
    const range = `${sheetName}!A1:D1`;
    
    await sheets.spreadsheets.values.append({
      spreadsheetId: sheetId,
      range: range,
      valueInputOption: 'USER_ENTERED',
      insertDataOption: 'INSERT_ROWS',
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
      details: process.env.NODE_ENV === 'development' ? error.stack : undefined
    });
  }
};

