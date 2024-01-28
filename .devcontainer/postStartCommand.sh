. /usr/local/share/nvm/nvm.sh
nvm install
nvm use
corepack enable
corepack prepare pnpm@latest --activate
printf '\n\n%b' "\033[34;1mAll set up. You are good to go!\033[0m\n"
$( exit 0 )
