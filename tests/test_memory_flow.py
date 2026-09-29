"""
Lightweight verification test for RecallIQ memory pipeline.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from recalliq.core.memory_service import MemoryService
from recalliq.core.prep_generator import PrepGenerator

def test_pipeline():
    print("==========================================")
    print("Testing RecallIQ Memory & Prep Pipeline")
    print("==========================================")

    memory_service = MemoryService()
    prep_generator = PrepGenerator()

    client_id = "novatech"
    client_info = memory_service.get_client_info(client_id)
    print(f"Client Info Loaded: {client_info.get('name')}")
    assert client_info.get('name') == "NovaTech Systems", "Client name mismatch"

    # Test Timeline & Count
    count = memory_service.get_interaction_count(client_id)
    print(f"Total Interactions for {client_id}: {count}")
    assert count >= 20, "Expected at least 20 interactions for NovaTech"

    # Test Hindsight Recall / Fallback
    query = "Prepare me for tomorrow's meeting with NovaTech."
    print(f"\nQuerying Hindsight memory for: '{query}'...")
    memories = memory_service.recall_memories(client_id, query)
    print(f"Retrieved {len(memories)} memories.")

    # Test Prep Generator (Memory ON vs OFF)
    print("\n--- Generating Prep WITHOUT Memory ---")
    gen_off = prep_generator.generate_without_memory(query, client_info)
    print(gen_off[:300] + "...\n")

    print("--- Generating Prep WITH Memory ---")
    gen_on = prep_generator.generate_meeting_prep(query, memories, client_info)
    print(gen_on[:400] + "...\n")

    print("✅ All core pipeline tests completed successfully!")

if __name__ == "__main__":
    test_pipeline()
