import os
import requests
import logging

logger = logging.getLogger(__name__)

try:
    from hindsight_client import Hindsight
    HAS_HINDSIGHT_SDK = True
except ImportError:
    HAS_HINDSIGHT_SDK = False

class RecallIQHindsightClient:
    def __init__(self):
        self.api_key = os.environ.get("HINDSIGHT_API_KEY")
        default_url = "https://api.hindsight.vectorize.io" if self.api_key else "http://localhost:8888"
        self.base_url = os.environ.get("HINDSIGHT_BASE_URL", default_url)
        self.client = None
        self._local_banks = {}
        self._is_server_available = None  # Cache server connectivity check
        
        if HAS_HINDSIGHT_SDK:
            try:
                if self.api_key:
                    self.client = Hindsight(base_url=self.base_url, api_key=self.api_key)
                else:
                    self.client = Hindsight(base_url=self.base_url)
            except Exception as e:
                logger.warning(f"Failed to initialize Hindsight SDK, falling back to REST/Local: {e}")
                self.client = None
    
    def _get_bank_id(self, client_id: str) -> str:
        return f"recalliq-{client_id}"

    def check_server(self) -> bool:
        """Quick 0.5s connectivity check to Hindsight server."""
        if self._is_server_available is not None:
            return self._is_server_available
        
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            resp = requests.get(f"{self.base_url}/health", headers=headers, timeout=0.5)
            self._is_server_available = (resp.status_code == 200)
        except Exception:
            self._is_server_available = False
            
        return self._is_server_available

    def retain_interaction(self, client_id: str, content: str) -> dict:
        bank_id = self._get_bank_id(client_id)
        
        # Store in local memory buffer
        if bank_id not in self._local_banks:
            self._local_banks[bank_id] = []
        if content not in self._local_banks[bank_id]:
            self._local_banks[bank_id].append(content)
        
        # Skip remote call fast if server is offline
        if not self.check_server():
            return {"success": True, "message": "Interaction retained in Hindsight memory buffer", "mode": "local"}

        try:
            if self.client:
                self.client.retain(bank_id=bank_id, content=content)
                return {"success": True, "message": "Interaction retained via Hindsight SDK", "mode": "sdk"}
            else:
                headers = {}
                if self.api_key:
                    headers["Authorization"] = f"Bearer {self.api_key}"
                
                url = f"{self.base_url}/banks/{bank_id}/retain"
                response = requests.post(url, json={"content": content}, headers=headers, timeout=2)
                response.raise_for_status()
                return {"success": True, "message": "Interaction retained via Hindsight REST API", "mode": "rest"}
        except Exception as e:
            logger.warning(f"Hindsight API retain failed ({e}), using local memory buffer.")
            return {"success": True, "message": "Interaction retained in Hindsight local buffer", "mode": "local"}

    def recall_memories(self, client_id: str, query: str) -> list:
        bank_id = self._get_bank_id(client_id)
        
        # If server is available, attempt remote recall
        if self.check_server():
            try:
                if self.client:
                    results = self.client.recall(bank_id=bank_id, query=query)
                    memories = []
                    if hasattr(results, 'results') and results.results:
                        for r in results.results:
                            memories.append(r.text if hasattr(r, 'text') else str(r))
                        return memories
                else:
                    headers = {}
                    if self.api_key:
                        headers["Authorization"] = f"Bearer {self.api_key}"
                    
                    url = f"{self.base_url}/banks/{bank_id}/recall"
                    response = requests.post(url, json={"query": query}, headers=headers, timeout=2)
                    if response.status_code == 200:
                        data = response.json()
                        raw_items = data if isinstance(data, list) else data.get("results", [])
                        memories = [item.get("text", str(item)) if isinstance(item, dict) else str(item) for item in raw_items]
                        if memories:
                            return memories
            except Exception as e:
                logger.warning(f"Hindsight API recall failed ({e}). Using local memory buffer.")

        # Return retained local memories
        return self._local_banks.get(bank_id, [])

    def test_connection(self) -> bool:
        return self.check_server()
