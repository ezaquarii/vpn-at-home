import urllib.request
import re
import validators


COMMENT_REGEX = re.compile('\s*[#;].*$')


def get_domains_from_bad_hosts_file(url):
    with urllib.request.urlopen(url) as response:
        size = response.length
        if size > 5*1024*1024:
            raise RuntimeError(f"Suspiciously large payload: {size} kB")
        lines = response.read().decode('utf8').split('\n')
        domains = []
        for line in lines:
            stripped = COMMENT_REGEX.sub('', line)
            fields = stripped.split()
            field_count = len(fields)
            if field_count == 1 and validators.domain(fields[0]):
                domains.append(fields[0])
            elif field_count == 2 and validators.ipv4(fields[0]) and validators.domain(fields[1]):
                domains.append(fields[1])
        return domains
