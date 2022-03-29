#!/bin/sh

is_continue() {
    echo "Do you want to keep doing it?"
    read -p "Continue by default,Enter your choice [Y/n]: " InstallWhileHostsExist

    case "${InstallWhileHostsExist}" in
    [yY][eE][sS] | [yY])
        echo "You will keep doing."
        ;;
    [nN][oO] | [nN])
        echo "exit!"
        exit 0
        ;;
    *)
        echo "No input, will keep doing."
        ;;
    esac
}

reset_git_commit() {
    echo "Name: $NAME", "Email: $EMAIL"
    is_continue
    git filter-branch --env-filter '
CORRECT_NAME='"$NAME"'
CORRECT_EMAIL='"$EMAIL"'
if [ "$GIT_COMMITTER_EMAIL" != "$CORRECT_EMAIL" ] || [ "$GIT_COMMITTER_NAME" != "$CORRECT_NAME" ];
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" != "$CORRECT_EMAIL" ] || [ "$GIT_AUTHOR_NAME" != "$CORRECT_NAME" ];
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags

}

change_git_commit() {
    echo "Wrong Eamil: $OLD_EMAIL, New Name: $NAME", "Email: $EMAIL"
    is_continue
    git filter-branch --env-filter '
OLD_EMAIL='"$OLD_EMAIL"'
CORRECT_NAME='"$NAME"'
CORRECT_EMAIL='"$EMAIL"'
if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi
if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL" ]
then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --branches --tags
}

main() {
    type=$1
    if [ "$type" = "change" ]; then
        OLD_EMAIL=$2
        NAME=$3
        EMAIL=$4

        if [ ! "$OLD_EMAIL" ]; then
            echo "please input wrong email."
            exit 1
        fi
    elif [ "$type" = "reset" ]; then
        NAME=$2
        EMAIL=$3
    else
        echo "change or reset?"
        exit 1
    fi

    if [ ! "$NAME" ]; then
        echo "please input your name"
        exit 1
    fi

    if [ ! "$EMAIL" ]; then
        echo "please input your email"
        exit 1
    fi

    if [ "$type" = "change" ]; then
        change_git_commit
    elif [ "$type" = "reset" ]; then
        reset_git_commit
    fi
}

main "$@"
