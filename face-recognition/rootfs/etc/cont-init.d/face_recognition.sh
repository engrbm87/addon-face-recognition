#!/usr/bin/with-contenv bashio
# ==============================================================================
# Home Assistant Add-on: Face Recognition
# ==============================================================================

# Creates initial Face recognition folder in case it is non-existing
if ! bashio::fs.directory_exists '/config/face_recognition'; then
    mkdir -p /config/face_recognition
fi

declare log_level

bashio::log.info "Starting Face Recognition..."

# Find the matching Tor log level
log_level="ERROR"
if bashio::config.has_value 'log_level'; then
    case "$(bashio::string.lower "$(bashio::config 'log_level')")" in
        all|trace|debug)
            log_level="DEBUG"
            ;;
        info|notice)
            log_level="INFO"
            ;;
        warning)
            log_level="WARNING"
            ;;
        error)
            log_level="ERROR"
            ;;
        fatal|off)
            log_level="FATAL"
            ;;
    esac
fi

# Run the Face recognition webserver
exec python3 /root/face_recognition/webserver.py "${log_level}"