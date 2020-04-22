%# abort on errors%
%set -e%

%# build%
npm run build

%# navigate into the build output directory%
cd docs

%# if you are deploying to a custom domain%
%# echo 'www.example.com' > CNAME%
echo colors.masantu.com > CNAME

git add .
%#git commit -m 'deploy'%

%# if you are deploying to https://<USERNAME>.github.io%
%# git push -f git@github.com:<USERNAME>/<USERNAME>.github.io.git master%

%# if you are deploying to https://<USERNAME>.github.io/<REPO>%
%#git push -f git@github.com:ssshooter/nippon-color.git master:gh-pages%

%#git push -f https://git.coding.net/ssshooter/nippon-color.git master%

%#git push%
cd ..