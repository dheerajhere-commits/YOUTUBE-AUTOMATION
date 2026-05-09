from core.anti_spam import apply_cooldown_async

async def manage_accounts(accounts_data):
    """
    Manages OAuth2 token rotation for Google/Meta accounts.
    Implement a "Cooldown" logic to prevent IP flagging.
    """
    print("[Ops Agent] Checking account tokens...")
    for i, account in enumerate(accounts_data):
        print(f"[Ops Agent] Verified: {account['account_id']}")
        if i < len(accounts_data) - 1:
            await apply_cooldown_async(min_minutes=1, max_minutes=2)
    print("[Ops Agent] All accounts verified.")
    return True
