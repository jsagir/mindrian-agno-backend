"""
Upload Ackoff's Pyramid (DIKW) Tool Deep-Dive to PWS Knowledge Base
Tier 2: T2_Tools/AckoffPyramid_*
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from google import genai

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_AI_API_KEY")
client = genai.Client(api_key=GOOGLE_API_KEY)

GEMINI_FILE_SEARCH_STORE = os.getenv(
    "GEMINI_FILE_SEARCH_STORE",
    "fileSearchStores/pwsknowledgebase-a4rnz3u41lsn"
)

ACKOFF_BASE = Path("/home/jsagi/Mindrian/PWS - Lectures and worksheets created by Mindrian-20251219T001450Z-1-001/PWS - Lectures and worksheets created by Mindrian/Akhoffs Pyramid")

# Ackoff's Pyramid files with T2_Tools naming
# Format: (filename, display_name, max_tokens_per_chunk, max_overlap_tokens)
FILES = [
    ("Lecture adhoffs pyramid.txt",
     "T2_Tools/AckoffPyramid_Lecture_DIKWValidation", 500, 100),

    ("Worksheet.txt",
     "T2_Tools/AckoffPyramid_Workbook_Exercises", 500, 100),

    ("System prompt.txt",
     "T2_Tools/AckoffPyramid_SystemPrompt_Complete", 500, 100),

    ("Materials_Guide_Complete.txt",
     "T2_Tools/AckoffPyramid_MaterialsGuide_CaseStudies", 500, 100),
]


def main():
    print("=" * 60)
    print("UPLOADING ACKOFF'S PYRAMID (DIKW) TO T2_Tools")
    print("=" * 60)
    print(f"Store: {GEMINI_FILE_SEARCH_STORE}")
    print(f"Source: {ACKOFF_BASE}\n")

    success = 0
    fail = 0

    for filename, display_name, max_tokens, overlap in FILES:
        file_path = ACKOFF_BASE / filename

        if not file_path.exists():
            print(f"  ⚠️ Not found: {filename}")
            fail += 1
            continue

        print(f"  📄 {display_name}")
        print(f"     Chunk: {max_tokens}tok / {overlap}overlap")

        try:
            operation = client.file_search_stores.upload_to_file_search_store(
                file=str(file_path),
                file_search_store_name=GEMINI_FILE_SEARCH_STORE,
                config={
                    'display_name': display_name,
                    'chunking_config': {
                        'white_space_config': {
                            'max_tokens_per_chunk': max_tokens,
                            'max_overlap_tokens': overlap
                        }
                    }
                }
            )

            while not operation.done:
                time.sleep(2)
                operation = client.operations.get(operation)

            print(f"     ✅ Indexed")
            success += 1

        except Exception as e:
            print(f"     ❌ Error: {e}")
            fail += 1

        time.sleep(0.5)

    print("\n" + "=" * 60)
    print(f"✅ Uploaded: {success}")
    print(f"❌ Failed: {fail}")
    print("=" * 60)


if __name__ == "__main__":
    main()
