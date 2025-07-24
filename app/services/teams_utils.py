import os
import requests
from app.services.azure_auth import get_graph_access_token

USER_ID = os.getenv("GRAPH_TEST_USER_EMAIL")  # Should be a full email address
GRAPH_API_ENDPOINT = f"https://graph.microsoft.com/v1.0/users/{USER_ID}/events"


def get_teams_meetings(access_token: str):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "$top": 10,
        "$orderby": "start/dateTime desc"
    }

    response = requests.get(GRAPH_API_ENDPOINT, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Graph API error: {response.status_code} - {response.text}")

    events = response.json().get("value", [])

    # Filter Teams meetings only
    teams_meetings = [
        {
            "subject": event["subject"],
            "start": event["start"]["dateTime"],
            "join_url": event.get("onlineMeeting", {}).get("joinUrl"),
        }
        for event in events if event.get("isOnlineMeeting")
    ]

    return teams_meetings


def create_teams_meeting(
    subject="AI Interview",
    start_time="2025-07-22T19:30:00",
    end_time="2025-07-22T20:00:00"
):
    token = get_graph_access_token()
    print("🔑 Access Token:", token[:60], "...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "subject": subject,
        "start": {
            "dateTime": start_time,
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "Asia/Kolkata"
        },
        "isOnlineMeeting": True,
        "onlineMeetingProvider": "teamsForBusiness"
    }

    response = requests.post(
        f"https://graph.microsoft.com/v1.0/users/{USER_ID}/events",
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        meeting = response.json()
        join_url = meeting.get("onlineMeeting", {}).get("joinUrl")
        print("✅ Meeting created successfully!")
        print("🔗 Join URL:", join_url)
        return join_url
    else:
        print(f"❌ Failed to create meeting: {response.status_code}")
        print(response.text)
        return None
