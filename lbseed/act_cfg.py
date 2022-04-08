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


def get_status(server="http://localhost:5279"):
    """Get raw lbrynet status."""
    if not res.server_exists(server=server):
        return None

    msg = {"method": "status"}
    out = requests.post(server, json=msg).json()
    status = out["result"]

    output = {}

    s = status["background_downloader"]
    dw1 = s.get("available_free_space_mb", 0) / 1024
    dw1 = "Availabe free space: " + f"{dw1:.4f} GB"
    dw2 = f"Ongoing download: " + str(s.get("ongoing_download", None))
    dw3 = "Running: " + str(s.get("running", None))
    output["background_downloader"] = dw3 + "\n" + dw2 + "\n" + dw1

    s = status["blob_manager"]
    c = s["connections"]
    bm0 = "Connections:"
    bm1 = "- Incoming bps: " + str(c.get("incoming_bps", None))
    bm2 = "- Max incoming mbs: " + str(c.get("max_incoming_mbs", 0))
    bm3 = "- Max outgoing mbs: " + str(c.get("max_outgoing_mbs", 0))
    bm4 = "- Outgoing bps: " + str(c.get("outgoing_bps", None))
    bm5 = "- Total incoming mbs: " + str(c.get("total_incoming_mbs", 0))
    bm6 = "- Total outgoing mbs: " + str(c.get("total_outgoing_mbs", 0))
    bm7 = "- Total received: " + str(c.get("total_received", 0))
    bm8 = "- Total sent: " + str(c.get("total_sent", 0))
    bm9 = "Finished blobs: " + str(s.get("finished_blobs", None))
    output["blob_manager"] = (bm0 + "\n"
                              + bm1 + "\n" + bm2 + "\n" + bm3 + "\n"
                              + bm4 + "\n" + bm5 + "\n" + bm6 + "\n"
                              + bm7 + "\n" + bm8 + "\n" + bm9)

    s = status["dht"]
    dht1 = "Node ID: " + s.get("node_id", "None")
    dht2 = str(s.get("peers_in_routing_table", None))
    dht2 = "Peers in routing table: " + dht2
    output["dht"] = dht1 + "\n" + dht2

    s = status["disk_space"]
    dsk1 = s.get("content_blobs_storage_used_mb", 0) / 1024
    dsk1 = "Content blobs used storage: " + f"{dsk1:.4f} GB"
    dsk2 = s.get("published_blobs_storage_used_mb", 0) / 1024
    dsk2 = "Published blobs used storage: " + f"{dsk2:.4f} GB"
    dsk3 = f"Running: " + str(s.get("running", None))
    dsk4 = s.get("seed_blobs_storage_used_mb", 0) / 1024
    dsk4 = "Seed blobs used storage: " + f"{dsk4:.4f} GB"
    dsk5 = s.get("total_used_mb", 0) / 1024
    dsk5 = "Total usage: " + f"{dsk5:.4f} GB"
    output["disk_space"] = (dsk3 + "\n"
                            + dsk2 + "\n" + dsk1 + "\n" + dsk4 + "\n"
                            + dsk5)

    s = status["ffmpeg_status"]
    ffm1 = str(s.get("analyze_audio_volume", None))
    ffm1 = "Analyze audio volume: " + ffm1
    ffm2 = "Available: " + str(s.get("available", None))
    ffm3 = "ffmpeg: " + s.get("which", "None")
    output["ffmpeg_status"] = ffm1 + "\n" + ffm2 + "\n" + ffm3

    s = status["file_manager"].get("managed_files", None)
    output["file_manager"] = f"Managed files: {s}"

    s = status["startup_status"]
    st1 = str(s.get("background_downloader", None))
    st1 = "background_downloader: " + st1
    st2 = "blob_manager: " + str(s.get("blob_manager", None))
    st3 = "database: " + str(s.get("database", None))
    st4 = "dht: " + str(s.get("dht", None))
    st5 = "disk_space: " + str(s.get("disk_space", None))
    st6 = str(s.get("exchange_rate_manager", None))
    st6 = "exchange_rate_manager: " + st6
    st7 = "file_manager: " + str(s.get("file_manager", None))
    st8 = "hash_announcer: " + str(s.get("hash_announcer", None))
    st9 = str(s.get("libtorrent_component", None))
    st9 = "libtorrent_component: " + st9
    st10 = str(s.get("peer_protocol_server", None))
    st10 = "peer_protocol_server: " + st10
    st11 = "upnp: " + str(s.get("upnp", None))
    st12 = "wallet: " + str(s.get("wallet", None))
    st13 = str(s.get("wallet_server_payments", None))
    st13 = "wallet_server_payments: " + st13
    output["startup_status"] = (st1 + "\n" + st2 + "\n" + st3 + "\n"
                                + st4 + "\n" + st5 + "\n" + st6 + "\n"
                                + st7 + "\n" + st8 + "\n" + st9 + "\n"
                                + st10 + "\n" + st11 + "\n" + st12 + "\n"
                                + st13)

    s = status["upnp"]
    upnp1 = "aioupnp version: " + str(s.get("aioupnp_version", None))
    upnp2 = "DHT redirect set: " + str(s.get("dht_redirect_set", None))
    upnp3 = "External IP: " + str(s.get("external_ip", None))
    upnp4 = "Gateway: " + str(s.get("gateway", None))
    upnp5 = "peer redirect set: " + str(s.get("peer_redirect_set", None))
    upnp6 = "redirects: " + str(s.get("redirects", None))
    output["upnp"] = (upnp1 + "\n" + upnp2 + "\n" + upnp3 + "\n"
                      + upnp4 + "\n" + upnp5 + "\n" + upnp6)

    s = status["wallet"]
    wall1 = "Blocks: " + str(s.get("blocks", None))
    wall2 = "Blocks behind: " + str(s.get("blocks_behind", None))
    wall3 = "Connected server: " + str(s.get("connected", None))
    wall3a = str(s["connected_features"].get("server_version", None))
    wall3a = "- Server version: " + wall3a
    wall3b = str(s["connected_features"].get("trending_algorithm", None))
    wall3b = "- Trending algorithm: " + wall3b
    output["wallet"] = (wall1 + "\n" + wall2 + "\n" + wall3 + "\n"
                        + wall3a + "\n" + wall3b)

    return output


def get_lbrynet_status(server="http://localhost:5279"):
    """Get lbrynet status."""
    output = get_status(server=server)

    if not output:
        return "(no status)"

    out = ["DHT", 40 * "-", output["dht"], "",
           "Disk space", 40 * "-", output["disk_space"], "",
           "Background downloader",
           40 * "-", output["background_downloader"], "",
           "Blob manager", 40 * "-", output["blob_manager"], "",
           "ffmpeg status", 40 * "-", output["ffmpeg_status"], "",
           "File manager", 40 * "-", output["file_manager"], "",
           "Startup status", 40 * "-", output["startup_status"], "",
           "Upnp", 40 * "-", output["upnp"], "",
           "Wallet", 40 * "-", output["wallet"]]

    content = "\n".join(out)

    return content
