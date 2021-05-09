#/usr/bin/env bash

_cobra ()
{
    local cur=${COMP_WORDS[COMP_CWORD]}
    case $COMP_CWORD in
    1)
        COMPREPLY=( $(compgen -W "scan start stop status config setpwd whitelist blacklist contain decontain remove list-threats clear-threats" -- $cur) )
        return 0;;
    2)
        local IFS=$'\n'
        case "${COMP_WORDS[1]}" in
            scan|whitelist|blacklist|contain)
                COMPREPLY=( $(compgen -o default -- $cur) );
                return 0;;
            remove|decontain)
                COMPREPLY=( $(compgen -W "$(find /opt/cobraav/quarantine/!(*.avmeta) -printf '%f\n' 2>/dev/null)" -- $cur) )
                return 0;;
            *)
                return 0;;
        esac
        ;;
    esac
}

complete -o filenames -F _cobra cobra
