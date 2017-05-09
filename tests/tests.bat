curl -i 127.0.0.1:8080/index.html?q=1
curl -i -X HEAD 127.0.0.1:8080/index.html
curl -i -d var1=atun 127.0.0.1:8080/index.html
curl -i 127.0.0.1:8080/forex.html
set accept="Accept: image/jpeg"
curl -i -H %accept% 127.0.0.1:8080/index.html