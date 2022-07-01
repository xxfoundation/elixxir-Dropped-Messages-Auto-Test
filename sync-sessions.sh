rsync --rsh=ssh -av generatedsessions/ anne@137.184.8.44:/home/anne/generatedsessions
ssh anne@137.184.8.44 sudo rm -rf /root/session-handout/sessions
ssh anne@137.184.8.44 sudo mv /home/anne/generatedsessions/ /root/session-handout/sessions