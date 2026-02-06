import datetime
import os
import json
import requests
import hmac
import hashlib

SIGNING_SECRET=b"hello-from-b12"
URL="https://b12.io/apply/submission"

def main():
    payload = {
        "action_run_link": os.environ["ACTION_RUN_LINK"],
        "email": "myburkek@gmail.com",
        "name": "Kevin Burke",
        "repository_link": "https://github.com/kevinburke24/b12-app",
        "resume_link": "https://drive.google.com/file/d/1cKObCmppjWJeArQOPn-PQlIGuLNJEtlf/view?usp=sharing",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds") + "Z",
    }

    body = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    signature = hmac.new(
        SIGNING_SECRET,
        body,
        hashlib.sha25,
    ).hexdigest()

    headers = {
        "Content-Type": "application/json",
        "X-Signature-256" : f"sha256={signature}",
    }

    response = requests.post(URL, data=body, headers=headers)
    response.raise_for_status()

    data = response.json()
    print(response)

if __name__ == "__main__":
    main()