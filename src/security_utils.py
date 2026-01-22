import requests
import hashlib
import zxcvbn # Standard library for realistic password strength

def check_password_strength(password):
    """
    Analyzes password using zxcvbn (entropy, dictionary checks, patterns).
    Returns a dict with score (0-4), feedback, and crack time.
    """
    results = zxcvbn.zxcvbn(password)
    return {
        'score': results['score'], # 0 (weak) to 4 (strong)
        'feedback': results['feedback']['suggestions'],
        'crack_time': results['crack_times_display']['offline_slow_hashing_1e4_per_second']
    }

def check_have_i_been_pwned(password):
    """
    Checks if password exists in data breaches via API.
    Uses k-Anonymity (only sends first 5 chars of hash).
    """
    sha1_password = hashlib.sha1(password.encode('utf-8'), usedforsecurity=False).hexdigest().upper()
    prefix = sha1_password[:5]
    suffix = sha1_password[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code != 200:
            return "Error checking API"
        
        # Check if our suffix is in the response
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return f"WARNING: Found in {count} data breaches!"
        return "Safe (Not found in known breaches)"
    except:
        return "API Unavailable"
