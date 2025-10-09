#!/usr/bin/env python3
"""Check for verbose data in the database."""
import os
from src.memory.crud import get_overview, get_items_by_keys
from src.memory.db import get_session

def main():
    # Get user ID from environment
    user_id = os.getenv('FITNESS_USER_ID') or os.getenv('DEFAULT_USER_ID')

    with get_session() as session:
        # Get overview (truncated view)
        overview = get_overview(session, user_id)

        print('=== DATA SUMMARY ===')
        for category in ['goals', 'plans', 'strategies', 'preferences', 'knowledge', 'principles', 'current']:
            if category in overview:
                if isinstance(overview[category], dict):
                    for status, items in overview[category].items():
                        print(f'{category}/{status}: {len(items)} items')
                else:
                    print(f'{category}: {len(overview[category])} items')

        print('\n=== VERBOSE ENTRIES (truncated in overview) ===')

        # Collect keys to fetch full content
        verbose_keys = []

        # Check knowledge entries
        if 'knowledge' in overview:
            print('\nKNOWLEDGE (showing truncated length):')
            for k in overview.get('knowledge', []):
                print(f"  - {k['key']}: {len(k.get('content', ''))} chars (truncated)")
                verbose_keys.append(('knowledge', k['key']))

        # Check principles
        if 'principles' in overview:
            print('\nPRINCIPLES (showing truncated length):')
            for p in overview.get('principles', []):
                print(f"  - {p['key']}: {len(p.get('content', ''))} chars (truncated)")
                verbose_keys.append(('principle', p['key']))

        # Check preferences
        if 'preferences' in overview:
            print('\nPREFERENCES (showing truncated length):')
            for pref in overview.get('preferences', []):
                print(f"  - {pref['key']}: {len(pref.get('content', ''))} chars (truncated)")
                verbose_keys.append(('preference', pref['key']))

        # Now fetch full content to see actual sizes
        if verbose_keys:
            print('\n=== ACTUAL FULL CONTENT SIZES ===')
            items_detail = get_items_by_keys(session, user_id, verbose_keys)

            for item in items_detail:
                content_len = len(item.get('content', ''))
                target_max = {
                    'knowledge': 400,
                    'principle': 300,
                    'preference': 200
                }.get(item['kind'], 500)

                status = '✓' if content_len <= target_max else '⚠️ VERBOSE'
                print(f"{status} {item['kind']}/{item['key']}: {content_len} chars (target: <{target_max})")

if __name__ == '__main__':
    main()
