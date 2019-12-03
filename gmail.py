import base64
import email
import pickle
import os.path
from googleapiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def list_messages_with_labels(service, user_id, label_ids=[]):
    """List all Messages of the user"s mailbox with label_ids applied.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        label_ids: Only return Messages with these labelIds applied.

    Returns:
        List of Messages that have all required Labels applied. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate id to get the details of a Message.
    """
    try:
        response = (
            service.users()
            .messages()
            .list(userId=user_id, labelIds=label_ids)
            .execute()
        )
        messages = []
        if "messages" in response:
            messages.extend(response["messages"])

        while "nextPageToken" in response:
            page_token = response["nextPageToken"]
            response = (
                service.users()
                .messages()
                .list(userId=user_id, labelIds=label_ids, pageToken=page_token)
                .execute()
            )
            messages.extend(response["messages"])

        return messages
    except errors.HttpError as error:
        print("An error occurred: {}".format(error))


def get_message(service, user_id, msg_id):
    """Get a Message with given ID.
    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

    Returns:
        A Message.
    """
    try:
        message = (
            service.users()
            .messages()
            .get(userId=user_id, id=msg_id, format="raw")
            .execute()
        )
        msg_str = base64.urlsafe_b64decode(message["raw"].encode("ASCII"))
        mime_msg = email.message_from_bytes(msg_str)
        return mime_msg
    except errors.HttpError as error:
        print("An error occurred: {}".format(error))


def main():
    """Shows basic usage of the Gmail API.
    Lists the user"s Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user"s access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)

    # Call the Gmail API
    messages = list_messages_with_labels(service, "me", label_ids=["SPAM"])
    test_message = get_message(service, "me", messages[0]["id"])
    # return test_message
    print(test_message.keys())


if __name__ == "__main__":
    main()
