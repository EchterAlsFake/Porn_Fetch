"""
This file is used to create the SSL context and handle the differences between truststore
and cacert.pem.

Truststore basically tells httpx (the network component) to use the system certificates for handling SSL, which allows
for custom SSL certificates, automatic updating of the SSL context and so on.

This would be the preferred way, but some systems are basically just too old and SSL wouldn't work on them with their
default configuration. Due to this, I also include the cacert.pem from Mozilla's CA, so that those systems also
can establish a secure https connection.

"""
import logging
import os
import ssl # Main library for handling ssl
from base_api.base import setup_logger


logger = setup_logger(name="Porn Fetch - [SSL Handler]", level=logging.DEBUG)


def build_ssl_context(use_truststore: bool = True) -> ssl.SSLContext:
    """
    Robust SSL context:
    1) Try native system trust store (truststore)
    2) Fall back to the default SSL context (respects SSL_CERT_FILE/SSL_CERT_DIR)
    3) Optionally add certifi roots as a last resort when no CA env vars are set

    You can specify your own CA bundle through SSL_CERT_FILE/SSL_CERT_DIR.
    Please read the documentation of httpx for more information on that.
    """
    ctx: ssl.SSLContext

    # 1) Prefer system trust store (corporate roots, auto-updates, etc.)
    if use_truststore:
        try:
            import truststore
            ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            logger.info("Truststore is available! Porn Fetch will use your OS SSL context.")
            return ctx
        except Exception:
            logger.info("Truststore is unavailable; falling back to default SSL context.")

    # 2) Default context respects SSL_CERT_FILE / SSL_CERT_DIR
    ctx = ssl.create_default_context()
    if not os.getenv("SSL_CERT_FILE") and not os.getenv("SSL_CERT_DIR"):
        try:
            import certifi
            ctx.load_verify_locations(cafile=certifi.where())
            logger.debug("Added certifi CA bundle as a fallback for stale systems.")
        except Exception:
            logger.warning("Couldn't add certifi CA bundle; using default SSL context.")
    else:
        logger.debug("SSL_CERT_FILE/SSL_CERT_DIR set; using default SSL context without certifi fallback.")
    return ctx

# EOF
