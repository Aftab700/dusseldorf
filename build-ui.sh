# build ui
cd ui/
npm install
npm run build
cd ..

# copy ui build files to API
rm -rf api/src/api/ui/
cp -r ui/build/ api/src/api/ui/
