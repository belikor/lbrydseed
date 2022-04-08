#!/usr/bin/env python3
# --------------------------------------------------------------------------- #
# The MIT License (MIT)                                                       #
#                                                                             #
# Copyright (c) 2022 Eliud Cabrera Castillo <e.cabrera-castillo@tum.de>       #
#                                                                             #
# Permission is hereby granted, free of charge, to any person obtaining       #
# a copy of this software and associated documentation files                  #
# (the "Software"), to deal in the Software without restriction, including    #
# without limitation the rights to use, copy, modify, merge, publish,         #
# distribute, sublicense, and/or sell copies of the Software, and to permit   #
# persons to whom the Software is furnished to do so, subject to the          #
# following conditions:                                                       #
#                                                                             #
# The above copyright notice and this permission notice shall be included     #
# in all copies or substantial portions of the Software.                      #
#                                                                             #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,    #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL     #
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING     #
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER         #
# DEALINGS IN THE SOFTWARE.                                                   #
# --------------------------------------------------------------------------- #
"""Methods to show settings and status of the lbrynet daemon."""
import requests

import lbseed.resolve as res


def get_settings(server="http://localhost:5279"):
    """Get the raw settings."""
    if not res.server_exists(server=server):
        return None

    msg = {"method": "settings_get"}
    out = requests.post(server, json=msg).json()
    status = out["result"]

    output = {}

    keys = ["jurisdiction", "max_key_fee"]

    keys_int = ["blob_lru_cache_size", "blob_storage_limit",
                "concurrent_blob_announcers", "concurrent_hub_requests",
                "concurrent_reflector_uploads", "max_connections_per_download",
                "network_storage_limit",
                "prometheus_port",
                "split_buckets_under_index",
                "tcp_port", "transaction_cache_size", "udp_port",
                "video_bitrate_maximum", "volume_analysis_time"]

    keys_float = ["blob_download_timeout", "download_timeout",
                  "fixed_peer_delay", "hub_timeout",
                  "node_rpc_timeout", "peer_connect_timeout"]

    keys_b = ["announce_head_and_sd_only", "reflect_streams",
              "save_blobs", "save_files", "save_resolved_claims",
              "share_usage_data", "streaming_get", "track_bandwidth",
              "use_upnp"]

    keys_str = ["allowed_origin", "api", "audio_encoder",
                "blockchain_name", "coin_selection_strategy",
                "config", "data_dir", "download_dir",
                "ffmpeg_path", "max_wallet_server_fee", "network_interface",
                "streaming_server", "video_encoder", "video_scaler",
                "volume_filter", "wallet_dir"]

    keys_lst = ["components_to_skip", "fixed_peers", "known_dht_nodes",
                "lbryum_servers", "reflector_servers", "wallets"]

    for k in keys:
        value = status.get(k, None)
        output[k] = f"{k}: {value}"

    for k in keys_int:
        value = status.get(k, None)
        output[k] = f"{k}: {value}"

    for k in keys_float:
        value = status.get(k, None)
        output[k] = f"{k}: {value:.1f}"

    for k in keys_b:
        value = str(status.get(k, None))
        output[k] = f"{k}: {value}"

    for k in keys_str:
        value = status.get(k, None)
        output[k] = f"{k}: '{value}'"

    for k in keys_lst:
        values = status.get(k, None)
        out = [f"{k}:"]

        for v in values:
            if isinstance(v, list):
                v1 = v[0]
                v2 = v[1]
                out.append(f"- {v1}:{v2}")
            else:
                out.append(f"- '{v}'")

        if len(values) < 1:
            out[0] = out[0] + " []"

        output[k] = "\n".join(out)

    return output


def get_lbrynet_settings(server="http://localhost:5279"):
    """Get the settings for the lbrynet daemon."""
    output = get_settings(server=server)

    if not output:
        return "(no settings)"

    out = [output["config"],
           output["data_dir"],
           output["download_dir"],
           output["wallet_dir"],
           output["wallets"], "",

           output["api"],
           output["streaming_get"],
           output["streaming_server"],
           output["allowed_origin"],
           output["share_usage_data"],
           output["components_to_skip"], "",

           output["network_interface"],
           output["node_rpc_timeout"],
           output["prometheus_port"], "",

           output["blockchain_name"],
           output["coin_selection_strategy"], "",

           output["announce_head_and_sd_only"],
           output["blob_download_timeout"],
           output["blob_lru_cache_size"],
           output["blob_storage_limit"],
           output["concurrent_blob_announcers"],
           output["concurrent_hub_requests"],
           output["concurrent_reflector_uploads"],
           output["network_storage_limit"],
           output["max_connections_per_download"], "",

           output["download_timeout"],
           output["save_blobs"],
           output["save_files"],
           output["save_resolved_claims"], "",

           output["peer_connect_timeout"],
           output["fixed_peer_delay"],
           output["fixed_peers"], "",

           output["use_upnp"],
           output["tcp_port"],
           output["udp_port"], "",

           output["known_dht_nodes"], "",

           output["hub_timeout"],
           output["jurisdiction"],
           output["lbryum_servers"], "",

           output["reflect_streams"],
           output["reflector_servers"], "",

           output["max_key_fee"],
           output["max_wallet_server_fee"], "",

           output["split_buckets_under_index"],
           output["track_bandwidth"],
           output["transaction_cache_size"], "",

           output["ffmpeg_path"],
           output["audio_encoder"],
           output["video_bitrate_maximum"],
           output["video_encoder"],
           output["video_scaler"],
           output["volume_analysis_time"],
           output["volume_filter"]]

    content = "\n".join(out)

    return content
