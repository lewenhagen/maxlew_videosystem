#!/usr/bin/env sh
PATH_TO_SYSTEM="$HOME/git/priv/maxlew_videosystem/script"
FILEPATH="$PATH_TO_SYSTEM/ips.txt"
rm $FILEPATH

check_prerequisities()
{
    type nmap >/dev/null 2>&1 || { echo >&2 "I require nmap but it's not installed.  Aborting."; exit 1; }
    type /sbin/ifconfig >/dev/null 2>&1 || { echo >&2 "I require ifconfig but it's not installed. Install it by running 'apt install net-tools'.  Aborting."; exit 1; }
}

run_nmap()
{
    nmap -sP $(/sbin/ifconfig | grep eno1 -a1 | tail -1 | sed -En 's/inet.([0-9]{3}.*)\s\snetmask.*/\1/p' | cut -d"." -f1-3 | xargs).0/24 | grep axis | cut -d"(" -f2 | cut -d ")" -f1 > "$FILEPATH"
    # || { echo >&2 "Something went wrong with the super command..."; exit 1; }
}

main()
{
    check_prerequisities

    run_nmap

    while [ ! -s "$FILEPATH" ]; do
        sleep 2
        echo "Checking..."
        run_nmap
    done

    if [ -s "$FILEPATH" ]
    then
        echo "At least one camera is recognized and active:"
        cat "$FILEPATH"
        echo "Booting the system..."
        "$PATH_TO_SYSTEM/maxlew.sh"
    else
        echo "No cameras detected!!"
    fi
}


main "$@"
