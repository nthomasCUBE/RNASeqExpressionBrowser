FROM php:7.0-apache

EXPOSE 80

RUN apt-get update
RUN apt-get -y install apache2
RUN apt-get -y install python python-mysqldb
RUN apt-get -y install python-pil python-matplotlib python-scipy python-sklearn
RUN docker-php-ext-install mysqli

#load apache cgi module
RUN a2enmod cgi
RUN service apache2 restart

#enable cgi in the website root
#second block to allow .htaccess
RUN echo "                       \n \
<Directory /var/www/html>        \n \
   Options +ExecCGI              \n \
   AddHandler cgi-script .cgi     \n \
   DirectoryIndex index.cgi       \n \
</Directory>                     \n \
" >> /etc/apache2/apache2.conf

RUN chmod -R u+rwx,g+x,o+x /var/www/html
RUN ln -sf /usr/bin/python /usr/local/bin/python

CMD /usr/sbin/apache2ctl -D FOREGROUND

COPY src/*cgi /var/www/html/
RUN chmod -R u+rwx,g+x,o+x /var/www/html/
RUN ln -sf /usr/bin/python /usr/local/bin/python
CMD /usr/sbin/apache2ctl -D FOREGROUND
RUN ln -sf /proc/$$/fd/1 /var/log/test.log
