#!/usr/bin/env sh

VERSION="1.0"

# Needed software
#
# google chrome
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo apt install ./google-chrome-stable_current_amd64.deb
#


# Installation:
# sudo apt install nmap net-tools xdotool xfce4-terminal

# Command to find connected Axis cameras
# nmap -sP $(ifconfig | grep eno1 -a1 | tail -1 | sed -En 's/inet.([0-9]{3}.*)\s\snetmask.*/\1/p' | cut -d"." -f1-3 | xargs).0/24 | grep axis | cut -d"(" -f2 | cut -d ")" -f1

PATH_TO_SYSTEM="$HOME/git/priv/maxlew_videosystem/script"
FILEPATH="$PATH_TO_SYSTEM/ips.txt"
# rm $FILEPATH


version()
{
    printf "Version: %s\n" "$VERSION"
}

check_prerequisities()
{
    type google-chrome >/dev/null 2>&1 || { echo >&2 "I require nmap but it's not installed.  Aborting."; exit 1; }
    type /sbin/ifconfig >/dev/null 2>&1 || { echo >&2 "I require ifconfig but it's not installed. Install it by running 'apt install net-tools'.  Aborting."; exit 1; }
}

run_nmap()
{
    nmap -sP $(/sbin/ifconfig | grep eno1 -a1 | tail -1 | sed -En 's/inet.([0-9]{3}.*)\s\snetmask.*/\1/p' | cut -d"." -f1-3 | xargs).0/24 | grep $1 | cut -d"(" -f2 | cut -d ")" -f1 > "$FILEPATH"
    # || { echo >&2 "Something went wrong with the super command..."; exit 1; }
}

boot()
{
    if [ ! -s "$FILEPATH" ]; then
        echo "Need the ip adress file."
        echo "I am on it..."
        read -p "Enter manufacturer: " manu
        init "$manu"
        read -p "Should i continue to boot the awesomeness? [Press any key for Hell Yeah! (then Enter)]" shouldiboot

        if [ "$shouldiboot" != "" ]; then
            boot
        else
            exit 0
        fi
    else
        sleep 5
        #
        oldport=$(lsof -i :5000 | cut -d" " -f2 | tail -n1)

        if [ -z "$oldport" ]; then
            echo "No port in use..."
        else
            kill $oldport && echo "Old stuff killed."
        fi

        cd ~/git/priv/maxlew_videosystem && python3 app.py &

        sleep 3

        google-chrome --app="http://localhost:5000/splashscreen" &

        sleep 1

        xdotool key F11
    fi
}

init()
{
    counter=0
    if [ -z "$1" ]; then
        echo "Additional argument needed."
        exit 1
    fi
    check_prerequisities
    run_nmap "$1"

    while [ ! -s "$FILEPATH" ]; do
        counter=`expr $counter + 1`
        sleep 2
        echo "Checking #$counter time(s)"
        run_nmap "$1"
        exit 0
    done

    if [ -s "$FILEPATH" ]
    then
        echo "At least one camera is recognized and active:"
        cat "$FILEPATH"
    else
        echo "No cameras detected!!"
    fi
}


main()
{
    while [ $(( $# )) ]
    do
        case "$1" in

            --help | -h)
                usage
                exit 0
            ;;

            --version | -v)
                version
                exit 0
            ;;

            init)
                shift
                init "$@"
                exit 0
            ;;

            boot)
                boot
                exit 0
            ;;

            install)
                install
                exit 0
            ;;

            *)
                echo "Option/command not recognized."
                exit 1
            ;;
        esac
    done
}

main "$@"
