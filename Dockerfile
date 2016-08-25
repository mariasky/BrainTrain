FROM ubuntu

# Update
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip

#inctall firefox to open apply
RUN apt-get install -y firefox


# Install app dependencies
RUN pip3 install Flask 
RUN echo "mysql-server-5.5 mysql-server/root_password password root" | debconf-set-selections
RUN echo "mysql-server-5.5 mysql-server/root_password_again password root" | debconf-set-selections
RUN apt-get update
RUN apt-get -y install mysql-server libmysqlclient-dev curl
RUN pip3 install mysqlclient
RUN pip3 install flask-mysqldb 



#RUN pip install mysql-python
#RUN pip install flask-mysqldb 



#DB creation
ADD MySQLDump/* /tmp/
ADD init_db.sh /tmp/init_db.sh
RUN chmod 700 /tmp/init_db.sh
RUN /tmp/init_db.sh

#sass install and start
RUN apt-get install -y curl
#RUN curl -L get.rvm.io > rvm-install
#RUN rvm install sass
#RUN export PATH=/usr/local/bin:$PATH
#RUN sass --watch sass/style.scss:css/style.css

COPY index.py /src/index.py
ADD templates/* /scr/templates/
ADD static/* /scr/static/
RUN chmod 700 /scr/static/sass_conv.sh
#RUN scr/static/sass_conv.sh
CMD ["python3", "/src/index.py"]



