# @author: adibarra (Alec Ibarra)
# @description: This file will run after the devcontainer is started

. ${NVM_DIR}/nvm.sh
nvm use || nvm install --lts
corepack enable
corepack prepare pnpm@latest --activate
pnpm config set store-dir $HOME/.pnpm-store
cp --no-clobber .env.example .env.production
cp --no-clobber .env.example .env.development
clear
$( exit 0 )
