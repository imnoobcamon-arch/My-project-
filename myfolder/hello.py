[build]
builder = "nixpacks"

[deploy]
startCommand = "python bot.py"
restartPolicyType = "always"
git clone https://github.com/imnoobcamon-arch/My-project-.git
cd My-project-
mkdir myfolder
nano myfolder/hello.py  
git add myfolder/hello.py
git commit -m "Add hello.py inside myfolder"
git push
