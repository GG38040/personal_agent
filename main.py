"""Personal Agent main module for handling user interactions and commands."""

from typing import Optional
import logging

from agent import run_agent
from memory.memory import update_memory, retrieve_context
from gmail_integration import send_email, list_emails
from calendar_integration import (
    add_event,
    list_upcoming_events,
    parse_date_time,
    format_event_time
)


def handle_email_send(user_input: str) -> None:
    """
    Handle the email sending command.
    
    Args:
        user_input: Raw user input containing email details
    """
    try:
        parts = user_input.split("|")
        if len(parts) != 4:
            msg = (
                "Please use format: "
                "send email|to@example.com|Subject|Message"
            )
            print(f"Agent: {msg}")
            return

        _, to, subject, body = parts
        send_email(to.strip(), subject.strip(), body.strip())
        print("Agent: Email sent successfully!")
        update_memory(user_input, "Email sent successfully!")
    except Exception as e:
        error_msg = f"Failed to send email: {str(e)}"
        print(f"Agent: {error_msg}")
        update_memory(user_input, error_msg)


def handle_email_list(max_results: int = 5) -> None:
    """Handle the email listing command."""
    try:
        emails = list_emails(max_results)
        if not emails:
            print("Agent: No emails found.")
            return

        print("Agent: Here are your recent emails:")
        for idx, email in enumerate(emails, 1):
            print(f"\n{idx}. From: {email['sender']}")
            print(f"   Subject: {email['subject']}")
            print(f"   Date: {email['date']}")
            print(f"   Preview: {email['snippet']}")

        update_memory("list emails", "Listed recent emails successfully")
    except Exception as e:
        error_msg = f"Failed to list emails: {str(e)}"
        print(f"Agent: {error_msg}")
        update_memory("list emails", error_msg)


def handle_calendar_add(user_input: str) -> None:
    """Handle adding calendar events."""
    try:
        # Format: add event|Summary|YYYY-MM-DD|HH:MM|[location]|[description]
        parts = user_input.split("|")
        if len(parts) < 4:
            print("Agent: Please use format: add event|Summary|YYYY-MM-DD|HH:MM|[location]|[description]")
            return

        _, summary, date_str, time_str, *extras = parts
        location = extras[0] if len(extras) > 0 else None
        description = extras[1] if len(extras) > 1 else None

        start_time = parse_date_time(date_str.strip(), time_str.strip())
        result = add_event(
            summary.strip(),
            start_time,
            description=description,
            location=location
        )
        print(f"Agent: {result}")
        update_memory(user_input, result)

    except Exception as e:
        error_msg = f"Failed to add event: {str(e)}"
        print(f"Agent: {error_msg}")
        update_memory(user_input, error_msg)


def handle_calendar_list() -> None:
    """Handle listing calendar events."""
    try:
        events = list_upcoming_events(max_results=5)
        if not events:
            print("Agent: No upcoming events found.")
            return

        print("Agent: Here are your upcoming events:")
        for idx, event in enumerate(events, 1):
            time_str = format_event_time(event)
            print(f"{idx}. {event['summary']} - {time_str}")
            if event.get('location'):
                print(f"   Location: {event['location']}")

        update_memory("list events", "Listed upcoming events successfully")

    except Exception as e:
        error_msg = f"Failed to list events: {str(e)}"
        print(f"Agent: {error_msg}")
        update_memory("list events", error_msg)


def process_user_input(user_input: str, context: Optional[str] = None) -> None:
    """Process user input and execute appropriate command."""
    # Convert input to lowercase for command matching
    input_lower = user_input.lower()
    
    # Handle email listing commands
    if any(cmd in input_lower for cmd in ['list email', 'show email', 'get email']):
        handle_email_list()
        return
        
    # Handle other commands
    if input_lower.startswith("send email"):
        handle_email_send(user_input)
    elif input_lower.startswith("add event"):
        handle_calendar_add(user_input)
    elif input_lower.startswith("list events"):
        handle_calendar_list()
    else:
        response = run_agent(user_input, context)
        print("Agent:", response)
        update_memory(user_input, response)


def main() -> None:
    """Main loop for the personal assistant."""
    print("Personal Agent initialized. Type 'exit' to quit.")
    print("Available commands:")
    print("- list emails")
    print("- send email|to@example.com|Subject|Message")
    print("- list events")
    print("- add event|Summary|YYYY-MM-DD|HH:MM")
    
    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() == 'exit':
                print("Goodbye!")
                break
                
            context = retrieve_context()
            process_user_input(user_input, context)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            logging.error("Error in main loop: %s", str(e))


if __name__ == "__main__":
    main()