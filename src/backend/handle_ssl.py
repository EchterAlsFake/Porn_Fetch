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
import ssl # Main library for handling ssl
from base_api.base import setup_logger


logger = setup_logger(name="Porn Fetch - [SSL Handler]", level=logging.DEBUG)


def build_ssl_context() -> ssl.SSLContext:
    """
    Robust SSL context:
    1) Try native system trust store (truststore)
    2) ALSO load certifi roots (helps on stale systems)

    You can specify your own CA bundle through environment variables.
    Please read the documentation of httpx for more information on that!
    """
    ctx: ssl.SSLContext

    # 1) Prefer system trust store (corporate roots, auto-updates, etc.)
    try:
        import truststore
        ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        logger.info(f"""Truststore is available! Porn Fetch will use your OS SSL context.""")

        # 2) Add certifi as additional roots (fallback for old systems)
        try:
            import certifi
            ctx.load_verify_locations(cafile=certifi.where())
            logger.debug("Added legacy certifi CA as an additional backup in case your system fails to resolve https")
        except Exception:
            logger.warning("Couldn't add certifi CA. This is NOT an error, but can cause issues later (rare)")
            pass

    except Exception:
        # truststore missing/unavailable -> use certifi bundle
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
        logger.info(f"""Couldn't import truststore due to an error. Using certifi's SSL context instead!""")

    return ctx

# EOF