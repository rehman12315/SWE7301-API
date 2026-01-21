import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def login(username, password):
    print(f"\nLogging in as {username}...")
    res = requests.post(f"{BASE_URL}/login", json={"username": username, "password": password})
    if res.status_code == 200:
        return res.json()["access_token"]
    print(f"Login failed: {res.text}")
    return None

def test_access(token, obs_id):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{BASE_URL}/api/observations/{obs_id}", headers=headers)
    return res.status_code, res.json()

def run_tests():
    # Observations seeded: ID 1 (Product 1), ID 2 (Product 2), ID 3 (Product 3), ID 4 (Product 4)
    
    users = [
        ("full_user", "password", [1, 2, 3, 4], []), # Should have access to all
        ("partial_user", "password", [1, 2], [3, 4]), # Should have access to 1, 2 only
        ("none_user", "password", [], [1, 2, 3, 4]), # Should have access to none
    ]

    for username, password, allowed, forbidden in users:
        token = login(username, password)
        if not token: continue

        for obs_id in allowed:
            status, data = test_access(token, obs_id)
            if status == 200:
                print(f"✅ {username} accessed Observation {obs_id}")
            else:
                print(f"❌ {username} FAILED to access Observation {obs_id} (Status: {status})")

        for obs_id in forbidden:
            status, data = test_access(token, obs_id)
            if status == 403:
                print(f"✅ {username} correctly blocked from Observation {obs_id}")
            else:
                print(f"❌ {username} was NOT blocked from Observation {obs_id} (Status: {status})")

if __name__ == "__main__":
    run_tests()
