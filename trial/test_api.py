"""
ReviewsAPIClient – class-based client for the Dinasour Reviews API.

Usage:
    1. Start the Django server:
           uv run python manage.py runserver 0.0.0.0:8000

    2. Run this script:
           uv run python trial/test_api.py

    3. Or import and use the client in your own code:
           from trial.test_api import ReviewsAPIClient
           client = ReviewsAPIClient("http://192.168.1.x:8000")
           client.create(5, "Great!")
"""

import json
import requests


class ReviewsAPIClient:
    """Client for the /api/dinasour/reviews/ REST API."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")
        self.endpoint = f"{self.base_url}/api/dinasour/reviews/"

    # ── Internal helpers ──────────────────────────────────────────────────

    def _print(self, label: str, response: requests.Response):
        print(f"\n{'=' * 55}")
        print(f"  {label}")
        print(f"  Status : {response.status_code}")
        try:
            body = json.dumps(response.json(), indent=4)
        except Exception:
            body = response.text
        print(f"  Body   :\n{body}")
        print("=" * 55)

    def _url(self, review_id: int) -> str:
        return f"{self.endpoint}{review_id}/"

    # ── CRUD methods ──────────────────────────────────────────────────────

    def list(self) -> list:
        """GET /api/dinasour/reviews/ — return all reviews."""
        response = requests.get(self.endpoint)
        self._print("GET  – List All Reviews", response)
        return response.json()

    def create(self, rating: int, comment: str) -> dict:
        """POST /api/dinasour/reviews/ — create a new review."""
        payload = {"rating": rating, "comment": comment}
        response = requests.post(self.endpoint, json=payload)
        self._print("POST – Create Review", response)
        return response.json()

    def get(self, review_id: int) -> dict:
        """GET /api/dinasour/reviews/<id>/ — retrieve one review."""
        response = requests.get(self._url(review_id))
        self._print(f"GET  – Get Review #{review_id}", response)
        return response.json()

    def update(self, review_id: int, rating: int, comment: str) -> dict:
        """PUT /api/dinasour/reviews/<id>/ — full update (both fields required)."""
        payload = {"rating": rating, "comment": comment}
        response = requests.put(self._url(review_id), json=payload)
        self._print(f"PUT  – Full Update Review #{review_id}", response)
        return response.json()

    def partial_update(self, review_id: int, **fields) -> dict:
        """PATCH /api/dinasour/reviews/<id>/ — update only the provided fields."""
        response = requests.patch(self._url(review_id), json=fields)
        self._print(f"PATCH – Partial Update Review #{review_id}", response)
        return response.json()

    def delete(self, review_id: int) -> bool:
        """DELETE /api/dinasour/reviews/<id>/ — delete a review."""
        response = requests.delete(self._url(review_id))
        self._print(f"DELETE – Delete Review #{review_id}", response)
        return response.status_code == 204


# ── Demo: run full CRUD cycle ─────────────────────────────────────────────

if __name__ == "__main__":
    # Change the host to your machine's IP for intranet testing, e.g.:
    #   client = ReviewsAPIClient("http://192.168.1.50:8000")
    client = ReviewsAPIClient("http://127.0.0.1:8000")

    print("\n===  Dinasour Reviews API – Full CRUD Demo  ===")

    # 1. Create
    review1 = client.create(rating=5, comment="Absolutely amazing experience!")
    review2 = client.create(rating=2, comment="Could have been much better.")

    # 2. List all
    client.list()

    # 3. Get one
    client.get(review1["id"])

    # 4. Full update (PUT)
    client.update(review1["id"], rating=4, comment="Actually pretty good on second thought.")

    # 5. Partial update (PATCH) – only change rating
    client.partial_update(review2["id"], rating=3)

    # 6. Delete
    client.delete(review2["id"])

    # 7. Final list to confirm
    client.list()
