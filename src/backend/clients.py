"""
This file will handle all network clients and allow for refreshing and creating session objects.
This is important, because Porn Fetch will dynamically need to update the different website APIs
for example if you apply a proxy.

If I only use one specific file that handles everything, it's easier to manage it, because I have more control
where I import stuff from.

I know this might seem a bit confusing if you read this the first time, but if you look at the `eaf_base_api` module
and the other Porn APIs and how they are working together, then you will definitely understand why this matters.
"""
import logging

"""
Current APIs:

1) PHUB           -> https://pornhub.com (ph_client, ph_video)
2) hqporner       -> https://hqporner.com (hq_client, hq_video)
3) xnxx           -> https://xnxx.com (xn_client, xn_video)
4) xvideos        -> https://xvideos.com (xv_client, xv_video)
5) eporner        -> https://eporner.com (ep_client, ep_video)
6) missav         -> https://missav.ws   (mv_client, mv_video)
7) xhamster       -> https://xhamster.com (xh_client, xh_video)
8) spankbang      -> https://spankbang.com (sp_client, sp_video)
9) youporn        -> https://youporn.com (yp_client, yp_video)
10) porntrex      -> https://porntrex.com (pt_client, pt_video)
11) xfreehd       -> https://xfreehd.com  (xf_client, xf_video)
12) beeg          -> https://beeg.com (bg_client, bg_video)
"""


from phub import Client as ph_Client
from xnxx_api import Client as xn_Client
from base_api.modules.config import config # This is the global configuration instance of base core config
from xvideos_api import Client as xv_Client
from eporner_api import Client as ep_Client
from hqporner_api import Client as hq_Client
from xhamster_api import Client as xh_Client
from spankbang_api import Client as sp_Client
from base_api.base import BaseCore, setup_logger
from beeg_api.beeg_api import Client as bg_Client
from missav_api.missav_api import Client as mv_Client
from youporn_api.youporn_api import Client as yp_Client
from xfreehd_api.xfreehd_api import Client as xf_Client
from porntrex_api.porntrex_api import Client as pt_Client

logger = setup_logger(name="Porn Fetch - [Clients]", level=logging.DEBUG)

# which is also affecting all other APIs when the refresh_clients function is called
# Initialize clients globally, so that we can override them later with a new configuration from BaseCore if needed
mv_client = mv_Client()
ep_client = ep_Client()
ph_client = ph_Client()
xv_client = xv_Client()
xh_client = xh_Client()
sp_client = sp_Client()
hq_client = hq_Client()
xn_client = xn_Client()
yp_client = yp_Client()
bg_client = bg_Client()
pt_client = pt_Client()
xf_client = xf_Client()
logger.debug("Successfully initialized all clients!")


core = BaseCore() # We need that sometimes in Porn Fetch's main class e.g., thumbnail fetching
core.config.max_retries = 2 # Only use 2 retries to prevent blocking
core.config.use_http2 = False # Fallback to http 1 for critical operations
core.config.timeout = 10 # Medium to low timeout to prevent blocking


def refresh_clients(enable_kill_switch=False):
    logger.info(f"Refreshing clients!")
    global mv_client, ep_client, ph_client, xv_client, xh_client, sp_client, \
        hq_client, xn_client, core, yp_client, bg_client, pt_client, xf_client

    # One BaseCore per site, with its own RuntimeConfig (isolated headers/cookies)
    core_common = BaseCore(config=config)   # if you want a “generic” core
    core_hq    = BaseCore(config=config)
    core_mv    = BaseCore(config=config)
    core_ep    = BaseCore(config=config)
    core_ph    = BaseCore(config=config)
    core_xv    = BaseCore(config=config)
    core_xh    = BaseCore(config=config)
    core_xn    = BaseCore(config=config)
    core_sp    = BaseCore(config=config)
    core_yp    = BaseCore(config=config)
    core_bg    = BaseCore(config=config)
    core_pt    = BaseCore(config=config)
    core_xf    = BaseCore(config=config)

    if enable_kill_switch:
        logger.warning("Warning: You have enabled the kill switch, refreshing clients with enabled kill switch")
        core_common.enable_kill_switch()
        core_hq.enable_kill_switch()
        core_mv.enable_kill_switch()
        core_ep.enable_kill_switch()
        core_ph.enable_kill_switch()
        core_xv.enable_kill_switch()
        core_xh.enable_kill_switch()
        core_xn.enable_kill_switch()
        core_yp.enable_kill_switch()
        core_bg.enable_kill_switch()
        core_pt.enable_kill_switch()
        core_xf.enable_kill_switch()

    # Instantiate clients with their site-specific cores
    mv_client = mv_Client(core=core_mv)
    ep_client = ep_Client(core=core_ep)
    xv_client = xv_Client(core=core_xv)
    xh_client = xh_Client(core=core_xh)
    sp_client = sp_Client(core=core_sp)
    hq_client = hq_Client(core=core_hq)
    xn_client = xn_Client(core=core_xn)
    yp_client = yp_Client(core=core_yp)
    bg_client = bg_Client(core=core_bg)
    pt_client = pt_Client(core=core_pt)
    xf_client = xf_Client(core=core_xf)
    ph_client = ph_Client(core=core_ph, use_webmaster_api=True)
    logger.debug("Applied new clients. Configurations should be overridden now e.g., if you have set a proxy.")

# EOF