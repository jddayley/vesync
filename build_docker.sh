docker stop vesync; docker rm vesync;docker build -t vesync .;docker run --restart=always -d --name=vesync vesync sh humidifier.sh 2>&1
