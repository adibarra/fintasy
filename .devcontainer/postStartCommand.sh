. ${NVM_DIR}/nvm.sh
nvm use || nvm install --lts
corepack enable
corepack prepare pnpm@latest --activate
pnpm config set store-dir $HOME/.pnpm-store
cp --no-clobber .env.production.example .env.production
printf '\n\n%b' "\033[34;1mAll scripts completed! Environment is now set up.\033[0m\n"
$( exit 0 )
