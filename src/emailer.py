"""
TODO - Logging
TODO - Tests
TODO - Unsub
TODO - Tidy
"""

import base64
import os
import googleapiclient.errors as errors

from email.mime.text import MIMEText

from emailauth import EmailAuth
from message import message, subject


class Emailer:

    @staticmethod
    def create_message(sender, to, subject, message_text):
        """Create a message for an email.
        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.

        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    @staticmethod
    def send_message(service, user_id, message):
        """
        Send an email message.
        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.
        Returns:
          Sent Message.
        """
        try:
            message = (service.users().messages().send(userId=user_id, body=message)
                       .execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as e:
            print(f'An error occurred: {e}')


if __name__ == '__main__':

    to_send = Emailer.create_message(os.environ['EMAILER_SENDER'],
                                     os.environ['EMAILER_RECEIVER'],
                                     subject=subject,
                                     message_text=message)

    Emailer.send_message(EmailAuth().get_service(), 'me', to_send)
