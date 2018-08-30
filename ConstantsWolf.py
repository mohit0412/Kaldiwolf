"""
Author: humblewolf
Description: <write description here...>
"""
import pyaudio


class ConstantsWolf:

    # pyro

    pyro_node_name_prefix = "kaldiwolf_pyro_node"
    max_pyro_nodes = 100
    pyro_ns_address = "52.168.84.235"  # this must be on an all-visible node

    #  read from wav file settings

    sampling_rate = 8000
    packet_length_ms = 30
    bytes_per_sample = 2
    channels = 1
    test_file_wav = "D:\\anagram\\asterisk-intg\\ivrag\\31512.wav"
    loop_sleep_secs = 0.001 # 0.001 gives best for 2 good nodes

    # server configs

    ws_server_host = "127.0.0.1"
    ws_server_port = 9000
    redis_server_host = "10.131.10.64"  # not used , if you want to change it change redispy initalization in Redisqueuewolf
    redis_server_port = 6379  # not used , if you want to change it change redispy initalization in Redisqueuewolf
    client_log_loc = "logs/client.log"
    srv_log_loc = "logs/server.log"
    srv_tcpt_queue_block_timeout = 3

    #  vad settings

    vad_agressiveness = 2  # 2 for file decoding, 3 for mic decoding
    """set its aggressiveness mode, which is an integer between 0 and 3.
     0 is the least aggressive about filtering out non-speech, 3 is the most aggressive"""
    padding_duration_ms = 300

    # decoding settings
    kaldi_home = "/home/humblewolf/kaldi-asr/"  # this path should have trailing slashes
    decode_script_name = "decode_kw.sh"

    #  read from microphone, configs

    sampling_format = pyaudio.paInt16
    record_buffer_samples = 10  # kind of mic buffer
    sampling_rate_mic = 8000
    packet_length_ms_mic = 30
    bytes_per_sample_mic = 2
    channels_mic = 1
    test_record_seconds = 10
    loop_sleep_secs_mic = 0.002