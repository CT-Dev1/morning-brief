# Extract
import os.path
import json # Although not strictly needed for list of dicts, good practice

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Define the scope for reading emails
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# Define paths relative to this script's location
TOKEN_PATH = os.path.join(os.path.dirname(__file__), "token.json")
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "oauth_credentials.json")


def get_top_emails_json(max_results=20):
    """
    Fetches the top N emails from the user's PRIMARY Gmail inbox using the Gmail API,
    extracts key metadata (Subject, From, Date, Snippet), and returns them
    as a list of dictionaries (JSON-like format).

    Handles OAuth 2.0 authentication flow. Requires 'oauth_credentials.json'.
    Stores/uses 'token.json' for credentials.

    Args:
        max_results (int): The maximum number of emails to retrieve. Defaults to 20.

    Returns:
        list: A list of dictionaries, where each dictionary represents an email
              with keys 'id', 'threadId', 'snippet', 'subject', 'from', 'date'.
              Returns an empty list if an error occurs or no emails are found.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
             print(f"Error loading credentials from {TOKEN_PATH}: {e}")
             creds = None # Ensure creds is None if loading fails

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                # Need to re-authenticate if refresh fails
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                print(f"Error: Credentials file not found at {CREDENTIALS_PATH}")
                print("Please download your OAuth 2.0 credentials file and place it there.")
                return []
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                 print(f"Error during authentication flow: {e}")
                 return []
        # Save the credentials for the next run
        try:
            with open(TOKEN_PATH, "w") as token:
                token.write(creds.to_json())
            print(f"Credentials saved to {TOKEN_PATH}")
        except Exception as e:
            print(f"Error saving token to {TOKEN_PATH}: {e}")
            # Continue execution even if saving fails, but warn user

    emails_list = []
    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)

        # EDIT THIS LINE TO GET OTHER INBOXES LIKE SOCIAL OR PROMOTIONS
        query = 'in:inbox category:primary'

        # Get the list of messages (only IDs) matching the query
        results = service.users().messages().list(
            userId="me",
            q=query, # Use the query parameter for filtering
            maxResults=max_results
        ).execute()
        messages = results.get("messages", [])

        if not messages:
            print("No emails found matching the criteria (inbox, not promotions/social/updates).")
            return []

        print(f"Fetching details for {len(messages)} emails matching criteria...")
        for message_ref in messages:
            msg_id = message_ref['id']
            # Get full message details (metadata only is efficient)
            msg = service.users().messages().get(
                userId="me",
                id=msg_id,
                format='metadata',
                metadataHeaders=['Subject', 'From', 'Date'] # Request specific headers
            ).execute()

            # Extract headers
            headers = msg.get('payload', {}).get('headers', [])
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')

            emails_list.append({
                'id': msg.get('id'),
                'threadId': msg.get('threadId'),
                'snippet': msg.get('snippet', ''), # Snippet is usually included
                'subject': subject,
                'from': sender,
                'date': date
            })

        return emails_list

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred fetching emails: {error}")
        # Attempt to parse error details if available
        try:
            error_details = json.loads(error.content).get('error', {})
            print(f"Error details: {error_details.get('message')}")
            if error_details.get('status') == 'UNAUTHENTICATED':
                 print("Authentication error. Consider deleting token.json and re-running.")
                 # Optionally delete token file here if desired
                 # if os.path.exists(TOKEN_PATH):
                 #    os.remove(TOKEN_PATH)
                 #    print(f"Removed potentially invalid {TOKEN_PATH}")

        except Exception as e:
            print(f"Could not parse error content: {e}")
        return [] # Return empty list on API error
    except FileNotFoundError:
        # This might catch the credentials file not found earlier, but good to have
        print(f"Error: Credentials file not found at {CREDENTIALS_PATH}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return [] # Return empty list on other errors


# Example usage
if __name__ == "__main__":
    top_emails = get_top_emails_json(max_results=10) # Get top 5 for example
    if top_emails:
        print(f"\n--- Top {len(top_emails)} Emails ---")
        for i, email_data in enumerate(top_emails):
             print(f"\nEmail {i+1}:")
             print(f"  ID: {email_data['id']}")
             print(f"  From: {email_data['from']}")
             print(f"  Date: {email_data['date']}")
             print(f"  Subject: {email_data['subject']}")
             print(f"  Snippet: {email_data['snippet'][:100]}...") # Print first 100 chars
        # Optional: Print as JSON
        # print("\n--- JSON Output ---")
        # print(json.dumps(top_emails, indent=2))
    else:
        print("Could not retrieve emails.")