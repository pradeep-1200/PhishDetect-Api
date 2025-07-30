import re
from urllib.parse import urlparse

def extract_features(url):
    features = []

    # Feature 1: Using IP instead of domain name
    ip = 1 if re.match(r"^http[s]?://\d+\.\d+\.\d+\.\d+", url) else -1
    features.append(ip)

    # Feature 2: Long URL (>75 characters)
    long_url = 1 if len(url) > 75 else -1
    features.append(long_url)

    # Feature 3: Short URL (<20 characters)
    short_url = 1 if len(url) < 20 else -1
    features.append(short_url)

    # Feature 4: "@" symbol in URL
    symbol_at = 1 if "@" in url else -1
    features.append(symbol_at)

    # Feature 5: "//" redirection after protocol
    double_slash = 1 if url.count("//") > 1 else -1
    features.append(double_slash)

    # Feature 6: Prefix or Suffix with '-'
    prefix_suffix = 1 if "-" in urlparse(url).netloc else -1
    features.append(prefix_suffix)

    # Feature 7: Subdomain count
    domain = urlparse(url).netloc
    subdomains = domain.split(".")
    subdomain_count = 1 if len(subdomains) > 3 else -1
    features.append(subdomain_count)

    # Feature 8: HTTPS present
    https = -1 if urlparse(url).scheme == "https" else 1
    features.append(https)

    # Feature 9: Domain registration length (unknown, assume short)
    features.append(1)

    # Feature 10: Favicon from external source (unknown, assume safe)
    features.append(-1)

    # Fill remaining features with dummy data for now
    while len(features) < 30:
        features.append(0)

    return features
