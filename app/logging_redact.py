import logging, re
class Redact(logging.Filter):
    PAT = re.compile(r"(x-api-key:\s*)(\S+)", re.I)
    def filter(self, record):
        record.msg = self.PAT.sub(r"\1[REDACTED]", str(record.msg))
        return True

def install_redaction():
    logger = logging.getLogger('uvicorn.access')
    logger.addFilter(Redact())
