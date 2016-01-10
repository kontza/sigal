#
# Prerequisites:
# - $HOME/.virtualenvs exists
mkdir $HOME/.virtualenvs >& /dev/null
# - virtualenvwrapper has been installed
vew_installed=$(pip3 show virtualenvwrapper|wc -l)
if [ "$vew_installed" -eq 0 ];then
    echo "'virtualenvwrapper' not installed, installing it."
    sudo pip3 install virtualenvwrapper
fi

# Set up some environment variables.
export WORKON_HOME=$HOME/.virtualenvs
export PROJECT_HOME=$(pwd)
export __PROJECT_NAME=$(basename $PROJECT_HOME)

if [[ $OSTYPE == darwin* ]];then
    pyenv virtualenvwrapper
else
    VIRTUALENVWRAPPER_PYTHON="$(command \which python3)"
    source /usr/local/bin/virtualenvwrapper.sh
fi

# Check if the virtual env has already been setup:
# if not, set it up,
# if yes, activate it.
echo "Set up or activate a virtual environment for '$__PROJECT_NAME'."
if [ -e $HOME/.virtualenvs/$__PROJECT_NAME ];then
    workon $__PROJECT_NAME
else
    mkvirtualenv -p $(which python3) $__PROJECT_NAME
fi
export PATH=$WORKON_HOME/$__PROJECT_NAME/bin:$PATH
cd ~/.cache/private
